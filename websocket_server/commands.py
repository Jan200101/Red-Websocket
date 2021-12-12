from redbot.core import __version__
from discord import errors
import logging
import json

command_list = {}

class Commands:

    output_queue = []

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("red.websocket.commands")

    def Command(name: str):
        def decorate(func):
            async def wrapper(self, *args):
                args = list(args) # allow us to modify the args

                args_string = ", ".join(["self"] + args)
                self.log.debug(f"{name}({args_string}) called")

                for arg_name, arg_type in func.__annotations__.items():
                    try:
                        index = func.__code__.co_varnames.index(arg_name) - 1
                        args[index] = arg_type(args[index]) # convert to the proper type if needed
                    except ValueError:
                        raise ValueError(f"{arg_name} is not of type {arg_type.__name__}")
                    except IndexError:
                        # instead of throwing an Index Error
                        # wait until we call func since that
                        # should give a better traceback
                        pass

                self.output_queue.clear()
                await func(self, *args)
                return "\n".join(self.output_queue)

            wrapper.__doc__ = func.__doc__
            command_list[name] = wrapper

        return decorate

    def print(self, *args):
        for msg in args:
            self.output_queue.append(str(msg))

    @Command("HELP")
    async def help_message(self):
        """Prints this message"""
        for name, func in command_list.items():
            desc = func.__doc__ if func.__doc__ else ""
            self.print(f"{name}\t{desc}")

    @Command("RED_VERSION")
    async def red_version(self):
        """Returns the current version of Red"""
        self.print(__version__)

    @Command("LIST_COGS")
    async def list_cogs(self):
        """Returns a JSON of all loaded and unloaded cogs"""
        loaded = set(self.bot.extensions.keys())

        all_cogs = set(await self.bot._cog_mgr.available_modules())

        unloaded = all_cogs - loaded

        loaded = sorted(list(loaded), key=str.lower)
        unloaded = sorted(list(unloaded), key=str.lower)

        self.print(json.dumps({
            "loaded": loaded,
            "unloaded": unloaded
        }))

    @Command("LOAD_COG")
    async def load_cog(self):
        """Loads a cog"""
        pass

    @Command("UNLOAD_COG")
    async def unload_cog(self):
        """Unloads a cog"""
        pass

    @Command("SEND_MESSAGE")
    async def send_message(self, channel_id: int, *message):
        """
        sends a message to a given channel
        example:

        SEND_MESSAGE 133081046869737472 this is a test
        """

        if not message:
            raise TypeError("no message given")

        message = " ".join(message)

        channel = self.bot.get_channel(channel_id)

        if channel:
            try:
                await channel.send(message)
            except errors.Forbidden:
                self.print("Unable to send message")
        else:
            self.print(f"Channel `{channel_id}` not found")
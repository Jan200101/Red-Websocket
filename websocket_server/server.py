import logging
from redbot.core import commands
from .commands import command_list, Commands
import traceback
import websockets
import asyncio

class Server(commands.Cog):
    """Websocket Server"""

    def __init__(self, bot):
        self.bot = bot
        self.log = logging.getLogger("red.websocket.websocket_server")
        self.server_task = self.bot.loop.create_task(self.serve())

        self.ip = "0.0.0.0"
        self.port = 8765

        self.log.info(f"Starting Websocket Server on {self.ip}:{self.port}")

        self.commands = Commands(self.bot)


    def cog_unload(self):
        self.log.info("Stopping Websocket Server")
        self.server_task.cancel()

    async def serve(self):
        async with websockets.serve(self.message_parser, self.ip, self.port):
            await asyncio.Future()  # run forever

    async def message_parser(self, websocket):
        try:
            async for message in websocket:
                split = message.split(" ")

                command = split[0]
                arguments = split[1:]

                try:
                    output = await command_list[command](self.commands, *arguments)
                    if output:
                        await websocket.send(output)
                except KeyError:
                    self.log.debug(f"Command `{command}` not found")
                except Exception as e:
                    self.log.error(traceback.format_exc())
                    await websocket.send(str(e))


        except websockets.exceptions.ConnectionClosedError:
            # Connection improperly closed
            pass
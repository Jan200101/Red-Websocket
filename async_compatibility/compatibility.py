import logging
import sys
from redbot.core import commands

_methods = []
_log = logging.getLogger("red.async.compatibility")

class AsyncCompatibility(commands.Cog):

    def __init__(self, bot):
        global _globat_bot
        self.bot = bot

        for func in _methods:
            setattr(self.bot, func.__name__, func)

        _log.info(f"Loaded {len(_methods)} compatibility methods")

    def cog_unload(self):
        for func in _methods:
            delattr(self.bot, func.__name__)

        _log.info("Unloaded compatibility methods")

    def compatibility_method(require_context=False):
        def decorate(func):
            async def wrapper(*args, **kwargs):
                frame = sys._getframe(2)
                stack = [x[1] for x in frame.f_locals.items() if isinstance(x[1], commands.Context)]
                if stack:
                    ctx = stack[0]
                else:
                    ctx = None

                    error_msg = f"Could not fetch context from {frame.f_code.co_name}"
                    print(error_msg)
                    if require_context:
                        _log.error(error_msg)
                        return
                    else:
                        _log.warn(error_msg)

                return await func(ctx, *args, **kwargs)

            wrapper.__name__ = func.__name__
            wrapper.__doc__ = func.__doc__
            _methods.append(wrapper)
        return decorate

    @compatibility_method(require_context=True)
    async def say(ctx, msg):
        await ctx.send(msg)
import sys

from . import utils
sys.modules["cogs.utils"] = utils

from .compatibility import AsyncCompatibility

def setup(bot):
    bot.add_cog(AsyncCompatibility(bot))
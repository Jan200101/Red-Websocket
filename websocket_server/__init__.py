from .server import Server

def setup(bot):
    bot.add_cog(Server(bot))
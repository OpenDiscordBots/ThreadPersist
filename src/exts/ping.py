from disnake.ext.commands import Cog, Context, command

from src.bot import Bot


class Ping(Cog):
    """A simple ping command."""

    def __init__(self, bot: Bot) -> None:
        self.bot = bot

    @command(name="ping")
    async def ping(self, ctx: Context) -> None:
        """Get the gateway latency of the bot."""

        await ctx.reply(f"Pong! {self.bot.latency*1000:.2f}ms")


def setup(bot: Bot) -> None:
    bot.add_cog(Ping(bot))

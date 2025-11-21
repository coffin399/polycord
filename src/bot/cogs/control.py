import discord
from discord.ext import commands
from discord.commands import slash_command, Option

class ControlCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="auto", description="Toggle auto-drive mode")
    async def auto_mode(self, ctx, enabled: Option(bool, "Enable or disable auto-drive")):
        self.bot.config['bot']['auto_mode'] = enabled
        status = "ENABLED" if enabled else "DISABLED"
        await ctx.respond(f"🤖 Auto-Drive Mode **{status}**")

    @slash_command(name="amount", description="Set default bet amount for auto-mode")
    async def set_amount(self, ctx, amount: Option(int, "Amount in USD")):
        self.bot.config['bot']['default_bet_amount'] = amount
        await ctx.respond(f"💰 Default Auto-Bet Amount set to **${amount}**")

    @slash_command(name="frequency", description="Set polling frequency in seconds")
    async def set_frequency(self, ctx, seconds: Option(int, "Seconds between checks")):
        self.bot.config['polymarket']['frequency'] = seconds
        await ctx.respond(f"⏱️ Polling frequency set to **{seconds}s**")

def setup(bot):
    bot.add_cog(ControlCog(bot))

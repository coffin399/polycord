import discord
import asyncio
import logging
from discord.ext import tasks
from src.services.gemini import GeminiClient
from src.services.polymarket import PolymarketService
from src.bot.ui import BettingView

logger = logging.getLogger(__name__)

class PolyCordBot(discord.Bot):
    def __init__(self, config):
        super().__init__(intents=discord.Intents.default())
        self.config = config
        self.gemini = GeminiClient(config['gemini']['keys'], config['gemini']['model'])
        self.polymarket = PolymarketService(
            config['polymarket']['private_key'],
            config['polymarket']['proxy_wallet']
        )
        self.seen_markets = set()
        self.report_channel = None

    async def on_ready(self):
        logger.info(f"Logged in as {self.user} (ID: {self.user.id})")
        self.report_channel = self.get_channel(self.config['discord']['report_channel_id'])
        self.market_loop.start()
        
        # Load extensions
        self.load_extension('src.bot.cogs.control')

    @tasks.loop(seconds=180) # Default, updated dynamically
    async def market_loop(self):
        # Update loop interval if config changed
        current_freq = self.config['polymarket']['frequency']
        if self.market_loop.seconds != current_freq:
            self.market_loop.change_interval(seconds=current_freq)

        logger.info("Fetching markets...")
        markets = self.polymarket.get_markets(limit=5)
        
        for market in markets:
            market_id = market.get('id')
            if market_id in self.seen_markets:
                continue
            
            self.seen_markets.add(market_id)
            await self.process_market(market)

    async def process_market(self, market):
        title = market.get('title')
        description = market.get('description', 'No description.')
        
        logger.info(f"Analyzing market: {title}")
        decision, reasoning = self.gemini.analyze_market(title, description)
        
        embed = discord.Embed(title=title, description=description, color=0x00ff00)
        embed.add_field(name="Gemini Recommendation", value=f"**{decision}**", inline=False)
        embed.add_field(name="Reasoning", value=reasoning, inline=False)
        
        # Auto Mode Logic
        if self.config['bot']['auto_mode']:
            if decision in ["YES", "NO"]:
                amount = self.config['bot']['default_bet_amount']
                result = self.polymarket.place_bet(market_id, amount, decision)
                
                if self.report_channel:
                    report_embed = discord.Embed(title="🤖 Auto-Bet Executed", color=0x3498db)
                    report_embed.add_field(name="Market", value=title)
                    report_embed.add_field(name="Decision", value=decision)
                    report_embed.add_field(name="Amount", value=f"${amount}")
                    report_embed.add_field(name="Status", value=result.get('status'))
                    await self.report_channel.send(embed=report_embed)
            else:
                logger.info(f"Skipping auto-bet for {title}: Decision was {decision}")

        # Always send manual interface to report channel (or another channel if configured)
        if self.report_channel:
            view = BettingView(market, self.polymarket, self.config['discord']['allowed_user_ids'])
            await self.report_channel.send(embed=embed, view=view)

    @market_loop.before_loop
    async def before_market_loop(self):
        await self.wait_until_ready()

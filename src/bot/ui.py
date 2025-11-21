import discord
from discord.ui import View, Button

class BettingView(View):
    def __init__(self, market_data, polymarket_service, allowed_users):
        super().__init__(timeout=None)
        self.market_data = market_data
        self.polymarket_service = polymarket_service
        self.allowed_users = allowed_users
        self.selected_side = None

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user.id not in self.allowed_users:
            await interaction.response.send_message("You are not authorized to use this bot.", ephemeral=True)
            return False
        return True

    @discord.ui.button(label="YES", style=discord.ButtonStyle.green, custom_id="bet_yes")
    async def yes_button(self, button: Button, interaction: discord.Interaction):
        self.selected_side = "YES"
        await self.show_amount_selection(interaction)

    @discord.ui.button(label="NO", style=discord.ButtonStyle.red, custom_id="bet_no")
    async def no_button(self, button: Button, interaction: discord.Interaction):
        self.selected_side = "NO"
        await self.show_amount_selection(interaction)

    async def show_amount_selection(self, interaction: discord.Interaction):
        # Disable side buttons
        for child in self.children:
            child.disabled = True
        
        # Add amount buttons
        self.add_item(AmountButton(1, self.market_data, self.polymarket_service, self.selected_side))
        self.add_item(AmountButton(5, self.market_data, self.polymarket_service, self.selected_side))
        self.add_item(AmountButton(10, self.market_data, self.polymarket_service, self.selected_side))
        
        await interaction.response.edit_message(content=f"Selected **{self.selected_side}**. Choose amount:", view=self)

class AmountButton(Button):
    def __init__(self, amount, market_data, polymarket_service, side):
        super().__init__(label=f"${amount}", style=discord.ButtonStyle.blurple)
        self.amount = amount
        self.market_data = market_data
        self.polymarket_service = polymarket_service
        self.side = side

    async def callback(self, interaction: discord.Interaction):
        # Execute bet
        # In real app, we'd use market_data['conditionId'] or similar
        condition_id = self.market_data.get('id', 'unknown') 
        result = self.polymarket_service.place_bet(condition_id, self.amount, self.side)
        
        if result['status'] == 'success':
            await interaction.response.send_message(f"✅ Bet placed! **${self.amount}** on **{self.side}** for *{self.market_data.get('title')}*", ephemeral=False)
        else:
            await interaction.response.send_message(f"❌ Bet failed: {result.get('message')}", ephemeral=True)

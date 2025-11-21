# PolyCord - Polymarket Betting Bot

A Discord bot that analyzes Polymarket events using Gemini 2.5 Flash and allows betting via Discord buttons or fully automated "Auto-Drive" mode.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configuration**:
    - Run the bot once to generate `config.yaml`:
      ```bash
      python src/main.py
      ```
    - Edit `config.yaml` and fill in your:
        - Discord Bot Token
        - Gemini API Keys
        - Polymarket Private Key (and Proxy Wallet if applicable)
        - User IDs and Channel IDs

3.  **Run**:
    ```bash
    python src/main.py
    ```

## Features

- **Market Analysis**: Uses Gemini to analyze market titles/descriptions and recommend YES/NO.
- **Key Rotation**: Automatically rotates Gemini API keys if rate limits or errors occur.
- **Discord Interface**:
    - Shows market details and recommendation.
    - Interactive buttons for manual betting ($1, $5, $10).
- **Auto-Drive Mode**:
    - Automatically bets on "Strong" recommendations (YES/NO).
    - Reports actions to a specific channel.
- **Slash Commands**:
    - `/auto <true/false>`: Toggle auto mode.
    - `/amount <int>`: Set auto-bet amount.
    - `/frequency <int>`: Set polling frequency.

## Structure

- `src/main.py`: Entry point.
- `src/services/`: Gemini and Polymarket logic.
- `src/bot/`: Discord bot logic, UI, and commands.
- `config.yaml`: Configuration file (git-ignored).

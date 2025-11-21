import os
import yaml
import shutil
import logging
from src.bot.client import PolyCordBot
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

CONFIG_PATH = "config.yaml"
DEFAULT_CONFIG_PATH = "config.default.yaml"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        logger.warning(f"{CONFIG_PATH} not found. Creating from default.")
        if os.path.exists(DEFAULT_CONFIG_PATH):
            shutil.copy(DEFAULT_CONFIG_PATH, CONFIG_PATH)
            logger.info(f"Created {CONFIG_PATH}. Please configure it before running again.")
            exit()
        else:
            logger.error(f"Default config {DEFAULT_CONFIG_PATH} not found!")
            exit(1)
            
    with open(CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def main():
    load_dotenv()
    config = load_config()
    
    bot = PolyCordBot(config)
    bot.run(config['discord']['token'])

if __name__ == "__main__":
    main()

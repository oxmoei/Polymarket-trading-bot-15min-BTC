import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Load .env file from project root if present.
# Do NOT override existing environment variables (so CI/terminal env wins over .env).
load_dotenv(override=False)


@dataclass
class Settings:
    api_key: str = os.getenv("POLYMARKET_API_KEY", "")
    api_secret: str = os.getenv("POLYMARKET_API_SECRET", "")
    api_passphrase: str = os.getenv("POLYMARKET_API_PASSPHRASE", "")
    private_key: str = os.getenv("POLYMARKET_PRIVATE_KEY", "")
    signature_type: int = int(os.getenv("POLYMARKET_SIGNATURE_TYPE", "1"))
    funder: str = os.getenv("POLYMARKET_FUNDER", "")
    market_slug: str = os.getenv("POLYMARKET_MARKET_SLUG", "")
    market_id: str = os.getenv("POLYMARKET_MARKET_ID", "")
    yes_token_id: str = os.getenv("POLYMARKET_YES_TOKEN_ID", "")
    no_token_id: str = os.getenv("POLYMARKET_NO_TOKEN_ID", "")
    ws_url: str = os.getenv("POLYMARKET_WS_URL", "wss://ws-subscriptions-clob.polymarket.com")
    use_wss: bool = os.getenv("USE_WSS", "false").lower() == "true"
    target_pair_cost: float = float(os.getenv("TARGET_PAIR_COST", "0.99"))
    balance_slack: float = float(os.getenv("BALANCE_SLACK", "0.15"))
    order_size: float = float(os.getenv("ORDER_SIZE", "50"))
    order_type: str = os.getenv("ORDER_TYPE", "FOK").upper()
    yes_buy_threshold: float = float(os.getenv("YES_BUY_THRESHOLD", "0.45"))
    no_buy_threshold: float = float(os.getenv("NO_BUY_THRESHOLD", "0.45"))
    verbose: bool = os.getenv("VERBOSE", "false").lower() == "true"
    dry_run: bool = os.getenv("DRY_RUN", "false").lower() == "true"
    cooldown_seconds: float = float(os.getenv("COOLDOWN_SECONDS", "10"))
    sim_balance: float = float(os.getenv("SIM_BALANCE", "0"))
    
    # Risk management settings
    max_daily_loss: float = float(os.getenv("MAX_DAILY_LOSS", "0"))  # 0 = disabled
    max_position_size: float = float(os.getenv("MAX_POSITION_SIZE", "0"))  # 0 = disabled
    max_trades_per_day: int = int(os.getenv("MAX_TRADES_PER_DAY", "0"))  # 0 = disabled
    min_balance_required: float = float(os.getenv("MIN_BALANCE_REQUIRED", "10.0"))
    max_balance_utilization: float = float(os.getenv("MAX_BALANCE_UTILIZATION", "0.8"))
    
    # Statistics and logging
    enable_stats: bool = os.getenv("ENABLE_STATS", "true").lower() == "true"
    trade_log_file: str = os.getenv("TRADE_LOG_FILE", "trades.json")
    use_rich_output: bool = os.getenv("USE_RICH_OUTPUT", "true").lower() == "true"


def load_settings() -> Settings:
    return Settings()

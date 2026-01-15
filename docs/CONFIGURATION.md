# Configuration Guide

[English](CONFIGURATION.md) | [中文说明](CONFIGURATION-CN.md)

Complete guide to configuring the BTC 15-minute arbitrage bot.

## 📁 Configuration File

The bot uses a `.env` file in the root directory for configuration. Create this file if it doesn't exist.

---

## 🔐 Required Settings

### Private Key & API Credentials

```env
# Your wallet's private key (starts with 0x)
POLYMARKET_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE

# Wallet type: 0 = MetaMask/external wallet, 1 = Email login (Magic.link)
POLYMARKET_SIGNATURE_TYPE=1

# For Magic.link users ONLY - your Polymarket proxy wallet address
# Leave empty for MetaMask/external wallet users
POLYMARKET_FUNDER=0xYOUR_PROXY_ADDRESS_HERE

# Generate these by running: poetry run python -m src.generate_api_key
POLYMARKET_API_KEY=your_api_key_here
POLYMARKET_API_SECRET=your_api_secret_here
POLYMARKET_API_PASSPHRASE=your_passphrase_here
```

**How to get your private key:**
- **MetaMask**: Account Details → Show Private Key
- **Email login**: Export from Polymarket settings
- ⚠️ **Never share your private key!**

**How to get API credentials:**
1. Set `POLYMARKET_PRIVATE_KEY` in `.env`
2. Run: `poetry run python -m src.generate_api_key`
3. Copy the output to your `.env` file

---

## ⚙️ Trading Settings

### Basic Trading Configuration

```env
# Maximum combined cost to trigger arbitrage (0.99 = 1% profit opportunity)
TARGET_PAIR_COST=0.99

# Number of shares to buy per trade (minimum is 5)
ORDER_SIZE=5

# Order type: FOK (Fill-or-Kill), FAK (Fill-and-Kill), GTC (Good-Till-Cancel)
ORDER_TYPE=FOK

# Minimum seconds between trades (prevents rapid-fire trading)
COOLDOWN_SECONDS=10
```

**Recommendations:**
- Start with `TARGET_PAIR_COST=0.99` (1% profit opportunities)
- Start with `ORDER_SIZE=5` (minimum, safe for testing)
- Use `ORDER_TYPE=FOK` (safest, ensures both legs fill or neither)
- Set `COOLDOWN_SECONDS=10` to avoid excessive trading

### Simulation Mode

```env
# Enable simulation mode (true = no real money, false = live trading)
DRY_RUN=true

# Starting balance for simulation (only used when DRY_RUN=true)
SIM_BALANCE=100
```

**Important:**
- Always start with `DRY_RUN=true` to test
- Set `SIM_BALANCE` to simulate your trading capital
- Only set `DRY_RUN=false` when ready for live trading

---

## 🛡️ Risk Management Settings

All risk management settings are **optional** (set to 0 to disable).

```env
# Maximum loss per day in USDC (0 = disabled)
MAX_DAILY_LOSS=50.0

# Maximum position size per trade in USDC (0 = disabled)
MAX_POSITION_SIZE=100.0

# Maximum number of trades per day (0 = disabled)
MAX_TRADES_PER_DAY=20

# Minimum balance required to continue trading
MIN_BALANCE_REQUIRED=10.0

# Maximum percentage of balance to use per trade (0.8 = 80%)
MAX_BALANCE_UTILIZATION=0.8
```

**Example Configuration:**
```env
# Stop trading after losing $50 in a day
MAX_DAILY_LOSS=50.0

# Never trade more than $100 per trade
MAX_POSITION_SIZE=100.0

# Limit to 20 trades per day
MAX_TRADES_PER_DAY=20

# Keep at least $10 in account
MIN_BALANCE_REQUIRED=10.0

# Use max 80% of balance per trade
MAX_BALANCE_UTILIZATION=0.8
```

**Why use risk management?**
- Prevents excessive losses
- Controls position sizing
- Limits trading frequency
- Protects your capital

---

## 📊 Statistics & Logging Settings

```env
# Enable statistics tracking (recommended: true)
ENABLE_STATS=true

# File path for trade history (JSON format)
TRADE_LOG_FILE=trades.json

# Use rich console formatting (requires 'rich' package)
USE_RICH_OUTPUT=true

# Enable verbose/debug logging
VERBOSE=false
```

**Recommendations:**
- Set `ENABLE_STATS=true` to track performance
- Keep `TRADE_LOG_FILE=trades.json` for trade history
- Set `USE_RICH_OUTPUT=true` for better console output (requires `rich`, included via Poetry)
- Set `VERBOSE=false` unless debugging

---

## 🔌 Advanced Settings

### WebSocket (Optional - Lower Latency)

```env
# Enable WebSocket market data feed (lower latency)
USE_WSS=false

# WebSocket URL (usually don't need to change)
POLYMARKET_WS_URL=wss://ws-subscriptions-clob.polymarket.com
```

**When to use WebSocket:**
- For lower latency trading
- If you have stable internet connection
- For high-frequency trading strategies

**Note:** WebSocket requires stable connection. If your connection drops frequently, use HTTPS polling (default).

### Market Selection

```env
# Force a specific market (usually leave empty for auto-discovery)
POLYMARKET_MARKET_SLUG=
```

**Usually leave this empty** - the bot auto-discovers the current BTC 15-minute market.

---

## 📝 Complete Example Configuration

Here's a complete example `.env` file for a beginner:

```env
# ============================================
# REQUIRED SETTINGS
# ============================================
POLYMARKET_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
POLYMARKET_SIGNATURE_TYPE=1
POLYMARKET_FUNDER=0xYOUR_PROXY_ADDRESS_HERE
POLYMARKET_API_KEY=your_api_key_here
POLYMARKET_API_SECRET=your_api_secret_here
POLYMARKET_API_PASSPHRASE=your_passphrase_here

# ============================================
# TRADING SETTINGS
# ============================================
DRY_RUN=true
SIM_BALANCE=100
TARGET_PAIR_COST=0.99
ORDER_SIZE=5
ORDER_TYPE=FOK
COOLDOWN_SECONDS=10

# ============================================
# RISK MANAGEMENT (Optional)
# ============================================
MAX_DAILY_LOSS=50.0
MAX_POSITION_SIZE=100.0
MAX_TRADES_PER_DAY=20
MIN_BALANCE_REQUIRED=10.0
MAX_BALANCE_UTILIZATION=0.8

# ============================================
# STATISTICS & LOGGING
# ============================================
ENABLE_STATS=true
TRADE_LOG_FILE=trades.json
USE_RICH_OUTPUT=true
VERBOSE=false
```

---

## ✅ Configuration Validation

The bot automatically validates your configuration on startup. If there are errors, you'll see clear messages.

You can also validate manually:

```bash
poetry run python -m src.diagnose_config
```

This checks:
- All required fields are set
- Private key format is correct
- Wallet type matches configuration
- API credentials are accessible
- Balance can be retrieved

---

## 🔄 Changing Configuration

1. **Edit `.env` file** with your changes
2. **Restart the bot** to apply changes
3. **Validate** with `poetry run python -m src.diagnose_config` if needed

**Important:** 
- Changing `POLYMARKET_PRIVATE_KEY` requires regenerating API credentials
- Changing risk limits takes effect immediately
- Some changes require bot restart

---

## 📚 Related Documentation

- [GETTING_STARTED.md](GETTING_STARTED.md) - Quick start guide
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Common configuration issues
- [FEATURES.md](FEATURES.md) - Detailed feature explanations

---

## 💡 Pro Tips

1. **Start conservative**: Use lower `ORDER_SIZE` and higher `COOLDOWN_SECONDS`
2. **Test first**: Always use `DRY_RUN=true` before live trading
3. **Set limits**: Use risk management to protect your capital
4. **Monitor**: Check `TRADE_LOG_FILE` regularly to review performance
5. **Adjust gradually**: Change one setting at a time and observe results

---

**Need help?** Contact [@terauss](https://t.me/terauss) on Telegram!


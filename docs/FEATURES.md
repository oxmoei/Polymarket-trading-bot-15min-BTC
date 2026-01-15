# Features Guide

[English](FEATURES.md) | [中文说明](FEATURES-CN.md)

Complete guide to all features of the BTC 15-minute arbitrage bot.

## 🎯 Core Features

### Auto-Market Discovery
- **What it does**: Automatically finds and connects to the current BTC 15-minute market
- **How it works**: Scans Polymarket for active markets matching the pattern
- **When it switches**: Automatically switches to the next market when current one closes
- **No configuration needed**: Works automatically

### Arbitrage Detection
- **What it does**: Continuously scans for arbitrage opportunities
- **How it works**: Monitors UP and DOWN prices, detects when total cost < $1.00
- **Real-time**: Uses live order book data (not historical prices)
- **Smart pricing**: Uses depth-aware pricing to ensure fills

### Execution Safety
- **What it does**: Ensures both legs (UP + DOWN) fill successfully
- **How it works**: Verifies both orders filled before confirming trade
- **Fallback**: If one leg fails, attempts to unwind the position
- **Protection**: Prevents partial fills and imbalanced positions

### Simulation Mode
- **What it does**: Lets you test the bot without real money
- **How it works**: Runs all logic but doesn't place real orders
- **Tracking**: Tracks simulated balance and profits
- **Safe testing**: Perfect for learning and strategy testing

---

## 📊 Statistics & Tracking

### Trade History
- **Automatic logging**: All trades are automatically logged to JSON file
- **Persistent storage**: Trade history survives bot restarts
- **Export options**: Export to CSV for analysis in spreadsheet apps
- **Rich data**: Includes prices, sizes, profits, timestamps, and more

### Performance Metrics
- **Win rate**: Percentage of profitable trades
- **Average profit**: Average profit per trade
- **Total statistics**: Total trades, invested, profits
- **Real-time updates**: Statistics update after each trade

### How to Use

```python
# Statistics are automatically enabled by default
# View in final summary after market closes

# Export to CSV:
from src.statistics import StatisticsTracker
tracker = StatisticsTracker(log_file="trades.json")
tracker.export_csv("trades.csv")
```

---

## 🛡️ Risk Management

### Daily Loss Limits
- **What it does**: Stops trading after reaching maximum daily loss
- **How to use**: Set `MAX_DAILY_LOSS=50.0` (stops after $50 loss)
- **Resets daily**: Limits reset at midnight
- **Safety**: Protects you from bad trading days

### Position Size Limits
- **What it does**: Limits the maximum size of each trade
- **How to use**: Set `MAX_POSITION_SIZE=100.0` (max $100 per trade)
- **Capital protection**: Prevents oversized positions
- **Flexible**: Set based on your risk tolerance

### Trade Frequency Limits
- **What it does**: Limits number of trades per day
- **How to use**: Set `MAX_TRADES_PER_DAY=20` (max 20 trades/day)
- **Prevents overtrading**: Helps avoid emotional trading
- **Cost control**: Limits transaction costs

### Balance Utilization
- **What it does**: Limits percentage of balance used per trade
- **How to use**: Set `MAX_BALANCE_UTILIZATION=0.8` (use max 80%)
- **Safety margin**: Always keeps some balance as buffer
- **Recommended**: 0.7-0.8 (70-80%)

### Minimum Balance
- **What it does**: Stops trading if balance drops below minimum
- **How to use**: Set `MIN_BALANCE_REQUIRED=10.0`
- **Prevents exhaustion**: Stops before running out of funds
- **Safety net**: Keeps some funds for emergencies

---

## 🎨 Enhanced Logging & UI

### Rich Console Output
- **What it does**: Beautiful, colored console output
- **Features**: Tables, colors, progress indicators
- **Optional**: Works without it (falls back to basic output)
- **Install**: `poetry install` (rich is included in dependencies)

### Progress Indicators
- **Real-time updates**: See bot activity as it happens
- **Clear formatting**: Easy to read status updates
- **Error highlighting**: Errors are clearly marked
- **Statistics display**: Beautiful tables for metrics

---

## ⚙️ Advanced Features

### WebSocket Mode
- **What it does**: Lower latency market data feed
- **How to use**: Set `USE_WSS=true` in `.env`
- **Benefits**: Faster order execution, real-time updates
- **Requirements**: Stable internet connection
- **Recommended**: For experienced users with stable connections

### Configuration Validation
- **What it does**: Checks your configuration before starting
- **How it works**: Validates all settings and reports errors
- **Benefits**: Prevents runtime errors from bad config
- **Automatic**: Runs on bot startup

### Graceful Shutdown
- **What it does**: Clean shutdown with data saving
- **How it works**: Handles Ctrl+C gracefully
- **Benefits**: Saves statistics, shows final summary
- **No data loss**: Trade history is preserved

---

## 🔄 Market Management

### Auto-Market Switching
- **What it does**: Automatically finds next market when current closes
- **How it works**: Scans for new market every 15 minutes
- **Seamless**: Continues trading without manual intervention
- **Reliable**: Handles market transitions smoothly

### Market Result Tracking
- **What it does**: Tracks which side (UP/DOWN) won each market
- **How it works**: Checks final prices when market closes
- **Integration**: Updates trade records with results
- **Analytics**: Helps analyze performance by outcome

---

## 📈 Performance Features

### Depth-Aware Pricing
- **What it does**: Uses order book depth to calculate real fill prices
- **How it works**: Walks the order book to ensure liquidity
- **Accuracy**: More accurate than just using best bid/ask
- **Safety**: Ensures orders can actually fill

### Concurrent Order Book Fetching
- **What it does**: Fetches UP and DOWN order books simultaneously
- **Benefits**: Faster scanning, lower latency
- **Efficiency**: Reduces time between scans
- **Automatic**: Works automatically

### Cooldown System
- **What it does**: Prevents rapid-fire trading on same opportunity
- **How to configure**: Set `COOLDOWN_SECONDS=10`
- **Benefits**: Avoids duplicate trades, saves on fees
- **Flexible**: Adjust based on market conditions

---

## 🧪 Testing & Development

### Simulation Mode
- **Full simulation**: All logic runs, no real orders
- **Realistic**: Uses real market data
- **Safe**: Perfect for testing strategies
- **Tracking**: Full statistics and tracking

### Verbose Logging
- **What it does**: Detailed debug information
- **How to enable**: Set `VERBOSE=true`
- **Use cases**: Debugging, development, troubleshooting
- **Output**: Detailed logs of all operations

### Balance Testing
- **Utility**: `poetry run python -m src.test_balance`
- **What it does**: Tests wallet connection and balance
- **Use cases**: Verify configuration, check funds
- **Safe**: Read-only, no trading

---

## 📋 Feature Comparison

| Feature | Basic Bot | Enhanced Bot |
|---------|-----------|--------------|
| Arbitrage Detection | ✅ | ✅ |
| Auto-Market Discovery | ✅ | ✅ |
| Simulation Mode | ✅ | ✅ |
| Statistics Tracking | ❌ | ✅ |
| Risk Management | ❌ | ✅ |
| Trade History Export | ❌ | ✅ |
| Rich Console Output | ❌ | ✅ |
| Configuration Validation | ❌ | ✅ |
| Graceful Shutdown | ❌ | ✅ |

---

## 💡 Using Features Effectively

### For Beginners
1. Start with **simulation mode** to learn
2. Use **default settings** initially
3. Enable **statistics tracking** to monitor performance
4. Set **conservative risk limits**
5. Review **trade history** regularly

### For Intermediate Users
1. Use **risk management** to protect capital
2. Enable **WebSocket** for lower latency
3. Analyze **statistics** to optimize settings
4. Export **trade history** for analysis
5. Adjust **cooldown** based on market conditions

### For Advanced Users
1. Fine-tune **risk limits** based on strategy
2. Use **verbose logging** for debugging
3. Analyze **performance metrics** in detail
4. Optimize **ORDER_SIZE** and **TARGET_PAIR_COST**
5. Monitor **multiple markets** (manual configuration)

---

## 🔗 Related Documentation

- [GETTING_STARTED.md](GETTING_STARTED.md) - Quick start
- [CONFIGURATION.md](CONFIGURATION.md) - Configure all features
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - Fix issues

---

**Need help?** Contact [@terauss](https://t.me/terauss) on Telegram!


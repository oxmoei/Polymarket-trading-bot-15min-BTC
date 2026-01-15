# Getting Started Guide

[English](GETTING_STARTED.md) | [中文说明](GETTING_STARTED-CN.md)

Welcome! This guide will help you get the BTC 15-minute arbitrage bot up and running quickly.

## 📋 Quick Start (5 Minutes)

### Step 1: Installation

```bash
# Clone the repository
git clone https://github.com/terauss/Polymarket-trading-bot-15min-BTC
cd Polymarket-trading-bot-15min-BTC

# Install Poetry (if needed)
pipx install poetry
# or: curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install
```

### Step 2: Create Configuration File

Create a `.env` file in the bot's root directory:

```env
# Required
POLYMARKET_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
POLYMARKET_SIGNATURE_TYPE=1

# Generate these with: poetry run python -m src.generate_api_key
POLYMARKET_API_KEY=
POLYMARKET_API_SECRET=
POLYMARKET_API_PASSPHRASE=

# Trading Settings (Recommended for beginners)
DRY_RUN=true
SIM_BALANCE=100
TARGET_PAIR_COST=0.99
ORDER_SIZE=5
ORDER_TYPE=FOK
COOLDOWN_SECONDS=10
```

### Step 3: Generate API Keys

```bash
poetry run python -m src.generate_api_key
```

Copy the output (API Key, Secret, Passphrase) to your `.env` file.

### Step 4: Test Your Setup

```bash
poetry run python -m src.test_balance
```

This verifies your configuration is correct.

### Step 5: Run in Simulation Mode (Recommended First)

```bash
poetry run python -m src.simple_arb_bot
```

The bot will run in simulation mode (no real money) so you can see how it works.

---

## 🎯 What You Need Before Starting

- ✅ Python 3.10 or higher
- ✅ Polymarket account
- ✅ USDC funds in your Polymarket wallet (for live trading)
- ✅ Your wallet private key
- ✅ Basic terminal/command prompt knowledge

---

## 📖 Next Steps

1. **For configuration**: See [CONFIGURATION.md](CONFIGURATION.md) for all settings
2. **For features**: See [FEATURES.md](FEATURES.md) to understand what the bot can do
3. **For troubleshooting**: See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if you have issues

---

## 🚦 Quick Checklist

Before running live trading, make sure:

- [ ] Bot runs successfully in simulation mode (`DRY_RUN=true`)
- [ ] You understand how the bot works
- [ ] You have tested with small amounts
- [ ] You have configured risk management (see [CONFIGURATION.md](CONFIGURATION.md))
- [ ] You have sufficient USDC in your Polymarket wallet
- [ ] You've set `DRY_RUN=false` for live trading

---

## ⚠️ Important Notes

1. **Always start in simulation mode** (`DRY_RUN=true`)
2. **Start with small order sizes** (`ORDER_SIZE=5`)
3. **Monitor your first trades closely**
4. **Never share your private key**
5. **Trading involves risk** - only invest what you can afford to lose

---

## 📞 Need Help?

- Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
- Telegram: [@terauss](https://t.me/terauss)

---

**Ready to go?** Run the bot in simulation mode first, then when you're comfortable, switch to live trading!


# Troubleshooting Guide

[English](TROUBLESHOOTING.md) | [中文说明](TROUBLESHOOTING-CN.md)

Common issues and solutions for the BTC 15-minute arbitrage bot.

## 🔍 Quick Diagnosis

Run the diagnostic tool first:

```bash
poetry run python -m src.diagnose_config
```

This will check your configuration and report any issues.

---

## ❌ Configuration Errors

### "POLYMARKET_PRIVATE_KEY is required"
**Problem**: Private key not set in `.env` file.

**Solution**:
1. Open `.env` file
2. Add: `POLYMARKET_PRIVATE_KEY=0xYOUR_KEY_HERE`
3. Make sure the key starts with `0x`
4. Restart the bot

---

### "Invalid signature" Error
**Problem**: Authentication failed with Polymarket API.

**Common Causes & Solutions**:

#### For Magic.link Users (signature_type=1):
1. **Missing POLYMARKET_FUNDER**
   - Set `POLYMARKET_FUNDER` to your Polymarket proxy wallet address
   - Find it at: `https://polymarket.com/@YOUR_USERNAME`
   - Copy the address next to your balance

2. **Wrong POLYMARKET_FUNDER**
   - Make sure it's your Polymarket proxy address (not your Polygon wallet)
   - Should look like: `0x...` (different from signer address)
   - Run `poetry run python -m src.diagnose_config` to verify

3. **API Credentials Mismatch**
   - Regenerate API keys: `poetry run python -m src.generate_api_key`
   - Update `.env` with new credentials
   - Make sure private key matches

#### For MetaMask Users (signature_type=0):
1. **Wrong Signature Type**
   - Set `POLYMARKET_SIGNATURE_TYPE=0`
   - Leave `POLYMARKET_FUNDER` empty

2. **Wrong Private Key**
   - Verify the private key matches your wallet
   - Make sure it starts with `0x`
   - Export from MetaMask if needed

---

### Configuration Validation Failed
**Problem**: Bot reports configuration errors on startup.

**Solution**:
1. Read the error messages carefully
2. Check each setting mentioned
3. Verify format (numbers, true/false, etc.)
4. Run `poetry run python -m src.diagnose_config` for details
5. See [CONFIGURATION.md](CONFIGURATION.md) for correct formats

---

## 💰 Balance Issues

### Balance Shows $0.00
**Problem**: Bot shows $0 balance but you have funds on Polymarket.

**Solutions**:

1. **For Magic.link Users**:
   - Verify `POLYMARKET_FUNDER` is set correctly
   - Check it's your Polymarket proxy address (not Polygon wallet)
   - Run `poetry run python -m src.test_balance` to verify

2. **For MetaMask Users**:
   - Verify `POLYMARKET_SIGNATURE_TYPE=0`
   - Check private key matches wallet with funds
   - Verify funds are in Polymarket (not just on Polygon)

3. **General Checks**:
   - Check balance on Polymarket website
   - Verify wallet is connected to Polymarket
   - Make sure funds are in USDC (not other tokens)

---

### Insufficient Balance Error
**Problem**: Bot can't execute trades due to low balance.

**Solutions**:
1. **Add more funds** to your Polymarket wallet
2. **Reduce ORDER_SIZE** (e.g., from 10 to 5)
3. **Check MIN_BALANCE_REQUIRED** setting
4. **Verify balance** with `poetry run python -m src.test_balance`

---

## 🤖 Bot Operation Issues

### "No active BTC 15min market found"
**Problem**: Bot can't find a market to trade.

**Solutions**:
1. **Wait for next market** - Markets open every 15 minutes
2. **Check internet connection**
3. **Verify manually**: Visit `https://polymarket.com/crypto/15M`
4. **Check firewall/proxy** - May block market discovery
5. **Retry** - Markets may be between cycles

---

### Bot Runs But Finds No Opportunities
**Problem**: Bot scans continuously but never trades.

**This is Normal!** Arbitrage opportunities are rare.

**To Increase Chances**:
1. **Lower TARGET_PAIR_COST** (e.g., 0.995 instead of 0.99)
   - More opportunities, but less profit per trade
2. **Wait during volatile periods** - More price gaps occur
3. **Check market liquidity** - More liquid markets have more opportunities
4. **Increase ORDER_SIZE** (requires more capital)

**Remember**: Finding opportunities is expected to be infrequent.

---

### "Partial fill detected" Warning
**Problem**: Only one leg of the arbitrage filled.

**What Happens**:
- Bot automatically attempts to unwind the position
- May result in small loss
- Both legs should fill for guaranteed profit

**Prevention**:
1. Use `ORDER_TYPE=FOK` (Fill-or-Kill)
2. Ensure sufficient liquidity
3. Use smaller `ORDER_SIZE` if this happens frequently

---

### Trade Blocked by Risk Management
**Problem**: Bot finds opportunity but doesn't trade.

**Solutions**:
1. **Check risk limits** in `.env`:
   - `MAX_DAILY_LOSS`
   - `MAX_POSITION_SIZE`
   - `MAX_TRADES_PER_DAY`
   - `MAX_BALANCE_UTILIZATION`

2. **Review daily stats** in bot output

3. **Adjust limits** if needed:
   - Set to `0` to disable (not recommended)
   - Increase limits if too restrictive
   - Check daily stats to understand current status

4. **Wait for reset** - Daily limits reset at midnight

---

## 📊 Statistics & Logging Issues

### Statistics Not Showing
**Problem**: No statistics in final summary.

**Solutions**:
1. **Enable statistics**: Set `ENABLE_STATS=true`
2. **Check file permissions**: Ensure bot can write to `TRADE_LOG_FILE`
3. **Verify file path**: Check `TRADE_LOG_FILE` is correct
4. **Check for errors**: Look for file permission errors in logs

---

### Trade History File Missing
**Problem**: `trades.json` file not created.

**Solutions**:
1. **Check ENABLE_STATS**: Must be `true`
2. **Check file path**: Verify `TRADE_LOG_FILE` setting
3. **Check permissions**: Ensure bot can write files
4. **Wait for trades**: File created after first trade

---

### CSV Export Fails
**Problem**: Can't export trade history to CSV.

**Solutions**:
1. **Check file permissions**: Ensure write permissions
2. **Check file path**: Verify output path is valid
3. **Check for trades**: Must have trades to export
4. **Try different path**: Use absolute path if relative fails

---

## 🔌 Connection Issues

### WebSocket Connection Errors
**Problem**: WebSocket mode fails to connect.

**Solutions**:
1. **Disable WebSocket**: Set `USE_WSS=false`
2. **Check firewall**: May block WebSocket connections
3. **Check network**: Requires stable connection
4. **Use HTTPS mode**: Default mode is more reliable
5. **Check proxy/VPN**: May interfere with WebSocket

---

### API Connection Timeout
**Problem**: Bot can't connect to Polymarket API.

**Solutions**:
1. **Check internet connection**
2. **Check firewall/proxy settings**
3. **Verify API credentials** are correct
4. **Check Polymarket status** - service may be down
5. **Retry** - may be temporary network issue

---

## 🐛 Other Issues

### Bot Crashes on Startup
**Problem**: Bot exits immediately after starting.

**Solutions**:
1. **Check Python version**: Requires Python 3.10+
2. **Check dependencies**: Run `poetry install`
3. **Check configuration**: Run `poetry run python -m src.diagnose_config`
4. **Check logs**: Look for error messages
5. **Verify imports**: Try `poetry run python -c "from src.config import load_settings"`

---

### Import Errors
**Problem**: "ModuleNotFoundError" or import errors.

**Solutions**:
1. **Check virtual environment**: Make sure it's activated
2. **Install dependencies**: `poetry install`
3. **Check Python path**: Run from bot's root directory
4. **Reinstall dependencies**: `poetry install --sync`

---

### Permission Errors
**Problem**: Can't write files or access resources.

**Solutions**:
1. **Check file permissions**: Ensure write access
2. **Run as correct user**: Don't use root/admin unnecessarily
3. **Check directory permissions**: Ensure bot can create files
4. **Use absolute paths**: If relative paths fail

---

## 🔧 Debug Mode

Enable verbose logging for detailed debugging:

```env
VERBOSE=true
```

This provides detailed logs of all operations.

---

## 📞 Getting Help

If you've tried the solutions above and still have issues:

1. **Check logs**: Look for error messages
2. **Run diagnostics**: `poetry run python -m src.diagnose_config`
3. **Check configuration**: See [CONFIGURATION.md](CONFIGURATION.md)
4. **Contact support**: Telegram [@terauss](https://t.me/terauss)

When asking for help, provide:
- Error messages
- Configuration (remove sensitive data)
- Steps to reproduce
- System information (OS, Python version)

---

## ✅ Prevention Checklist

To avoid common issues:

- [ ] Run `poetry run python -m src.diagnose_config` before first use
- [ ] Test in simulation mode first (`DRY_RUN=true`)
- [ ] Verify balance with `poetry run python -m src.test_balance`
- [ ] Start with conservative settings
- [ ] Enable risk management
- [ ] Monitor first few trades closely
- [ ] Keep backup of `.env` file (without private key!)
- [ ] Read configuration documentation

---

## 📚 Related Documentation

- [GETTING_STARTED.md](GETTING_STARTED.md) - Initial setup
- [CONFIGURATION.md](CONFIGURATION.md) - Configuration guide
- [FEATURES.md](FEATURES.md) - Feature explanations

---

**Still having issues?** Contact [@terauss](https://t.me/terauss) on Telegram!


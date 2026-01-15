# 配置指南

[English](CONFIGURATION.md) | [中文说明](CONFIGURATION-CN.md)

本指南详细介绍 BTC 15 分钟套利机器人的所有配置项。

## 📁 配置文件

机器人使用根目录下的 `.env` 文件进行配置。如果不存在请创建该文件。

---

## 🔐 必需设置

### 私钥与 API 凭据

```env
# 你的钱包私钥（以 0x 开头）
POLYMARKET_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE

# 钱包类型：0 = MetaMask/外部钱包，1 = 邮箱登录 (Magic.link)
POLYMARKET_SIGNATURE_TYPE=1

# 仅 Magic.link 用户需要 - Polymarket 代理钱包地址
# MetaMask/外部钱包用户请留空
POLYMARKET_FUNDER=0xYOUR_PROXY_ADDRESS_HERE

# 通过以下命令生成：poetry run python -m src.generate_api_key
POLYMARKET_API_KEY=your_api_key_here
POLYMARKET_API_SECRET=your_api_secret_here
POLYMARKET_API_PASSPHRASE=your_passphrase_here
```

**如何获取私钥：**
- **MetaMask**：账户详情 → 显示私钥
- **邮箱登录**：在 Polymarket 设置中导出
- ⚠️ **绝不要分享你的私钥！**

**如何获取 API 凭据：**
1. 在 `.env` 中设置 `POLYMARKET_PRIVATE_KEY`
2. 运行：`poetry run python -m src.generate_api_key`
3. 将输出结果复制到 `.env` 文件中

---

## ⚙️ 交易设置

### 基础交易配置

```env
# 触发套利的最大组合成本（0.99 = 1% 利润空间）
TARGET_PAIR_COST=0.99

# 每次交易的股数（最低 5）
ORDER_SIZE=5

# 订单类型：FOK（全部成交否则取消），FAK（立即成交否则取消），GTC（一直挂单）
ORDER_TYPE=FOK

# 两次交易间最小间隔（防止过于频繁）
COOLDOWN_SECONDS=10
```

**建议：**
- `TARGET_PAIR_COST=0.99`（1% 利润空间）
- `ORDER_SIZE=5`（最小值，便于测试）
- `ORDER_TYPE=FOK`（最安全，双边未同时成交则取消）
- `COOLDOWN_SECONDS=10` 避免过度交易

### 模拟模式

```env
# 启用模拟模式（true = 不下真实订单，false = 实盘）
DRY_RUN=true

# 模拟初始余额（仅 DRY_RUN=true 时生效）
SIM_BALANCE=100
```

**重要提示：**
- 务必先用 `DRY_RUN=true` 进行测试
- 用 `SIM_BALANCE` 模拟你的实际交易资金
- 准备实盘时再设置 `DRY_RUN=false`

---

## 🛡️ 风险管理设置

所有风险管理项均为 **可选**（设为 0 则禁用）。

```env
# 每日最大亏损（USDC，0 = 禁用）
MAX_DAILY_LOSS=50.0

# 单笔最大持仓规模（USDC，0 = 禁用）
MAX_POSITION_SIZE=100.0

# 每日最大交易次数（0 = 禁用）
MAX_TRADES_PER_DAY=20

# 继续交易所需最小余额
MIN_BALANCE_REQUIRED=10.0

# 单笔交易最大资金占用比例（0.8 = 80%）
MAX_BALANCE_UTILIZATION=0.8
```

**示例配置：**
```env
# 当日亏损达到 $50 后停止交易
MAX_DAILY_LOSS=50.0

# 单笔交易不超过 $100
MAX_POSITION_SIZE=100.0

# 每日最多 20 笔交易
MAX_TRADES_PER_DAY=20

# 账户至少保留 $10
MIN_BALANCE_REQUIRED=10.0

# 单笔最多使用 80% 余额
MAX_BALANCE_UTILIZATION=0.8
```

**为什么需要风险管理？**
- 避免过度亏损
- 控制仓位大小
- 限制交易频率
- 保护资金安全

---

## 📊 统计与日志设置

```env
# 启用统计跟踪（推荐 true）
ENABLE_STATS=true

# 交易历史文件路径（JSON 格式）
TRADE_LOG_FILE=trades.json

# 使用 Rich 控制台输出（需要 rich 包）
USE_RICH_OUTPUT=true

# 启用详细/调试日志
VERBOSE=false
```

**建议：**
- `ENABLE_STATS=true` 用于跟踪绩效
- `TRADE_LOG_FILE=trades.json` 保留交易历史
- `USE_RICH_OUTPUT=true` 提升控制台显示效果（rich 已包含在 Poetry 依赖中）
- 除非调试，否则保持 `VERBOSE=false`

---

## 🔌 高级设置

### WebSocket（可选 - 更低延迟）

```env
# 启用 WebSocket 市场数据（更低延迟）
USE_WSS=false

# WebSocket 地址（通常无需更改）
POLYMARKET_WS_URL=wss://ws-subscriptions-clob.polymarket.com
```

**适用场景：**
- 需要更低延迟
- 网络连接稳定
- 高频交易策略

**注意：** WebSocket 需要稳定网络；若连接不稳定，请使用默认 HTTPS 轮询模式。

### 市场选择

```env
# 强制指定市场（通常留空，自动发现）
POLYMARKET_MARKET_SLUG=
```

**通常建议留空** - 机器人会自动发现当前 BTC 15 分钟市场。

---

## 📝 完整示例配置

以下是适合新手的完整 `.env` 示例：

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

## ✅ 配置验证

机器人启动时会自动验证配置，如有错误将显示清晰提示。

你也可以手动验证：

```bash
poetry run python -m src.diagnose_config
```

它会检查：
- 是否已设置全部必需字段
- 私钥格式是否正确
- 钱包类型是否与配置一致
- API 凭据是否可用
- 是否能获取余额

---

## 🔄 修改配置

1. **编辑 `.env` 文件** 完成修改
2. **重启机器人** 应用新配置
3. 如有需要，使用 `poetry run python -m src.diagnose_config` 验证

**重要提示：** 
- 修改 `POLYMARKET_PRIVATE_KEY` 后需要重新生成 API 凭据
- 调整风险限制会立即生效
- 部分修改需要重启机器人

---

## 📚 相关文档

- [GETTING_STARTED-CN.md](GETTING_STARTED-CN.md) - 快速入门
- [TROUBLESHOOTING-CN.md](TROUBLESHOOTING-CN.md) - 常见配置问题
- [FEATURES-CN.md](FEATURES-CN.md) - 功能详解

---

## 💡 使用小贴士

1. **保守起步**：降低 `ORDER_SIZE`，提高 `COOLDOWN_SECONDS`
2. **先测试**：实盘前务必 `DRY_RUN=true`
3. **设置限制**：使用风险管理保护资金
4. **持续监控**：定期查看 `TRADE_LOG_FILE` 评估表现
5. **逐步调整**：一次只改一个设置并观察效果

---

**需要帮助？** 请联系 Telegram：[@terauss](https://t.me/terauss)


# 比特币 15分钟套利机器人 - Polymarket

[English](README.md) | [中文说明](README-CN.md)

专为 Polymarket 上的比特币 15 分钟市场设计的专业套利机器人。

> 🆕 **增强版**：该机器人已进行了重大改进，增加了专业功能，包括统计跟踪、风险管理、增强型日志记录和配置验证。详情请参阅 [CHANGELOG.md](CHANGELOG.md)。**100% 向后兼容** - 所有新功能均为可选。
>
> 📚 **机器人新手？** 请查看 [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md) 获取快速入门指南！

---

## 🎯 策略

**纯套利**：当总成本 < $1.00 时，同时买入双方（看涨 UP + 看跌 DOWN），无论结果如何都能保证获利。

### 示例：
```
比特币上涨 (UP):     $0.48
比特币下跌 (DOWN):   $0.51
─────────────────────────
总计:                $0.99  ✅ < $1.00
利润:                每股 $0.01 (1.01%)
```

**为什么有效？**
- 在结算时，两方中的一方将支付每股 $1.00。
- 如果你总共支付了 $0.99，无论哪一方获胜，你都会赚取 $0.01。
- 这是 **保证利润**（纯套利）。

---

## 🚀 安装

### 1. 克隆仓库并进入项目目录
（确保你已安装 `git`，如果未安装请参考➡️[安装git教程](./安装git教程.md)）
```
git clone https://github.com/terauss/Polymarket-trading-bot-15min-BTC.git

cd Polymarket-trading-bot-15min-BTC
```

### 2. 安装依赖

- 📌 **Linux / macOS / WSL 用户**
```bash
# 自动检查并安装缺失依赖和配置环境
./install.sh
```

- 📌 **Windows 用户**
```powershell
# 以管理员身份运行 PowerShell，然后在项目根目录执行
Set-ExecutionPolicy Bypass -Scope CurrentUser
.\install.ps1
```

### 3. 复制示例环境变量文件
```
cp .env.example .env 
```

### 4. 参照以下说明配置环境变量

#### 必需变量

| 变量 | 描述 | 如何获取 |
|----------|-------------|---------------|
| `POLYMARKET_PRIVATE_KEY` | 你的钱包私钥（以 `0x` 开头） | 从你的钱包（MetaMask 等）导出，或使用与你的 Polymarket 账户关联的私钥 |
| `POLYMARKET_API_KEY` | Polymarket CLOB 的 API Key | 运行 `poetry run python -m src.generate_api_key` |
| `POLYMARKET_API_SECRET` | Polymarket CLOB 的 API Secret | 运行 `poetry run python -m src.generate_api_key` |
| `POLYMARKET_API_PASSPHRASE` | Polymarket CLOB 的 API Passphrase | 运行 `poetry run python -m src.generate_api_key` |

#### 钱包配置

| 变量 | 描述 | 值 |
|----------|-------------|-------|
| `POLYMARKET_SIGNATURE_TYPE` | 钱包签名类型 | `0` = EOA (MetaMask, 硬件钱包)<br>`1` = Magic.link (Polymarket 邮箱登录)<br>`2` = Gnosis Safe |
| `POLYMARKET_FUNDER` | 代理钱包地址（仅限 Magic.link 用户） | EOA 钱包请留 **空**。Magic.link 请参见下文说明。 |

##### ⚠️ 重要提示：Magic.link 用户 (signature_type=1)

如果你在 Polymarket 上使用 **邮箱登录** (Magic.link)，你拥有 **两个地址**：

1. **签名者地址 (Signer address)**（由你的私钥派生）：这是用于签署交易的钱包。
2. **代理钱包地址 (Proxy wallet address)** (`POLYMARKET_FUNDER`)：这是你在 Polymarket 上实际存放资金的地方。

**如何找到你的代理钱包地址：**
1. 进入你的 Polymarket 个人资料：`https://polymarket.com/@YOUR_USERNAME`
2. 点击余额旁边的 **"Copy address"**（复制地址）按钮。
3. 这就是你的 `POLYMARKET_FUNDER` —— 它应该以 `0x...` 开头，且与你的签名者地址 **不同**。

**常见错误：** 将 `POLYMARKET_FUNDER` 设置为你的 Polygon 钱包地址（你链上持有 USDC 的地方），而不是 Polymarket 代理地址。这会导致 `"invalid signature"` 错误。

**如何验证：** 运行 `poetry run python -m src.test_balance`：
- "Getting USDC balance" 通过 Polymarket API 显示余额（应显示你的资金）。
- "Balance on-chain" 直接查询 Polygon 链（如果你的资金在代理中，可能显示 $0，这是正常的）。

#### 交易配置

| 变量 | 描述 | 默认值 | 推荐值 |
|----------|-------------|---------|-------------|
| `TARGET_PAIR_COST` | 触发套利的最大组合成本 | `0.99` | `0.99` - `0.995` |
| `ORDER_SIZE` | 每次交易的股数（最小为 5） | `50` | 从 `5` 开始，测试后再增加 |
| `ORDER_TYPE` | 订单生效时间类型 (`FOK`, `FAK`, `GTC`) | `FOK` | 使用 `FOK` (全部成交否则取消) 以避免单边持仓 |
| `DRY_RUN` | 模拟模式 | `true` | 先设为 `true`，实盘交易时改为 `false` |
| `SIM_BALANCE` | 模拟模式下的初始资金 (`DRY_RUN=true`) | `0` | 例如 `100` |
| `COOLDOWN_SECONDS` | 执行之间的最小秒数间隔 | `10` | 如果看到重复触发，请调高此值 |

#### 风险管理 (新) ⚡

| 变量 | 描述 | 默认值 | 推荐值 |
|----------|-------------|---------|-------------|
| `MAX_DAILY_LOSS` | 每日最大亏损 (USDC, 0 = 禁用) | `0` | 例如 `50.0` 以限制每日亏损 |
| `MAX_POSITION_SIZE` | 每笔交易最大持仓规模 (USDC, 0 = 禁用) | `0` | 例如 `100.0` 以限制单笔交易规模 |
| `MAX_TRADES_PER_DAY` | 每日最大交易次数 (0 = 禁用) | `0` | 例如 `20` 以限制交易频率 |
| `MIN_BALANCE_REQUIRED` | 继续交易所需的最小余额 | `10.0` | 根据你的风险偏好调整 |
| `MAX_BALANCE_UTILIZATION` | 每笔交易最大资金利用率 (0.8 = 80%) | `0.8` | 越低越保守 |

#### 统计与日志 (新) 📊

| 变量 | 描述 | 默认值 |
|----------|-------------|---------|
| `ENABLE_STATS` | 启用统计跟踪和交易历史记录 | `true` |
| `TRADE_LOG_FILE` | 交易历史 JSON 文件路径 | `trades.json` |
| `USE_RICH_OUTPUT` | 使用 Rich 控制台格式化（需要 `rich` 包） | `true` |
| `VERBOSE` | 启用详细 (DEBUG) 日志记录 | `false` |

#### 可选变量

| 变量 | 描述 |
|----------|-------------|
| `POLYMARKET_MARKET_SLUG` | 强制指定特定的市场标识符 (留空则自动发现) |
| `USE_WSS` | 启用 Polymarket 市场 WebSocket 推送 (`true`/`false`) |
| `POLYMARKET_WS_URL` | 基础 WSS URL (默认: `wss://ws-subscriptions-clob.polymarket.com`) |

---

## 🔑 生成 API Key

在运行机器人之前，你需要生成你的 Polymarket API 凭据。

### 第一步：设置你的私钥

确保 `.env` 文件已配置了私钥：
```env
POLYMARKET_PRIVATE_KEY=0x你的私钥填在这里
```

### 第二步：运行 API Key 生成器

```
poetry run python -m src.generate_api_key
```

它将输出类似以下内容：
```
API Key: abc123...
Secret: xyz789...
Passphrase: mypassphrase
```

### 第三步：将凭据添加到 `.env`

```env
POLYMARKET_API_KEY=abc123...
POLYMARKET_API_SECRET=xyz789...
POLYMARKET_API_PASSPHRASE=mypassphrase
```

> ⚠️ **重要**：API 凭据是根据你的私钥派生的。如果你更改了私钥，则需要重新生成 API 凭据。

---

## 🔍 诊断配置问题

如果你遇到 `"invalid signature"`（签名无效）错误，请运行诊断工具：

```
poetry run python -m src.diagnose_config
```

这将检查：
- `POLYMARKET_FUNDER` 是否正确设置（Magic.link 账户必需）。
- 签名者地址和资助者地址是否不同（Magic.link 账户应该不同）。
- 机器人是否能检测到 BTC 15分钟市场的 `neg_risk` 标志。
- 通过 Polymarket API 查询的当前 USDC 余额。

**"invalid signature" 的常见原因：**
1. Magic.link 账户的 `POLYMARKET_FUNDER` 为空。
2. `POLYMARKET_FUNDER` 设置成了你的 Polygon 钱包地址，而不是 Polymarket 代理钱包地址。
3. API 凭据是使用不同的私钥或配置生成的。
4. `neg_risk` 标志检测不正确（已在最新版本中修复 - 机器人现在对 BTC 15分钟市场强制设置 `neg_risk=True`）。

**关于 "Balance on-chain" 显示 $0：**
这对于 Magic.link 账户是 **正常** 的。你的资金存放在 Polymarket 代理合约中，而不是直接在你的 Polygon 钱包里。通过 API 显示的 "USDC balance" 才是正确的余额。

---

## 💰 检查余额

在开始交易前，验证你的钱包配置是否正确且有资金：

```
poetry run python -m src.test_balance
```

输出示例：
```
======================================================================
POLYMARKET 余额测试
======================================================================
Host: https://clob.polymarket.com
Signature Type: 1
Private Key: ✓
API Key: ✓
API Secret: ✓
API Passphrase: ✓
======================================================================

1. 正在创建 ClobClient...
   ✓ 客户端已创建

2. 正在从私钥派生 API 凭据...
   ✓ 凭据已配置

3. 正在获取钱包地址...
   ✓ 地址: 0x52e78F6071719C...

4. 正在获取 USDC 余额 (抵押品)...
   💰 USDC 余额: $25.123456

5. 正在直接在 Polygon 上验证余额...
   🔗 链上余额: $25.123456

======================================================================
测试完成
======================================================================
```

> ⚠️ 如果余额显示 `$0.00` 但你在 Polymarket 上确有资金，请检查你的 `POLYMARKET_SIGNATURE_TYPE` 和 `POLYMARKET_FUNDER` 设置。

---

## 💻 使用方法

### 模拟模式（建议首先使用）：

确保 `.env` 中的 `DRY_RUN=true`，然后运行：

```
poetry run python -m src.simple_arb_bot
```

机器人将扫描机会，但不会下达真实订单。

### 可选：WebSocket 市场数据（低延迟）

默认情况下，机器人通过 HTTPS 轮询 CLOB 订单簿。你可以选择启用 Polymarket CLOB **Market WebSocket** 推送，以接收实时的订单簿更新并减少每次扫描的延迟。

在 `.env` 中设置如下：

```env
USE_WSS=true
POLYMARKET_WS_URL=wss://ws-subscriptions-clob.polymarket.com
```

关于 WSS 模式的说明：
- 市场频道可以发送单个 JSON 对象或 JSON 数组（批量事件）。机器人可以处理这两种情况。
- 如果连接断开或代理/防火墙阻止了 WSS，机器人将重新连接并打印错误原因。
- 在内部，WSS 模式使用 `book` 快照 + `price_change` 增量维护内存中的 L2 订单簿。

然后以同样的方式运行机器人：

```
poetry run python -m src.simple_arb_bot
```

### 实盘交易模式：

1. 将 `.env` 中的 `DRY_RUN` 改为 `false`
2. 确保你的 Polymarket 钱包中有 USDC
3. 运行：
```
poetry run python -m src.simple_arb_bot
```

### 成对执行安全机制（避免“单边成交”）

在实际交易中，由于订单簿变动，可能出现 **仅一侧**（UP 或 DOWN）成交的情况。
为了降低出现不平衡头寸的风险，机器人现在：

- **同时提交双边订单**，然后通过轮询 `get_order` **验证** 每个订单。
- 只有当确认 **双方** 订单均已完全成交时，才会记录 **“EXECUTED (BOTH LEGS FILLED)”** 并增加 `trades_executed`。
- 如果仅有一侧成交，它将 **尽力取消** 剩余订单，并尝试通过提交 filled 一侧的 `SELL` 订单（使用 `FAK` - 立即成交否则取消，价格为当前的 `best_bid`）来 **平仓以抵消风险**。

建议：
- 入场时保持 `ORDER_TYPE=FOK` (全部成交否则取消)，以避免留下挂单。

重要提示：
- 这是一种 **风险降低** 手段，并非完美保证。在快速变动的市场中，平仓订单也可能失败或部分成交。
- 请始终在 Polymarket 上监控你的头寸，尤其是当你看到 “Partial fill detected”（检测到部分成交）警告时。

---

## 📊 功能特性

### 核心功能
✅ **自动发现** 活跃的比特币 15 分钟市场
✅ **检测机会**：当 price_up + price_down < 阈值时触发
✅ **执行感知定价**：使用订单簿卖单价 (Ask)，而非最后成交价
✅ **深度感知规模**：遍历卖单簿以确保 `ORDER_SIZE` 可以成交（使用保守的“最差成交”价格）
✅ **持续扫描**：无延迟（最大速度）
✅ **低延迟轮询**：并发获取 UP/DOWN 订单簿
✅ **自动切换**：当前市场关闭时自动切换到下一个市场
✅ **最终总结**：显示总投资、利润和市场结果
✅ **模拟模式**：进行无风险测试
✅ **余额验证**：在执行交易前验证余额
✅ **成对执行验证**：确认双边成交（否则取消并尝试平仓）

### 增强功能 (新) ⚡
✅ **统计跟踪**：全面的交易历史和性能指标
✅ **风险管理**：每日亏损限制、持仓规模限制、交易频率控制
✅ **配置验证**：启动前验证设置并提供有用的错误提示
✅ **增强日志**：带颜色的 Rich 控制台输出和更好的格式化（可选）
✅ **优雅停机**：保存统计数据后安全退出
✅ **交易历史导出**：将交易数据导出为 JSON 和 CSV 格式
✅ **性能分析**：胜率、平均利润和详细统计

---

## 📈 输出示例

```
🚀 比特币 15分钟套利机器人已启动
======================================================================
市场: btc-updown-15m-1765301400
剩余时间: 12m 34s
模式: 🔸 模拟模式
成本阈值: $0.99
订单规模: 5 股
======================================================================

[Scan #1] 12:34:56
无套利机会: UP=$0.48 + DOWN=$0.52 = $1.00 (需要 < $0.99)

🎯 检测到套利机会
======================================================================
UP 价格 (上涨):       $0.4800
DOWN 价格 (下跌):     $0.5100
总成本:               $0.9900
每股利润:             $0.0100
利润率 %:             1.01%
----------------------------------------------------------------------
订单规模:             双边各 5 股
总投资:               $4.95
预期赔付:             $5.00
预期利润:             $0.05
======================================================================
✅ 套利执行成功

🏁 市场已关闭 - 最终总结
======================================================================
市场: btc-updown-15m-1765301400
结果: UP (上涨) 📈
模式: 🔴 实盘交易
----------------------------------------------------------------------
检测到的总机会:      3
执行的总交易:        3
买入的总股数:        30
----------------------------------------------------------------------
总投入:               $14.85
结算时的预期赔付:    $15.00
预期利润:             $0.15 (1.01%)
----------------------------------------------------------------------
📊 总体统计数据:
  总交易次数:          3
  胜率:                100.0%
  每笔交易平均利润:    $0.05
  平均利润率 %:        1.01%
----------------------------------------------------------------------
⚠️ 风险管理:
  今日交易次数:        3
  今日净盈亏:          $0.15
======================================================================
```

---

## 📁 项目结构

```
Bot/
├── src/
│   ├── simple_arb_bot.py    # 主套利机器人脚本
│   ├── config.py            # 配置加载器
│   ├── config_validator.py  # 配置验证 (新)
│   ├── lookup.py            # 市场 ID 获取器
│   ├── trading.py           # 订单执行
│   ├── statistics.py        # 统计跟踪 (新)
│   ├── risk_manager.py      # 风险管理 (新)
│   ├── logger.py            # 增强型日志记录 (新)
│   ├── utils.py             # 工具函数 (新)
│   ├── wss_market.py        # WebSocket 市场客户端
│   ├── generate_api_key.py  # API Key 生成工具
│   ├── diagnose_config.py   # 配置诊断工具
│   └── test_balance.py      # 余额验证工具
├── tests/
│   └── test_state.py        # 单元测试
├── .env                     # 环境变量 (从 .env.example 创建)
├── .env.example             # 环境变量模板
├── requirements.txt         # 依赖库
├── README.md                # 英文原版 README
├── README-CN.md             # 本文件 (中文版)
├── CHANGELOG.md             # 详细更新日志
└── docs/                    # 文档目录
    ├── README.md            # 文档索引
    ├── GETTING_STARTED.md   # 快速入门指南
    ├── CONFIGURATION.md     # 配置指南
    ├── FEATURES.md          # 功能指南
    └── TROUBLESHOOTING.md   # 故障排除指南
```

---

## ⚠️ 警告

- ⚠️ **切勿在 Polymarket 钱包无资金时使用 `DRY_RUN=false`**
- ⚠️ **价差 (Spreads)** 可能会抵消利润（请验证流动性）
- ⚠️ 市场每 **15 分钟** 关闭一次（不要积压头寸）
- ⚠️ 从 **小额订单** 开始测试 (`ORDER_SIZE=5`)
- ⚠️ 本软件仅供 **教学使用** - 使用风险自担
- ⚠️ **绝不要向任何人泄露你的私钥**

---

## 🔧 故障排除

### 配置验证

机器人在启动前会验证你的配置。如果你看到验证错误：
- 检查错误消息以获取具体问题
- 验证 `.env` 文件格式
- 确保所有必需字段均已设置
- 运行 `poetry run python -m src.diagnose_config` 获取详细诊断

### "Invalid signature"（签名无效）错误
- 验证 `POLYMARKET_SIGNATURE_TYPE` 是否匹配你的钱包类型
- 使用 `poetry run python -m src.generate_api_key` 重新生成 API 凭据
- Magic.link 用户：确保 `POLYMARKET_FUNDER` 设置正确
- 运行 `poetry run python -m src.diagnose_config` 获取详细诊断

### 余额显示 $0 但我有资金
- 检查你的私钥是否对应于有资金的钱包
- 对于 Magic.link：私钥对应的是你的 EOA，而非代理钱包
- 运行 `poetry run python -m src.test_balance` 查看你的钱包地址
- 验证 Magic.link 账户是否设置了 `POLYMARKET_FUNDER`

### "No active BTC 15min market found"（未发现活跃的比特币15分钟市场）
- 市场每 15 分钟开放一次；请等待下一个
- 检查你的互联网连接
- 尝试手动访问 https://polymarket.com/crypto/15M

### 交易被风险管理拦截
- 检查你的风险管理设置 (`MAX_DAILY_LOSS`, `MAX_POSITION_SIZE` 等)
- 查看最终总结中的风险管理统计数据
- 根据需要调整限制（设为 0 以禁用）

### 统计数据未显示
- 确保 `.env` 文件中设置了 `ENABLE_STATS=true`
- 检查 `TRADE_LOG_FILE` 是否可写
- 验证你对机器人目录具有写权限

---

## 📚 资源与文档

### 内部文档
- **[docs/README.md](docs/README.md)** - 文档索引与导航
- **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)** - 快速入门指南（5分钟）
- **[docs/CONFIGURATION.md](docs/CONFIGURATION.md)** - 完整配置指南
- **[docs/FEATURES.md](docs/FEATURES.md)** - 详细功能说明
- **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - 常见问题与解决方案
- **[CHANGELOG.md](CHANGELOG.md)** - 所有改进的详细日志

### 外部资源
- [Polymarket 官网](https://polymarket.com/)
- [比特币 15分钟市场](https://polymarket.com/crypto/15M)
- [py-clob-client 文档](https://github.com/Polymarket/py-clob-client)

### 实用工具
- `poetry run python -m src.generate_api_key` - 生成 API 凭据
- `poetry run python -m src.test_balance` - 验证钱包配置和余额
- `poetry run python -m src.diagnose_config` - 诊断配置问题

---

## 🆕 新增内容

该机器人已通过专业功能进行了显著增强：

- **统计跟踪**：跟踪所有交易、性能指标并导出数据
- **风险管理**：配置每日限制、持仓规模和交易频率
- **增强日志**：带格式的 Rich 控制台输出
- **配置验证**：在交易前捕捉配置错误
- **优雅停机**：带数据保存的安全退出
- **更完善的文档**：全面的新手指南和详细文档

所有新功能均为 **可选**，且机器人 **100% 向后兼容**。详情请参阅 [CHANGELOG.md](CHANGELOG.md)。

---

## ⚖️ 免责声明

本软件仅供教学目的。交易涉及风险。本人对任何财务损失不承担责任。请始终进行自己的研究，切勿投入超过你承受能力的资金。

**风险管理功能**：虽然机器人包含风险管理工具，但这些并不能完全保证避免亏损。请始终监控你的交易，并根据你的风险承受能力设置适当的限制。

☕ **请我喝杯咖啡 (EVM):** `0xd9c5d6111983ea3692f1d29bec4ac7d6f723217a`
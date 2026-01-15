# 快速入门指南

[English](GETTING_STARTED.md) | [中文说明](GETTING_STARTED-CN.md)

欢迎！本指南将帮助你在几分钟内运行 BTC 15 分钟套利机器人。

## 📋 快速开始（5 分钟）

### 第一步：安装

```bash
# 克隆仓库
git clone https://github.com/terauss/Polymarket-trading-bot-15min-BTC
cd Polymarket-trading-bot-15min-BTC

# 安装 Poetry（如未安装）
pipx install poetry
# 或者: curl -sSL https://install.python-poetry.org | python3 -

# 安装依赖
poetry install
```

### 第二步：创建配置文件

在机器人根目录创建 `.env` 文件：

```env
# 必填
POLYMARKET_PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
POLYMARKET_SIGNATURE_TYPE=1

# 通过以下命令生成：poetry run python -m src.generate_api_key
POLYMARKET_API_KEY=
POLYMARKET_API_SECRET=
POLYMARKET_API_PASSPHRASE=

# 交易设置（新手推荐）
DRY_RUN=true
SIM_BALANCE=100
TARGET_PAIR_COST=0.99
ORDER_SIZE=5
ORDER_TYPE=FOK
COOLDOWN_SECONDS=10
```

### 第三步：生成 API Key

```bash
poetry run python -m src.generate_api_key
```

将输出的 API Key、Secret、Passphrase 填入 `.env` 文件。

### 第四步：测试配置

```bash
poetry run python -m src.test_balance
```

该步骤用于验证你的配置是否正确。

### 第五步：模拟模式运行（推荐先做）

```bash
poetry run python -m src.simple_arb_bot
```

机器人会以模拟模式运行（不会下真实订单），便于熟悉流程。

---

## 🎯 开始前你需要准备

- ✅ Python 3.10 或更高版本
- ✅ Polymarket 账号
- ✅ Polymarket 钱包中的 USDC（用于实盘交易）
- ✅ 钱包私钥
- ✅ 基本的终端/命令行知识

---

## 📖 下一步

1. **配置相关**：查看 [CONFIGURATION-CN.md](CONFIGURATION-CN.md)
2. **功能说明**：查看 [FEATURES-CN.md](FEATURES-CN.md)
3. **问题排查**：查看 [TROUBLESHOOTING-CN.md](TROUBLESHOOTING-CN.md)

---

## 🚦 快速检查清单

在开始实盘交易前，请确保：

- [ ] 模拟模式能成功运行（`DRY_RUN=true`）
- [ ] 已理解机器人工作流程
- [ ] 以小额资金完成过测试
- [ ] 已配置风险管理（见 [CONFIGURATION-CN.md](CONFIGURATION-CN.md)）
- [ ] Polymarket 钱包中有足够 USDC
- [ ] 实盘前将 `DRY_RUN=false`

---

## ⚠️ 重要提示

1. **务必先用模拟模式**（`DRY_RUN=true`）
2. **从小订单开始**（`ORDER_SIZE=5`）
3. **第一批交易请重点关注**
4. **不要泄露私钥**
5. **交易有风险** - 仅投入可承受损失的资金

---

## 📞 需要帮助？

- 查看 [TROUBLESHOOTING-CN.md](TROUBLESHOOTING-CN.md)
- Telegram：[@terauss](https://t.me/terauss)

---

**准备好了吗？** 请先在模拟模式下运行机器人，熟悉后再切换到实盘交易。


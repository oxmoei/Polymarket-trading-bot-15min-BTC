# 故障排除指南

[English](TROUBLESHOOTING.md) | [中文说明](TROUBLESHOOTING-CN.md)

BTC 15 分钟套利机器人常见问题与解决方案。

## 🔍 快速诊断

优先运行诊断工具：

```bash
poetry run python -m src.diagnose_config
```

该命令会检查你的配置并报告问题。

---

## ❌ 配置错误

### “POLYMARKET_PRIVATE_KEY is required”
**问题**：`.env` 文件中未设置私钥。

**解决方案**：
1. 打开 `.env` 文件
2. 添加：`POLYMARKET_PRIVATE_KEY=0xYOUR_KEY_HERE`
3. 确保以 `0x` 开头
4. 重启机器人

---

### “Invalid signature” 错误
**问题**：Polymarket API 认证失败。

**常见原因与解决方案**：

#### Magic.link 用户（signature_type=1）
1. **缺少 POLYMARKET_FUNDER**
   - 设置 `POLYMARKET_FUNDER` 为你的 Polymarket 代理钱包地址
   - 在以下页面查看：`https://polymarket.com/@YOUR_USERNAME`
   - 复制余额旁的地址

2. **POLYMARKET_FUNDER 错误**
   - 必须是 Polymarket 代理地址（不是 Polygon 钱包）
   - 地址应类似 `0x...`（与签名地址不同）
   - 使用 `poetry run python -m src.diagnose_config` 验证

3. **API 凭据不匹配**
   - 重新生成 API Key：`poetry run python -m src.generate_api_key`
   - 更新 `.env` 中的凭据
   - 确保私钥与凭据对应

#### MetaMask 用户（signature_type=0）
1. **签名类型错误**
   - 设置 `POLYMARKET_SIGNATURE_TYPE=0`
   - `POLYMARKET_FUNDER` 留空

2. **私钥错误**
   - 确认私钥对应你的钱包
   - 确保以 `0x` 开头
   - 如需导出，请从 MetaMask 获取

---

### 配置验证失败
**问题**：机器人启动时报告配置错误。

**解决方案**：
1. 仔细阅读错误提示
2. 检查提示中的每个设置
3. 验证格式（数字、true/false 等）
4. 运行 `poetry run python -m src.diagnose_config` 查看详细信息
5. 参考 [CONFIGURATION-CN.md](CONFIGURATION-CN.md) 纠正格式

---

## 💰 余额问题

### 余额显示 $0.00
**问题**：机器人显示余额为 $0，但你在 Polymarket 有资金。

**解决方案**：

1. **Magic.link 用户**：
   - 确保 `POLYMARKET_FUNDER` 设置正确
   - 确认是代理地址（非 Polygon 钱包地址）
   - 运行 `poetry run python -m src.test_balance` 验证

2. **MetaMask 用户**：
   - 确认 `POLYMARKET_SIGNATURE_TYPE=0`
   - 确认私钥对应有资金的钱包
   - 资金需在 Polymarket 内（不是仅在 Polygon 链上）

3. **通用检查**：
   - 检查 Polymarket 网站上的余额
   - 确认钱包已连接 Polymarket
   - 确保资金是 USDC（不是其他代币）

---

### 余额不足错误
**问题**：余额过低导致无法执行交易。

**解决方案**：
1. **充值资金** 到 Polymarket 钱包
2. **减少 ORDER_SIZE**（如 10 调整为 5）
3. **检查 MIN_BALANCE_REQUIRED** 设置
4. 使用 `poetry run python -m src.test_balance` **验证余额**

---

## 🤖 机器人运行问题

### “No active BTC 15min market found”
**问题**：机器人找不到可交易市场。

**解决方案**：
1. **等待下一个市场** - 市场每 15 分钟开放一次
2. **检查网络连接**
3. **手动验证**：访问 `https://polymarket.com/crypto/15M`
4. **检查代理/防火墙** - 可能阻止市场发现
5. **重试** - 可能处于空窗期

---

### 机器人运行但未发现机会
**问题**：机器人持续扫描但从未交易。

**这是正常情况！** 套利机会本就稀少。

**提高概率的方法**：
1. **降低 TARGET_PAIR_COST**（如 0.995 替代 0.99）
   - 机会更多，但利润更低
2. **在波动较大时段等待** - 价差更容易出现
3. **检查市场流动性** - 流动性越高机会越多
4. **提高 ORDER_SIZE**（需要更多资金）

**提示**：机会不频繁是预期内的现象。

---

### “Partial fill detected” 警告
**问题**：仅有一侧成交。

**系统行为**：
- 机器人会尝试自动平仓
- 可能产生小额亏损
- 为保证套利，需双边都成交

**预防建议**：
1. 使用 `ORDER_TYPE=FOK`（全部成交否则取消）
2. 确保流动性充足
3. 如频繁出现，可降低 `ORDER_SIZE`

---

### 交易被风险管理阻止
**问题**：发现机会但不执行交易。

**解决方案**：
1. **检查风险限制**（`.env`）：
   - `MAX_DAILY_LOSS`
   - `MAX_POSITION_SIZE`
   - `MAX_TRADES_PER_DAY`
   - `MAX_BALANCE_UTILIZATION`

2. **查看当日统计**（机器人输出）

3. **调整限制**（如有必要）：
   - 设置为 `0` 可禁用（不推荐）
   - 如果过于严格，可适当提高
   - 结合统计数据判断当前状态

4. **等待重置** - 每日限制在午夜重置

---

## 📊 统计与日志问题

### 统计数据未显示
**问题**：最终总结中没有统计信息。

**解决方案**：
1. **启用统计**：设置 `ENABLE_STATS=true`
2. **检查权限**：确保机器人能写入 `TRADE_LOG_FILE`
3. **检查路径**：确认 `TRADE_LOG_FILE` 设置正确
4. **检查错误日志**：是否有文件权限错误

---

### 交易历史文件缺失
**问题**：未生成 `trades.json` 文件。

**解决方案**：
1. **检查 ENABLE_STATS**：必须为 `true`
2. **检查路径**：确认 `TRADE_LOG_FILE` 设置正确
3. **检查权限**：确保目录可写
4. **等待交易**：文件在首次交易后生成

---

### CSV 导出失败
**问题**：无法导出交易历史为 CSV。

**解决方案**：
1. **检查权限**：确保可写
2. **检查路径**：输出路径是否有效
3. **确认有交易记录**：必须存在交易数据
4. **尝试绝对路径**：相对路径失败时使用绝对路径

---

## 🔌 连接问题

### WebSocket 连接失败
**问题**：WebSocket 模式无法连接。

**解决方案**：
1. **禁用 WebSocket**：设置 `USE_WSS=false`
2. **检查防火墙**：可能阻止 WebSocket 连接
3. **检查网络**：需要稳定连接
4. **改用 HTTPS 模式**：默认更稳定
5. **检查代理/VPN**：可能干扰连接

---

### API 连接超时
**问题**：无法连接 Polymarket API。

**解决方案**：
1. **检查网络连接**
2. **检查防火墙/代理设置**
3. **确认 API 凭据正确**
4. **检查 Polymarket 状态** - 可能服务异常
5. **重试** - 可能是临时网络问题

---

## 🐛 其他问题

### 启动即崩溃
**问题**：机器人启动后立即退出。

**解决方案**：
1. **检查 Python 版本**：要求 Python 3.10+
2. **检查依赖**：运行 `poetry install`
3. **检查配置**：运行 `poetry run python -m src.diagnose_config`
4. **检查日志**：查看错误提示
5. **验证导入**：尝试 `poetry run python -c "from src.config import load_settings"`

---

### 导入错误
**问题**：出现 “ModuleNotFoundError” 或导入异常。

**解决方案**：
1. **检查虚拟环境**：确保使用 Poetry 环境
2. **安装依赖**：`poetry install`
3. **检查运行路径**：在项目根目录执行命令
4. **重新同步依赖**：`poetry install --sync`

---

### 权限错误
**问题**：无法写入文件或访问资源。

**解决方案**：
1. **检查文件权限**：确保可写
2. **使用正确用户**：避免使用 root/admin
3. **检查目录权限**：确保可创建文件
4. **使用绝对路径**：相对路径失败时使用绝对路径

---

## 🔧 调试模式

启用详细日志以便调试：

```env
VERBOSE=true
```

这会输出更详细的运行日志。

---

## 📞 获取帮助

如仍有问题，请：

1. **查看日志**：寻找错误信息
2. **运行诊断**：`poetry run python -m src.diagnose_config`
3. **检查配置**：参考 [CONFIGURATION-CN.md](CONFIGURATION-CN.md)
4. **联系支持**：Telegram [@terauss](https://t.me/terauss)

提问时请提供：
- 错误信息
- 配置内容（删除敏感信息）
- 复现步骤
- 系统信息（OS、Python 版本）

---

## ✅ 预防检查清单

为了减少常见问题：

- [ ] 初次使用前运行 `poetry run python -m src.diagnose_config`
- [ ] 先在模拟模式测试（`DRY_RUN=true`）
- [ ] 使用 `poetry run python -m src.test_balance` 验证余额
- [ ] 保持保守的交易设置
- [ ] 启用风险管理
- [ ] 关注前几次交易
- [ ] 备份 `.env`（不包含私钥）
- [ ] 阅读配置文档

---

## 📚 相关文档

- [GETTING_STARTED-CN.md](GETTING_STARTED-CN.md) - 初始设置
- [CONFIGURATION-CN.md](CONFIGURATION-CN.md) - 配置指南
- [FEATURES-CN.md](FEATURES-CN.md) - 功能说明

---

**仍有疑问？** 请联系 Telegram：[@terauss](https://t.me/terauss)


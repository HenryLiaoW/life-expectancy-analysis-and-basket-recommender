# CRUD 手动测试指南

## 测试准备

当前测试数据库：`task1/data/CLI_demo.db`
- 初始记录数：12条
- 国家：China, India, USA, Brazil
- 年份：2015-2017

---

## 测试流程

### 📋 步骤1：查看初始状态

```bash
# 查看数据库概况
python task1/cli.py --db task1/data/CLI_demo.db info

# 查看所有记录（可选）
sqlite3 task1/data/CLI_demo.db "SELECT country, year, life_expect FROM life_expectancy ORDER BY country, year;"
```

---

### ➕ 步骤2：CREATE - 创建新记录

```bash
# 启动交互式创建
python task1/cli.py --db task1/data/CLI_demo.db create
```

**建议输入：**
- Country: `Japan`
- Year: `2020`
- Region: `Asia`
- Life Expectancy: `84.5`
- BMI: `23.2`
- Basic Water Access: `99.5`
- Health Expenditure: `10.9`
- Alcohol Consumption: `7.5`
- Polio Vaccination: `99`
- Diphtheria Vaccination: `99`
- 确认: `yes`

**验证创建成功：**
```bash
# 查看Japan的记录
python task1/cli.py --db task1/data/CLI_demo.db filter --country Japan

# 或用SQL直接查询
sqlite3 task1/data/CLI_demo.db "SELECT * FROM life_expectancy WHERE country='Japan';"
```

---

### 🔍 步骤3：READ - 查询记录

```bash
# 按国家查询
python task1/cli.py --db task1/data/CLI_demo.db filter --country Japan --stats

# 按地区查询
python task1/cli.py --db task1/data/CLI_demo.db filter --region Asia

# 按年份查询
python task1/cli.py --db task1/data/CLI_demo.db filter --year-min 2020 --year-max 2020
```

---

### ✏️ 步骤4：UPDATE - 更新记录

```bash
# 启动交互式更新
python task1/cli.py --db task1/data/CLI_demo.db update
```

**建议输入：**
- Country: `Japan`
- Year: `2020`
- Life Expectancy: `85.0` (从84.5改为85.0)
- BMI: `23.5` (从23.2改为23.5)
- 其他字段按Enter跳过
- 确认: `yes`

**验证更新成功：**
```bash
# 查看更新后的数据
python task1/cli.py --db task1/data/CLI_demo.db filter --country Japan

# 或用SQL确认
sqlite3 task1/data/CLI_demo.db "SELECT country, year, life_expect, bmi FROM life_expectancy WHERE country='Japan';"
```

---

### 🗑️ 步骤5：DELETE - 删除记录

```bash
# 启动交互式删除
python task1/cli.py --db task1/data/CLI_demo.db delete
```

**建议输入：**
- Country: `Japan`
- Year: `2020`
- 第一次确认: `yes`
- 第二次确认: `DELETE` (必须大写)

**验证删除成功：**
```bash
# 应该显示 "No records found"
python task1/cli.py --db task1/data/CLI_demo.db filter --country Japan

# 检查数据库回到初始状态
python task1/cli.py --db task1/data/CLI_demo.db info
```

---

## 快速验证命令

### 在每次操作后运行，观察记录数变化：

```bash
# 查看总记录数（初始应为12）
python task1/cli.py --db task1/data/CLI_demo.db info | grep "Total Records"

# 或直接SQL查询
sqlite3 task1/data/CLI_demo.db "SELECT COUNT(*) as total FROM life_expectancy;"
```

### 查看所有国家列表：

```bash
sqlite3 task1/data/CLI_demo.db "SELECT DISTINCT country FROM life_expectancy ORDER BY country;"
```

---

## 预期结果

| 操作 | 记录数变化 | 国家数变化 |
|------|-----------|-----------|
| 初始状态 | 12 | 4 (China, India, USA, Brazil) |
| CREATE Japan | 12 → 13 | 4 → 5 |
| UPDATE Japan | 13 (不变) | 5 (不变) |
| DELETE Japan | 13 → 12 | 5 → 4 |

---

## 故障排查

### 如果CREATE失败：
- 检查是否已存在相同的 country-year 组合
- 使用 `filter` 命令查询是否有冲突

### 如果UPDATE找不到记录：
- 确认国家名和年份拼写正确（区分大小写）
- 用 `filter` 命令先查询记录是否存在

### 如果DELETE没有反应：
- 第二次确认必须输入大写 `DELETE`
- 不是 `delete` 或 `Yes`

---

## 高级测试（可选）

### 测试错误处理：

```bash
# 尝试创建重复记录（应该失败）
python task1/cli.py --db task1/data/CLI_demo.db create
# 输入已存在的 China + 2015

# 尝试更新不存在的记录（应该失败）
python task1/cli.py --db task1/data/CLI_demo.db update
# 输入 NonExistent + 2099

# 尝试删除不存在的记录（应该失败）
python task1/cli.py --db task1/data/CLI_demo.db delete
# 输入 NonExistent + 2099
```

---

## 完成测试后

确认所有功能正常后，可以提交代码：

```bash
git add task1/cli.py task1/CRUD_CLI_GUIDE.md
git commit -m "feat(cli): Add interactive CRUD commands"
```

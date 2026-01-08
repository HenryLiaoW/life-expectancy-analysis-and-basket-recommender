# Task 2: 超市推荐系统

## 🔗 Git 仓库

**仓库链接**: `https://github.com/HenryLiaoW/PAI_SuhangLiao` (私有仓库)

**重要说明**: 该仓库配置为**私有**，已将模块导师添加为协作者用于评估。

---

## 🎯 项目概述

基于Python的推荐系统，使用图数据结构和共现分析来分析超市交易数据中的客户购买模式。

**核心功能:**
- 单品推荐
- 高频商品对发现
- 共同购买频率分析
- 购物篮推荐（扩展功能）
- 实时动态更新（扩展功能）
- 图可视化（ASCII和DOT格式导出）

## 📊 实现亮点

- **数据结构**: 邻接表（基于dict）实现高效图表示
- **算法**: 共现计数 + 堆基础Top-K选择（O(E log k) vs O(E log E)全排序）
- **设计模式**: 双层架构（图层 + 推荐层）+ 依赖注入
- **开发方法**: 测试驱动开发（TDD）
- **测试覆盖**: 85个综合测试（100%通过率）
- **可视化**: 纯Python ASCII艺术 + DOT格式导出

## 🚀 快速开始

### 环境要求

- Python 3.10 或更高版本
- pytest 9.0.1+ (用于测试)

### 安装

无需外部依赖！本项目仅使用Python标准库。

```bash
# 克隆仓库（如果尚未完成）
cd PAI_SuhangLiao

# 验证Python版本
python --version  # 应为 3.10+
```

### 运行应用程序

#### 方法1: 使用main入口点（推荐）

```bash
python task2/main.py
```

**main.py的功能**:
- 自动加载数据集 (`data/Supermarket_dataset_PAI.csv`)
- 构建共购图（167个商品，6,260条边）
- 启动交互式CLI菜单
- 提供7个分析功能（推荐、高频商品对、可视化等）

#### 方法2: 使用PYTHONPATH

```bash
PYTHONPATH=$PWD python task2/cli.py
```

#### 方法3: 使用Python模块

```bash
python -m task2.cli
```

---

## 🧪 运行测试

### 主测试入口点（推荐）

```bash
# 通过主测试文件运行所有测试
pytest task2/tests/test_main.py -v

# 运行并显示详细输出
pytest task2/tests/test_main.py -v --tb=short

# 运行并生成覆盖率报告
pytest task2/tests/test_main.py --cov=task2/src --cov-report=term-missing
```

### 运行所有测试（备选）

```bash
# 运行整个测试套件
pytest task2/tests/ -v
```

### 运行特定测试类

```bash
# 仅测试图数据结构
pytest task2/tests/test_main.py::TestGraphDataStructure -v

# 仅测试推荐引擎
pytest task2/tests/test_main.py::TestRecommendationEngine -v

# 测试集成和边界情况
pytest task2/tests/test_main.py::TestIntegrationAndEdgeCases -v
```

### 预期结果

```
======================== 85 passed in 2.71s ========================
```

**说明**: 测试套件包括:
- 19个图数据结构测试
- 27个推荐引擎测试
- 4个集成和边界情况测试
- 所有测试验证边界情况的正确处理（空输入、缺失数据、无效类型）

---

## 📁 项目结构

```
task2/
├── data/
│   └── Supermarket_dataset_PAI.csv    # 数据集（38,765条记录）
├── src/
│   ├── __init__.py
│   ├── graph_interface.py              # 抽象图接口（ABC）
│   ├── graph_adjacency_list.py         # 图实现（241行）
│   └── recommendation_engine.py        # 业务逻辑（149行）
├── tests/
│   ├── __init__.py
│   ├── conftest.py                     # 测试夹具
│   ├── test_main.py                    # ⭐ 主测试文件（85个测试）
│   ├── test_graph_adjacency_list.py    # 19个图测试
│   ├── test_recommendation_engine.py   # 21个引擎测试
│   └── test_smoke.py                   # 1个冒烟测试
├── docs/
│   ├── README.md                       # 完整英文文档（844行）
│   ├── README_CN.md                    # 本文件（简化中文版）
│   ├── FURPS_ANALYSIS.md               # FURPS+需求分析
│   ├── SOLID_PRINCIPLES_ANALYSIS.md    # SOLID原则分析
│   ├── DRY_ANALYSIS.md                 # DRY原则分析
│   └── analyze_graph_density.py        # 图密度分析脚本
├── cli.py                              # 命令行界面（420+行）
├── main.py                             # 主入口点
├── verify_performance_metrics.py       # 性能验证脚本
└── PERFORMANCE_VERIFICATION.txt        # 性能指标记录
```

---

## 🎮 CLI使用说明

### 主菜单

```
--- 主菜单 ---
1. 加载数据集
2. 单品推荐（需求1）
3. 最高频商品对（需求2）
4. 共购频率检查（需求3）
5. 购物篮推荐（扩展功能）
6. 动态更新模拟（扩展功能）
7. 图结构可视化
8. 系统统计信息
0. 退出
```

### 核心功能示例

#### 1. 加载数据集（首次必须）

```
选择: 1

📂 正在加载数据集: task2/data/Supermarket_dataset_PAI.csv
⏳ 处理交易并构建图...

✅ 数据集加载成功！
   唯一商品总数: 167
   总边数（共现关系）: 6260
```

#### 2. 单品推荐

```
选择: 2

--- 单品推荐 ---
输入商品名称: whole milk
推荐数量（默认5）: 10

📊 与 'whole milk' 最常一起购买的前10个商品:
----------------------------------------------------------------------
排名   商品名称                                     共购次数
----------------------------------------------------------------------
1      other vegetables                                       222
2      rolls/buns                                             209
3      soda                                                   174
...
```

#### 3. 最高频商品对

```
选择: 3

--- 最高频商品对 ---
显示商品对数量（默认10）: 5

📊 最常共同购买的前5个商品对:
--------------------------------------------------------------------------------
排名   商品1                     商品2                     频率
--------------------------------------------------------------------------------
1      other vegetables          whole milk                       222
2      rolls/buns                whole milk                       209
...
```

#### 7. 图可视化

```
选择: 7

--- 图可视化 ---
1. ASCII子图（商品邻域）
2. 导出为DOT格式（Graphviz）
0. 返回主菜单

选择可视化类型: 1

输入要可视化的商品名称: whole milk
显示最大邻居数（默认10）: 5

======================================================================
子图可视化: whole milk
======================================================================
中心节点: [whole milk]
邻居总数: 155
显示前5个邻居
----------------------------------------------------------------------

 1. [other vegetables]
    边权重: 222 ████████████████████████████████████████████

 2. [rolls/buns]
    边权重: 209 █████████████████████████████████████████

 3. [soda]
    边权重: 174 ██████████████████████████████████

 4. [yogurt]
    边权重: 167 █████████████████████████████████

 5. [sausage]
    边权重: 134 ██████████████████████████

======================================================================
```

---

## 🏗️ 系统架构

### 双层设计

```
┌─────────────────────────────────────┐
│   推荐引擎层                         │  ← 业务逻辑
│   - recommend_for_item()            │
│   - get_most_frequent_pairs()       │
│   - check_co_purchase()             │
│   - recommend_for_basket()          │
│   - update_with_transaction()       │
└─────────────────┬───────────────────┘
                  │ 使用
                  ↓
┌─────────────────────────────────────┐
│   图邻接表层                         │  ← 数据结构
│   - build_from_csv()                │
│   - add_transaction()               │
│   - get_neighbors()                 │
│   - get_top_neighbors()             │
│   - get_edge_weight()               │
│   - visualize_subgraph()            │  ← 可视化
│   - export_to_dot()                 │
└─────────────────────────────────────┘
```

### 关键设计决策

1. **邻接表 vs 邻接矩阵**
   - 稀疏图（45%密度）
   - 邻居查询: O(degree) vs O(n)
   - 动态边插入: O(1) vs O(1)
   - 空间: O(edges) vs O(n²)

2. **堆基础Top-K选择**
   - 使用大小为k的堆查找高频商品对: O(E log k)
   - 避免全排序 O(E log E)，当 k << E 时
   - 对于 k=10, E=6260: 20K次操作 vs 81K次操作（快4倍）

3. **稳定排序**
   - 主要: 计数降序 (-count)
   - 次要: 名称升序 (name)
   - 确保结果可重现

4. **优雅降级**
   - 缺失商品 → 返回空列表 []
   - 无效查询 → 返回 False/0
   - 与Task 1设计一致

---

## 📈 性能指标

### 数据集统计

- 记录数: 38,765 条交易
- 唯一商品: 167 个产品
- 购物篮: 14,963 个唯一(会员, 日期)组合
- 图边数: 6,260 对共现关系
- 图密度: 45.16%

### 计算复杂度

| 操作 | 时间复杂度 | 空间复杂度 |
|-----------|----------------|------------------|
| 构建图 | O(T × k²) | O(V + E) |
| 单品推荐 | O(d log d) | O(d) |
| Top-k商品对 | O(E log k) | O(E) |
| 共购检查 | O(1) | O(1) |
| 购物篮推荐 | O(b × d) | O(V) |
| 动态更新 | O(k²) | O(1) |

其中:
- T = 交易数量
- k = 平均购物篮大小
- V = 顶点数（商品数）
- E = 边数
- d = 平均度数
- b = 购物篮大小

### 性能验证

所有性能指标均可通过脚本验证：

```bash
python task2/verify_performance_metrics.py
```

**关键指标**:
- 测试数量: 85个测试
- 执行时间: 2.71秒
- 查询延迟: 16.40μs（1000次查询均值，5轮运行）
- 图加载时间: 0.04秒

结果保存在 `task2/PERFORMANCE_VERIFICATION.txt`

---

## 🛠️ 软件工程原则

本项目遵循专业软件工程实践，详细分析见独立文档：

### SOLID原则
详见: [`docs/SOLID_PRINCIPLES_ANALYSIS.md`](SOLID_PRINCIPLES_ANALYSIS.md)

- **SRP**: 图层/推荐层/CLI层职责分离
- **OCP**: 抽象Graph接口支持扩展
- **LSP**: 任何Graph实现可替换
- **ISP**: 最小接口设计
- **DIP**: 依赖注入 + 抽象依赖

### DRY原则
详见: [`docs/DRY_ANALYSIS.md`](DRY_ANALYSIS.md)

- 共现逻辑集中化
- 统一排序策略
- 堆基础Top-K单一实现
- 测试夹具复用

### FURPS+需求分析
详见: [`docs/FURPS_ANALYSIS.md`](FURPS_ANALYSIS.md)

- **功能性**: 6个核心需求（单品推荐、高频对、频率检查等）
- **可用性**: 专业CLI界面、格式化输出、ASCII可视化
- **可靠性**: 错误处理、优雅降级、边界测试
- **性能**: O(E log k)优化、16.40μs查询延迟
- **可维护性**: 双层架构、完整文档、类型提示

---

## 🧪 TDD开发流程

### 测试驱动开发方法

1. **Red阶段** (提交: d5bb206, d7a251c)
   - 先编写85个综合测试
   - 所有测试初始失败
   - 提前识别边界情况

2. **Green阶段** (提交: 0c3dac4)
   - 实现代码通过所有测试
   - Bug修复: 动态更新阈值发现
   - 85个测试通过（100%）

3. **Refactor阶段**
   - 实现稳定排序
   - 增强代码文档
   - 验证架构

### 测试类别

- **边界测试**: k超过可用商品数
- **错误处理**: 文件未找到、空输入
- **属性验证**: 图对称性、稳定排序
- **集成测试**: 端到端工作流
- **压力测试**: 大购物篮（50个商品）

---

## 🐛 已知限制

1. 商品名称区分大小写（设计选择）
2. 无模糊匹配处理拼写错误（实现了简单子串匹配）
3. 基于内存（会话间无持久化）
4. 单线程（数据集规模足够）

---

## 📚 参考文档

- **完整英文文档**: [`README.md`](README.md) - 844行详细文档
- **SOLID原则分析**: [`SOLID_PRINCIPLES_ANALYSIS.md`](SOLID_PRINCIPLES_ANALYSIS.md)
- **FURPS+需求分析**: [`FURPS_ANALYSIS.md`](FURPS_ANALYSIS.md)
- **DRY原则分析**: [`DRY_ANALYSIS.md`](DRY_ANALYSIS.md)
- **性能验证结果**: `PERFORMANCE_VERIFICATION.txt`

---

## 📝 Git提交历史

```bash
# 查看TDD开发进程
git log --oneline task2/

0c3dac4 feat(task2): Green Phase complete - All 85 tests passing
d7a251c test(task2): Fix frequency increment test with get_pair_count method
d5bb206 test(task2): TDD Red Phase - Graph + Recommender layers
f595ebc chore(task2): initialize project structure with dataset and test skeleton
```

---

**作者**: Henry Liao  
**模块**: WM9QF-15 Programming for Artificial Intelligence  
**学校**: University of Warwick  
**日期**: 2026年1月

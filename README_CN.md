# PAI 个人作业 - 数据洞察仪表板

## 项目概述

本项目实现了一个基于Python的数据洞察工具，用于分析公共健康数据，特别是WHO预期寿命数据集。系统支持数据访问、清洗、过滤、相关性分析和展示，遵循专业软件工程实践。

**课程模块**: 人工智能编程 (WM9QF-15)  
**作者**: 廖苏航 (Suhang Liao)  
**作业权重**: 70%

## 代码仓库

- **GitHub 仓库**: [PAI_SuhangLiao](https://github.com/HenryLiaoW/PAI_SuhangLiao)
- **仓库状态**: 私有（课程导师作为协作者可访问）

## 功能特性

### Task 1: 公共健康报告的数据洞察仪表板

**已实现功能**:
1. **数据访问与加载**
   - 支持UTF-8编码的CSV文件加载
   - 数据加载到SQLite数据库（开发中）
   
2. **数据清洗与结构化**
   - 数值类型转换及错误处理
   - 缺失值处理（转换为None）
   - 字段级数据验证
   
3. **统计分析**
   - 预期寿命预测变量的Pearson相关性分析
   - 手工编码的相关性算法（无scipy依赖）
   
4. **管道编排**
   - 自动化数据清洗工作流
   - 导出清洗后的数据为CSV

## 系统要求

### 环境要求
- **Python**: 3.13+ （在3.13.5和3.14.0上测试通过）
- **操作系统**: macOS、Linux 或 Windows
- **依赖项**: 见下方要求列表

### Python依赖
```
pytest>=8.3.4
```

所有核心功能仅使用Python标准库：
- `csv` - CSV文件处理
- `math` - 数学运算
- `sqlite3` - 数据库操作
- `typing` - 类型提示

## 安装步骤

### 1. 克隆仓库
```bash
git clone https://github.com/HenryLiaoW/PAI_SuhangLiao.git
cd PAI_SuhangLiao
```

### 2. 设置Python环境

**方式A: 使用venv（推荐）**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

**方式B: 使用conda**
```bash
conda create -n pai python=3.13
conda activate pai
pip install pytest
```

### 3. 验证安装
```bash
python --version  # 应显示 Python 3.13+
pytest --version  # 应显示 pytest 8.3.4+
```

## 如何运行代码

### 运行数据清洗管道
```bash
# 清洗原始数据并导出为CSV
python -c "from task1.pipeline_clean_export import export_cleaned_dataset; export_cleaned_dataset('task1/data/life_expectancy.csv', 'task1/data/life_expectancy_cleaned.csv')"
```

### 运行相关性分析
```bash
# 分析预期寿命与预测变量之间的相关性
python -c "from task1.analysis_correlation import run_correlation_analysis; results = run_correlation_analysis('task1/data/life_expectancy_cleaned.csv'); print('\\n'.join([f'{var}: r={corr:.3f}' for var, corr in results]))"
```

### 运行所有测试
```bash
# 运行完整测试套件（27个测试）
pytest

# 运行带详细输出的测试
pytest -v

# 运行特定测试文件
pytest task1/tests/test_cleaner.py -v

# 运行带覆盖率报告的测试
pytest --cov=task1 --cov-report=html
```

### 测试输出示例
```
=========== test session starts ============
collected 27 items

task1/tests/test_analysis_correlation.py ..................  [ 66%]
task1/tests/test_cleaner.py .......                          [ 92%]
task1/tests/test_data_loader.py ..                           [100%]

============ 27 passed in 0.02s ============
```

## 项目结构

```
PAI_SuhangLiao/
├── README.md                          # 英文说明文档
├── README_CN.md                       # 中文说明文档（本文件）
├── pytest.ini                         # Pytest配置
├── SOLID_PRINCIPLES_ANALYSIS.md       # SOLID原则文档（英文）
├── SOLID_PRINCIPLES_ANALYSIS_CN.md    # SOLID原则文档（中文）
│
├── task1/                             # Task 1: 数据洞察仪表板
│   ├── __init__.py
│   ├── data_loader.py                 # CSV加载（单一职责）
│   ├── cleaner.py                     # 数据清洗和类型转换
│   ├── pipeline_clean_export.py       # 编排层
│   ├── analysis_correlation.py        # Pearson相关性分析
│   ├── database_loader.py             # SQLite数据库操作（开发中）
│   │
│   ├── data/
│   │   ├── life_expectancy.csv        # 原始WHO数据集
│   │   └── life_expectancy_cleaned.csv # 清洗后的输出
│   │
│   └── tests/
│       ├── test_data_loader.py        # 2个测试
│       ├── test_cleaner.py            # 7个测试
│       ├── test_analysis_correlation.py # 18个测试
│       └── test_database_loader.py    # 7个测试（开发中）
│
└── task2/                             # Task 2: 数据结构与算法
    ├── __init__.py
    └── tests/
```

## 开发方法论

### 测试驱动开发（TDD）
本项目严格遵循TDD工作流程：

1. **RED阶段**: 首先编写失败的测试
2. **GREEN阶段**: 实现最小代码以通过测试
3. **REFACTOR阶段**: 在保持测试通过的同时改进代码质量

**Git历史中的证据**:
```bash
git log --oneline
# 显示清晰的TDD进展：
# 1. test: 添加全面的测试（RED）
# 2. test: 添加桩实现（RED完成）
# 3. feat: 实现功能（GREEN）
# 4. docs: 增强文档（REFACTOR）
```

### SOLID原则
详细文档见 `SOLID_PRINCIPLES_ANALYSIS_CN.md`，包括：
- 单一职责原则（SRP）
- 开闭原则（OCP）
- 里氏替换原则（LSP）
- 接口隔离原则（ISP）
- 依赖倒置原则（DIP）

## 代码质量指标

- **测试总数**: 27个自动化测试
- **测试覆盖率**: 所有公共函数都已测试
- **模块数**: 4个核心模块，边界清晰
- **依赖项**: 最小化（核心功能仅使用Python标准库）
- **PEP 8合规性**: 通过命名约定和结构强制执行
- **文档**: 所有公共函数都有全面的文档字符串

## 数据来源

**数据集**: WHO预期寿命数据  
**格式**: UTF-8编码的CSV  
**字段**: 国家、年份、预期寿命、成人死亡率、婴儿死亡率、BMI、GDP等  
**来源**: 公共健康研究数据集

## 故障排除

### 常见问题

**1. 模块未找到错误**
```bash
# 确保从项目根目录运行
cd PAI_SuhangLiao

# 或添加到PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

**2. 文件编码错误**
- 所有文件使用UTF-8编码
- 如果Windows上仍有问题，确保控制台使用UTF-8: `chcp 65001`

**3. 测试失败**
```bash
# 清理测试工件
find . -name "test_*.db" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# 重新运行测试
pytest -v
```

## Git工作流程

### 提交规范
本项目使用[约定式提交](https://www.conventionalcommits.org/zh-hans/):
- `test:` - 添加或更新测试
- `feat:` - 新功能
- `fix:` - 错误修复
- `docs:` - 文档更改
- `refactor:` - 代码重构

### 查看Git历史
```bash
# 查看所有提交
git log --oneline --graph

# 查看TDD工作流程
git log --oneline | grep -E "(test|feat|docs)"
```

## 许可证与学术诚信

这是华威大学的学术作业。  
**AI协作级别**: 允许使用AI协作进行起草、改进和代码编写。

所有AI生成的内容都经过批判性评估和修改。

## 联系方式

**学生**: 廖苏航 (Suhang Liao)  
**邮箱**: u5697414@live.warwick.ac.uk  
**课程导师**: Amir Kayhani

---

*最后更新*: 2025年12月15日

# Data Filter - 函数调用流程图（快速参考）

**12个函数，46个测试 - 简明版**

---

## 📊 基础数据流

### 1. 获取数据
```
数据库 → get_data_as_dataframe() → DataFrame
```

### 2. 国家过滤
```
DataFrame → filter_by_country("China") → China的所有数据
```

### 3. 年份过滤
```
DataFrame → filter_by_year_range(2015, 2017) → 2015-2017年数据
```

### 4. 地区过滤
```
DataFrame → filter_by_region("Asia") → 亚洲地区数据
```

---

## 🔗 组合过滤流程

### 国家 + 年份
```
数据库 → get_data_as_dataframe() → DataFrame
                ↓
        filter_by_country("China")
                ↓
        filter_by_year_range(2016, 2017)
                ↓
        China 2016-2017年数据
```

### 地区 + 年份
```
数据库 → get_data_as_dataframe() → DataFrame
                ↓
        filter_by_region("Asia")
                ↓
        filter_by_year_range(2015, 2015)
                ↓
        亚洲2015年数据
```

---

## 📈 统计分析流程

### 计算统计指标
```
数据库 → get_data_as_dataframe() → DataFrame
                ↓
        filter_by_country("India")
                ↓
        calculate_statistics("life_expect")
                ↓
        {
            mean: 68.6,
            median: 68.6,
            std: 0.35,
            min: 68.3,
            max: 69.0,
            count: 3
        }
```

### 查看趋势
```
数据库 → get_country_trend("India", "life_expect")
                ↓
        DataFrame:
        year  | life_expect
        ------|------------
        2015  | 68.3
        2016  | 68.6
        2017  | 69.0
```

---

## 🔬 专题分析流程

### 基础设施分析
```
数据库 → get_data_as_dataframe() → DataFrame
                ↓
        analyze_infrastructure_impact()
                ↓
        输出: DataFrame with basic_water列
        
        发现: India 88-91% < USA 99%
        建议: 优先改善供水覆盖率
```

### 医疗支出分析
```
数据库 → get_data_as_dataframe() → DataFrame
                ↓
        analyze_healthcare_spending()
                ↓
        {
            mean_gghe_d: 4.2%,
            median_gghe_d: 3.6%,
            country_rankings: {
                "USA": 8.3%,
                "Brazil": 3.9%,
                "China": 3.3%,
                "India": 1.3%
            }
        }
```

### 营养指标分析
```
数据库 → get_data_as_dataframe() → DataFrame
                ↓
        analyze_nutrition_indicators()
                ↓
        DataFrame with bmi列
        
        发现: USA平均BMI 28.7 (超重)
             India平均BMI 21.7 (正常)
```

### 疫苗缺口识别
```
数据库 → get_data_as_dataframe() → DataFrame
                ↓
        identify_vaccination_gaps(threshold=90.0)
                ↓
        输出: 低于90%的国家
        
        country | polio | diphtheria | hepatitis
        --------|-------|------------|----------
        India   | 85%   | 87%        | 89%
        
        建议: 提高印度疫苗覆盖率
```

### 多国对比
```
数据库 → get_data_as_dataframe() → DataFrame
                ↓
        compare_modifiable_factors(
            countries=["China", "India"],
            factors=["basic_water", "gghe-d", "bmi"]
        )
                ↓
        country | year | basic_water | gghe-d | bmi
        --------|------|-------------|--------|-----
        China   | 2017 | 96.5%       | 3.4%   | 24.2
        India   | 2017 | 91.0%       | 1.4%   | 21.9
        
        差距: China在所有指标上都优于India
```

---

## 🎯 决策支持流程（终极武器）

### 政策干预优先级推荐
```
数据库 → get_data_as_dataframe() → DataFrame
                ↓
        get_policy_intervention_priorities(
            country="India",
            target_life_expectancy=75.0
        )
                ↓
        内部调用:
            filter_by_country("India")
            analyze_infrastructure_impact()
            analyze_healthcare_spending()
            analyze_nutrition_indicators()
            calculate_statistics()
                ↓
        输出: {
            "current_gap": 6.0年,
            "top_priorities": [
                "提高basic_water (88%→95%)",
                "增加gghe-d (1.2%→3%)",
                "改善bmi (21.5→23)"
            ],
            "estimated_impact": {
                "basic_water": +2.3年,
                "gghe-d": +1.8年,
                "bmi": +1.1年
            }
        }
```

---

## 🏗️ 三层架构（LEGO模型）

```
┌─────────────────────────────────────┐
│  决策层 (1个函数)                    │
│  get_policy_intervention_priorities │ ← 政策建议
└─────────────────────────────────────┘
                ↑ 调用
┌─────────────────────────────────────┐
│  专题分析层 (5个函数)                │
│  - analyze_infrastructure_impact    │
│  - analyze_healthcare_spending      │
│  - analyze_nutrition_indicators     │
│  - identify_vaccination_gaps        │
│  - compare_modifiable_factors       │
└─────────────────────────────────────┘
                ↑ 调用
┌─────────────────────────────────────┐
│  基础层 (6个函数)                    │
│  - get_data_as_dataframe            │ ← 数据源
│  - filter_by_country                │
│  - filter_by_year_range             │
│  - filter_by_region                 │
│  - calculate_statistics             │
│  - get_country_trend                │
└─────────────────────────────────────┘
```

**记忆诀窍**：
- 基础层 = 乐高积木 （6块）
- 专题层 = 用积木搭房子 （5座房子）
- 决策层 = 用房子建社区 （1个完整社区）

---

## 🎓 实战案例：印度健康政策分析

### 完整分析流程（6步）

**步骤1: 加载数据**
```
df = get_data_as_dataframe("life_expectancy.db")
```

**步骤2: 筛选印度**
```
india_df = filter_by_country(df, "India")
```

**步骤3: 查看趋势**
```
trend = get_country_trend("life_expectancy.db", "India", "life_expect")
→ 68.3 (2015) → 68.6 (2016) → 69.0 (2017)
```

**步骤4: 基础设施分析**
```
infra = analyze_infrastructure_impact(india_df)
→ basic_water: 88-91% (vs USA 99%)
→ 建议: 改善供水系统
```

**步骤5: 医疗支出分析**
```
healthcare = analyze_healthcare_spending(india_df)
→ gghe-d: 1.2-1.4% (vs USA 8.3%)
→ 建议: 增加政府医疗投入
```

**步骤6: 获取综合建议**
```
priorities = get_policy_intervention_priorities(
    df, "India", target_life_expectancy=75.0
)
→ 优先改善: 1) 供水 2) 医疗支出 3) 营养
→ 预期效果: 寿命提升6年
```

---

## 📋 函数速查表

| 函数 | 输入 | 输出 | 用途 |
|------|------|------|------|
| `get_data_as_dataframe` | db_path | DataFrame | 加载数据 |
| `filter_by_country` | df, country | DataFrame | 国家过滤 |
| `filter_by_year_range` | df, start, end | DataFrame | 年份过滤 |
| `filter_by_region` | df, region | DataFrame | 地区过滤 |
| `calculate_statistics` | df, column | Dict | 统计指标 |
| `get_country_trend` | db_path, country, metric | DataFrame | 时间序列 |
| `analyze_infrastructure_impact` | df, vars | DataFrame | 基础设施 |
| `analyze_healthcare_spending` | df, region | Dict | 医疗支出 |
| `analyze_nutrition_indicators` | df, year_range | DataFrame | 营养分析 |
| `identify_vaccination_gaps` | df, threshold | DataFrame | 疫苗缺口 |
| `compare_modifiable_factors` | df, countries, factors | DataFrame | 多国对比 |
| `get_policy_intervention_priorities` | df, country, target | Dict | 政策建议 |

---

## ✨ 核心设计理念

**排除循环定义**:
- ❌ infant_mort ↔ life_expect （定义上就相关）
- ❌ adult_mortality ↔ life_expect （废话）

**聚焦可修改因素**:
- ✅ basic_water (r=0.831) - 可以建供水系统
- ✅ gghe-d (r=0.610) - 可以增加预算
- ✅ bmi (r=0.598) - 可以改善营养

**目标**: 提供**可执行的政策建议**，而不是验证显而易见的事实。

---

*写报告时直接复制这些流程图即可！*

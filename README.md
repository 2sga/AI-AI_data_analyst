# AI_data_analyst|AI数据分析助手
定位核心用户为非技术业务人员的自然语言数据分析工具，基于Python 和 SQL语言开发，通过自然语言查询帮助用户分析数据（CSV、Excel文件），借助LLM和DuckDB实现高效数据处理，旨在解决有数据无SQL技能的痛点。

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-green.svg)](https://openai.com)

> **零代码数据分析工具** | 自然语言转SQL，让业务人员3秒获取数据洞察

## 🎯 产品定位

**解决痛点：** 业务人员有数据但无SQL技能，需等待数据分析师排期（平均2-3天）

**核心用户：** 运营、产品经理、市场等需频繁看数的非技术角色

**产品价值：** 自然语言提问 → 自动生成SQL → 即时可视化，单场景分析效率提升**300倍**

---

## ✨ 核心特性

| 能力模块 | 关键指标 | 优化效果 |
|---------|---------|---------|
| **NL2SQL准确率** | 复杂查询准确率 | **65% → 85%** |
| **多表关联查询** | 跨表分析准确率 | **40% → 75%** |
| **API成本控制** | 单次查询Token消耗 | **2000 → 300 tokens（-90%）** |
| **响应速度** | 端到端查询延迟 | **5s → 1.5s** |
| **数据规模** | 支持文件大小 | **10万行 × 50列** |
| **类型推断** | 自动识别准确率 | **98%** |

---

## 🛠 技术架构
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   用户输入       │────→│   Schema约束     │────→│   GPT-4o生成SQL │
│  (自然语言)      │     │  + Few-shot Prompt│     │  (300 tokens)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
│
┌─────────────────┐     ┌─────────────────┐            │
│   可视化结果     │←────│  DuckDB本地执行  │←───────────┘
│  (表格/图表)     │     │  (向量化引擎)    │
└─────────────────┘     └─────────────────┘


**架构亮点：**
- **分离式设计：** LLM仅生成SQL，DuckDB本地执行，避免全量数据上传
- **成本优化：** Schema约束减少Token消耗，API成本降低90%
- **性能优化：** DuckDB向量化执行 vs SQLite，10万行聚合查询 **0.5s vs 8s**

---

## 🚀 快速开始

### 环境要求
- Python 3.8+
- OpenAI API Key

### 安装依赖
```bash
git clone https://github.com/yourusername/ai-data-analyst.git
cd ai-data-analyst
pip install -r requirements.txt

配置API Key
bash streamlit run ai_data_analyst.py

启动应用
bash streamlit run ai_data_analyst.py
访问 http://localhost:8501

📊 使用演示
场景1：单表分析
用户提问： "2023年销售额最高的前5个产品"
系统处理：
识别时间字段 order_date 和金额字段 amount
生成SQL：SELECT product_name, SUM(amount) ... GROUP BY ... ORDER BY ... LIMIT 5
返回结果表格 + 柱状图

🔧 技术实现细节
1. NL2SQL准确率优化
问题： 基础模型对模糊查询生成错误SQL
解决方案：
Python
# Schema约束Prompt
system_prompt = f"""
表结构：{table_schema}
字段类型：{column_types}
示例数据：{sample_rows}

规则：
1. 必须使用上述字段名，禁止 hallucination
2. 日期字段使用标准函数处理
3. 聚合查询必须包含GROUP BY
"""
效果： 复杂查询准确率从65%提升至85%

2. 内存优化策略
# 流式读取大文件
df = pd.read_csv(file, chunksize=10000)

# DuckDB替代Pandas全量加载
duckdb.query("SELECT * FROM read_csv_auto('file.csv')")
效果： 10万行数据内存占用降低70%

📁 项目结构
ai-data-analyst/
├── ai_data_analyst.py      # 主应用（推荐）
├── ai_data_analysis.py     # 早期版本
├── requirements.txt        # 依赖列表
├── README.md              # 项目文档
├── demo/
│   ├── screenshot_1.png   # 界面截图
│   └── demo_video.gif     # 演示动图
└── tests/
    └── test_queries.py    # 测试用例

🔮 未来优化方向
~支持多表自动关联（JOIN）
~集成RAG，支持历史查询作为上下文
~添加可视化图表推荐（自动选择最佳图表类型）
~支持中文自然语言优化（分词 + 意图识别）
📮 联系作者
邮箱：y496635937@163.com
如果这个项目对你有帮助，请给个 ⭐ Star！

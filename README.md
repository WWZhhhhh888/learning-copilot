# 学习CoPilot 📚🤖

[![演示视频](https://img.shields.io/badge/▶️-观看演示视频-FF0000?style=for-the-badge&logo=bilibili)](https://www.bilibili.com/video/BV1AQGv6BE6D/)
[![GitHub stars](https://img.shields.io/github/stars/WWZhhhhh888/learning-copilot?style=social)](https://github.com/WWZhhhhh888/learning-copilot)

> AI驱动的个性化学习效率规划系统 + 多Agent联动 + 凑单机器人

## 📖 项目背景

大学生普遍面临以下问题：
- 不知道自己的高效学习时段
- 计划难执行，缺乏个性化规划
- 学习时间被琐事打乱
- 外卖凑单麻烦，统计混乱

学习CoPilot系列项目通过AI Agent解决这些问题。

## ✨ 核心项目

### 1. 学习CoPilot - AI学习规划系统
- 📊 **自动采集**：每分钟记录活动窗口，4097条数据
- 🤖 **AI预测**：随机森林预测高效时段，MAE 0.06分
- 📋 **智能规划**：DeepSeek大模型生成学习计划
- 🚀 **飞书推送**：每天早上8点自动推送
- 🔗 **多Agent联动**：计划自动同步到待办服务

### 2. 凑单助手 - 群聊凑单机器人
- 💬 **自然语言交互**：`我要凑单，目标50元`
- 📊 **自动统计**：实时累加金额、订单明细
- 💰 **自动算人均**：凑满后自动计算
- 🔔 **凑满提醒**：自动通知所有人

## 📁 产品设计文档

- [用户调研报告](docs/用户调研报告.md) - 基于29份问卷分析用户痛点
- [竞品分析](docs/竞品分析.md) - 对比微信群、美团拼单、小程序
- [产品需求文档](docs/PRD.md) - 功能列表、交互流程
- [原型图](docs/prototype.png) - 界面原型

## 🛠️ 技术栈

Python 3.10、Streamlit、scikit-learn、SQLite、DeepSeek API、飞书机器人、FastAPI

## 📊 项目效果

| 指标 | 数值 |
|------|------|
| 训练数据 | 4097条 |
| 模型误差 | MAE = 0.06分 |
| 用户采纳率 | 70% |
| 凑单意愿 | 82.75% |

## 🚀 快速开始

```bash
git clone https://github.com/WWZhhhhh888/learning-copilot.git
cd learning-copilot
conda create -n copilot python=3.10 -y
conda activate copilot
pip install -r requirements.txt
echo "DEEPSEEK_API_KEY=你的密钥" > .env

# 测试凑单机器人
python test_cli.py

# 运行学习Agent
python planner.py

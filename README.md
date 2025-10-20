# Kubernetes Release Tracker

自动监控和分析 Kubernetes 版本发布，使用 AI 生成详细的分析报告并发送通知。

## ✨ 特性

- 🔍 **自动追踪** Kubernetes 最新版本发布
- 📚 **CHANGELOG 解析** 自动从 Kubernetes CHANGELOG 文件中提取和分析变更内容
- 🤖 **AI 驱动分析** 使用大语言模型深入分析版本变更
- 📊 **详细报告** 生成 Markdown 和 JSON 格式的完整分析报告
- 📢 **即时通知** 通过如流（Ruliu）发送版本更新通知
- 🔗 **链式分析** 自动跟踪 PR 和 Issues 的关联关系
- ⚠️ **重点标注** 识别安全问题、破坏性变更、API 变更和废弃功能

## 📋 Kubernetes 版本特点

与 containerd 不同，Kubernetes 的 release 信息存储在 CHANGELOG 文件中：

- **Release Body**: 仅包含简短说明和 CHANGELOG 链接
- **CHANGELOG 文件**: 实际的版本变更内容在 `CHANGELOG-X.XX.md` 文件中
- **多版本共存**: 同一大版本的所有小版本（如 v1.34.0、v1.34.1、v1.34.0-rc.2）都在同一个 CHANGELOG 文件中
- **重点部分**:
  - Urgent Upgrade Notes（紧急升级注意事项）
  - API Changes（API 变更）
  - Deprecations（废弃功能）
  - Breaking Changes（破坏性变更）
  - Bug Fixes（Bug 修复）

## 🚀 快速开始

### 方式一：本地运行

#### 1. 安装依赖

```bash
pip install -r requirements.txt
```

#### 2. 配置环境

复制 `.env.example` 为 `.env` 并填写必要的 API tokens：

```bash
cp .env.example .env
```

编辑 `.env` 文件：

```bash
# GitHub API Token (可选，但推荐设置以提高 API 速率限制)
GITHUB_TOKEN=your_github_token

# Baidu Qianfan LLM API Token (必需)
QIANFAN_TOKEN=your_qianfan_token

# Ruliu Access Token (通知功能必需)
RULIU_ACCESS_TOKEN=your_ruliu_token

# Ruliu Target IDs (通知功能必需)
RULIU_TARGET_IDS=[123456789, 987654321]
```

#### 3. 测试连接

```bash
python main.py test
```

#### 4. 运行分析

```bash
# 分析最新稳定版本
python main.py analyze

# 包含预发布版本（alpha, beta, rc）
python main.py analyze --include-prerelease

# 只生成报告，不发送通知
python main.py analyze --no-notification

# 只发送通知，不生成报告
python main.py analyze --no-report
```

### 方式二：使用 GitHub Actions（推荐）

#### 1. Fork 项目并配置 Secrets

在 GitHub 仓库设置中添加：
- `PAT_TOKEN`: Personal Access Token（用于创建 PR）
- `QIANFAN_TOKEN`: 百度千帆 API Token
- `RULIU_ACCESS_TOKEN`: 如流 Access Token
- `RULIU_TARGET_IDS`: 如流目标用户 IDs

#### 2. 自动运行

- ⏰ 每天北京时间 09:00 自动运行
- 📋 自动创建 Pull Request 保存报告
- 📢 自动发送如流通知

#### 3. 手动触发

在 Actions 页面点击 "Run workflow" 按钮

#### 4. PR 评论触发

在任何 PR 中评论 `/rerun` 即可触发分析

详见 [DEPLOYMENT.md](DEPLOYMENT.md) 了解更多部署选项。

## 📖 命令说明

### analyze
运行完整的版本分析：

```bash
python main.py analyze [OPTIONS]

选项：
  --no-notification    跳过发送通知
  --no-report         跳过生成报告
  --include-prerelease 包含预发布版本
```

### test
测试所有外部连接（GitHub API、LLM API、Ruliu API）：

```bash
python main.py test
```

### summary
快速查看最新版本摘要：

```bash
python main.py summary [--include-prerelease]
```

### notify
发送测试通知：

```bash
python main.py notify -m "测试消息"
```

### notify_release
分析并发送版本通知：

```bash
python main.py notify_release [--include-prerelease]
```

### preview_notification
预览通知内容（不发送）：

```bash
python main.py preview_notification [--include-prerelease]
```

### config_info
显示当前配置：

```bash
python main.py config_info
```

### setup
初始化项目环境：

```bash
python main.py setup
```

## 📁 项目结构

```
kubernetes-release-tracker/
├── .github/
│   └── workflows/
│       ├── release-tracker.yml    # 主工作流（定时 + 手动）
│       └── pr-comment-trigger.yml # PR 评论触发工作流
├── main.py              # CLI 入口
├── config/
│   └── config.yaml     # 配置文件
├── src/
│   ├── __init__.py
│   ├── config.py       # 配置管理
│   ├── github_client.py    # GitHub API 客户端（支持 CHANGELOG 解析）
│   ├── link_analyzer.py    # 链接分析器
│   ├── llm_analyzer.py     # LLM 分析器
│   ├── notifier.py         # 通知模块
│   ├── report_generator.py # 报告生成器
│   └── tracker.py          # 主追踪器
├── reports/            # 生成的报告目录
├── tests/              # 测试文件
├── .env.example        # 环境变量模板
└── requirements.txt    # Python 依赖
```

## 🔧 配置说明

编辑 `config/config.yaml` 自定义配置：

```yaml
github:
  repo_owner: "kubernetes"
  repo_name: "kubernetes"

llm:
  model: "deepseek-r1"  # LLM 模型名称
  max_tokens: 4000
  temperature: 0.1

analysis:
  max_links_to_analyze: 50  # 最多分析的 PR 数量
  important_keywords:       # 重要关键词列表
    - "security"
    - "breaking change"
    - "deprecation"
  focus_sections:          # 重点关注的 CHANGELOG 部分
    - "Urgent Upgrade Notes"
    - "API Change"
    - "Deprecation"
```

## 📊 报告示例

工具会生成两种格式的报告：

1. **Markdown 报告** (`reports/kubernetes_release_vX.XX.X_TIMESTAMP.md`)
   - 包含完整的分析结果
   - AI 生成的总结和建议
   - PR 和 Issue 详细信息

2. **JSON 报告** (`reports/kubernetes_release_vX.XX.X_TIMESTAMP.json`)
   - 结构化数据，便于程序化处理
   - 包含所有分析数据

## 🔔 通知示例

通知内容包括：

- 📋 版本概要
- 📚 CHANGELOG 概览
- ⚠️ 破坏性变更
- 🔄 主要变更
- 🔒 安全更新
- 🐛 重要修复
- ⚡ 性能优化
- 📊 风险评估
- 💡 升级建议

## 🛠️ 开发

### 运行测试

```bash
pytest tests/
```

### 添加新功能

1. 在 `src/` 目录下创建新模块
2. 在 `config.py` 中添加相应配置
3. 更新 `tracker.py` 集成新功能
4. 添加测试用例

## 📝 注意事项

- GitHub API 有速率限制，建议设置 `GITHUB_TOKEN`
- CHANGELOG 文件可能很大，首次运行可能需要较长时间
- LLM 分析的质量依赖于提供的上下文和模型能力

## 🤝 贡献

欢迎提交 Issues 和 Pull Requests！

## 📄 许可证

MIT License

## 🔗 相关链接

- [Kubernetes Releases](https://github.com/kubernetes/kubernetes/releases)
- [Kubernetes CHANGELOG](https://github.com/kubernetes/kubernetes/tree/master/CHANGELOG)
- [GitHub API Documentation](https://docs.github.com/en/rest)

---

**🤖 Kubernetes Release Tracker** -


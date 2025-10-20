# Kubernetes Release Tracker 部署指南

本文档介绍如何部署和运行 Kubernetes Release Tracker。

## 🚀 部署方式

### 方式一：本地运行

#### 1. 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd kubernetes-release-tracker

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

#### 2. 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑 .env 文件，填写必要的 API tokens
vim .env
```

必需的环境变量：
- `QIANFAN_TOKEN`: 百度千帆 LLM API Token
- `RULIU_ACCESS_TOKEN`: 如流通知 Access Token
- `RULIU_TARGET_IDS`: 如流目标用户 IDs (JSON 数组格式)

可选的环境变量：
- `GITHUB_TOKEN`: GitHub API Token（推荐设置以提高速率限制）

#### 3. 测试

```bash
# 测试所有连接
python main.py test

# 查看最新版本信息
python main.py summary
```

#### 4. 运行

```bash
# 完整分析（生成报告 + 发送通知）
python main.py analyze

# 只发送通知，不生成报告
python main.py analyze --no-report

# 包含预发布版本
python main.py analyze --include-prerelease
```

### 方式二：使用 GitHub Actions

#### 1. Fork 项目

Fork 此仓库到你的 GitHub 账号。

#### 2. 配置 Secrets

在仓库的 Settings > Secrets and variables > Actions 中添加以下 secrets：

- `GITHUB_TOKEN`: 自动提供（用于基本 API 访问）
- `PAT_TOKEN`: GitHub Personal Access Token（用于创建 PR，可选）
- `QIANFAN_TOKEN`: 百度千帆 LLM API Token
- `RULIU_ACCESS_TOKEN`: 如流 Access Token
- `RULIU_TARGET_IDS`: 如流目标用户 IDs (JSON 数组格式，如 `[123456789]`)

**关于 PAT_TOKEN**:
- 如果你希望 workflow 自动创建 Pull Request 来保存分析报告，需要设置 `PAT_TOKEN`
- 创建方法：GitHub Settings > Developer settings > Personal access tokens > Generate new token
- 所需权限：`repo` (Full control of private repositories)

#### 3. 启用 Actions

1. 进入仓库的 Actions 标签页
2. 启用 GitHub Actions
3. Workflow 将自动按计划运行（每天北京时间 09:00）

#### 4. 触发方式

**自动触发**：
- 每天 UTC 时间 01:00 (北京时间 09:00) 自动运行
- 分析结果会自动创建 PR 并发送通知

**手动触发**：
- 在 Actions 标签页中，选择 "Kubernetes Release Tracker" workflow
- 点击 "Run workflow" 按钮

**PR 评论触发**：
- 在任何 Pull Request 中评论 `/rerun`
- 需要有 write 或 admin 权限
- 会自动运行分析并创建新的 PR

#### 5. Workflow 功能

**主 Workflow** (`release-tracker.yml`):
- ✅ 定时自动运行
- ✅ 手动触发支持
- ✅ 自动创建 Pull Request 保存报告
- ✅ 上传 Artifacts 作为备份
- ✅ 详细的执行日志

**PR 触发 Workflow** (`pr-comment-trigger.yml`):
- ✅ 通过 `/rerun` 命令触发
- ✅ 权限检查（只允许 write/admin 用户）
- ✅ 自动创建独立的 PR
- ✅ 评论反馈（成功/失败/权限不足）
- ✅ Emoji 反应确认

### 方式三：使用 Docker

#### 1. 构建镜像

```bash
# 创建 Dockerfile
cat > Dockerfile << 'EOF'
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

CMD ["python", "main.py", "analyze"]
EOF

# 构建镜像
docker build -t kubernetes-release-tracker .
```

#### 2. 运行容器

```bash
docker run --rm \
  -e GITHUB_TOKEN=$GITHUB_TOKEN \
  -e QIANFAN_TOKEN=$QIANFAN_TOKEN \
  -e RULIU_ACCESS_TOKEN=$RULIU_ACCESS_TOKEN \
  -e RULIU_TARGET_IDS=$RULIU_TARGET_IDS \
  -v $(pwd)/reports:/app/reports \
  kubernetes-release-tracker
```

#### 3. 使用 Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  tracker:
    build: .
    environment:
      - GITHUB_TOKEN=${GITHUB_TOKEN}
      - QIANFAN_TOKEN=${QIANFAN_TOKEN}
      - RULIU_ACCESS_TOKEN=${RULIU_ACCESS_TOKEN}
      - RULIU_TARGET_IDS=${RULIU_TARGET_IDS}
    volumes:
      - ./reports:/app/reports
```

运行：
```bash
docker-compose run --rm tracker
```

### 方式四：定时任务（Cron）

在 Linux/Mac 系统上使用 cron 定时运行：

```bash
# 编辑 crontab
crontab -e

# 添加定时任务（每天 09:00 运行）
0 9 * * * cd /path/to/kubernetes-release-tracker && /path/to/venv/bin/python main.py analyze --no-report >> /var/log/k8s-tracker.log 2>&1
```

## 📊 监控和日志

### 日志记录

所有输出都会打印到标准输出（stdout）。建议：

1. **本地运行**：重定向到日志文件
   ```bash
   python main.py analyze 2>&1 | tee -a tracker.log
   ```

2. **Docker 运行**：使用 Docker 日志
   ```bash
   docker logs <container-id>
   ```

3. **GitHub Actions**：在 Actions 标签页查看运行日志

### 报告存储

- 报告默认存储在 `reports/` 目录
- 每次运行生成两个文件：
  - `kubernetes_release_vX.XX.X_TIMESTAMP.md`: Markdown 格式报告
  - `kubernetes_release_vX.XX.X_TIMESTAMP.json`: JSON 格式数据

### 通知监控

通知发送到如流群聊，可以在如流中查看通知历史。

## 🔧 故障排查

### 问题：GitHub API 速率限制

**症状**：提示 "API rate limit exceeded"

**解决方案**：
1. 设置 `GITHUB_TOKEN` 环境变量
2. 减少 `max_links_to_analyze` 配置值
3. 增加运行间隔时间

### 问题：CHANGELOG 解析失败

**症状**：无法找到 CHANGELOG 或解析 sections 失败

**解决方案**：
1. 检查 Kubernetes 版本号是否正确
2. 确认 CHANGELOG URL 模板配置正确
3. 检查网络连接是否正常

### 问题：LLM API 调用失败

**症状**：AI 分析失败

**解决方案**：
1. 验证 `QIANFAN_TOKEN` 是否正确
2. 检查 LLM API URL 是否可访问
3. 确认账户余额充足

### 问题：通知发送失败

**症状**：无法发送如流通知

**解决方案**：
1. 验证 `RULIU_ACCESS_TOKEN` 是否有效
2. 确认 `RULIU_TARGET_IDS` 格式正确（JSON 数组）
3. 测试如流 API 连接：`python main.py notify -m "测试"`

## 🔒 安全建议

1. **不要在代码中硬编码敏感信息**
   - 使用环境变量或密钥管理服务
   - 将 `.env` 文件添加到 `.gitignore`

2. **最小权限原则**
   - GitHub Token 只需要 `public_repo` 权限
   - 定期轮换 API tokens

3. **定期审计**
   - 检查生成的报告内容
   - 监控 API 使用情况

## 📈 性能优化

1. **减少 API 调用**：
   - 调整 `max_links_to_analyze` 参数
   - 使用 `--no-report` 跳过报告生成

2. **缓存机制**：
   - 可以实现本地缓存减少重复的 API 调用

3. **并发处理**：
   - 考虑使用异步 API 调用提高性能

## 🔄 更新和维护

### 更新依赖

```bash
pip install --upgrade -r requirements.txt
```

### 更新代码

```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

### 清理旧报告

```bash
# 删除 30 天前的报告
find reports/ -name "*.md" -mtime +30 -delete
find reports/ -name "*.json" -mtime +30 -delete
```

## 📞 支持

遇到问题？

1. 查看 [README.md](README.md) 中的常见问题
2. 检查 [Issues](../../issues) 是否有相关问题
3. 提交新的 Issue 描述问题

---

**最后更新**: 2025-01-15


# Kubernetes 版本发布分析报告
## Kubernetes v1.35.0-rc.0 (v1.35.0-rc.0)

### 📋 版本信息
- **版本标签：** v1.35.0-rc.0
- **版本名称：** Kubernetes v1.35.0-rc.0
- **发布时间：** 2025-12-03T06:27:07Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.0-rc.0

### 🔍 分析统计
- **分析时间：** 2025-12-03 06:47:02
- **分析的 PR 数量：** 3
- **分析的 Issue 数量：** 2
- **重要项目数量：** 5

## 📊 版本概述
Kubernetes v1.35.0-rc.0 主要修复了admission控制中的竞争条件bug和alpha API警告问题，同时升级了Go版本以提升构建安全性。

## 🐛 重要问题修复
1. 修复alpha API在apiserver启动时产生不必要的版本警告日志 - [PR #135327](https://github.com/kubernetes/kubernetes/pull/135327) - **影响：** 减少生产环境日志噪音，避免误导性警告信息
2. 修复ValidatingAdmissionPolicy在新建命名空间后立即创建工作负载时出现虚假'namespace not found'错误 - [PR #135359](https://github.com/kubernetes/kubernetes/pull/135359) - **影响：** 防止admission控制误拒合法请求，提升工作负载创建可靠性

## ✨ 主要变更
1. 修复alpha API版本差异警告问题 - [PR #135327](https://github.com/kubernetes/kubernetes/pull/135327)
2. Admission控制中命名空间查找回退机制优化 - [PR #135359](https://github.com/kubernetes/kubernetes/pull/135359)
3. 升级Go版本到1.25.4和distroless iptables - [PR #135492](https://github.com/kubernetes/kubernetes/pull/135492)

## 🚀 性能优化
1. 升级Go语言版本到1.25.4，包含运行时性能优化和安全补丁 - [PR #135492](https://github.com/kubernetes/kubernetes/pull/135492) - **提升：** 潜在的内存和CPU效率改进，具体数据需实测验证

## 🎯 风险评估
整体风险评估：中等风险。作为RC版本，可能存在未发现的边缘情况。建议的升级时机：在测试集群验证无误后，可考虑在非关键生产环境小范围试用。需要特别关注admission控制策略的稳定性和Go版本升级后的运行时表现。

## 📋 升级建议
1. 建议在测试环境中充分验证ValidatingAdmissionPolicy的行为，特别是命名空间创建后的工作负载部署场景
2. 升级前检查是否使用了alpha API，确保版本兼容性
3. 由于是Release Candidate版本，不建议直接在生产环境部署，等待正式版发布

## 📋 Release 包含的变更

### PR #135327: Fix alpha API warnings for patch version differences
- **链接：** https://github.com/kubernetes/kubernetes/pull/135327
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复alpha API在补丁版本差异时产生的警告问题，这是对PR #134035的后续改进，涉及apiserver组件。

### PR #135359: Fallback to live ns lookup on admission if lister cannot find namespace
- **链接：** https://github.com/kubernetes/kubernetes/pull/135359
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复ValidatingAdmissionPolicy和MutatingAdmissionPolicy在lister过时时无法找到新创建namespace的问题，通过回退到实时查找namespace对象，使其行为与webhook admission等插件一致。解决1.30+版本中可能出现的虚假'namespace not found'错误。

### PR #135492: [go] Bump images and versions to go 1.25.4 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/135492
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, release-note, size/S, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将Kubernetes构建环境升级到Go 1.25.4和distroless iptables镜像，更新相关版本和镜像以保持最新。

---
*本报告由 Containerd Release Tracker 自动生成*
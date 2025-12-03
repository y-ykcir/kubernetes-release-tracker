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
- **分析时间：** 2025-12-03 06:47:18
- **分析的 PR 数量：** 3
- **分析的 Issue 数量：** 2
- **重要项目数量：** 5

## 📊 版本概述
Kubernetes v1.35.0-rc.0 主要修复了API服务器启动时的Alpha API版本警告和准入控制中的namespace查找竞争条件，提升了系统稳定性

## 🐛 重要问题修复
1. Alpha API版本警告修复 - [PR #135327](https://github.com/kubernetes/kubernetes/pull/135327) - **影响：** 消除apiserver日志中的误导性警告，避免运维人员误判 - 关联Issue: [#134023](https://github.com/kubernetes/kubernetes/issues/134023)
2. ValidatingAdmissionPolicy namespace竞争条件修复 - [PR #135359](https://github.com/kubernetes/kubernetes/pull/135359) - **影响：** 解决新建namespace后立即创建资源时可能出现的"namespace not found"错误拒绝 - 关联Issue: [#135352](https://github.com/kubernetes/kubernetes/issues/135352)

## ✨ 主要变更
1. 修复Alpha API版本警告 - [PR #135327](https://github.com/kubernetes/kubernetes/pull/135327) - 解决apiserver启动时因补丁版本差异导致的虚假警告
2. 准入控制namespace查找回退机制 - [PR #135359](https://github.com/kubernetes/kubernetes/pull/135359) - 当lister找不到新创建的namespace时回退到实时查找
3. 升级Go版本至1.25.4 - [PR #135492](https://github.com/kubernetes/kubernetes/pull/135492) - 构建环境更新

## 🚀 性能优化
1. Go 1.25.4版本升级 - [PR #135492](https://github.com/kubernetes/kubernetes/pull/135492) - **提升：** 可能带来运行时性能改进和安全补丁

## 🎯 风险评估
整体风险评估：低风险。主要包含bug修复，无重大API变更。但作为rc版本，仍需在测试环境充分验证准入控制功能的稳定性。

## 📋 升级建议
1. **生产环境建议：** 此版本为候选版本(rc.0)，不建议直接在生产环境部署
2. **测试重点：** 重点验证ValidatingAdmissionPolicy在快速创建namespace和资源时的稳定性
3. **监控建议：** 升级后关注apiserver日志中是否还有Alpha API相关警告
4. **升级时机：** 等待v1.35.0正式发布后再考虑生产环境升级

## 📋 Release 包含的变更

### PR #135327: Fix alpha API warnings for patch version differences
- **链接：** https://github.com/kubernetes/kubernetes/pull/135327
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  **PR #135327:** Fix alpha API warnings for patch version differences
**标签:** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage

**PR内容:** Follow up to #134035

<!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributor guidelines: https://git.k8...

### PR #135359: Fallback to live ns lookup on admission if lister cannot find namespace
- **链接：** https://github.com/kubernetes/kubernetes/pull/135359
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复ValidatingAdmissionPolicy和MutatingAdmissionPolicy在1.30+版本中的命名空间查找问题。当lister缓存中找不到新创建的命名空间时，会回退到实时查找命名空间对象，与其他admission插件行为保持一致。解决了默认配置下拦截新创建命名空间对象时可能出现的虚假'namespace not found'错误。

### PR #135492: [go] Bump images and versions to go 1.25.4 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/135492
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, release-note, size/S, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将Kubernetes构建环境升级到Go 1.25.4版本，并更新distroless iptables镜像。这是常规的版本更新，确保使用最新的Go语言特性和安全修复。更新后Kubernetes将基于Go 1.25.4构建。

---
*本报告由 Containerd Release Tracker 自动生成*
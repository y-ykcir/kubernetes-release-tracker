# Kubernetes 版本发布分析报告
## v1.35.4 (v1.35.4)

### 📋 版本信息
- **版本标签：** v1.35.4
- **版本名称：** v1.35.4
- **发布时间：** 2026-04-15T21:54:01Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.4

### 🔍 分析统计
- **分析时间：** 2026-04-15 22:47:03
- **分析的 PR 数量：** 6
- **分析的 Issue 数量：** 1
- **重要项目数量：** 7

## 📊 版本概述
Kubernetes v1.35.4 是一个补丁版本，主要修复了 StatefulSet 并行更新、kubelet 容器重启以及 kube-proxy 兼容性等多个关键回归问题，提升了集群的稳定性和可靠性。

## 🔒 安全问题修复
1. ⚠️ 升级构建工具链至 Go 1.25.9 - [PR #138304](https://github.com/kubernetes/kubernetes/pull/138304) - **风险级别：** 中 - 此升级通常包含 Go 运行时的安全补丁和漏洞修复，建议升级以获得最新的安全更新。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复审计日志中请求延迟计算错误（1.34+ 回归） - [PR #136281](https://github.com/kubernetes/kubernetes/pull/136281) - **影响：** 当请求耗时超过 500ms 时，审计日志中的 `requestReceivedTimestamp` 注解可能计算错误，影响监控和排障。
2. 修复 kubelet 重启后设备插件准入失败的问题 - [PR #138042](https://github.com/kubernetes/kubernetes/pull/138042) - **影响：** 使用 GPU 等设备插件的 Pod 在 kubelet 重启后可能无法被正确调度和启动。

## 💥 破坏性变更
1. 🚨 StatefulSet 的 `MaxUnavailableStatefulSet` 功能门控默认值从 `true` 改回 `false` - [PR #137926](https://github.com/kubernetes/kubernetes/pull/137926) - **影响：** 在 v1.35.0-1.35.3 中默认启用的并行 Pod 更新行为被恢复为串行更新。如果您的部署依赖此并行行为，需要显式启用该功能门控（`--feature-gates=MaxUnavailableStatefulSet=true`）。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复 StatefulSet MaxUnavailable 功能回归，将其默认值改回 `false` - [PR #137926](https://github.com/kubernetes/kubernetes/pull/137926) - **影响：** 修复了启用该功能时，首个 Pod 版本有缺陷会导致 StatefulSet 更新卡死的问题。
2. 修复 kubelet 重启后，带有 sidecar 和 startupProbe 的 Pod 中普通容器崩溃后无法重启的问题 - [PR #137885](https://github.com/kubernetes/kubernetes/pull/137885) - **影响：** 受影响的 Pod 会一直卡在 `RestartCount: 0` 状态，导致服务中断。
3. 修复 kube-proxy 在 nftables 1.1.3 系统上的兼容性问题 - [PR #137807](https://github.com/kubernetes/kubernetes/pull/137807) - **影响：** 使用 nftables 后端的 kube-proxy 在特定系统版本上可能无法正常工作。

## 🚀 性能优化
1. 升级至 Go 1.25.9 并更新基础镜像 - [PR #138304](https://github.com/kubernetes/kubernetes/pull/138304) - **提升：** 获得 Go 1.25.9 带来的运行时性能改进和安全修复，同时基础镜像更新可能带来更小的体积和更少的漏洞。

## 🎯 风险评估
整体风险评估：**中低风险**。此版本主要目的是修复 v1.35 系列中引入的几个严重回归性错误，特别是 StatefulSet 和 kubelet 相关的问题，这些修复显著提升了生产环境的稳定性。破坏性变更（MaxUnavailable 默认值回退）是为了纠正一个错误行为，对大多数用户而言是正向修复。建议的升级时机是：在测试环境验证通过后，尽快为生产环境安排维护窗口进行升级。需要特别关注的方面是 StatefulSet 的更新行为变化以及 sidecar 容器的重启逻辑。

## 📋 升级建议
1. **立即评估：** 如果您正在使用 v1.35.0-1.35.3 并启用了 StatefulSet 的并行更新（或依赖其默认开启行为），请检查您的 StatefulSet 滚动更新是否正常。升级到 v1.35.4 后，该功能默认关闭，更新将恢复为串行。如需并行，请显式设置功能门控。
2. **重点测试：** 如果您的集群中存在带有 sidecar（`restartPolicy: Always` 的 initContainer）和 `startupProbe` 的 Pod，请在升级前在测试环境中验证容器崩溃后能否正常重启。
3. **检查环境：** 如果节点系统使用 nftables 1.1.3，请确保升级到此版本以修复 kube-proxy 的兼容性问题。
4. **升级策略：** 这是一个修复关键回归的补丁版本，建议受影响的集群尽快安排升级。升级前，请在测试集群中充分验证上述修复点。

## 📋 Release 包含的变更

### PR #136281: Automated cherry pick of #135685: Bugfix: calculate request latency properly in audit log filter
- **链接：** https://github.com/kubernetes/kubernetes/pull/136281
- **状态：** closed
- **已合并：** 是
- **作者：** chaochn47
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了自 1.34 版本引入的一个回归问题：当 API 服务器请求延迟超过 500 毫秒时，审计日志中的请求延迟注解计算错误。

### PR #137807: Automated cherry pick of #137501: Fix kube-proxy on systems with nft 1.1.3 (take 2)
- **链接：** https://github.com/kubernetes/kubernetes/pull/137807
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, area/dependency, needs-triage
- **变更说明：**
  修复了 kube-proxy 在 nftables 模式下与 nft 1.1.3 版本系统的兼容性问题，确保 kube-proxy 能在这些系统上正常工作。

### PR #137885: Automated cherry pick of #137146: kubelet: fix containers not restarting when sidecar keeps running
- **链接：** https://github.com/kubernetes/kubernetes/pull/137885
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复了一个回归性 Bug：当 Pod 包含一个 restartPolicy 为 Always 的 sidecar（initContainer）并设置了 startupProbe 时，kubelet 重启后，常规容器崩溃后可能无法自动重启，导致 Pod 卡在 RestartCount: 0 状态。

### PR #137926: Automated cherry pick of #137904: KEP-961: demote maxUnavailable feature in statefulset to off by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/137926
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/XS, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复了 StatefulSet 在 1.35 版本中的一个回归问题：当启用 MaxUnavailableStatefulSet 特性时，Pod 版本可能无法更新。解决方案是将该特性默认设置为关闭。

### PR #138042: Automated cherry pick of #135485: Fix device plugin admission failure after container restart
- **链接：** https://github.com/kubernetes/kubernetes/pull/138042
- **状态：** closed
- **已合并：** 是
- **作者：** zxqlxy
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-triage
- **变更说明：**
  修复了 kubelet 重启后，设备插件准入可能失败导致相关测试用例失败的问题。该修复确保了容器重启后设备插件的正确管理。

### PR #138304: [release-1.35] Bump images and versions to go 1.25.9 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/138304
- **状态：** closed
- **已合并：** 是
- **作者：** xmudrii
- **标签：** area/test, lgtm, release-note, size/M, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将 Kubernetes 构建基础升级至 Go 1.25.9 并更新 distroless iptables 镜像。这是 release-1.35 分支的常规版本更新，不涉及功能变更。

---
*本报告由 Containerd Release Tracker 自动生成*
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
- **分析时间：** 2026-04-15 22:47:17
- **分析的 PR 数量：** 6
- **分析的 Issue 数量：** 1
- **重要项目数量：** 7

## 📊 版本概述
Kubernetes v1.35.4 是一个关键的补丁版本，主要修复了 v1.35 中引入的多个严重回归问题，特别是 StatefulSet 并行更新和 Sidecar 容器场景下的稳定性问题，强烈建议所有 v1.35.x 用户升级。

## 🐛 重要问题修复
1. 修复 StatefulSet 并行更新 (`MaxUnavailableStatefulSet`) 功能默认开启时，如果首个 Pod 版本有缺陷，会导致所有 Pod 卡在崩溃循环中且无法更新的致命问题 - [PR #137926](https://github.com/kubernetes/kubernetes/pull/137926) - **影响：** 使用 StatefulSet 且依赖滚动更新的应用（如数据库、有状态中间件）可能永远无法完成部署或更新，导致服务中断。
2. 修复当 Pod 包含 `restartPolicy: Always` 的 Sidecar 容器且定义了 `startupProbe` 时，kubelet 重启后普通容器崩溃无法自动重启的问题 - [PR #137885](https://github.com/kubernetes/kubernetes/pull/137885) - **影响：** 使用 Sidecar 模式的应用（如服务网格、日志收集代理）在主容器异常退出后无法恢复，导致 Pod 虽在运行但核心服务已死。
3. 修复 kube-proxy 在 nftables 版本为 1.1.3 的系统上无法正常工作的问题 - [PR #137807](https://github.com/kubernetes/kubernetes/pull/137807) - **影响：** 使用较新 Linux 发行版（携带 nft 1.1.3）的节点，其 Service 网络流量将无法被正确转发，导致服务访问失败。
4. 修复设备插件在容器重启后可能出现的准入失败问题 - [PR #138042](https://github.com/kubernetes/kubernetes/pull/138042) - **影响：** 使用 GPU、FPGA 等硬件加速设备的 Pod 在 kubelet 重启或容器重启后可能无法成功分配设备资源。

## 💥 破坏性变更
1. 🚨 StatefulSet 的 `MaxUnavailableStatefulSet` 功能（KEP-961）在此版本中默认被关闭 (`off by default`) - [PR #137926](https://github.com/kubernetes/kubernetes/pull/137926) - **影响：** 在 v1.35.0-1.35.3 中默认启用的并行 Pod 更新行为被回退为串行更新。如果您的应用依赖或已适配了并行更新以获得更快的 StatefulSet 滚动速度，升级后需要显式通过 `MaxUnavailableStatefulSet` 特性门控重新启用。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复 StatefulSet 并行更新 (`MaxUnavailableStatefulSet`) 功能默认开启导致的 Pod 无法更新问题 - [PR #137926](https://github.com/kubernetes/kubernetes/pull/137926) (关联 [Issue #137409](https://github.com/kubernetes/kubernetes/issues/137409))
2. 修复当 Pod 包含 Sidecar 容器时，普通容器崩溃后无法自动重启的问题 - [PR #137885](https://github.com/kubernetes/kubernetes/pull/137885)
3. 修复 kube-proxy 在 nftables 1.1.3 系统上的兼容性问题 - [PR #137807](https://github.com/kubernetes/kubernetes/pull/137807)
4. 修复审计日志中请求延迟注解在请求超过 500ms 时计算错误的问题 - [PR #136281](https://github.com/kubernetes/kubernetes/pull/136281)
5. 基础镜像升级至 Go 1.25.9 和 distroless iptables - [PR #138304](https://github.com/kubernetes/kubernetes/pull/138304)

## 🚀 性能优化
1. 基础构建版本升级至 Go 1.25.9 - [PR #138304](https://github.com/kubernetes/kubernetes/pull/138304) - **提升：** 包含 Go 语言运行时的安全补丁和性能改进，间接提升组件稳定性和安全性。

## 🎯 风险评估
**整体风险评估：中低风险（强烈建议升级）**。此版本主要为修复性版本，解决了前序版本中已知的、影响面较广的回归缺陷。升级风险主要来源于 `MaxUnavailableStatefulSet` 功能的默认行为变更，但这正是为了修复一个更严重的阻塞性问题。对于大多数集群，升级将显著提升稳定性。建议在测试环境验证后，尽快在生产环境安排升级窗口。

## 📋 升级建议
1. **立即升级**：如果您正在使用 v1.35.0 至 v1.35.3 版本，尤其是使用了 StatefulSet 或 Sidecar 容器模式，应尽快安排升级到 v1.35.4，以修复可能导致服务不可用的严重回归问题。
2. **StatefulSet 用户注意**：升级后，StatefulSet 的滚动更新策略将恢复为一次只更新一个 Pod 的串行模式。如果您希望保持并行更新能力，需要在 API Server、Controller Manager 和 Scheduler 的启动参数中显式设置 `--feature-gates=MaxUnavailableStatefulSet=true`。
3. **验证 Sidecar 行为**：升级后，请观察包含 Sidecar 容器的 Pod，确保其主容器在崩溃后能按预期重启。
4. **检查 nftables 版本**：如果节点使用 nftables 作为 kube-proxy 后端，请确认系统 nftables 版本，确保升级后 Service 网络正常。

## 📋 Release 包含的变更

### PR #136281: Automated cherry pick of #135685: Bugfix: calculate request latency properly in audit log filter
- **链接：** https://github.com/kubernetes/kubernetes/pull/136281
- **状态：** closed
- **已合并：** 是
- **作者：** chaochn47
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了从 1.34 版本引入的回归问题：当 API 服务器请求延迟超过 500 毫秒时，审计日志过滤器中的请求延迟注解计算不正确。

### PR #137807: Automated cherry pick of #137501: Fix kube-proxy on systems with nft 1.1.3 (take 2)
- **链接：** https://github.com/kubernetes/kubernetes/pull/137807
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, area/dependency, needs-triage
- **变更说明：**
  修复了 kube-proxy 在 nftables 模式下与 nft 1.1.3 版本系统的兼容性问题，确保其能正常工作。

### PR #137885: Automated cherry pick of #137146: kubelet: fix containers not restarting when sidecar keeps running
- **链接：** https://github.com/kubernetes/kubernetes/pull/137885
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复了 kubelet 重启后，Pod 中若存在 restartPolicy 为 Always 的 sidecar (initContainer) 且配置了 startupProbe，则常规容器在崩溃后无法重启的 bug。受影响的 Pod 会无限期卡在 RestartCount: 0 的状态。

### PR #137926: Automated cherry pick of #137904: KEP-961: demote maxUnavailable feature in statefulset to off by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/137926
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/XS, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复了 StatefulSet 在启用 MaxUnavailableStatefulSet 功能时 Pod 版本不更新的回归问题。该 PR 将此功能在 1.35 版本中默认设置为关闭，以恢复正常的并行 Pod 管理行为。

### PR #138042: Automated cherry pick of #135485: Fix device plugin admission failure after container restart
- **链接：** https://github.com/kubernetes/kubernetes/pull/138042
- **状态：** closed
- **已合并：** 是
- **作者：** zxqlxy
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-triage
- **变更说明：**
  修复了 kubelet 重启后，设备插件准入测试失败的问题。该修复确保了设备插件在容器重启后的正常工作。

### PR #138304: [release-1.35] Bump images and versions to go 1.25.9 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/138304
- **状态：** closed
- **已合并：** 是
- **作者：** xmudrii
- **标签：** area/test, lgtm, release-note, size/M, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将 Kubernetes 1.35 版本的构建基础升级至 Go 1.25.9，并更新了相关镜像以使用 distroless iptables。这是 release-engineering 的常规版本更新。

---
*本报告由 Containerd Release Tracker 自动生成*
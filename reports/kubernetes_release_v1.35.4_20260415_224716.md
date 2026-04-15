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
- **分析时间：** 2026-04-15 22:47:16
- **分析的 PR 数量：** 6
- **分析的 Issue 数量：** 1
- **重要项目数量：** 7

## 📊 版本概述
Kubernetes v1.35.4 是一个关键的补丁版本，主要修复了 v1.35 系列中几个严重的回归性问题，特别是 StatefulSet 滚动更新卡死和 sidecar 容器导致的 Pod 重启故障，建议所有运行 v1.35 的生产集群尽快升级。

## 🐛 重要问题修复
1. 修复 StatefulSet 滚动更新卡死：当 `MaxUnavailableStatefulSet` 功能启用且 Pod 的第一个版本有缺陷时，控制器无法更新 Pod 版本，导致滚动更新永久卡住 - [PR #137926](https://github.com/kubernetes/kubernetes/pull/137926) - **影响：** 生产环境中 StatefulSet 的滚动部署会失败，服务无法更新。
2. 修复 Sidecar 容器阻止重启：在包含 `restartPolicy: Always` 的 initContainer (sidecar) 且配置了 `startupProbe` 的 Pod 中，kubelet 重启后普通容器崩溃无法重启 - [PR #137885](https://github.com/kubernetes/kubernetes/pull/137885) - **影响：** 关键工作负载（如使用了 sidecar 模式的 Istio 服务网格）可能因容器崩溃而无法自动恢复，导致服务中断。
3. 修复 kube-proxy nftables 兼容性：修复了 kube-proxy 在 nftables 1.1.3 版本系统上的运行问题 - [PR #137807](https://github.com/kubernetes/kubernetes/pull/137807) - **影响：** 升级了系统 nftables 版本的节点，其上的 Service 流量会全部失效。
4. 修复设备插件测试失败/准入失败：解决 kubelet 重启后，依赖于设备插件（如 NVIDIA GPU）的容器可能无法通过准入检查的问题 - [PR #138042](https://github.com/kubernetes/kubernetes/pull/138042) - **影响：** AI/ML 或高性能计算等依赖特殊硬件的工作负载可靠性降低。

## ✨ 主要变更
1. 修复 StatefulSet `MaxUnavailable` 功能回归，默认将其关闭以避免 Pod 版本卡死 - [PR #137926](https://github.com/kubernetes/kubernetes/pull/137926) - **影响：** 启用了 `MaxUnavailableStatefulSet` 功能的集群，在 Pod 首次启动失败时，滚动更新会完全卡住，无法恢复。
2. 修复 kubelet 重启后，带有 sidecar 和 startupProbe 的 Pod 中普通容器崩溃后无法重启的问题 - [PR #137885](https://github.com/kubernetes/kubernetes/pull/137885) - **影响：** 受影响的 Pod 会一直处于 `RestartCount: 0` 的假死状态，导致服务不可用。
3. 修复 kube-proxy 在 nftables 1.1.3 系统上的兼容性问题 - [PR #137807](https://github.com/kubernetes/kubernetes/pull/137807) - **影响：** 使用 nftables 后端的 kube-proxy 在新版系统上无法正常工作，导致 Service 网络故障。
4. 修复审计日志中请求延迟注解在请求超过 500ms 时计算错误的问题 - [PR #136281](https://github.com/kubernetes/kubernetes/pull/136281) - **影响：** 影响从 v1.34 开始的版本，导致审计日志中的延迟指标不准确，影响监控和排障。
5. 修复 kubelet 重启后设备插件准入失败的问题 - [PR #138042](https://github.com/kubernetes/kubernetes/pull/138042) - **影响：** 使用 GPU、FPGA 等设备插件的 Pod 在 kubelet 重启后可能无法被正确调度和启动。

## 🚀 性能优化
1. 基础镜像和编译工具链升级：将构建所用的 Go 版本升级至 1.25.9，并更新 distroless iptables 镜像 - [PR #138304](https://github.com/kubernetes/kubernetes/pull/138304) - **提升：** 包含 Go 语言的安全补丁和运行时改进，可能带来潜在的性能和稳定性提升。

## 🎯 风险评估
**整体风险评估：中高**。此版本修复了多个具有高破坏性的回归性 Bug，特别是影响 StatefulSet 和 Pod 自愈能力的缺陷。**不升级的风险远大于升级的风险**。升级本身是低风险的补丁版本更新，但修复的问题直接影响核心控制器（StatefulSet）和节点组件（kubelet， kube-proxy）的稳定性。**建议升级时机**：应在下一个维护窗口立即安排升级。**需要特别关注的方面**：升级后观察 StatefulSet 工作负载的状态，并确认所有使用设备插件的工作负载调度正常。

## 📋 升级建议
1. **立即升级**：如果您正在运行 Kubernetes v1.35.0 到 v1.35.3，强烈建议尽快安排升级到 v1.35.4，以修复可能导致服务中断的严重回归性 Bug。
2. **重点验证**：升级后，请重点测试：1) StatefulSet 的滚动更新流程；2) 使用了 `sidecar` 容器模式且带有 `startupProbe` 的 Pod 的故障恢复能力；3) 节点网络（Service）功能。
3. **功能标志注意**：`MaxUnavailableStatefulSet` 功能在此版本中已被**默认禁用**。如果您之前显式启用了此功能并依赖其行为，升级后该功能将失效，需要重新评估。相关 Issue 描述了其风险 - [Issue #137409](https://github.com/kubernetes/kubernetes/issues/137409)。
4. **监控审计日志**：如果您依赖审计日志中的 `requestReceivedTimestamp` 和 `stageTimestamp` 注解来计算 API 延迟，升级后相关数据将恢复准确。

## 📋 Release 包含的变更

### PR #136281: Automated cherry pick of #135685: Bugfix: calculate request latency properly in audit log filter
- **链接：** https://github.com/kubernetes/kubernetes/pull/136281
- **状态：** closed
- **已合并：** 是
- **作者：** chaochn47
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了自1.34版本以来审计日志过滤器中的一个回归问题，该问题导致请求延迟超过500毫秒时，延迟注解计算不正确。

### PR #137807: Automated cherry pick of #137501: Fix kube-proxy on systems with nft 1.1.3 (take 2)
- **链接：** https://github.com/kubernetes/kubernetes/pull/137807
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, area/dependency, needs-triage
- **变更说明：**
  修复了kube-proxy在nftables模式下与nft 1.1.3版本系统的兼容性问题，确保其能正常工作。

### PR #137885: Automated cherry pick of #137146: kubelet: fix containers not restarting when sidecar keeps running
- **链接：** https://github.com/kubernetes/kubernetes/pull/137885
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复了一个回归bug：当Pod包含一个restartPolicy为Always的sidecar（initContainer）并设置了startupProbe时，kubelet重启后，常规容器崩溃后无法自动重启，导致Pod卡住。

### PR #137926: Automated cherry pick of #137904: KEP-961: demote maxUnavailable feature in statefulset to off by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/137926
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/XS, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复了StatefulSet在1.35版本中的一个回归问题：当启用MaxUnavailableStatefulSet特性时，Pod版本可能无法更新。此PR将该特性默认设置为关闭。

### PR #138042: Automated cherry pick of #135485: Fix device plugin admission failure after container restart
- **链接：** https://github.com/kubernetes/kubernetes/pull/138042
- **状态：** closed
- **已合并：** 是
- **作者：** zxqlxy
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-triage
- **变更说明：**
  修复了kubelet重启后，设备插件准入测试失败的问题。此cherry-pick包含了多个相关修复提交。

### PR #138304: [release-1.35] Bump images and versions to go 1.25.9 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/138304
- **状态：** closed
- **已合并：** 是
- **作者：** xmudrii
- **标签：** area/test, lgtm, release-note, size/M, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将Kubernetes构建版本升级至Go 1.25.9，并更新了distroless iptables基础镜像。这是一个针对release-1.35分支的版本更新PR。

---
*本报告由 Containerd Release Tracker 自动生成*
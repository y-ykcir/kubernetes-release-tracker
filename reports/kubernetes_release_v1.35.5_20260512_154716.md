# Kubernetes 版本发布分析报告
## v1.35.5 (v1.35.5)

### 📋 版本信息
- **版本标签：** v1.35.5
- **版本名称：** v1.35.5
- **发布时间：** 2026-05-12T15:37:25Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.5

### 🔍 分析统计
- **分析时间：** 2026-05-12 15:47:16
- **分析的 PR 数量：** 8
- **分析的 Issue 数量：** 0
- **重要项目数量：** 8

## 📊 版本概述
Kubernetes v1.35.5 是一个补丁版本，主要包含针对调度器、kube-proxy、kubeadm 和 Windows 网络的多个关键 Bug 修复，旨在提升集群的稳定性、性能和可靠性，无新增功能或破坏性变更。

## 🐛 重要问题修复
1. 修复调度器内存泄漏：当 Pod 在调度失败期间被同名 Pod 替换时，会导致 `inFlightPods` 状态泄漏和无限增长 - [PR #138434](https://github.com/kubernetes/kubernetes/pull/138434) - **影响：** 长期运行可能导致调度器内存使用量不断上升，影响调度性能。
2. 修复 Windows 网络端点清理：当 Pod IP 在 L2Bridge 网络的不同节点间复用时，陈旧的远程 HNS 端点未被清理 - [PR #138602](https://github.com/kubernetes/kubernetes/pull/138602) - **影响：** 导致流量被错误路由，引发 DNS 超时和服务中断，影响 Windows 节点上的 Pod 网络。
3. 修复 kubeadm etcd 健康检查：原先要求所有 etcd 成员健康，现在采用法定人数原则 - [PR #138539](https://github.com/kubernetes/kubernetes/pull/138539) - **影响：** 在部分 etcd 成员临时不健康（如重启）时，`kubeadm` 操作（如升级）可能失败，现在更符合高可用逻辑。
4. 修复 kubeadm `init` 阶段的 API 端点配置：确保使用 `localAPIEndpoint` 而非 `controlPlaneEndpoint` 进行初始 API 调用 - [PR #138683](https://github.com/kubernetes/kubernetes/pull/138683) - **影响：** 解决了在负载均衡器（如云厂商 LB）延迟配置时，`kubeadm init` 可能失败的问题。
5. 修复 Pod 启动延迟指标：`kubelet_pod_start_sli_duration_seconds_bucket` 现在正确排除了 init 容器运行时间、镜像拉取时间等 - [PR #138153](https://github.com/kubernetes/kubernetes/pull/138153) - **影响：** 该 SLI/SLO 监控指标现在更准确，基于不准确指标的告警可能需要调整阈值。
6. 修复 kubeadm worker 节点加入：跳过对 worker 节点 `LocalAPIEndpoint` 的默认值设置 - [PR #138803](https://github.com/kubernetes/kubernetes/pull/138803) - **影响：** 避免在 worker 节点加入时产生不必要的配置或潜在错误。

## ✨ 主要变更
1. 调度器修复了因 Pod 重建导致的内存泄漏问题 - [PR #138434](https://github.com/kubernetes/kubernetes/pull/138434)
2. kube-proxy 在大集群模式下优化，避免不必要的全量同步 - [PR #138636](https://github.com/kubernetes/kubernetes/pull/138636)
3. kubeadm 改进 etcd 集群健康检查逻辑，使用法定人数而非全部成员 - [PR #138539](https://github.com/kubernetes/kubernetes/pull/138539)
4. 修复 Windows L2Bridge 网络下 Pod IP 重用导致的 DNS 超时问题 - [PR #138602](https://github.com/kubernetes/kubernetes/pull/138602)
5. kubeadm 在 `init` 阶段使用 `localAPIEndpoint` 以解决负载均衡器延迟问题 - [PR #138683](https://github.com/kubernetes/kubernetes/pull/138683)
6. kubeadm 为 API Server 的 kubelet 客户端使用专用 ClusterRole - [PR #138959](https://github.com/kubernetes/kubernetes/pull/138959)

## 🚀 性能优化
1. kube-proxy 性能优化：在大型集群模式（端点超过1000个）下，不再执行周期性的全量同步操作 - [PR #138636](https://github.com/kubernetes/kubernetes/pull/138636) - **提升：** 减少 kube-proxy 在大型集群中的 CPU 和网络开销，提升网络平面的稳定性。
2. Windows 网络性能/稳定性修复：清理陈旧的远程端点，避免错误路由 - [PR #138602](https://github.com/kubernetes/kubernetes/pull/138602) - **提升：** 解决 DNS 超时问题，提升 Windows Pod 的网络性能和连接可靠性。

## 🎯 风险评估
整体风险评估：**低风险**。此版本为补丁版本，仅包含向后兼容的 Bug 修复和优化，无已知的破坏性变更或安全漏洞修复。升级风险较低。建议的升级时机：下一个常规维护窗口。需要特别关注的方面：1) Windows 节点升级后的网络验证；2) 调度器内存使用率在升级后的变化；3) 与 Pod 启动延迟 SLI 相关的监控告警。

## 📋 升级建议
1. **建议升级**：对于运行 1.35.x 版本且受上述 Bug 影响的集群，建议安排升级到此版本，特别是存在调度器内存增长、Windows 网络问题或使用 kubeadm 管理集群的情况。
2. **重点测试**：如果集群包含 Windows 节点，升级后需重点测试 Pod 网络连通性和 DNS 解析功能。
3. **监控指标**：如果正在使用 `kubelet_pod_start_sli_duration_seconds` 指标进行监控或告警，请注意其计算逻辑已变更，升级后需观察指标变化，必要时调整告警阈值。
4. **kubeadm 用户**：在新集群初始化或现有集群添加节点时，将受益于更健壮的 etcd 检查和对负载均衡器延迟的容忍。
5. **滚动升级**：按照标准滚动升级流程进行，确保关键工作负载有足够的副本和 Pod 中断预算（PDB）。

## 📋 Release 包含的变更

### PR #138153: Automated cherry pick of #131950: PodStartSLIDuration should exclude init container runtime, image pulling time, stateful pods, not immediately schedulable pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/138153
- **状态：** closed
- **已合并：** 是
- **作者：** alimaazamat
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/XL, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修正kubelet_pod_start_sli_duration_seconds_bucket metric，使其符合pod启动延迟SLI/SLO文档。排除init容器运行时、镜像拉取时间、stateful pods和不可立即调度的pods。

### PR #138434: Automated cherry pick of #138324: scheduler: fix inFlightPods leak when pod is recreated during scheduling failure
- **链接：** https://github.com/kubernetes/kubernetes/pull/138434
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复scheduler中inFlightPods泄漏问题。当Pod在调度失败期间被同名替换时，会导致队列状态残留和无限增长。scheduler现使用调度尝试的UID（而非刷新后Pod对象的UID）清除in-flight状态。

### PR #138539: Automated cherry pick of #138403: kubeadm: Evaluate etcd cluster health using quorum
- **链接：** https://github.com/kubernetes/kubernetes/pull/138539
- **状态：** closed
- **已合并：** 是
- **作者：** ahrtr
- **标签：** kind/bug, priority/important-soon, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubeadm改进etcd集群健康检查，采用quorum方法而非检查所有成员。当有足够健康投票成员时，检查不会失败，提高容错性。

### PR #138602: Automated cherry pick of #138000: Delete remote endpoint if it has same ip as local endpoint in the system.
- **链接：** https://github.com/kubernetes/kubernetes/pull/138602
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/XL, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复Windows上L2Bridge网络中Pod IP跨节点重用时，远程HNS端点清理问题。删除与本地端点IP相同的远程端点，防止DNS超时和流量错误路由。

### PR #138636: Automated cherry pick of #138571: kube-proxy: don't do full periodic syncs on large cluster mode
- **链接：** https://github.com/kubernetes/kubernetes/pull/138636
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  kube-proxy在大集群模式（超过1000个endpoints）下不再执行全同步操作，减少性能开销。

### PR #138683: Automated cherry pick of #138449: kubeadm: use the localAPIEndpoint for all API calls in 'init'
- **链接：** https://github.com/kubernetes/kubernetes/pull/138683
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, priority/backlog, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubeadm在'init'期间使用localAPIEndpoint进行所有API调用，而非ClusterConfiguration.controlPlaneEndpoint。解决负载均衡器延迟启动导致的问题。

### PR #138803: Automated cherry pick of #138692: kubeadm: skip LocalAPIEndpoint defaulting on worker join
- **链接：** https://github.com/kubernetes/kubernetes/pull/138803
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubeadm在worker节点执行'kubeadm join'时跳过LocalAPIEndpoint默认设置，避免不必要配置。

### PR #138959: Automated cherry pick of #138957: kubeadm: use dedicated ClusterRole for apiserver kubelet client
- **链接：** https://github.com/kubernetes/kubernetes/pull/138959
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  kubeadm使用专用ClusterRole 'system:kubelet-api-admin' 用于kube-apiserver kubelet客户端，提升权限管理安全性。

---
*本报告由 Containerd Release Tracker 自动生成*
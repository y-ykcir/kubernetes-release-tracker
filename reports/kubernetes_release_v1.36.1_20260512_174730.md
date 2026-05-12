# Kubernetes 版本发布分析报告
## v1.36.1 (v1.36.1)

### 📋 版本信息
- **版本标签：** v1.36.1
- **版本名称：** v1.36.1
- **发布时间：** 2026-05-12T16:39:25Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.36.1

### 🔍 分析统计
- **分析时间：** 2026-05-12 17:47:30
- **分析的 PR 数量：** 8
- **分析的 Issue 数量：** 1
- **重要项目数量：** 9

## 📊 版本概述
Kubernetes v1.36.1 是一个紧急补丁版本，主要修复了 v1.36.0 中导致 kubelet 在 ZFS 文件系统上崩溃、Windows 网络 DNS 超时以及大集群模式下 kube-proxy 性能退化等关键回归问题。

## 🐛 重要问题修复
1. 修复 ZFS 支持回归：在 v1.36.0 中，如果 `/var/lib/kubelet` 目录位于 ZFS 文件系统上，kubelet 将因 cAdvisor 插件缺失而无法启动 - [PR #138590](https://github.com/kubernetes/kubernetes/pull/138590) - **影响：** 使用 ZFS 的节点将完全不可用，导致 Pod 调度失败和节点失联。
2. 修复 Windows 网络端点清理：当 Pod IP 在 L2Bridge 网络的不同节点间复用时，未能清理陈旧的远程 HNS 端点，导致流量被错误路由和 DNS 超时 - [PR #138603](https://github.com/kubernetes/kubernetes/pull/138603) - **影响：** Windows 节点上的 Pod 网络连接不稳定，特别是 DNS 解析会间歇性失败。
3. 修复 kube-proxy 性能退化：在大型集群模式下，kube-proxy 错误地执行了全量同步操作，增加了不必要的 CPU 和网络开销 - [PR #138635](https://github.com/kubernetes/kubernetes/pull/138635) - **影响：** 大型集群的控制平面和节点网络性能下降，可能影响服务发现和负载均衡的响应速度。
4. 修复 kubeadm etcd 健康检查过于严格：原先要求所有 etcd 成员健康，现在采用法定人数原则，允许在部分成员不健康时仍能通过检查 - [PR #138538](https://github.com/kubernetes/kubernetes/pull/138538) - **影响：** 在 etcd 集群部分成员临时故障时，kubeadm 操作（如升级）可能被不必要的阻塞。
5. 修复 kubeadm init 对延迟负载均衡器的兼容性：在 init 阶段，使用本地 API 端点而非控制平面端点来构造内存中的 kubeconfig - [PR #138682](https://github.com/kubernetes/kubernetes/pull/138682) - **影响：** 在云环境或外部负载均衡器配置延迟的场景下，`kubeadm init` 可能失败。

## 💥 破坏性变更
1. 🚨 无新增的破坏性变更。此版本主要修复 v1.36.0 的回归问题。但请注意，从 v1.36.0 升级到 v1.36.1 是修复这些回归问题的必要步骤。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复 kubelet 在 ZFS 文件系统上因 cAdvisor 插件缺失而无法启动的严重回归 - [PR #138590](https://github.com/kubernetes/kubernetes/pull/138590)
2. 修复 Windows L2Bridge 网络中因 IP 重用导致 DNS 超时的网络问题 - [PR #138603](https://github.com/kubernetes/kubernetes/pull/138603)
3. 优化 kube-proxy 在大集群模式（>1000 endpoints）下避免执行全量同步的性能问题 - [PR #138635](https://github.com/kubernetes/kubernetes/pull/138635)
4. 改进 kubeadm 对 etcd 集群的健康检查逻辑，采用法定人数而非全部成员健康 - [PR #138538](https://github.com/kubernetes/kubernetes/pull/138538)
5. 修复 kubeadm init 阶段因负载均衡器延迟就绪导致的 API 调用问题 - [PR #138682](https://github.com/kubernetes/kubernetes/pull/138682)
6. 修复 kubeadm join worker 节点时不必要的 LocalAPIEndpoint 默认设置 - [PR #138802](https://github.com/kubernetes/kubernetes/pull/138802)
7. 修复动态资源分配（DRA）元数据解析器对未知 API 版本的处理逻辑 - [PR #138859](https://github.com/kubernetes/kubernetes/pull/138859)
8. 为 kube-apiserver 的 kubelet 客户端使用专用的 ClusterRole 以提升权限隔离 - [PR #138958](https://github.com/kubernetes/kubernetes/pull/138958)

## 🚀 性能优化
1. kube-proxy 大集群模式优化：避免在 endpoints 数量超过 1000 时进行全量同步，减少不必要的计算和网络流量 - [PR #138635](https://github.com/kubernetes/kubernetes/pull/138635) - **提升：** 显著降低大型集群中 kube-proxy 的周期性资源消耗，提升网络平面的稳定性。
2. 恢复 cAdvisor 对 ZFS 文件系统的支持：解决因缺失插件导致的 kubelet 启动失败和存储容量监控失效问题 - [PR #138590](https://github.com/kubernetes/kubernetes/pull/138590) - **提升：** 确保 ZFS 节点正常运行并恢复准确的临时存储（ephemeral storage）监控能力。

## 🎯 风险评估
整体风险评估：**低风险**。这是一个针对 v1.36.0 严重回归问题的补丁版本，修复了导致节点不可用和网络故障的核心缺陷，升级收益远大于风险。建议的升级时机：**尽快安排**，特别是受影响的集群。需要特别关注的方面：升级后验证 ZFS 节点上的 kubelet 状态、Windows 节点的网络功能以及大型集群中 kube-proxy 的负载是否恢复正常。

## 📋 升级建议
1. **强烈建议所有正在运行或计划部署 Kubernetes v1.36.0 的集群立即升级到 v1.36.1。** 特别是：1) 使用 ZFS 文件系统的节点；2) 包含 Windows 节点的集群；3) 大型集群（endpoints > 1000）。
2. 升级前，请确保已备份关键组件配置和 etcd 数据。对于生产集群，建议先在测试环境中验证升级流程。
3. 如果您的集群使用 kubeadm 且 etcd 集群处于非完全健康状态，此版本修复后，`kubeadm upgrade` 等操作的成功率会提高。
4. 关注节点（尤其是 Windows 节点）升级后的网络连通性测试，特别是跨节点 Pod 通信和 DNS 解析功能。

## 📋 Release 包含的变更

### PR #138538: Automated cherry pick of #138403: kubeadm: Evaluate etcd cluster health using quorum
- **链接：** https://github.com/kubernetes/kubernetes/pull/138538
- **状态：** closed
- **已合并：** 是
- **作者：** ahrtr
- **标签：** kind/bug, priority/important-soon, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubeadm 修复 etcd 集群健康检查逻辑，从检查所有成员健康改为基于 quorum（法定人数）判断。只要拥有足够数量的健康投票成员，检查即通过，提高了集群在部分成员故障时的健壮性。

### PR #138590: release-1.36: re-introduce cadvisor ZFS support to kubelet
- **链接：** https://github.com/kubernetes/kubernetes/pull/138590
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, kind/regression, needs-triage
- **变更说明：**
  在 Kubernetes 1.36 版本中重新引入 cadvisor 对 ZFS 文件系统的监控支持，修复了此前版本中意外移除该功能导致的回归问题。

### PR #138603: Automated cherry pick of #138000: Delete remote endpoint if it has same ip as local endpoint in the system.
- **链接：** https://github.com/kubernetes/kubernetes/pull/138603
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/XL, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复 Windows L2Bridge 网络中 Pod IP 跨节点重用时，陈旧的远程 HNS 端点未清理的问题。该问题曾导致 DNS 超时，因为流量被错误路由。修复确保清理同 IP 的远程端点。

### PR #138635: Automated cherry pick of #138571: kube-proxy: don't do full periodic syncs on large cluster mode
- **链接：** https://github.com/kubernetes/kubernetes/pull/138635
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  优化 kube-proxy 在大规模集群模式（endpoints 超过 1000）下的性能，停止执行全量周期性同步操作，以减少资源消耗。

### PR #138682: Automated cherry pick of #138449: kubeadm: use the localAPIEndpoint for all API calls in 'init'
- **链接：** https://github.com/kubernetes/kubernetes/pull/138682
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, priority/backlog, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm init 时 API 调用问题：当使用默认 admin.conf 和 super-admin.conf 时，在内存中构造指向 InitConfiguration.localAPIEndpoint 的 kubeconfig，而非 ClusterConfiguration.controlPlaneEndpoint，解决负载均衡器延迟配置导致的问题。

### PR #138802: Automated cherry pick of #138692: kubeadm: skip LocalAPIEndpoint defaulting on worker join
- **链接：** https://github.com/kubernetes/kubernetes/pull/138802
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm join 流程：对于工作节点，跳过 LocalAPIEndpoint 的默认设置步骤，避免不必要的配置操作。

### PR #138859: Automated cherry pick of #138530: KEP-5304:  DecodeMetadataFromStream only skips metadata entries with unknown API versions
- **链接：** https://github.com/kubernetes/kubernetes/pull/138859
- **状态：** closed
- **已合并：** 是
- **作者：** alaypatel07
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 KEP-5304 DRA 元数据读取助手 (DecodeMetadataFromStream) 的逻辑：仅在 API 版本未知时跳过元数据条目，若对象或文件格式错误则返回错误，提高错误处理的准确性。

### PR #138958: Automated cherry pick of #138957: kubeadm: use dedicated ClusterRole for apiserver kubelet client
- **链接：** https://github.com/kubernetes/kubernetes/pull/138958
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  kubeadm 权限清理：为 kube-apiserver 的 kubelet 客户端使用专用的 ClusterRole 'system:kubelet-api-admin'，替代原有可能权限过大的角色，遵循最小权限原则。

---
*本报告由 Containerd Release Tracker 自动生成*
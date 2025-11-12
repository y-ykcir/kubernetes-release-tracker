# Kubernetes 版本发布分析报告
## Kubernetes v1.34.2 (v1.34.2)

### 📋 版本信息
- **版本标签：** v1.34.2
- **版本名称：** Kubernetes v1.34.2
- **发布时间：** 2025-11-12T09:26:08Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.34.2

### 🔍 分析统计
- **分析时间：** 2025-11-12 12:46:51
- **分析的 PR 数量：** 15
- **分析的 Issue 数量：** 0
- **重要项目数量：** 15

## 📊 版本概述
Kubernetes v1.34.2 是一个稳定性修复版本，主要解决了 kubelet、kube-proxy、调度器和 kubeadm 的关键 bug，并升级了 Go 和 etcd 版本以提升安全性和性能。

## 🐛 重要问题修复
1. 修复 kubelet 指标注册问题：缺失 kubelet_volume_stats_* 指标，影响监控和告警 - [PR #133905](https://github.com/kubernetes/kubernetes/pull/133905) - **影响：** 生产环境中卷使用情况监控数据丢失
2. 修复 DRA kubelet 死锁：当 gRPC 连接空闲 30 分钟后导致设备资源分配失败 - [PR #133934](https://github.com/kubernetes/kubernetes/pull/133934) - **影响：** 使用动态资源分配的 Pod 可能无法正常启动
3. 修复 kube-proxy nftables 模式接口匹配错误：导致本地流量识别失败 - [PR #134118](https://github.com/kubernetes/kubernetes/pull/134118) - **影响：** 网络策略和服务路由可能异常
4. 修复调度器异步抢占 bug：减少抢占 Pod 的过度重试 - [PR #134247](https://github.com/kubernetes/kubernetes/pull/134247) - **影响：** 高负载下调度延迟增加
5. 修复 kube-controller-manager pod 控制器索引问题：处理错误 ownerReference 时可能崩溃 - [PR #134658](https://github.com/kubernetes/kubernetes/pull/134658) - **影响：** 控制器管理功能不稳定

## ✨ 主要变更
1. 修复 kubelet 指标多次注册导致缺失 volume 统计指标的问题 - [PR #133905](https://github.com/kubernetes/kubernetes/pull/133905)
2. 修复 DRA kubelet 在 gRPC 连接空闲时发生死锁的问题 - [PR #133934](https://github.com/kubernetes/kubernetes/pull/133934)
3. 修复 Windows kube-proxy 在 InternalTrafficPolicy=Local 时 ClusterIP 负载均衡器消失的问题 - [PR #134031](https://github.com/kubernetes/kubernetes/pull/134031)
4. 禁用 SchedulerAsyncAPICalls 特性门控以缓解调度器性能回归 - [PR #134401](https://github.com/kubernetes/kubernetes/pull/134401)
5. 升级 Go 版本到 1.24.9 并更新基础镜像 - [PR #134612](https://github.com/kubernetes/kubernetes/pull/134612)
6. 升级支持的 etcd 版本到 v3.5.24 - [PR #134861](https://github.com/kubernetes/kubernetes/pull/134861)

## 🚀 性能优化
1. 禁用 SchedulerAsyncAPICalls 特性门控：缓解高负载下调度器性能退化 - [PR #134401](https://github.com/kubernetes/kubernetes/pull/134401) - **提升：** 减少 kube-apiserver 负载，改善调度延迟
2. 升级 Go 到 1.24.9：包含运行时和安全性改进 - [PR #134612](https://github.com/kubernetes/kubernetes/pull/134612) - **提升：** 整体运行时性能和安全性提升
3. 升级 etcd 到 v3.5.24：修复已知问题并优化性能 - [PR #134861](https://github.com/kubernetes/kubernetes/pull/134861) - **提升：** 集群数据存储稳定性和效率改善

## 🎯 风险评估
整体风险评估：低风险。此版本主要为 bug 修复和稳定性改进，无破坏性变更。建议在业务低峰期升级，并重点关注网络、存储和调度组件的验证。

## 📋 升级建议
1. 建议所有 v1.34 用户尽快升级，以修复关键稳定性问题
2. 如果启用了 SchedulerAsyncAPICalls 特性门控，升级后它将自动禁用，需评估调度性能影响
3. 在生产环境升级前，在测试环境中验证网络、存储和调度功能
4. 对于使用 DRA 或 Windows 节点的集群，优先测试相关功能

## 📋 Release 包含的变更

### PR #133905: Automated cherry pick of #133890: kubelet/metrics: fix multiple Register call
- **链接：** https://github.com/kubernetes/kubernetes/pull/133905
- **状态：** closed
- **已合并：** 是
- **作者：** huww98
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, sig/instrumentation, kind/regression, triage/accepted
- **变更说明：**
  修复 kubelet 指标多次 Register 调用导致的 kubelet_volume_stats_* 指标缺失问题。

### PR #133934: Automated cherry pick of #133926: DRA kubelet: avoid deadlock when gRPC connection to driver goes idle
- **链接：** https://github.com/kubernetes/kubernetes/pull/133934
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted, wg/device-management
- **变更说明：**
  解决 DRA kubelet 与驱动程序 gRPC 连接空闲 30 分钟后出现死锁的问题，避免连接不可用。

### PR #134031: Automated cherry pick of #133953: Fix ClusterIP load balancer disappearing when InternalTrafficPolicy: Local is set.
- **链接：** https://github.com/kubernetes/kubernetes/pull/134031
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/L, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复 Windows kube-proxy 在 internalTrafficPolicy=Local 时 ClusterIP 负载均衡器在 HNS 中间歇性删除的问题，确保服务连接稳定性。

### PR #134087: release-1.34: pin system-validators to v1.10.2
- **链接：** https://github.com/kubernetes/kubernetes/pull/134087
- **状态：** closed
- **已合并：** 是
- **作者：** pacoxu
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, area/dependency, needs-triage
- **变更说明：**
  将 system-validators 固定至 v1.10.2，移除版本特定 cgroup 内核配置检查，避免在 cgroup v2 系统上因缺失 v1 配置而错误失败。

### PR #134118: Automated cherry pick of #134024: fix: use iifname for input interface name matches
- **链接：** https://github.com/kubernetes/kubernetes/pull/134118
- **状态：** closed
- **已合并：** 是
- **作者：** jack4it
- **标签：** kind/bug, priority/important-soon, sig/network, area/kube-proxy, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  修复 kube-proxy nftables 模式（v1.33 GA）中使用 meta iif 而非 iifname 导致的本地流量来源判断错误。

### PR #134133: Automated cherry pick of #134054: fix incorrect warning whenever headless service is created/updated
- **链接：** https://github.com/kubernetes/kubernetes/pull/134133
- **状态：** closed
- **已合并：** 是
- **作者：** Peac36
- **标签：** kind/bug, sig/network, lgtm, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  移除创建/更新 headless service 时错误打印的 SessionAffinity 警告信息。

### PR #134222: [release-1.34][go] Bump images, dependencies and versions to go 1.24.7 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/134222
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, release-note, size/L, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  升级依赖项、镜像和构建版本至 Go 1.24.7 并采用 distroless iptables。

### PR #134247: Automated cherry pick of #134245: Revert "fix: handle corner cases in the async preemption"
- **链接：** https://github.com/kubernetes/kubernetes/pull/134247
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复 kube-scheduler 中待处理 Pod 抢占导致抢占 Pod 过度重试的问题（通过回退异步抢占相关修改）。

### PR #134270: Automated cherry pick of #134265: kubeadm: ensure waiting for apiserver uses a local client
- **链接：** https://github.com/kubernetes/kubernetes/pull/134270
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  确保 kubeadm 等待 apiserver 时使用本地客户端（直接连接本地 API 服务器端点，而非控制平面端点）。

### PR #134362: Automated cherry pick of #134319: kubeadm: rework the FetchInitConfigurationFromCluster node flags
- **链接：** https://github.com/kubernetes/kubernetes/pull/134362
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复 kubeadm upgrade node 中节点注册信息获取错误的问题（当节点名与主机名不同时可能导致节点名不正确）。

### PR #134401: Automated cherry pick of #134400: Disable SchedulerAsyncAPICalls feature gate due to a known regression in v1.34
- **链接：** https://github.com/kubernetes/kubernetes/pull/134401
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, kind/regression, needs-triage
- **变更说明：**
  禁用 SchedulerAsyncAPICalls 功能门以缓解 v1.34 中的已知回归问题：该功能门与异步抢占交互时可能导致 kube-scheduler 性能下降（尤其在高 kube-apiserver 负载下）。

### PR #134589: Automated cherry pick of #134588: go 1.25.2/1.24.8 related fixes
- **链接：** https://github.com/kubernetes/kubernetes/pull/134589
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, sig/auth, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, triage/accepted
- **变更说明：**
  修复 kubeadm 在 IPv6 环境中主机名构造可能失败的预检检查问题（涉及 Go 1.25.2/1.24.8 相关修复）。

### PR #134612: [release-1.34][go] Bump dependencies, images and versions used to Go 1.24.9 and distroless iptables 
- **链接：** https://github.com/kubernetes/kubernetes/pull/134612
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, area/provider/gcp, sig/storage, release-note, size/L, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, sig/architecture, area/conformance, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  升级至 Go 1.24.9 和 distroless iptables，同时更新 setcap 和 debian-base 至 bookworm-v1.0.6。

### PR #134658: Automated cherry pick of #134654: Include relevant dimensions in pod controller indexing
- **链接：** https://github.com/kubernetes/kubernetes/pull/134658
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复 kube-controller-manager 在 Pod 控制器索引中缺失相关维度的问题，确保正确处理 ownerReference 包含不正确 uid 的 Pod。

### PR #134861: [release-1.34] etcd: Bump supported etcd version to v3.5.24 for release v1.31, v1.32, and v1.33
- **链接：** https://github.com/kubernetes/kubernetes/pull/134861
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** priority/important-soon, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/XS, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  将支持的 etcd 版本升级至 v3.5.24，适用于 Kubernetes v1.31、v1.32 和 v1.33 版本。

---
*本报告由 Containerd Release Tracker 自动生成*
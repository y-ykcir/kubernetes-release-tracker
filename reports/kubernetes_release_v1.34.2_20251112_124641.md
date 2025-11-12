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
- **分析时间：** 2025-11-12 12:46:41
- **分析的 PR 数量：** 15
- **分析的 Issue 数量：** 0
- **重要项目数量：** 15

## 📊 版本概述
Kubernetes v1.34.2 是一个重要的补丁版本，主要修复了多个关键bug和性能回归问题，特别是解决了调度器、kubelet指标和网络服务的稳定性问题

## 🐛 重要问题修复
1. 修复 kubelet 卷统计指标丢失问题 - [PR #133905](https://github.com/kubernetes/kubernetes/pull/133905) - **影响：** 监控系统无法获取卷使用情况指标
2. 修复 DRA 设备插件连接空闲30分钟后死锁 - [PR #133934](https://github.com/kubernetes/kubernetes/pull/133934) - **影响：** 使用设备资源分配的应用可能无法正常工作
3. 修复 Windows 服务连接稳定性问题 - [PR #134031](https://github.com/kubernetes/kubernetes/pull/134031) - **影响：** InternalTrafficPolicy=Local 的服务可能出现连接中断
4. 修复 kube-proxy nftables 模式本地流量识别错误 - [PR #134118](https://github.com/kubernetes/kubernetes/pull/134118) - **影响：** 网络策略和本地流量处理可能异常
5. 修复调度器异步抢占导致的频繁重试问题 - [PR #134247](https://github.com/kubernetes/kubernetes/pull/134247) - **影响：** 高负载下调度性能下降

## 💥 破坏性变更
1. 🚨 SchedulerAsyncAPICalls 功能门控被强制禁用 - [PR #134401](https://github.com/kubernetes/kubernetes/pull/134401) - **影响：** 依赖此功能的用户需要等待后续修复版本

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复 kubelet 指标多次注册导致指标丢失的问题 - [PR #133905](https://github.com/kubernetes/kubernetes/pull/133905)
2. 修复 DRA kubelet 在gRPC连接空闲时发生死锁的问题 - [PR #133934](https://github.com/kubernetes/kubernetes/pull/133934)
3. 修复 Windows kube-proxy 在 InternalTrafficPolicy=Local 时 ClusterIP 负载均衡器间歇性消失的问题 - [PR #134031](https://github.com/kubernetes/kubernetes/pull/134031)
4. 禁用 SchedulerAsyncAPICalls 功能门控以修复调度器性能回归 - [PR #134401](https://github.com/kubernetes/kubernetes/pull/134401)
5. 升级 Go 版本到 1.24.9 并更新基础镜像 - [PR #134612](https://github.com/kubernetes/kubernetes/pull/134612)
6. 支持 etcd v3.5.24 版本 - [PR #134861](https://github.com/kubernetes/kubernetes/pull/134861)

## 🚀 性能优化
1. 升级到 Go 1.24.9 提升运行时性能和安全性 - [PR #134612](https://github.com/kubernetes/kubernetes/pull/134612) - **提升：** 内存管理和垃圾回收优化
2. 支持 etcd v3.5.24 包含性能改进和bug修复 - [PR #134861](https://github.com/kubernetes/kubernetes/pull/134861) - **提升：** 集群数据存储稳定性和性能
3. 优化 kubeadm 节点升级流程 - [PR #134362](https://github.com/kubernetes/kubernetes/pull/134362) - **提升：** 集群维护操作更可靠

## 🎯 风险评估
整体风险评估：低风险。这是一个稳定性修复版本，主要解决已知的回归问题。建议在测试环境验证后尽快安排生产环境升级，特别关注调度器和网络组件的稳定性验证。

## 📋 升级建议
1. 建议所有运行 v1.34.x 的生产环境尽快升级到此版本，特别是使用 DRA 设备管理或 Windows 节点的集群
2. 升级前测试调度器性能，确保 SchedulerAsyncAPICalls 功能禁用后不影响业务调度需求
3. 监控系统需要验证 kubelet 卷指标是否正常恢复
4. kubeadm 用户升级时注意节点名称与主机名不一致的情况

## 📋 Release 包含的变更

### PR #133905: Automated cherry pick of #133890: kubelet/metrics: fix multiple Register call
- **链接：** https://github.com/kubernetes/kubernetes/pull/133905
- **状态：** closed
- **已合并：** 是
- **作者：** huww98
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, sig/instrumentation, kind/regression, triage/accepted
- **变更说明：**
  修复kubelet指标多次Register调用导致kubelet_volume_stats_*指标缺失的问题。

### PR #133934: Automated cherry pick of #133926: DRA kubelet: avoid deadlock when gRPC connection to driver goes idle
- **链接：** https://github.com/kubernetes/kubernetes/pull/133934
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted, wg/device-management
- **变更说明：**
  修复kubelet中DRA驱动gRPC连接空闲30分钟后发生内部死锁的问题，避免连接不可用。

### PR #134031: Automated cherry pick of #133953: Fix ClusterIP load balancer disappearing when InternalTrafficPolicy: Local is set.
- **链接：** https://github.com/kubernetes/kubernetes/pull/134031
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/L, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复Windows kube-proxy在internalTrafficPolicy=Local时HNS中ClusterIP负载均衡器间歇性删除的问题，确保服务连接稳定性。

### PR #134087: release-1.34: pin system-validators to v1.10.2
- **链接：** https://github.com/kubernetes/kubernetes/pull/134087
- **状态：** closed
- **已合并：** 是
- **作者：** pacoxu
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, area/dependency, needs-triage
- **变更说明：**
  将system-validators固定到v1.10.2，移除版本特定cgroup内核配置检查，避免cgroup v2系统上因缺少v1配置而误报失败。

### PR #134118: Automated cherry pick of #134024: fix: use iifname for input interface name matches
- **链接：** https://github.com/kubernetes/kubernetes/pull/134118
- **状态：** closed
- **已合并：** 是
- **作者：** jack4it
- **标签：** kind/bug, priority/important-soon, sig/network, area/kube-proxy, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  修复kube-proxy nftables模式（从1.33起GA）中使用错误meta iif而非iifname导致无法判断流量是否来自本地节点的问题。

### PR #134133: Automated cherry pick of #134054: fix incorrect warning whenever headless service is created/updated
- **链接：** https://github.com/kubernetes/kubernetes/pull/134133
- **状态：** closed
- **已合并：** 是
- **作者：** Peac36
- **标签：** kind/bug, sig/network, lgtm, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  移除在创建或更新headless service时错误打印的SessionAffinity警告。

### PR #134222: [release-1.34][go] Bump images, dependencies and versions to go 1.24.7 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/134222
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, release-note, size/L, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将Kubernetes构建依赖升级到Go 1.24.7，并更新为distroless iptables镜像。

### PR #134247: Automated cherry pick of #134245: Revert "fix: handle corner cases in the async preemption"
- **链接：** https://github.com/kubernetes/kubernetes/pull/134247
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复kube-scheduler中因异步抢占处理导致抢占pod被更频繁重试的bug。

### PR #134270: Automated cherry pick of #134265: kubeadm: ensure waiting for apiserver uses a local client
- **链接：** https://github.com/kubernetes/kubernetes/pull/134270
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  确保kubeadm在等待apiserver时使用本地客户端，直接访问本地API服务器端点而非控制平面端点。

### PR #134362: Automated cherry pick of #134319: kubeadm: rework the FetchInitConfigurationFromCluster node flags
- **链接：** https://github.com/kubernetes/kubernetes/pull/134362
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复kubeadm在'kubeadm upgrade node'过程中获取节点注册信息的bug，确保节点名与主机名不同时能正确获取节点名。

### PR #134401: Automated cherry pick of #134400: Disable SchedulerAsyncAPICalls feature gate due to a known regression in v1.34
- **链接：** https://github.com/kubernetes/kubernetes/pull/134401
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, kind/regression, needs-triage
- **变更说明：**
  在v1.34中禁用SchedulerAsyncAPICalls功能门，修复因与异步抢占交互导致的kube-scheduler性能下降问题，特别在高kube-apiserver负载下。

### PR #134589: Automated cherry pick of #134588: go 1.25.2/1.24.8 related fixes
- **链接：** https://github.com/kubernetes/kubernetes/pull/134589
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, sig/auth, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, triage/accepted
- **变更说明：**
  修复kubeadm预检检查，解决IPv6设置中主机名构建可能失败的问题。

### PR #134612: [release-1.34][go] Bump dependencies, images and versions used to Go 1.24.9 and distroless iptables 
- **链接：** https://github.com/kubernetes/kubernetes/pull/134612
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, area/provider/gcp, sig/storage, release-note, size/L, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, sig/architecture, area/conformance, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将Kubernetes构建依赖升级到Go 1.24.9，并更新setcap和debian-base到bookworm-v1.0.6。

### PR #134658: Automated cherry pick of #134654: Include relevant dimensions in pod controller indexing
- **链接：** https://github.com/kubernetes/kubernetes/pull/134658
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复kube-controller-manager的pod控制器索引问题，确保正确处理ownerReference中uid不正确的pod。

### PR #134861: [release-1.34] etcd: Bump supported etcd version to v3.5.24 for release v1.31, v1.32, and v1.33
- **链接：** https://github.com/kubernetes/kubernetes/pull/134861
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** priority/important-soon, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/XS, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  将支持的etcd版本升级到v3.5.24，适用于v1.31、v1.32和v1.33版本。

---
*本报告由 Containerd Release Tracker 自动生成*
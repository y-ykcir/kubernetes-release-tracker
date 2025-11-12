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
- **分析时间：** 2025-11-12 10:46:51
- **分析的 PR 数量：** 15
- **分析的 Issue 数量：** 0
- **重要项目数量：** 15

## 📊 版本概述
Kubernetes v1.34.2 是一个关键补丁版本，主要修复了 kubelet 死锁、调度器性能回归和网络稳定性问题，显著提升了生产环境的可靠性

## 🐛 重要问题修复
1. DRA kubelet 死锁修复：当 gRPC 连接闲置 30 分钟后会出现死锁 - [PR #133934](https://github.com/kubernetes/kubernetes/pull/133934) - **影响：** 导致设备资源分配功能不可用，影响 GPU 等特殊设备的工作负载
2. ClusterIP 负载均衡器消失修复：Windows 环境下 InternalTrafficPolicy=Local 时负载均衡器间歇性删除 - [PR #134031](https://github.com/kubernetes/kubernetes/pull/134031) - **影响：** 导致服务连接不稳定，影响 Windows 节点上的服务发现
3. kubelet 卷统计指标修复：多次 Register 调用导致指标丢失 - [PR #133905](https://github.com/kubernetes/kubernetes/pull/133905) - **影响：** 监控系统无法获取卷使用情况指标，影响存储监控和告警
4. 调度器异步抢占修复：解决 pending pod 抢占导致的频繁重试问题 - [PR #134247](https://github.com/kubernetes/kubernetes/pull/134247) - **影响：** 调度性能下降，特别是在高负载场景下
5. kube-proxy nftables 模式本地流量识别修复 - [PR #134118](https://github.com/kubernetes/kubernetes/pull/134118) - **影响：** 网络策略执行不正确，可能影响服务网格和网络安全性

## 💥 破坏性变更
1. 🚨 SchedulerAsyncAPICalls 功能门被强制禁用 - [PR #134401](https://github.com/kubernetes/kubernetes/pull/134401) - **影响：** 依赖此功能的用户需要调整配置，该功能将保持禁用直到问题彻底解决

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复 DRA kubelet 死锁问题 - [PR #133934](https://github.com/kubernetes/kubernetes/pull/133934)
2. 禁用 SchedulerAsyncAPICalls 功能门以解决性能回归 - [PR #134401](https://github.com/kubernetes/kubernetes/pull/134401)
3. 修复 Windows kube-proxy ClusterIP 负载均衡器消失问题 - [PR #134031](https://github.com/kubernetes/kubernetes/pull/134031)
4. 修复 kubelet 卷统计指标丢失问题 - [PR #133905](https://github.com/kubernetes/kubernetes/pull/133905)
5. 升级 Go 版本至 1.24.9 并更新基础镜像 - [PR #134612](https://github.com/kubernetes/kubernetes/pull/134612)

## 🚀 性能优化
1. 禁用 SchedulerAsyncAPICalls 功能门缓解调度器性能回归 - [PR #134401](https://github.com/kubernetes/kubernetes/pull/134401) - **提升：** 显著改善高 API 服务器负载下的调度性能
2. 升级至 Go 1.24.9 包含运行时性能优化 - [PR #134612](https://github.com/kubernetes/kubernetes/pull/134612) - **提升：** 整体运行时性能和安全补丁
3. 优化 kube-controller-manager Pod 控制器索引处理 - [PR #134658](https://github.com/kubernetes/kubernetes/pull/134658) - **提升：** 改善控制器处理异常 ownerReference 的性能

## 🎯 风险评估
整体风险评估：低风险。此版本主要包含稳定性修复，升级风险较低。建议在测试环境验证后尽快安排生产环境升级，特别关注调度器和网络组件的表现。需要重点监控 DRA 设备插件和 Windows 网络服务的稳定性。

## 📋 升级建议
1. 建议所有运行 v1.34.x 的生产环境尽快升级到此版本，特别是使用 DRA 设备插件或 Windows 节点的集群
2. 升级前测试调度器性能，确保在高负载场景下表现正常
3. 检查是否依赖 SchedulerAsyncAPICalls 功能门，如有依赖需要调整相关配置
4. 监控升级后的 kubelet 指标收集和网络连接稳定性
5. 对于 kubeadm 集群，确保使用正确的节点注册信息进行升级操作

## 📋 Release 包含的变更

### PR #133905: Automated cherry pick of #133890: kubelet/metrics: fix multiple Register call
- **链接：** https://github.com/kubernetes/kubernetes/pull/133905
- **状态：** closed
- **已合并：** 是
- **作者：** huww98
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, sig/instrumentation, kind/regression, triage/accepted
- **变更说明：**
  修复kubelet中多次注册调用导致的kubelet_volume_stats_*指标缺失问题。

### PR #133934: Automated cherry pick of #133926: DRA kubelet: avoid deadlock when gRPC connection to driver goes idle
- **链接：** https://github.com/kubernetes/kubernetes/pull/133934
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted, wg/device-management
- **变更说明：**
  修复kubelet中DRA驱动器gRPC连接空闲30分钟后因死锁导致连接不可用的问题。

### PR #134031: Automated cherry pick of #133953: Fix ClusterIP load balancer disappearing when InternalTrafficPolicy: Local is set.
- **链接：** https://github.com/kubernetes/kubernetes/pull/134031
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/L, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复Windows kube-proxy中InternalTrafficPolicy=Local时ClusterIP负载均衡器在HNS中间歇性删除的问题，保证服务连接稳定性。

### PR #134087: release-1.34: pin system-validators to v1.10.2
- **链接：** https://github.com/kubernetes/kubernetes/pull/134087
- **状态：** closed
- **已合并：** 是
- **作者：** pacoxu
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, area/dependency, needs-triage
- **变更说明：**
  将system-validators固定到v1.10.2，移除cgroup内核配置的版本特定检查，避免在cgroup v2系统上因v1-only配置缺失而错误失败。

### PR #134118: Automated cherry pick of #134024: fix: use iifname for input interface name matches
- **链接：** https://github.com/kubernetes/kubernetes/pull/134118
- **状态：** closed
- **已合并：** 是
- **作者：** jack4it
- **标签：** kind/bug, priority/important-soon, sig/network, area/kube-proxy, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  修复kube-proxy nftables模式中接口名匹配错误，使用iifname替代iif以正确判断本地流量来源。

### PR #134133: Automated cherry pick of #134054: fix incorrect warning whenever headless service is created/updated
- **链接：** https://github.com/kubernetes/kubernetes/pull/134133
- **状态：** closed
- **已合并：** 是
- **作者：** Peac36
- **标签：** kind/bug, sig/network, lgtm, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  移除创建或更新无头服务时错误打印的SessionAffinity警告。

### PR #134222: [release-1.34][go] Bump images, dependencies and versions to go 1.24.7 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/134222
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, release-note, size/L, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将Kubernetes构建依赖升级到Go 1.24.7和distroless iptables。

### PR #134247: Automated cherry pick of #134245: Revert "fix: handle corner cases in the async preemption"
- **链接：** https://github.com/kubernetes/kubernetes/pull/134247
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复kube-scheduler中异步抢占导致抢占pod频繁重试的问题。

### PR #134270: Automated cherry pick of #134265: kubeadm: ensure waiting for apiserver uses a local client
- **链接：** https://github.com/kubernetes/kubernetes/pull/134270
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复kubeadm中等待apiserver时使用本地客户端，直接连接本地端点而非控制平面端点。

### PR #134362: Automated cherry pick of #134319: kubeadm: rework the FetchInitConfigurationFromCluster node flags
- **链接：** https://github.com/kubernetes/kubernetes/pull/134362
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复kubeadm upgrade node中节点注册信息获取错误的问题，确保在节点名与主机名不同时正确获取节点名。

### PR #134401: Automated cherry pick of #134400: Disable SchedulerAsyncAPICalls feature gate due to a known regression in v1.34
- **链接：** https://github.com/kubernetes/kubernetes/pull/134401
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, kind/regression, needs-triage
- **变更说明：**
  在v1.34中禁用SchedulerAsyncAPICalls特性门控，解决其与异步抢占交互导致的kube-scheduler性能下降问题，尤其在高kube-apiserver负载下。

### PR #134589: Automated cherry pick of #134588: go 1.25.2/1.24.8 related fixes
- **链接：** https://github.com/kubernetes/kubernetes/pull/134589
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, sig/auth, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, triage/accepted
- **变更说明：**
  修复kubeadm预检检查在IPv6设置中因主机名构造失败的问题，涉及Go 1.25.2/1.24.8相关修复。

### PR #134612: [release-1.34][go] Bump dependencies, images and versions used to Go 1.24.9 and distroless iptables 
- **链接：** https://github.com/kubernetes/kubernetes/pull/134612
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, area/provider/gcp, sig/storage, release-note, size/L, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, sig/architecture, area/conformance, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将Kubernetes构建依赖升级到Go 1.24.9和distroless iptables，并更新setcap和debian-base到bookworm-v1.0.6。

### PR #134658: Automated cherry pick of #134654: Include relevant dimensions in pod controller indexing
- **链接：** https://github.com/kubernetes/kubernetes/pull/134658
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复kube-controller-manager中pod控制器索引问题，确保正确处理ownerReference uid不正确的pod。

### PR #134861: [release-1.34] etcd: Bump supported etcd version to v3.5.24 for release v1.31, v1.32, and v1.33
- **链接：** https://github.com/kubernetes/kubernetes/pull/134861
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** priority/important-soon, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/XS, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  将支持的etcd版本升级到v3.5.24，适用于Kubernetes v1.31、v1.32和v1.33版本。

---
*本报告由 Containerd Release Tracker 自动生成*
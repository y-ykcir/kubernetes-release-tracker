# Kubernetes 版本发布分析报告
## Kubernetes v1.35.0-beta.0 (v1.35.0-beta.0)

### 📋 版本信息
- **版本标签：** v1.35.0-beta.0
- **版本名称：** Kubernetes v1.35.0-beta.0
- **发布时间：** 2025-11-19T20:32:24Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.0-beta.0

### 🔍 分析统计
- **分析时间：** 2025-11-19 21:47:57
- **分析的 PR 数量：** 39
- **分析的 Issue 数量：** 20
- **重要项目数量：** 49

## 📊 版本概述
Kubernetes v1.35.0-beta.0 引入了工作负载 API、DRA 扩展资源管理和节点声明特性等重大功能，同时修复了多个关键的生产环境稳定性问题。

## 🔒 安全问题修复
1. ⚠️ 本次版本未发现新的安全漏洞报告

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kube-proxy/winkernel 中 stale RemoteEndpoints 问题 - [PR #135146](https://github.com/kubernetes/kubernetes/pull/135146) - **影响：** 在大规模环境中，当 Deployment 被多个 Service 引用时，可能导致网络端点清理不彻底 - [Issue #135144](https://github.com/kubernetes/kubernetes/issues/135144)
2. 修复 CEL schema wrappers 中的 NPE 导致 kube-controller-manager 崩溃 - [PR #135155](https://github.com/kubernetes/kubernetes/pull/135155) - **影响：** 使用 additionalProperties=true 的 CRD 时会导致控制平面崩溃 - [Issue #135145](https://github.com/kubernetes/kubernetes/issues/135145)
3. 修复创建带有空卷的 Pod 时的并发映射写错误 - [PR #135174](https://github.com/kubernetes/kubernetes/pull/135174) - **影响：** 可能导致 kubelet 崩溃，影响 Pod 创建 - [Issue #135089](https://github.com/kubernetes/kubernetes/issues/135089)
4. 修复非 sidecar init 容器的设备请求计算 - [PR #134882](https://github.com/kubernetes/kubernetes/pull/134882)
5. 修复设备管理器健康检查在首次启动前失败的问题 - [PR #135153](https://github.com/kubernetes/kubernetes/pull/135153) - **影响：** 可能导致 kubelet 被系统看门狗杀死 - [Issue #135113](https://github.com/kubernetes/kubernetes/issues/135113)
6. 修复静态 Pod 验证选项问题 - [PR #135031](https://github.com/kubernetes/kubernetes/pull/135031) - **影响：** 静态 Pod 无法使用重启规则等特性 - [Issue #135030](https://github.com/kubernetes/kubernetes/issues/135030)
7. 修复 Alpha API 版本差异警告 - [PR #135327](https://github.com/kubernetes/kubernetes/pull/135327)

## 💥 破坏性变更
1. 🚨 在 kubectl 中删除对 networkingv1beta1.IngressClass 的支持 - [PR #135108](https://github.com/kubernetes/kubernetes/pull/135108) - **影响：** 用户需要迁移到 networking/v1 API 版本
2. 🚨 在 kubectl 中删除对 networkingv1beta1.Ingress 的支持 - [PR #135176](https://github.com/kubernetes/kubernetes/pull/135176) - **影响：** 必须更新所有使用旧版本 Ingress 的 YAML 配置
3. 🚨 锁定 AggregatedDiscoveryRemoveBetaType 为 true - [PR #134230](https://github.com/kubernetes/kubernetes/pull/134230) - **影响：** 移除 beta 类型的聚合发现支持
4. 🚨 Pod Certificates API 从 v1alpha1 移除 - [PR #134790](https://github.com/kubernetes/kubernetes/pull/134790) - **影响：** 需要迁移到 v1beta1 版本

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 工作负载 API 引入，支持 Gang Scheduling - [PR #134564](https://github.com/kubernetes/kubernetes/pull/134564)
2. DRA 扩展资源配额管理 - [PR #134210](https://github.com/kubernetes/kubernetes/pull/134210)
3. 节点声明特性框架，允许节点声明故障概率/SLA - [PR #133389](https://github.com/kubernetes/kubernetes/pull/133389)
4. 对等聚合发现机制 - [PR #133648](https://github.com/kubernetes/kubernetes/pull/133648)
5. Pod 级别原地 Pod 调整 - Alpha 功能 - [PR #132919](https://github.com/kubernetes/kubernetes/pull/132919)
6. 可分区设备特性更新 - [PR #134189](https://github.com/kubernetes/kubernetes/pull/134189)
7. 容忍度操作符扩展，新增 Gt 和 Lt 操作符 - [PR #134665](https://github.com/kubernetes/kubernetes/pull/134665)
8. EnvFiles 特性门控升级到 Beta - [PR #134414](https://github.com/kubernetes/kubernetes/pull/134414)
9. RestartAllContainers 功能实现 - [PR #134345](https://github.com/kubernetes/kubernetes/pull/134345)

## 🚀 性能优化
1. 图像拉取记录存储版本迁移到文件系统缓存 - [PR #132579](https://github.com/kubernetes/kubernetes/pull/132579) - **提升：** 改善缓存性能和一致性
2. 启用 WatchListClient 功能 - [PR #134180](https://github.com/kubernetes/kubernetes/pull/134180) - **提升：** 减少 API 服务器负载和网络流量
3. DRA 扩展资源评分机制 - [PR #134058](https://github.com/kubernetes/kubernetes/pull/134058) - **提升：** 改善资源调度效率
4. 基于 watch 的路由控制器协调 - [PR #131220](https://github.com/kubernetes/kubernetes/pull/131220) - **提升：** 避免云提供商速率限制问题 - [Issue #60646](https://github.com/kubernetes/kubernetes/issues/60646)
5. 图像 GC 最大年龄特性升级到稳定 - [PR #134736](https://github.com/kubernetes/kubernetes/pull/134736)

## 🎯 风险评估
整体风险评估：作为 beta 版本，升级风险中等偏高，主要风险来自 API 废弃和网络组件稳定性问题。建议在非生产环境充分测试后，再考虑生产部署。重点关注网络端点清理、控制平面崩溃修复和资源调度改进。

## 📋 升级建议
1. 在升级前，全面测试所有使用 networkingv1beta1.Ingress 和 IngressClass 的应用
2. 启用 KubeletCrashLoopBackOffMax 特性门控以改善容器重启管理
3. 对于使用 DRA 扩展资源的环境，建议逐步启用新功能并进行性能监控
4. 注意新引入的 alpha 功能（如 Pod 级别原地调整、RestartAllContainers 等）默认禁用，需要显式启用
5. 监控 kube-controller-manager 的稳定性，特别是使用 ValidatingAdmissionPolicies 的场景
6. 对于大规模 Windows 环境，特别关注 kube-proxy/winkernel 的端点清理问题
7. 建议在测试环境中充分验证新功能，特别是与资源调度和配额管理相关的变更

## 📋 Release 包含的变更

### PR #131220: feat(ccm): watch-based route controller reconciliation
- **链接：** https://github.com/kubernetes/kubernetes/pull/131220
- **状态：** closed
- **已合并：** 是
- **作者：** lukasmetzner
- **标签：** lgtm, area/cloudprovider, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  为云控制器管理器引入基于watch的路由控制器，替代静态间隔协调，新增CloudControllerManagerWatchBasedRoutesReconciliation功能门（默认禁用）。

### PR #132441: [KEP-5440]: MutablePodResourcesForSuspendedJobs 
- **链接：** https://github.com/kubernetes/kubernetes/pull/132441
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/XL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, api-review, triage/accepted
- **变更说明：**
  实现KEP-5440挂起作业的可变Pod资源功能：允许更新未启动的挂起Job的容器资源，其他Pod模板字段保持不可变。需启用MutablePodResourcesForSuspendedJobs特性门控。

### PR #132579: KEP-2535: move objects to beta, add storage version migration to filesystem cache
- **链接：** https://github.com/kubernetes/kubernetes/pull/132579
- **状态：** closed
- **已合并：** 是
- **作者：** stlaz
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/L, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  将ImagePullIntent和ImagePulledRecord对象从v1alpha1升级至v1beta1，并添加文件系统缓存的存储版本迁移。支持KEP-2535镜像拉取记录功能进入beta。

### PR #132812: kubelet: add metrics related to image pull records
- **链接：** https://github.com/kubernetes/kubernetes/pull/132812
- **状态：** closed
- **已合并：** 是
- **作者：** stlaz
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/XL, kind/feature, sig/auth, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  新增kubelet镜像管理相关指标：kubelet_imagemanager_ondisk_pullintents（拉取记录数）、kubelet_imagemanager_image_mustpull_checks_total（拉取检查次数），支持KEP-2535镜像拉取监控。

### PR #132919: Pod level in place pod resize - alpha
- **链接：** https://github.com/kubernetes/kubernetes/pull/132919
- **状态：** closed
- **已合并：** 是
- **作者：** ndixita
- **标签：** area/test, area/kubelet, sig/scheduling, area/kubectl, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, ok-to-test, needs-priority, api-review, area/e2e-test-framework, needs-triage, area/stable-metrics
- **变更说明：**
  实现Pod级别原地资源调整alpha功能，允许在不重启Pod的情况下修改资源请求/限制。需启用InPlacePodVerticalScaling特性门控。

### PR #133389: Introduce node declared features framework
- **链接：** https://github.com/kubernetes/kubernetes/pull/133389
- **状态：** closed
- **已合并：** 是
- **作者：** pravk03
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, area/release-eng, sig/apps, approved, cncf-cla: yes, sig/testing, sig/release, area/code-generation, ok-to-test, needs-priority, api-review, area/dependency, triage/accepted
- **变更说明：**
  引入节点声明功能框架，支持节点特征动态管理，涉及API变更和多个SIG协作。

### PR #133648: [KEP:4020] Peer-aggregated discovery
- **链接：** https://github.com/kubernetes/kubernetes/pull/133648
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/test, sig/scheduling, area/apiserver, lgtm, area/cloudprovider, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, sig/cloud-provider, ok-to-test, needs-priority, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  实现对等聚合发现功能，基于KEP-4020，改进跨节点资源发现机制。

### PR #133968: Update coredns to v1.13.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/133968
- **状态：** closed
- **已合并：** 是
- **作者：** yashsingh74
- **标签：** kind/cleanup, lgtm, area/provider/gcp, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/cloud-provider, needs-priority, area/dependency, needs-triage
- **变更说明：**
  更新CoreDNS依赖至v1.13.1版本，包含安全修复和功能改进。影响kubeadm集群部署的默认DNS配置。

### PR #134058: Implement scoring for extended resources backed up by DRA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134058
- **状态：** closed
- **已合并：** 是
- **作者：** bart0sh
- **标签：** area/test, sig/scheduling, lgtm, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  实现DRA扩展资源的调度评分功能，解决与device-plugin资源评分不一致问题。确保DRA资源allocatable和requested值参与节点评分，保持向后兼容性，为DRA Beta毕业必备条件。

### PR #134180: Promote/Enable WatchListClient feature for release 1.35
- **链接：** https://github.com/kubernetes/kubernetes/pull/134180
- **状态：** closed
- **已合并：** 是
- **作者：** p0lyn0mial
- **标签：** area/test, area/kubelet, area/apiserver, area/kubectl, lgtm, sig/node, sig/api-machinery, release-note, size/S, kind/feature, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  为Kubernetes 1.35启用WatchListClient功能，改进列表观察效率，涉及多个组件更新。

### PR #134189: Updates to DRA Partitionable Devices feature
- **链接：** https://github.com/kubernetes/kubernetes/pull/134189
- **状态：** closed
- **已合并：** 是
- **作者：** mortent
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, triage/accepted, wg/device-management
- **变更说明：**
  更新DRA Partitionable Devices alpha功能：支持跨ResourceSlices引用计数器集，不完整资源池的设备不再参与分配。包含不兼容变更，需更新现有ResourceSlices。

### PR #134210: DRA extended resource quota
- **链接：** https://github.com/kubernetes/kubernetes/pull/134210
- **状态：** closed
- **已合并：** 是
- **作者：** yliaog
- **标签：** area/test, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted, wg/device-management
- **变更说明：**
  为DRA扩展资源添加配额支持，扩展ResourceQuota机制以涵盖DRA资源分配。涉及API变更，需更新配额控制器。

### PR #134230: Lock AggregatedDiscoveryRemoveBetaType to true
- **链接：** https://github.com/kubernetes/kubernetes/pull/134230
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/S, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  锁定AggregatedDiscoveryRemoveBetaType特性门控为true，移除已废弃的v2beta1聚合发现API。为后续完全移除该API做准备。

### PR #134339: KEP-5381: mutable pv nodeAffinity
- **链接：** https://github.com/kubernetes/kubernetes/pull/134339
- **状态：** closed
- **已合并：** 是
- **作者：** huww98
- **标签：** priority/important-soon, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, area/code-generation, needs-triage
- **变更说明：**
  实现KEP-5381可变PV节点亲和性功能，允许动态更新PersistentVolume的nodeAffinity字段。支持存储迁移和节点维护场景。

### PR #134345: Implement RestartAllContainers
- **链接：** https://github.com/kubernetes/kubernetes/pull/134345
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/XXL, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, api-review, triage/accepted
- **变更说明：**
  实现RestartAllContainers alpha功能：当容器退出且符合重启策略时，重启Pod内所有容器。需启用RestartAllContainersOnContainerExit特性门控。

### PR #134414: KEP-3721: Promote EnvFiles feature gate to Beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/134414
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-triage
- **变更说明：**
  将EnvFiles功能门提升至beta状态，增强kubelet环境文件处理能力。

### PR #134520: [DRA] Add ShareID to kubelet plugin API
- **链接：** https://github.com/kubernetes/kubernetes/pull/134520
- **状态：** closed
- **已合并：** 是
- **作者：** sunya-ch
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  为 kubelet 插件 API 添加 ShareID 支持，作为 Dynamic Resource Allocation (DRA) 功能扩展，增强资源共享能力。

### PR #134523: KEP-5004: DRAExtendedResource metrics
- **链接：** https://github.com/kubernetes/kubernetes/pull/134523
- **状态：** closed
- **已合并：** 是
- **作者：** bitoku
- **标签：** sig/scheduling, lgtm, sig/node, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, sig/instrumentation, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  基于 KEP-5004 为 DRA 扩展资源引入指标监控功能，提供资源分配和使用情况的可见性。

### PR #134564: KEP-4671: Add Workload API
- **链接：** https://github.com/kubernetes/kubernetes/pull/134564
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, area/apiserver, area/kubectl, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage, sig/etcd
- **变更说明：**
  引入Workload API，基于KEP-4671，提供统一工作负载管理接口，涉及apiserver和kubectl变更。

### PR #134665: KEP-5471: Extend tolerations operators
- **链接：** https://github.com/kubernetes/kubernetes/pull/134665
- **状态：** closed
- **已合并：** 是
- **作者：** helayoty
- **标签：** area/test, priority/important-soon, area/kubelet, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/apps, approved, sig/windows, cncf-cla: yes, sig/testing, area/code-generation, tide/merge-method-squash, area/e2e-test-framework, area/dependency, triage/accepted
- **变更说明：**
  扩展Pod容忍度操作符，新增Gt（大于）和Lt（小于）比较操作符，引入TaintTolerationComparisonOperators功能门，要求值为规范十进制整数。

### PR #134711: DRA: Add scoring for Prioritized List feature
- **链接：** https://github.com/kubernetes/kubernetes/pull/134711
- **状态：** closed
- **已合并：** 是
- **作者：** mortent
- **标签：** area/test, sig/scheduling, lgtm, sig/node, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  为DRA Prioritized List功能添加简单评分机制，优先选择能满足最高排名子请求的节点。基于KEP-4816实现调度优化。

### PR #134736: features: bump image gc max age feature to stable
- **链接：** https://github.com/kubernetes/kubernetes/pull/134736
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/S, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, api-review, needs-triage
- **变更说明：**
  将ImageGcMaxAge特性门控升级至稳定阶段，允许配置镜像垃圾回收的最大保留时间。默认启用，无需额外配置。

### PR #134790: Promote Pod Certificates feature to beta-with metrics/events and e2e tests.
- **链接：** https://github.com/kubernetes/kubernetes/pull/134790
- **状态：** closed
- **已合并：** 是
- **作者：** yt2985
- **标签：** area/test, lgtm, release-note, size/XL, kind/feature, sig/auth, approved, cncf-cla: yes, sig/instrumentation, sig/testing, ok-to-test, needs-priority, needs-triage, area/stable-metrics
- **变更说明：**
  Pod Certificates功能升级至beta，引入v1beta1 API，移除v1alpha1 API，添加kubelet指标和事件，并包含e2e测试。

### PR #134825: [InPlacePodVerticalScaling] emit more events when the pod resize status changes
- **链接：** https://github.com/kubernetes/kubernetes/pull/134825
- **状态：** closed
- **已合并：** 是
- **作者：** natasha41575
- **标签：** priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/XL, kind/feature, approved, cncf-cla: yes, needs-triage
- **变更说明：**
  为InPlacePodVerticalScaling功能增强事件记录，在Pod调整状态变化时（延迟、开始、错误、完成）触发事件。

### PR #134882: Fix non-sidecar init container device requests
- **链接：** https://github.com/kubernetes/kubernetes/pull/134882
- **状态：** closed
- **已合并：** 是
- **作者：** yliaog
- **标签：** kind/bug, area/test, area/kubelet, sig/scheduling, area/kubectl, lgtm, sig/node, release-note, size/XL, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复非sidecar init容器设备请求处理bug，确保DRA设备资源在初始化容器中的正确分配。影响包含设备请求的init容器调度。

### PR #134890: kubeadm: support specifying HTTP endpoints for external etcd, allowing users to separate gRPC and HTTP traffic for etcd
- **链接：** https://github.com/kubernetes/kubernetes/pull/134890
- **状态：** closed
- **已合并：** 是
- **作者：** SataQiu
- **标签：** priority/important-soon, lgtm, sig/cluster-lifecycle, release-note, size/M, kind/feature, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubeadm 新增支持为外部 etcd 指定 HTTP 端点，允许用户分离 gRPC 和 HTTP 流量，提升 etcd 网络配置灵活性。

### PR #134893: KEP-5607: Allow hostNetwork pods to use user namespace
- **链接：** https://github.com/kubernetes/kubernetes/pull/134893
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** area/test, priority/important-soon, lgtm, sig/node, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, api-review, needs-triage
- **变更说明：**
  基于 KEP-5607 实现功能，允许 hostNetwork pods 使用 user namespace，扩展了 hostNetwork 容器的隔离能力。

### PR #135031: Add validation options for static pod
- **链接：** https://github.com/kubernetes/kubernetes/pull/135031
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复静态 pod 验证问题，允许静态 pod 使用重启策略等特性。通过正确初始化 ValidationOptions 解决功能禁用问题，关联 KEP-5307。

### PR #135037: pick one device class deterministically for extended resource
- **链接：** https://github.com/kubernetes/kubernetes/pull/135037
- **状态：** closed
- **已合并：** 是
- **作者：** yliaog
- **标签：** area/test, sig/scheduling, lgtm, sig/node, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  改进扩展资源的设备类选择逻辑，从随机选择改为确定性选择，确保设备分配的一致性。

### PR #135044: Set KubeletCrashLoopBackOffMax feature gate to default enabled for beta.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135044
- **状态：** closed
- **已合并：** 是
- **作者：** hankfreund
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/M, kind/feature, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  将KubeletCrashLoopBackOffMax功能门默认启用并标记为beta状态，提升kubelet崩溃循环处理能力。

### PR #135072: Gracefully shutdown typed queue
- **链接：** https://github.com/kubernetes/kubernetes/pull/135072
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  改进类型化队列的优雅关闭机制，确保updateUnfinishedWorkLoop goroutine在Shutdown()返回前终止。

### PR #135108: Drop support for networkingv1beta1.IngressClass in kubectl
- **链接：** https://github.com/kubernetes/kubernetes/pull/135108
- **状态：** closed
- **已合并：** 是
- **作者：** scaliby
- **标签：** kind/cleanup, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  清理kubectl中已弃用的networking/v1beta1 IngressClass支持，为后续API改进做准备。用户需迁移至networking/v1版本。

### PR #135146: kube-proxy/winkernel: fix stale RemoteEndpoints due to premature clearing of terminatedEndpoints map
- **链接：** https://github.com/kubernetes/kubernetes/pull/135146
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/XS, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复 kube-proxy winkernel 模式中 terminatedEndpoints map 被过早清除导致的 stale RemoteEndpoints 问题。通过将 clearTerminatedEndpointsMap() 移至 syncProxyRules() 开始处，确保批量更新 Service 时端点信息不丢失。

### PR #135153: mark device manager as haelthy before it started for the first time
- **链接：** https://github.com/kubernetes/kubernetes/pull/135153
- **状态：** closed
- **已合并：** 是
- **作者：** SergeyKanzhelev
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复设备管理器健康检查逻辑，在设备管理器完全启动前标记为健康状态，避免 kubelet 因初始化缓慢被 System WatchDog 误杀。

### PR #135155: Fix NPE in CEL schema wrappers of additionalProperties=true objects
- **链接：** https://github.com/kubernetes/kubernetes/pull/135155
- **状态：** closed
- **已合并：** 是
- **作者：** jpbetz
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复 ValidatingAdmissionPolicy 中 CRD 使用 additionalProperties:true 时导致 kube-controller-manager 空指针异常崩溃的问题。

### PR #135174: kubelet: fix concurrent map write error when creating a pod with empty volume
- **链接：** https://github.com/kubernetes/kubernetes/pull/135174
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/bug, priority/important-soon, lgtm, sig/storage, release-note, size/S, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复kubelet在创建带空卷pod时的并发map写错误，解决supportsQuotasMap锁不一致问题。

### PR #135176: Drop support for networkingv1beta1.Ingress in kubectl
- **链接：** https://github.com/kubernetes/kubernetes/pull/135176
- **状态：** closed
- **已合并：** 是
- **作者：** scaliby
- **标签：** kind/cleanup, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  kubectl移除对networking/v1beta1 Ingress的支持，清理已弃用API为后续改进做准备。

### PR #135197: Revert- Don't pick versions that have a replacement as storage
- **链接：** https://github.com/kubernetes/kubernetes/pull/135197
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  撤销PR #128454更改，修复API存储版本选择逻辑，因v1alpha3资源版本已被移除。

### PR #135327: Fix alpha API warnings for patch version differences
- **链接：** https://github.com/kubernetes/kubernetes/pull/135327
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复alpha API版本差异导致的警告显示问题，是PR #134035的后续补丁。

---
*本报告由 Containerd Release Tracker 自动生成*
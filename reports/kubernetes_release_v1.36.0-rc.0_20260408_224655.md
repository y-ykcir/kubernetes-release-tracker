# Kubernetes 版本发布分析报告
## v1.36.0-rc.0 (v1.36.0-rc.0)

### 📋 版本信息
- **版本标签：** v1.36.0-rc.0
- **版本名称：** v1.36.0-rc.0
- **发布时间：** 2026-04-08T22:15:08Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.36.0-rc.0

### 🔍 分析统计
- **分析时间：** 2026-04-08 22:46:55
- **分析的 PR 数量：** 15
- **分析的 Issue 数量：** 2
- **重要项目数量：** 17

## 📊 版本概述
Kubernetes v1.36.0-rc.0 是一个以增强动态资源分配（DRA）安全性、引入工作负载感知抢占以及修复关键 StatefulSet 回归问题为核心的版本，标志着 DRA 和高级调度功能进入成熟阶段。

## 🔒 安全问题修复
1. ⚠️ Go 语言版本升级至 1.26.2，包含安全修复 - [PR #138261](https://github.com/kubernetes/kubernetes/pull/138261) - **风险级别：** 中 - 升级 Go 版本以包含上游安全补丁，建议升级以降低潜在风险。
2. ⚠️ DRA ResourceClaim 状态更新的细粒度授权（见关键变更） - [PR #134947](https://github.com/kubernetes/kubernetes/pull/134947) - **风险级别：** 低（正向增强） - 此变更是安全增强，但需要检查现有 DRA 插件或控制器的 RBAC 权限是否足够。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 StatefulSet 并行 Pod 管理中的回归问题，默认关闭 MaxUnavailable 特性 - [PR #137904](https://github.com/kubernetes/kubernetes/pull/137904) - **影响：** 修复了在 v1.35 中引入的严重问题（[Issue #137409](https://github.com/kubernetes/kubernetes/issues/137409)），当启用 `MaxUnavailableStatefulSet` 且首个副本集版本有缺陷时，Pod 可能永远无法就绪。此修复通过默认关闭该特性来防止生产环境中断。
2. 修复 kubelet 销毁 NodeAllocatableResourceClaimStatuses 的问题 - [PR #138030](https://github.com/kubernetes/kubernetes/pull/138030) - **影响：** 确保由 DRA 管理的节点可分配资源声明状态在 kubelet 更新 Pod 状态时不被意外清除，保障了 Alpha 阶段 `DRANodeAllocatableResources` 功能的可靠性。
3. 修复 Pod 事件问题 - [PR #138049](https://github.com/kubernetes/kubernetes/pull/138049) - **影响：** 解决了与 Pod 事件生成相关的问题，提高了事件系统的准确性。
4. 修复 pause 容器版本漂移并强制执行完整的 SemVer 验证 - [PR #138199](https://github.com/kubernetes/kubernetes/pull/138199) - **影响：** 确保 pause 容器版本一致性，避免因版本不匹配导致的潜在兼容性问题。
5. 修复启用 PLR 特性门控时不必要的 ResizeCompleted 事件发射 - [Issue #137858](https://github.com/kubernetes/kubernetes/issues/137858) - **影响：** 解决了在启用 `InPlacePodLevelResourcesVerticalScaling` 后，Pod 创建时可能错误触发 `ResizeCompleted` 事件的问题，减少了事件噪音。

## 💥 破坏性变更
1. 🚨 StatefulSet 的 MaxUnavailable 特性默认被关闭 - [PR #137904](https://github.com/kubernetes/kubernetes/pull/137904) - **影响：** 在 v1.35 中默认启用的 `MaxUnavailableStatefulSet` 特性在 v1.36 中恢复为默认关闭。如果您的应用依赖此特性进行快速滚动更新，升级后需要显式启用该特性门控，并确保了解其已知问题。
2. 🚨 DRA 资源声明状态更新需要新的 RBAC 权限 - [PR #134947](https://github.com/kubernetes/kubernetes/pull/134947) - **影响：** 如果使用 DRA 且有自定义控制器或插件更新 `ResourceClaim` 状态，升级后必须为其添加 `resourceclaims/binding` 子资源的更新权限，否则状态更新会失败。
3. 🚨 Pod 级别资源垂直伸缩特性行为可能变化 - [PR #137684](https://github.com/kubernetes/kubernetes/pull/137684) - **影响：** 随着特性从 Alpha 进入 Beta，API 和行为可能趋于稳定但仍可能有调整。使用此功能的用户需关注后续 Beta 阶段的文档更新。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. DRA 资源声明状态更新细粒度授权 - [PR #134947](https://github.com/kubernetes/kubernetes/pull/134947) - **影响：** 默认启用新的 `DRAResourceClaimGranularStatusAuthorization` 特性门控，要求 DRA 插件或控制器需要更具体的 RBAC 权限（`resourceclaims/binding`）来更新分配状态，增强了安全性。
2. 为 Workload 和 PodGroup API 添加工作负载感知抢占字段 - [PR #136589](https://github.com/kubernetes/kubernetes/pull/136589) - **影响：** 引入 `DisruptionMode`、`PriorityClassName` 和 `Priority` 字段，支持将 Pod 组作为一个整体进行抢占，优化了批处理工作负载的调度。
3. DRA：为工作负载添加 ResourceClaim 支持 - [PR #136989](https://github.com/kubernetes/kubernetes/pull/136989) - **影响：** 扩展 DRA 以原生支持工作负载（如 Job、Deployment）的资源声明，简化了 GPU 等稀缺设备的管理。
4. 添加 ResourcePoolStatusRequest API 以查询 DRA 资源可用性 - [PR #137028](https://github.com/kubernetes/kubernetes/pull/137028) - **影响：** 新增 Alpha API，允许用户和外部调度器查询 DRA 资源池的容量和分配状态，提升了资源规划可见性。
5. NodeLogQuery 特性晋升至 GA - [PR #137544](https://github.com/kubernetes/kubernetes/pull/137544) - **影响：** `NodeLogQuery` 特性门控默认锁定为 `true`，通过 kubelet API 查询节点日志的功能进入稳定阶段。
6. Pod 级别资源原地垂直伸缩特性晋升至 Beta - [PR #137684](https://github.com/kubernetes/kubernetes/pull/137684) - **影响：** `InPlacePodLevelResourcesVerticalScaling` 特性进入 Beta 阶段，稳定性提升，允许在不重启 Pod 的情况下调整容器资源。

## 🚀 性能优化
1. 实现工作负载感知抢占 - [PR #137606](https://github.com/kubernetes/kubernetes/pull/137606) - **提升：** 通过将 Pod 组作为整体进行抢占决策，减少了批处理工作负载（如 AI/ML 训练任务）的碎片化调度和启动延迟。
2. 添加 ResourcePoolStatusRequest API（见关键变更） - [PR #137028](https://github.com/kubernetes/kubernetes/pull/137028) - **提升：** 提供了 DRA 资源池的全局视图，有助于外部调度器做出更优的放置决策，提升集群整体资源利用率。

## 🎯 风险评估
整体风险评估：**中等**。此版本包含了重要的安全增强和性能改进，但同时也修复了一个高优先级的 StatefulSet 回归问题，并引入了对 DRA 权限模型的破坏性变更。对于未使用 DRA 和 StatefulSet 高级特性的集群，升级风险较低。对于使用了相关功能的集群，需要仔细评估和测试。建议的升级时机是在 v1.36.0 正式发布后，留出足够的测试周期。需要特别关注的方面包括：StatefulSet 的滚动更新行为、所有 DRA 相关组件的兼容性与权限、以及任何 Beta/Alpha 特性门控的默认值变化。

## 📋 升级建议
1. **升级前必须测试：** 由于存在 StatefulSet 的关键回归修复和 DRA 授权变更，请在非生产环境充分测试工作负载，特别是使用了 StatefulSet 并行更新和 DRA 功能的场景。
2. **检查 DRA 相关 RBAC：** 如果集群中使用 Dynamic Resource Allocation (DRA)，请审计并更新相关 ServiceAccount 的 ClusterRole，确保包含对 `resourceclaims/binding` 子资源的权限。
3. **评估特性门控：** 明确列出并测试您所依赖的特性门控。注意 `MaxUnavailableStatefulSet` 已默认关闭，`NodeLogQuery` 已锁定开启。
4. **关注实验性功能：** `ResourcePoolStatusRequest`、`UserNamespacesHostNetworkSupport` 等仍为 Alpha 功能，不建议在生产环境使用。
5. **规划升级窗口：** 鉴于这是一个 Release Candidate 版本，建议等待 v1.36.0 正式发布并经过社区初步验证后，再规划生产集群的升级。

## 📋 Release 包含的变更

### PR #134947: Fine-grained Authorization for ResourceClaim Status Updates
- **链接：** https://github.com/kubernetes/kubernetes/pull/134947
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, size/XXL, kind/api-change, kind/feature, release-note-action-required, sig/auth, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, needs-priority, area/dependency, needs-triage, wg/device-management
- **变更说明：**
  实现KEP-4817，为DRA ResourceClaim状态更新引入细粒度授权检查。通过新特性门控DRAResourceClaimGranularStatusAuthorization（Beta，1.36默认启用），要求调用者分别拥有更新resourceclaims/binding和resourceclaims/driver子资源的权限，以增强安全性并遵循最小权限原则。

### PR #135828: Kubelet: Add alpha-2 stage implementation for UserNamespacesHostNetworkSupport feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/135828
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** area/test, area/kubelet, sig/scheduling, lgtm, sig/node, release-note, sig/autoscaling, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, area/dependency, needs-triage
- **变更说明：**
  为UserNamespacesHostNetworkSupport特性门控添加alpha-2阶段的实现，该功能涉及用户命名空间对主机网络的支持。

### PR #136589: Add Workload-Aware Preemption fields to Workload and PodGroup APIs
- **链接：** https://github.com/kubernetes/kubernetes/pull/136589
- **状态：** closed
- **已合并：** 是
- **作者：** tosi3k
- **标签：** area/test, priority/important-soon, sig/scheduling, area/apiserver, area/kubectl, lgtm, area/provider/gcp, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, area/code-generation, sig/cloud-provider, api-review, needs-triage, sig/etcd, area/workload-aware
- **变更说明：**
  在WorkloadAwarePreemption特性门控下，为Workload和PodGroup API新增DisruptionMode、PriorityClassName和Priority字段。DisruptionMode用于控制Pod组在抢占时是作为整体还是单独处理，Priority字段用于调度和抢占优先级决策。

### PR #136989: KEP-5729: DRA: ResourceClaim Support for Workloads
- **链接：** https://github.com/kubernetes/kubernetes/pull/136989
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, area/kubectl, lgtm, area/provider/gcp, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, area/code-generation, sig/cloud-provider, needs-priority, api-review, needs-triage, sig/etcd, wg/device-management, area/workload-aware
- **变更说明：**
  实现KEP-5729，为Workloads（工作负载）添加Dynamic Resource Allocation (DRA) ResourceClaim支持，扩展了DRA功能以允许工作负载声明资源。

### PR #137028: KEP-5677: Add ResourcePoolStatusRequest API for DRA resource availability visibility
- **链接：** https://github.com/kubernetes/kubernetes/pull/137028
- **状态：** closed
- **已合并：** 是
- **作者：** nmn3m
- **标签：** area/test, sig/scheduling, area/apiserver, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, needs-priority, api-review, triage/accepted, sig/etcd, wg/device-management
- **变更说明：**
  实现KEP-5677，新增ResourcePoolStatusRequest API（v1alpha1）用于查询DRA资源池的可用性状态。该API提供资源池容量、已分配量等信息的快照，解决了用户无法在提交工作负载前了解资源可用性的问题。

### PR #137190: KEP-5491: DRA: List Types for Attributes [Alpha] 
- **链接：** https://github.com/kubernetes/kubernetes/pull/137190
- **状态：** closed
- **已合并：** 是
- **作者：** everpeace
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage, wg/device-management
- **变更说明：**
  实现KEP-5491，为DRA（Dynamic Resource Allocation）属性支持列表类型，该功能处于Alpha阶段。

### PR #137544: [FeatureGate] Promote NodeLogQuery to GA in  v1.36 and lock default to `true`
- **链接：** https://github.com/kubernetes/kubernetes/pull/137544
- **状态：** closed
- **已合并：** 是
- **作者：** jrvaldes
- **标签：** priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, kind/api-change, kind/feature, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-triage
- **变更说明：**
  将NodeLogQuery功能升级为GA（正式可用），并在v1.36版本中将其特性门控默认值锁定为启用（true）。

### PR #137606: Add workload aware preemption
- **链接：** https://github.com/kubernetes/kubernetes/pull/137606
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** area/test, sig/scheduling, lgtm, sig/storage, sig/node, release-note, size/XXL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, area/e2e-test-framework, needs-triage, wg/device-management, area/workload-aware
- **变更说明：**
  实现KEP-5710的工作负载感知抢占功能。当启用WorkloadAwarePreemption特性门控且Pod组调度失败时，将对整个Pod组执行抢占，而非对组内每个Pod执行默认抢占。

### PR #137684: [PodLevelResources] Graduate InPlacePodLevelResourcesVerticalScaling feature to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/137684
- **状态：** closed
- **已合并：** 是
- **作者：** ndixita
- **标签：** area/test, area/kubelet, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, sig/autoscaling, size/XS, kind/api-change, area/release-eng, sig/apps, approved, cncf-cla: yes, sig/testing, sig/release, area/code-generation, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将InPlacePodLevelResourcesVerticalScaling（原地Pod级别资源垂直伸缩）特性从Alpha升级至Beta阶段。

### PR #137904: KEP-961: demote maxUnavailable feature in statefulset to off by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/137904
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/XS, sig/apps, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  将StatefulSet的MaxUnavailableStatefulSet特性默认关闭，以修复其在1.35版本中导致的Parallel Pod管理回归问题（关联issue #137409）。

### PR #138030: kubelet: do not destroy nodeAllocatableResourceClaimStatuses
- **链接：** https://github.com/kubernetes/kubernetes/pull/138030
- **状态：** closed
- **已合并：** 是
- **作者：** askervin
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复kubelet在更新Pod.Status时意外销毁NodeAllocatableResourceClaimStatuses信息的问题。该信息由DRANodeAllocatableResources特性引入，用于记录Pod的DRA原生资源分配状态，对即将在1.36成为Alpha的特性至关重要。

### PR #138035: kep-5304: bump cdi spec version to 0.5.0
- **链接：** https://github.com/kubernetes/kubernetes/pull/138035
- **状态：** closed
- **已合并：** 是
- **作者：** alaypatel07
- **标签：** kind/bug, lgtm, sig/node, release-note, size/XS, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  根据KEP-5304，将CDI（Container Device Interface）规范版本升级至0.5.0。

### PR #138049: Pod events fix
- **链接：** https://github.com/kubernetes/kubernetes/pull/138049
- **状态：** closed
- **已合并：** 是
- **作者：** ndixita
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复了与Pod事件相关的bug，涉及kubelet组件。

### PR #138199: pause: fix version drift and enforce full SemVer validation
- **链接：** https://github.com/kubernetes/kubernetes/pull/138199
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, area/test, priority/important-soon, kind/cleanup, sig/scheduling, area/kubectl, lgtm, area/provider/gcp, sig/cluster-lifecycle, release-note, size/M, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, triage/accepted
- **变更说明：**
  修复pause容器镜像的版本漂移问题，并强制进行完整的SemVer版本号验证。

### PR #138261: Bump golang version from 1.26.1 to 1.26.2
- **链接：** https://github.com/kubernetes/kubernetes/pull/138261
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** priority/critical-urgent, kind/cleanup, lgtm, release-note, size/XS, approved, cncf-cla: yes, sig/testing, sig/architecture, needs-triage
- **变更说明：**
  将项目使用的Golang版本从1.26.1升级至1.26.2。

---
*本报告由 Containerd Release Tracker 自动生成*
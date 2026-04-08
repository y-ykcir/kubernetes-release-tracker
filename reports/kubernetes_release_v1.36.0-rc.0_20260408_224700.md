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
- **分析时间：** 2026-04-08 22:47:00
- **分析的 PR 数量：** 15
- **分析的 Issue 数量：** 2
- **重要项目数量：** 17

## 📊 版本概述
Kubernetes v1.36.0-rc.0 是一个以增强动态资源分配（DRA）安全性、修复关键 StatefulSet 回归问题、推进工作负载感知抢占和节点日志查询功能为核心的技术预览版本。

## 🔒 安全问题修复
1. ⚠️ Go 语言版本升级至 1.26.2 - [PR #138261](https://github.com/kubernetes/kubernetes/pull/138261) - **风险级别：** 中。此升级通常包含 Go 运行时的安全修复和漏洞补丁，是维护集群基础安全性的重要举措。建议关注 Go 1.26.2 的官方安全公告。
2. ⚠️ DRA 资源声明状态更新的细粒度授权（如前所述） - [PR #134947](https://github.com/kubernetes/kubernetes/pull/134947) - **风险级别：** 低（安全增强）。此变更是主动安全加固，但可能因权限不足导致现有的 DRA 控制器或插件更新失败，属于兼容性风险。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 StatefulSet 并行 Pod 管理中的严重回归问题 - [PR #137904](https://github.com/kubernetes/kubernetes/pull/137904) / [Issue #137409](https://github.com/kubernetes/kubernetes/issues/137409) - **影响：** 在 v1.35 中，当启用 `MaxUnavailableStatefulSet` 特性且首个 Pod 版本有缺陷时，StatefulSet 控制器可能无法更新 Pod 版本，导致 Pod 持续崩溃循环且无法恢复。此 PR 将该特性默认关闭以阻止此问题。**生产影响：高**，使用此特性的用户需立即关注。
2. 修复 kubelet 销毁 DRA 节点可分配资源声明状态的问题 - [PR #138030](https://github.com/kubernetes/kubernetes/pull/138030) - **影响：** 修复了 kubelet 在更新 Pod 状态时，错误地清除了 `nodeAllocatableResourceClaimStatuses` 字段的问题，确保了 DRA 原生资源分配信息的正确性。
3. 修复 Pod 事件中不必要的 ResizeCompleted 事件 - [Issue #137858](https://github.com/kubernetes/kubernetes/issues/137858) - **影响：** 当启用 `InPlacePodLevelResourcesVerticalScaling` 特性门控时，Pod 创建后会错误地发出 `ResizeCompleted` 事件，造成事件噪音和可能的监控误报。
4. 修复 pause 容器版本漂移并强制执行完整 SemVer 验证 - [PR #138199](https://github.com/kubernetes/kubernetes/pull/138199) - **影响：** 确保 pause 容器版本符合完整的语义化版本规范，提升集群组件版本管理的一致性和可靠性。

## 💥 破坏性变更
1. 🚨 默认关闭 StatefulSet 的 MaxUnavailable 特性 - [PR #137904](https://github.com/kubernetes/kubernetes/pull/137904) - **影响：** 为修复严重回归，`MaxUnavailableStatefulSet` 特性门控在此版本中默认被设置为 `false`。**迁移动作：** 依赖此功能实现快速 StatefulSet 滚动的用户，在升级后需要显式启用该特性门控（`--feature-gates=MaxUnavailableStatefulSet=true`），并充分测试其稳定性。
2. 🚨 DRA 资源声明状态更新需要新的 RBAC 权限 - [PR #134947](https://github.com/kubernetes/kubernetes/pull/134947) - **影响：** 启用 `DRAResourceClaimGranularStatusAuthorization`（默认开启）后，更新 `ResourceClaim` 状态的 DRA 驱动程序或控制器需要被授予 `resourceclaims/binding` 子资源的 `update` 权限。**迁移动作：** 检查并更新相关 ServiceAccount 的 ClusterRole 绑定，确保包含对新子资源的权限。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 动态资源分配（DRA）细粒度状态更新授权 - [PR #134947](https://github.com/kubernetes/kubernetes/pull/134947) - **影响：** 为 DRA ResourceClaim 的状态更新引入了更精细的 RBAC 权限控制（`resourceclaims/binding` 子资源），默认启用。DRA 插件或控制器现在需要特定权限才能更新 `allocations` 和 `device statuses`，增强了安全性但可能影响现有插件权限配置。
2. 工作负载感知抢占（Workload-Aware Preemption）API 扩展 - [PR #136589](https://github.com/kubernetes/kubernetes/pull/136589) - **影响：** 为 Workload 和 PodGroup API 新增了 `DisruptionMode`、`PriorityClassName` 和 `Priority` 字段。当启用 `WorkloadAwarePreemption` 特性门控时，可以按 Pod 组进行整体抢占，提升批处理工作负载的调度公平性。
3. NodeLogQuery 功能升级至 GA - [PR #137544](https://github.com/kubernetes/kubernetes/pull/137544) - **影响：** `NodeLogQuery` 特性门控默认锁定为 `true`（GA）。通过 kubelet API 查询节点日志的功能现已稳定，可用于生产环境，增强了节点的可观测性。
4. 原地 Pod 级别资源垂直伸缩（InPlacePodLevelResourcesVerticalScaling）升级至 Beta - [PR #137684](https://github.com/kubernetes/kubernetes/pull/137684) - **影响：** 该功能进入 Beta 阶段，稳定性提升。允许在不重启 Pod 的情况下调整容器资源请求/限制，对需要动态调整资源的应用（如 Java）有益。
5. 新增 DRA 资源池状态查询 API（ResourcePoolStatusRequest） - [PR #137028](https://github.com/kubernetes/kubernetes/pull/137028) - **影响：** 引入新的 `v1alpha1` API，允许用户查询 DRA 资源池（如 GPU）的可用性、分配状态，为外部调度器和用户提供了资源可见性。

## 🚀 性能优化
1. 实现工作负载感知抢占逻辑 - [PR #137606](https://github.com/kubernetes/kubernetes/pull/137606) - **提升：** 当 `WorkloadAwarePreemption` 启用且 Pod 组调度失败时，会尝试进行工作负载感知的抢占，而非默认的单个 Pod 抢占。这有望提升批处理作业（如 AI/ML 训练）的整体调度成功率和集群利用率。
2. DRA 属性列表类型支持（Alpha） - [PR #137190](https://github.com/kubernetes/kubernetes/pull/137190) - **提升：** 为 DRA 资源属性引入了列表类型支持，可以更高效地表达和管理具有多个实例或复杂属性的设备资源。

## 🎯 风险评估
**整体风险评估：中等。** 此版本包含一个标记为 `critical-urgent` 的 StatefulSet 回归修复（#137904），对受影响用户而言升级风险较高，必须优先验证。对于广泛使用 DRA 或相关 Alpha/Beta 功能的集群，由于 API 和授权模型的变更，升级风险为中等，需要充分的兼容性测试。对于未使用这些前沿功能的常规集群，升级风险相对较低，主要受益于稳定性修复和 NodeLogQuery 等功能的 GA。**建议升级时机：** 生产环境建议等待 v1.36.0 正式发布后，在测试集群中充分验证所有工作负载，特别是 StatefulSet 和 DRA 相关功能，再规划生产升级。

## 📋 升级建议
1. **立即测试 StatefulSet 行为：** 如果您的集群使用 StatefulSet 并计划升级到 v1.36，务必在测试环境中验证 Pod 滚动更新逻辑，特别是检查 PR #137904 修复的回归问题是否影响您的应用。
2. **审查 DRA 插件权限：** 如果使用 Dynamic Resource Allocation（如 GPU、FPGA 设备插件），在升级前，根据 PR #134947 的要求，预先为相关组件配置 `resourceclaims/binding` 子资源的更新权限，避免升级后功能中断。
3. **评估特性门控影响：** 明确您集群中启用的特性门控。本次版本涉及 `MaxUnavailableStatefulSet`（默认关）、`DRAResourceClaimGranularStatusAuthorization`（默认开）、`WorkloadAwarePreemption`（Alpha）、`InPlacePodLevelResourcesVerticalScaling`（Beta）等。根据您的使用情况决定是否调整配置。
4. **关注 API 变化：** 注意新增的 `ResourcePoolStatusRequest` (`v1alpha1`) 等 API。如果使用客户端库，确保其版本与 v1.36 API 兼容。
5. **将 Go 版本升级视为安全基线更新：** 虽然由项目维护，但此次 Go 1.26.1 -> 1.26.2 的升级应被视为一次重要的安全基础更新。

## 📋 Release 包含的变更

### PR #134947: Fine-grained Authorization for ResourceClaim Status Updates
- **链接：** https://github.com/kubernetes/kubernetes/pull/134947
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, size/XXL, kind/api-change, kind/feature, release-note-action-required, sig/auth, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, needs-priority, area/dependency, needs-triage, wg/device-management
- **变更说明：**
  实现 KEP-4817，为 DRA ResourceClaim 状态更新引入细粒度授权检查。新增 feature gate `DRAResourceClaimGranularStatusAuthorization`（Beta，在 1.36 版本默认启用），要求调用者拥有特定子资源（如 `resourceclaims/binding`、`resourceclaims/driver`）的更新权限，以提升安全性。

### PR #135828: Kubelet: Add alpha-2 stage implementation for UserNamespacesHostNetworkSupport feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/135828
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** area/test, area/kubelet, sig/scheduling, lgtm, sig/node, release-note, sig/autoscaling, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, area/dependency, needs-triage
- **变更说明：**
  为 `UserNamespacesHostNetworkSupport` feature gate 添加 alpha-2 阶段的实现。

### PR #136589: Add Workload-Aware Preemption fields to Workload and PodGroup APIs
- **链接：** https://github.com/kubernetes/kubernetes/pull/136589
- **状态：** closed
- **已合并：** 是
- **作者：** tosi3k
- **标签：** area/test, priority/important-soon, sig/scheduling, area/apiserver, area/kubectl, lgtm, area/provider/gcp, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, area/code-generation, sig/cloud-provider, api-review, needs-triage, sig/etcd, area/workload-aware
- **变更说明：**
  为工作负载感知抢占（Workload Aware Preemption）在 Workload 和 PodGroup API 中新增 `DisruptionMode`、`PriorityClassName` 和 `Priority` 字段。`DisruptionMode` 控制 Pod 组是否作为整体被抢占，优先级字段影响调度和抢占决策。

### PR #136989: KEP-5729: DRA: ResourceClaim Support for Workloads
- **链接：** https://github.com/kubernetes/kubernetes/pull/136989
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, area/kubectl, lgtm, area/provider/gcp, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, area/code-generation, sig/cloud-provider, needs-priority, api-review, needs-triage, sig/etcd, wg/device-management, area/workload-aware
- **变更说明：**
  实现 KEP-5729，为 DRA ResourceClaim 提供对 Workloads（如 Job、CronJob）的支持。这是一项重大的 API 变更和功能扩展，使工作负载能够声明和使用 DRA 资源。

### PR #137028: KEP-5677: Add ResourcePoolStatusRequest API for DRA resource availability visibility
- **链接：** https://github.com/kubernetes/kubernetes/pull/137028
- **状态：** closed
- **已合并：** 是
- **作者：** nmn3m
- **标签：** area/test, sig/scheduling, area/apiserver, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, needs-priority, api-review, triage/accepted, sig/etcd, wg/device-management
- **变更说明：**
  实现 KEP-5677，新增 `ResourcePoolStatusRequest` API（v1alpha1）以提供 DRA 资源池可用性的一次性快照。包含控制器、按驱动和池名过滤、以及大集群的限流/截断支持，解决了用户无法查询 DRA 资源可用性的问题。

### PR #137190: KEP-5491: DRA: List Types for Attributes [Alpha] 
- **链接：** https://github.com/kubernetes/kubernetes/pull/137190
- **状态：** closed
- **已合并：** 是
- **作者：** everpeace
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage, wg/device-management
- **变更说明：**
  实现 KEP-5491，为 DRA 属性（Attributes）引入列表类型支持，目前处于 Alpha 阶段。这是一项 API 变更，旨在增强 DRA 资源描述的灵活性。

### PR #137544: [FeatureGate] Promote NodeLogQuery to GA in  v1.36 and lock default to `true`
- **链接：** https://github.com/kubernetes/kubernetes/pull/137544
- **状态：** closed
- **已合并：** 是
- **作者：** jrvaldes
- **标签：** priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, kind/api-change, kind/feature, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-triage
- **变更说明：**
  将 `NodeLogQuery` 功能从 Beta 升级为 GA（正式发布），并在 v1.36 版本中将其 feature gate 默认值锁定为 `true`。

### PR #137606: Add workload aware preemption
- **链接：** https://github.com/kubernetes/kubernetes/pull/137606
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** area/test, sig/scheduling, lgtm, sig/storage, sig/node, release-note, size/XXL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, area/e2e-test-framework, needs-triage, wg/device-management, area/workload-aware
- **变更说明：**
  实现 KEP-5710 的工作负载感知抢占（Workload Aware Preemption）。当启用对应 feature gate 且 Pod 组调度失败时，将对整个 Pod 组进行抢占，而非对组内每个 Pod 单独执行默认抢占逻辑。

### PR #137684: [PodLevelResources] Graduate InPlacePodLevelResourcesVerticalScaling feature to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/137684
- **状态：** closed
- **已合并：** 是
- **作者：** ndixita
- **标签：** area/test, area/kubelet, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, sig/autoscaling, size/XS, kind/api-change, area/release-eng, sig/apps, approved, cncf-cla: yes, sig/testing, sig/release, area/code-generation, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将 `InPlacePodLevelResourcesVerticalScaling`（原地 Pod 级别资源垂直伸缩）功能从 Alpha 升级至 Beta 阶段。

### PR #137904: KEP-961: demote maxUnavailable feature in statefulset to off by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/137904
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/XS, sig/apps, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  由于在 1.35 版本中引入的 `MaxUnavailableStatefulSet` 特性破坏了 StatefulSet 的 Parallel pod 管理模式（见 Issue #137409），此 PR 将该 feature gate 默认值改回 `false` 以修复此回归问题。

### PR #138030: kubelet: do not destroy nodeAllocatableResourceClaimStatuses
- **链接：** https://github.com/kubernetes/kubernetes/pull/138030
- **状态：** closed
- **已合并：** 是
- **作者：** askervin
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 kubelet 在更新 Pod.Status 时意外清除 `NodeAllocatableResourceClaimStatuses` 字段的问题。该字段由 DRANodeAllocatableResources 特性引入，用于 DRA 原生资源分配，此修复确保了信息的正确保留。

### PR #138035: kep-5304: bump cdi spec version to 0.5.0
- **链接：** https://github.com/kubernetes/kubernetes/pull/138035
- **状态：** closed
- **已合并：** 是
- **作者：** alaypatel07
- **标签：** kind/bug, lgtm, sig/node, release-note, size/XS, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  根据 KEP-5304，将 Container Device Interface (CDI) 规范版本升级至 0.5.0。

### PR #138049: Pod events fix
- **链接：** https://github.com/kubernetes/kubernetes/pull/138049
- **状态：** closed
- **已合并：** 是
- **作者：** ndixita
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复 Pod 事件相关的问题。具体细节未在提供的片段中完整展示，但根据标签和标题，这是一个针对 kubelet 的 bug 修复。

### PR #138199: pause: fix version drift and enforce full SemVer validation
- **链接：** https://github.com/kubernetes/kubernetes/pull/138199
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, area/test, priority/important-soon, kind/cleanup, sig/scheduling, area/kubectl, lgtm, area/provider/gcp, sig/cluster-lifecycle, release-note, size/M, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, triage/accepted
- **变更说明：**
  修复 pause 容器镜像的版本漂移问题，并强制执行完整的 SemVer 版本验证。

### PR #138261: Bump golang version from 1.26.1 to 1.26.2
- **链接：** https://github.com/kubernetes/kubernetes/pull/138261
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** priority/critical-urgent, kind/cleanup, lgtm, release-note, size/XS, approved, cncf-cla: yes, sig/testing, sig/architecture, needs-triage
- **变更说明：**
  将 Kubernetes 项目使用的 Golang 版本从 1.26.1 升级至 1.26.2。

---
*本报告由 Containerd Release Tracker 自动生成*
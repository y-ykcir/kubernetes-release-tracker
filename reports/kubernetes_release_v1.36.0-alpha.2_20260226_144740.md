# Kubernetes 版本发布分析报告
## v1.36.0-alpha.2 (v1.36.0-alpha.2)

### 📋 版本信息
- **版本标签：** v1.36.0-alpha.2
- **版本名称：** v1.36.0-alpha.2
- **发布时间：** 2026-02-26T14:31:43Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.36.0-alpha.2

### 🔍 分析统计
- **分析时间：** 2026-02-26 14:47:40
- **分析的 PR 数量：** 43
- **分析的 Issue 数量：** 12
- **重要项目数量：** 53

## 📊 版本概述
Kubernetes v1.36.0-alpha.2 是一个早期预览版本，引入了多项重要的 API 变更和功能改进，重点关注调度优化、API 稳定化以及废弃功能的移除，同时包含多个关键 Bug 修复。

## 🔒 安全问题修复
1. ⚠️ 允许 kube-apiserver 从意外连接到错误服务器的情况中恢复 - [PR #137157](https://github.com/kubernetes/kubernetes/pull/137157) - **风险级别：** 中 - **影响：** 修复了因连接复用和跳过证书验证导致 APIService 持续显示不健康的问题，提升了控制平面的健壮性。
2. ⚠️ 锁定并计划移除 gitRepo 卷类型 - [PR #136400](https://github.com/kubernetes/kubernetes/pull/136400) - **风险级别：** 低 - **影响：** 该卷类型因潜在安全风险被禁用，需评估现有工作负载并迁移。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kube-proxy 在 nftables 1.1.3+ 版本上崩溃的问题（修复被回退，问题仍存在） - [PR #136796](https://github.com/kubernetes/kubernetes/pull/136796) & [PR #137169](https://github.com/kubernetes/kubernetes/pull/137169) - **影响：** 使用 nftables 模式且系统版本较新时，kube-proxy 可能崩溃导致网络故障，目前暂无稳定修复。
2. 修复 kubectl logs -f 在 Pod 启动阶段抛出错误的问题 - [PR #136411](https://github.com/kubernetes/kubernetes/pull/136411) - **影响：** 改善用户体验，命令会等待 Pod 就绪而非立即报错。
3. 修复 PodCertificateRequest 中 OwnerReference 的 apiVersion 错误，避免资源泄漏 - [PR #137008](https://github.com/kubernetes/kubernetes/pull/137008) - **影响：** 确保 Pod 删除后其证书请求能被正确垃圾回收。
4. 修复 kube-proxy 在所有端点未就绪时产生误导性日志刷屏的问题 - [PR #136743](https://github.com/kubernetes/kubernetes/pull/136743) - **影响：** 减少日志噪音，避免对日志系统造成压力。
5. 修复容器交换内存使用量指标 (`container_swap_usage_bytes`) 始终为 0 的问题 - [PR #137098](https://github.com/kubernetes/kubernetes/pull/137098) - **影响：** 监控系统现在能正确获取容器级别的 Swap 使用数据。
6. 修复 client-go Reflector 无法处理 Table 格式资源的问题 - [PR #136937](https://github.com/kubernetes/kubernetes/pull/136937) - **影响：** 防止因接收到意外格式的资源导致 Informer 存储为空或行为异常。

## 💥 破坏性变更
1. 🚨 API 服务器 admission 子系统弃用 `sets.String`，改用 `sets.Set[string]` - [PR #134044](https://github.com/kubernetes/kubernetes/pull/134044) - **影响：** 直接导入并使用 `k8s.io/apiserver/pkg/admission` 包中相关 API 的客户端代码需要更新类型。
2. 🚨 kubeadm 完全移除对 FlexVolume 的内置支持 - [PR #136423](https://github.com/kubernetes/kubernetes/pull/136423) - **影响：** 依赖此功能的集群升级前必须按照说明进行手动配置迁移，否则控制器管理器可能无法启动。
3. 🚨 Pod 证书 Beta API 废弃 `spec.pkixPublicKey` 和 `spec.proofOfPossession`，改用 `spec.stubPKCS10Request` - [PR #136729](https://github.com/kubernetes/kubernetes/pull/136729) - **影响：** 使用旧字段的客户端和签名器实现需要迁移到新字段。
4. 🚨 移除临时构建标签的 `ProtoMessage` 方法 - [PR #137084](https://github.com/kubernetes/kubernetes/pull/137084) - **影响：** 极少数依赖此误导性方法的外部工具（如 Karmada）需要更新其代码，否则可能编译失败。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 调度器 PostFilter 插件接口变更，为延迟抢占机制做准备 - [PR #136254](https://github.com/kubernetes/kubernetes/pull/136254) - **影响：** 自定义调度器 PostFilter 插件需要更新以返回被抢占的 Pod 列表，否则可能导致抢占逻辑异常。
2. MutatingAdmissionPolicy 功能正式毕业为 GA (v1) - [PR #136039](https://github.com/kubernetes/kubernetes/pull/136039) - **影响：** 提供稳定的声明式 CEL 变更准入 API，可替代部分 Mutating Webhook，降低运维复杂度。
3. Pod 证书 API (Beta) 引入 `stubPKCS10Request` 字段并废弃旧字段 - [PR #136729](https://github.com/kubernetes/kubernetes/pull/136729) - **影响：** 提升与外部 CA（如 Vault）的兼容性，使用 `pkixPublicKey` 和 `proofOfPossession` 的代码需要迁移。
4. 一组核心组件指标从 Alpha 提升至 Beta 稳定性 - [PR #136154](https://github.com/kubernetes/kubernetes/pull/136154) - **影响：** `kubernetes_build_info` 等关键监控指标获得更强的 API 和标签稳定性保证。
5. kubeadm 移除对 FlexVolume 的内置支持 - [PR #136423](https://github.com/kubernetes/kubernetes/pull/136423) - **影响：** 自 1.22 起已废弃，用户需按说明自定义 KCM 镜像和挂载卷以继续使用，或迁移至 CSI。
6. gitRepo 卷驱动被锁定为禁用状态 - [PR #136400](https://github.com/kubernetes/kubernetes/pull/136400) - **影响：** 由于安全考虑，此卷类型将无法使用，需寻找替代方案（如 Git 同步 Sidecar 容器）。

## 🚀 性能优化
1. 调度器 PostFilter 结果扩展，为延迟抢占（Delayed Preemption）奠定基础 - [PR #136254](https://github.com/kubernetes/kubernetes/pull/136254) - **提升：** 未来可将抢占决策计算与执行解耦，优化高负载集群的调度性能。
2. 优化抢占逻辑，避免对处于 PreBind 阶段的 Pod 进行删除 API 调用 - [PR #135502](https://github.com/kubernetes/kubernetes/pull/135502) - **提升：** 减少不必要的 API 调用，让被抢占的 Pod 能重新入队而非完全删除。
3. 为 kubelet 添加 `kubelet_metrics_provider` 指标 - [PR #136952](https://github.com/kubernetes/kubernetes/pull/136952) - **提升：** 增强对 kubelet 指标提供子系统的可观测性，便于性能分析和调试。

## 🎯 风险评估
整体风险评估：**高**。作为 Alpha 版本，其稳定性、性能和兼容性均未得到保证，包含实验性变更和多个破坏性更新。

**建议的升级时机：** 仅限开发和测试集群进行早期功能验证。生产环境应等待至少 Beta 甚至 Release Candidate (RC) 版本。

**需要特别关注的方面：**
1.  **调度器插件兼容性：** PostFilter 接口变更可能影响调度行为。
2.  **存储驱动迁移：** FlexVolume 支持的移除和 gitRepo 的禁用需要立即评估影响。
3.  **kube-proxy 稳定性：** nftables 崩溃问题尚未有最终稳定修复，是网络层面的重大风险点。
4.  **客户端库更新：** 涉及 `sets.String` 等 API 变更，需要同步更新客户端代码和依赖库。

## 📋 升级建议
1. **切勿在生产环境使用 Alpha 版本。** 此版本仅用于早期测试和评估。
2. **评估自定义调度器插件：** 如果使用了自定义的 PostFilter 调度器插件，必须检查并更新插件实现以适配新的接口要求。
3. **检查 FlexVolume 使用情况：** 如果集群通过 kubeadm 部署且仍在使用 FlexVolume，请立即制定迁移计划至 CSI，或按照 PR #136423 的说明准备自定义升级方案。
4. **关注 API 废弃通知：** 检查代码库是否使用了已废弃的 API，如 `sets.String`、Pod 证书的旧字段等，并计划在升级前完成迁移。
5. **测试 nftables 兼容性：** 如果使用 kube-proxy 的 nftables 模式，请在测试环境中验证与系统 nftables 版本的兼容性，关注相关崩溃问题的修复进展。
6. **利用新稳定功能：** 计划评估并采用已 GA 的 MutatingAdmissionPolicy 来简化准入控制。

## 📋 Release 包含的变更

### PR #10: Move everything out of src and reorganize scripts.
- **链接：** https://github.com/kubernetes/kubernetes/pull/10
- **状态：** closed
- **已合并：** 是
- **作者：** jbeda
- **变更说明：**
  重组脚本目录结构，将内容移出 src 目录，更新文档。调整 e2e 测试使用 g1-small 实例，并禁用未经充分测试的 `curl | bash` 集群启动方式。

### PR #134044: Replace deprecated sets.String with sets.Set[string] in apiserver
- **链接：** https://github.com/kubernetes/kubernetes/pull/134044
- **状态：** closed
- **已合并：** 是
- **作者：** mcallzbl
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  在 apiserver 的 admission 子系统中，将所有已弃用的 `sets.String` 类型用法替换为推荐的 `sets.Set[string]` 类型。这是一个代码现代化清理工作，涉及 API 破坏性变更。

### PR #134675: Enforce either optional or required tag on apiserverinternal API group
- **链接：** https://github.com/kubernetes/kubernetes/pull/134675
- **状态：** closed
- **已合并：** 是
- **作者：** JoelSpeed
- **标签：** lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  强制要求 apiserverinternal API 组中的字段必须标注 `optional` 或 `required` 标签。这是相关变更浪潮中的第一项。

### PR #134827: Add Resource Version query and Bookmarks to thread safe store
- **链接：** https://github.com/kubernetes/kubernetes/pull/134827
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, lgtm, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  为线程安全存储（thread safe store）添加了Resource Version查询和Bookmarks功能。这是一个API机制的特性增强，改进了存储层的查询能力和数据同步机制。

### PR #134937: Daemonset controller staleness detection
- **链接：** https://github.com/kubernetes/kubernetes/pull/134937
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, area/e2e-test-framework, triage/accepted, wg/device-management
- **变更说明：**
  为 DaemonSet 控制器添加陈旧性检测功能。这是一个大型功能变更。

### PR #134981: kubelet: drop cpu load metrics from container metrics test
- **链接：** https://github.com/kubernetes/kubernetes/pull/134981
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  从容器指标测试中移除了CPU负载指标。这是一个测试修复，因为CPU负载指标不稳定，导致测试失败，移除后提高了测试的可靠性。

### PR #135335: [1.36] Remove feature gate HonorPVReclaimPolicy
- **链接：** https://github.com/kubernetes/kubernetes/pull/135335
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/cleanup, lgtm, sig/storage, release-note, size/M, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  在Kubernetes 1.36版本中，移除了HonorPVReclaimPolicy特性门控。这是一项清理工作，表明该功能已稳定或默认启用，无需再通过特性门控控制。

### PR #135502: Preempt pods in prebind phase without delete calls.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135502
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  允许调度器在PreBind阶段抢占Pod，而无需向apiserver发出删除调用。被抢占的Pod将返回退避队列而非被完全删除，改变了抢占行为，解决了issue #132332。

### PR #135749: Fix: Incorrect duration metric recording incorrect values
- **链接：** https://github.com/kubernetes/kubernetes/pull/135749
- **状态：** closed
- **已合并：** 是
- **作者：** novahe
- **标签：** kind/bug, area/kubelet, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/instrumentation, sig/architecture, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了持续时间指标记录错误值的问题。这是一个涉及kubelet和调度的bug修复，确保指标（如调度延迟）能够被正确记录和反映。

### PR #135808: SeparateCacheWatchRPC LockToDefault set true
- **链接：** https://github.com/kubernetes/kubernetes/pull/135808
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  将 SeparateCacheWatchRPC 特性门锁定为默认值 false，无法再被覆盖，为未来版本移除该特性门做准备。这是一个针对 apiserver 的清理工作。

### PR #135965: set KEP-5440 to enabled by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/135965
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  将 KEP-5440 默认启用，并为此添加了两个 e2e 测试。

### PR #136039: Promote MutatingAdmissionPolicy to v1 (GA)
- **链接：** https://github.com/kubernetes/kubernetes/pull/136039
- **状态：** closed
- **已合并：** 是
- **作者：** lalitc375
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, sig/architecture, area/conformance, area/code-generation, needs-priority, api-review, needs-triage, sig/etcd
- **变更说明：**
  将 `MutatingAdmissionPolicy` 功能提升至 General Availability (GA) 状态，API 版本升级为 `admissionregistration.k8s.io/v1`。该功能提供基于 CEL 的声明式准入控制，可作为 mutating webhook 的替代方案。

### PR #136154: Promote component-base metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136154
- **状态：** closed
- **已合并：** 是
- **作者：** bhope
- **标签：** area/test, sig/network, area/kubelet, sig/scalability, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, priority/important-longterm, sig/architecture, area/code-generation, sig/cloud-provider, ok-to-test, area/e2e-test-framework, area/dependency, triage/accepted, area/stable-metrics, sig/etcd, wg/device-management
- **变更说明：**
  将一组广泛使用的 component-base 指标从 Alpha 提升至 Beta 稳定性，包括 `kubernetes_build_info`、`rest_client_requests_total`、`rest_client_request_duration_seconds` 和 `running_managed_controllers`。此举为这些在生产中已使用多个版本的指标提供了更强的 API 和标签稳定性保证。

### PR #136254: Extend PostFilterResult with a list of victim Pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/136254
- **状态：** closed
- **已合并：** 是
- **作者：** tosi3k
- **标签：** sig/scheduling, lgtm, size/L, kind/feature, release-note-action-required, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  扩展了PostFilterResult结构体，新增了被抢占Pod（victim Pods）列表字段。这是实现延迟抢占机制的第一步，旨在将抢占决策的计算与执行解耦。

### PR #136400: KEP:5040 Lock gitRepo Volume Driver to disabled.
- **链接：** https://github.com/kubernetes/kubernetes/pull/136400
- **状态：** closed
- **已合并：** 是
- **作者：** vinayakankugoyal
- **标签：** lgtm, sig/storage, release-note, size/S, approved, cncf-cla: yes, needs-priority, kind/deprecation, needs-triage
- **变更说明：**
  根据KEP-5040，将gitRepo卷驱动锁定为禁用状态。这是一项弃用（deprecation）工作，标志着该卷类型将被逐步淘汰。

### PR #136411: fix cli throwing an error when trying to tail the logs for a Pod
- **链接：** https://github.com/kubernetes/kubernetes/pull/136411
- **状态：** closed
- **已合并：** 是
- **作者：** olamilekan000
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  修复了 `kubectl logs --tail` 命令在 Pod 处于 `Pending` 或 `Succeeded` 状态时抛出错误的问题。通过调整 Pod 状态检查逻辑，现在可以正确获取这些状态 Pod 的日志。

### PR #136423: kubeadm: removed the built-in flex volume support
- **链接：** https://github.com/kubernetes/kubernetes/pull/136423
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/backlog, kind/cleanup, lgtm, sig/cluster-lifecycle, size/S, release-note-action-required, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  从 kubeadm 中移除了内置的 flex volume 支持，作为代码清理的一部分。用户需迁移至 CSI 驱动，简化了 kubeadm 的代码库。

### PR #136618: KEP-4671: Introduce Workload Scheduling Cycle
- **链接：** https://github.com/kubernetes/kubernetes/pull/136618
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, area/workload-aware
- **变更说明：**
  根据KEP-4671引入Workload Scheduling Cycle（工作负载调度周期）。这是一个大型特性，旨在改进调度器对工作负载的感知和处理能力，属于sig/scheduling领域。

### PR #136689: Fix kubectl plugin list overshadow detection on Windows
- **链接：** https://github.com/kubernetes/kubernetes/pull/136689
- **状态：** closed
- **已合并：** 是
- **作者：** kfess
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 `kubectl plugin list` 在 Windows 系统上因路径分隔符处理不当而无法正确检测插件 overshadow 的问题。现在使用 `filepath.Base` 来正确提取插件二进制文件名。

### PR #136716: Split from concurrent-node-syncs a separate flag for node status updates
- **链接：** https://github.com/kubernetes/kubernetes/pull/136716
- **状态：** closed
- **已合并：** 是
- **作者：** yonizxz
- **标签：** lgtm, area/cloudprovider, release-note, size/M, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  从 `concurrent-node-syncs` 标志中分离出一个独立的标志，用于控制节点状态更新。这是一个 API 变更，引入了新的配置选项。

### PR #136729: Pod Certificates: Add StubPKCS10Request; migrate in-tree usages
- **链接：** https://github.com/kubernetes/kubernetes/pull/136729
- **状态：** closed
- **已合并：** 是
- **作者：** ahmedtd
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage
- **变更说明：**
  在 Pod Certificates beta API 中添加 `spec.stubPKCS10Request` 字段，以提升与现有 CA 软件的兼容性。同时弃用 `spec.pkixPublicKey` 和 `spec.proofOfPossession` 字段。

### PR #136734: Fix missing GetSharedDeviceIDs bug in GatherAllocatedState
- **链接：** https://github.com/kubernetes/kubernetes/pull/136734
- **状态：** closed
- **已合并：** 是
- **作者：** sunya-ch
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复在启用 DRAConsumableCapacity 时，`pkg/scheduler/framework/plugins/noderesources` 单元测试中发现的 `GatherAllocatedState` 函数缺失 `GetSharedDeviceIDs` 调用的 bug。

### PR #136743: fix(kube-proxy): skip topology hints logging when no ready endpoints exist
- **链接：** https://github.com/kubernetes/kubernetes/pull/136743
- **状态：** closed
- **已合并：** 是
- **作者：** ansilh
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复当 Service 的所有端点都处于非就绪状态时，kube-proxy 错误地记录“忽略相同区域拓扑提示”的日志问题。修复方法是当没有就绪端点时提前返回，避免误导性日志。

### PR #136793: KEP-5073:  Declarative Validation Lifecycle Update
- **链接：** https://github.com/kubernetes/kubernetes/pull/136793
- **状态：** closed
- **已合并：** 是
- **作者：** yongruilin
- **标签：** sig/scheduling, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, needs-priority, needs-triage
- **变更说明：**
  根据KEP-5073，更新了声明式验证（Declarative Validation）的生命周期。这是一个大型的API变更和特性，涉及代码生成，旨在改进验证机制。

### PR #136796: Fix kube-proxy nftables crash with newer nftables versions
- **链接：** https://github.com/kubernetes/kubernetes/pull/136796
- **状态：** closed
- **已合并：** 是
- **作者：** kairosci
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, sig/api-machinery, release-note, size/S, sig/auth, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  修复了 kube-proxy 在 nftables 1.1.3+ 版本上因列出支持 udata 的 nftables sets 而导致段错误崩溃的问题。该修复无需修改 nftables 本身，并向后兼容旧版本。

### PR #136802: Fix data race in PopulateRefs by copying Items and AdditionalProperties
- **链接：** https://github.com/kubernetes/kubernetes/pull/136802
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, area/test, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复了 `PopulateRefs` 函数中因浅拷贝导致的数据竞争问题。通过深拷贝 `Items.Schema` 和 `AdditionalProperties.Schema` 指针字段，解决了多个 goroutine 并发调用时修改共享数据结构的问题。

### PR #136816: k8s.io/cloud-provider: Adds missing TLS flags to webhook serving options
- **链接：** https://github.com/kubernetes/kubernetes/pull/136816
- **状态：** closed
- **已合并：** 是
- **作者：** damdo
- **标签：** lgtm, area/cloudprovider, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  为 cloud-provider webhook 服务选项添加了缺失的 TLS 配置标志，包括 `--webhook-disable-http2-serving`、`--webhook-tls-cipher-suites`、`--webhook-tls-min-version` 和 `--webhook-tls-sni-cert-key`，使其 TLS 配置能力与主服务端点对齐。

### PR #136846: kubelet: defer the configurations flags (and the related fallback behavior) deprecation removal timeline from 1.36 to 1.37 to align with containerd v1.7 support
- **链接：** https://github.com/kubernetes/kubernetes/pull/136846
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  将 kubelet 配置标志（及相关回退行为）的弃用移除时间线从 1.36 版本推迟到 1.37 版本，以与 containerd v1.7 的支持时间对齐。

### PR #136892: Update/kubectl in kustomize to v5.8.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/136892
- **状态：** closed
- **已合并：** 是
- **作者：** koba1t
- **标签：** priority/important-soon, kind/cleanup, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, sig/architecture, needs-priority, area/dependency, needs-triage
- **变更说明：**
  将kustomize中集成的kubectl依赖版本更新至v5.8.1。这是一项依赖项更新/清理工作，旨在获取bug修复和新功能。

### PR #136898: kubeadm:  bump the version in the ContainerRuntimeVersionCheck warning message from 1.36 to 1.37
- **链接：** https://github.com/kubernetes/kubernetes/pull/136898
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** lgtm, sig/cluster-lifecycle, release-note, size/XS, kind/feature, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将kubeadm中ContainerRuntimeVersionCheck警告信息的版本号从1.36更新至1.37。这是一个微小的版本更新，确保警告信息与即将发布的版本保持一致。

### PR #136937: client-go/reflector: reject Table format resources in List and Watch paths
- **链接：** https://github.com/kubernetes/kubernetes/pull/136937
- **状态：** closed
- **已合并：** 是
- **作者：** p0lyn0mial
- **标签：** kind/bug, area/test, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复了 client-go reflector 在处理 `Table` 格式资源时可能崩溃的问题。通过在 List 和 Watch 路径中拒绝 `Table` 格式，确保 reflector 仅处理预期的 `PartialObjectMetadata` 格式。

### PR #136952: Add kubelet_metrics_provider metric
- **链接：** https://github.com/kubernetes/kubernetes/pull/136952
- **状态：** closed
- **已合并：** 是
- **作者：** dgrisonnet
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/M, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  新增 `kubelet_metrics_provider` 指标，用于监控 kubelet 指标提供者的状态，包含 `provider` 和 `status` 标签，帮助诊断指标收集问题。

### PR #136982: Bump images and versions to go 1.25.7 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/136982
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, release-note, size/S, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将构建镜像和版本升级至 Go 1.25.7 并使用 distroless iptables 基础镜像。

### PR #137008: [KEP 4317] Fix incorrect APIVersion in PodCertificateRequest OwnerReference
- **链接：** https://github.com/kubernetes/kubernetes/pull/137008
- **状态：** closed
- **已合并：** 是
- **作者：** srhppr
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了PodCertificateRequest对象中OwnerReference的apiVersion错误，从“core/v1”更正为“v1”。此bug导致垃圾收集器无法清理已删除Pod关联的PodCertificateRequest对象。修复包含代码和测试更新。

### PR #137019: add show-secret flag to the diff command
- **链接：** https://github.com/kubernetes/kubernetes/pull/137019
- **状态：** closed
- **已合并：** 是
- **作者：** olamilekan000
- **标签：** area/kubectl, lgtm, release-note, size/L, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  为kubectl diff命令新增了--show-secret标志。这是一个CLI特性，允许用户在diff输出中查看Secret对象的内容，提升了调试和审查的便利性。

### PR #137063: Add group, version, resource labels to alpha metric apiserver_rerouted_request_total
- **链接：** https://github.com/kubernetes/kubernetes/pull/137063
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 alpha 指标 `apiserver_rerouted_request_total` 添加了 `group`、`version`、`resource` 标签，提高了请求重定向监控的粒度和可观测性。

### PR #137065: Add more metrics for Mixed Version Proxy
- **链接：** https://github.com/kubernetes/kubernetes/pull/137065
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 Mixed Version Proxy 功能添加了更多监控指标，包括 `apiserver_request_rerouted_total` 和 `apiserver_request_rerouted_duration_seconds`，以帮助监控代理请求的行为和性能。

### PR #137084: KEP-5589: Drop temporary build-tagged ProtoMessage methods
- **链接：** https://github.com/kubernetes/kubernetes/pull/137084
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/cleanup, sig/scheduling, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, sig/architecture, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  根据 KEP-5589，移除了在 1.35 版本中临时添加的、带有构建标签的 `ProtoMessage()` 方法实现。这些方法原本是为依赖 gogo protobuf 的消费者提供的临时缓解措施，现在已不再需要。

### PR #137098: Fix container swap metrics
- **链接：** https://github.com/kubernetes/kubernetes/pull/137098
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复 kubelet 资源指标端点（/metrics/resource）中 container_swap_usage_bytes 指标始终为 0 的问题。根本原因是 CRI 不包含 swap 信息，且 `addCadvisorContainerCPUAndMemoryStats` 函数未将 cAdvisor 的 swap 数据传播到容器统计对象中。

### PR #137107: etcd: update etcd image to v3.6.8
- **链接：** https://github.com/kubernetes/kubernetes/pull/137107
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将 etcd 镜像版本更新至 v3.6.8。这是一个依赖项更新。

### PR #137157: Allow kube-apiserver to recover from an accidentally made connection to a wrong server
- **链接：** https://github.com/kubernetes/kubernetes/pull/137157
- **状态：** closed
- **已合并：** 是
- **作者：** bsalamat
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复了一个bug，允许kube-apiserver在意外连接到错误服务器后能够恢复。通过可选地强制TLS验证和改进连接管理逻辑来实现，增强了API服务器的健壮性。

### PR #137169: Revert nftables fix for nftables 1.1.3
- **链接：** https://github.com/kubernetes/kubernetes/pull/137169
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, kind/failing-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  回退了针对nftables 1.1.3的修复（#136796），因为该修复在5000节点规模的测试中导致了严重的性能问题。需要寻找替代方案。

### PR #137251: kubeadm: do not add learner member to etcd client endpoints
- **链接：** https://github.com/kubernetes/kubernetes/pull/137251
- **状态：** closed
- **已合并：** 是
- **作者：** pacoxu
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复 kubeadm 在添加 etcd learner 成员时，错误地将其客户端 URL 添加到 c.Endpoints 的问题。因为 learner 不处理客户端流量。

---
*本报告由 Containerd Release Tracker 自动生成*
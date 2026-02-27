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
- **分析时间：** 2026-02-27 00:47:42
- **分析的 PR 数量：** 43
- **分析的 Issue 数量：** 12
- **重要项目数量：** 53

## 📊 版本概述
Kubernetes v1.36.0-alpha.2 是一个为未来功能（如延迟抢占、工作负载调度）铺路的早期版本，包含多项API升级（如MutatingAdmissionPolicy GA）、关键Bug修复（如kube-proxy nftables崩溃）和持续进行的废弃清理（如FlexVolume）。

## 🔒 安全问题修复
1. ⚠️ 允许 kube-apiserver 从意外连接到错误服务器的情况中恢复 - [PR #137157](https://github.com/kubernetes/kubernetes/pull/137157) - **风险级别：** 中 - **影响：** 修复了在特定启动顺序下，Aggregated APIService 可能因连接缓存和证书验证问题而永久显示不健康的状态，提高了控制平面的健壮性。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kube-proxy 在 nftables 1.1.3+ 版本上崩溃的问题（修复尝试被回退，问题仍存在） - [PR #136796](https://github.com/kubernetes/kubernetes/pull/136796) & [PR #137169](https://github.com/kubernetes/kubernetes/pull/137169) - **影响：** 在运行新版本 nftables 的系统上，kube-proxy 会持续崩溃，导致服务网络故障。**这是一个未解决的严重问题。**
2. 修复 `PopulateRefs` 函数中的数据竞争 - [PR #136802](https://github.com/kubernetes/kubernetes/pull/136802) - **影响：** 修复了在 CEL 策略评估等并发场景下可能出现的随机崩溃或数据损坏。
3. 修复 kubelet `container_swap_usage_bytes` 指标始终为 0 的问题 - [PR #137098](https://github.com/kubernetes/kubernetes/pull/137098) - **影响：** 容器级别的 Swap 使用量监控数据恢复，对于监控有 Swap 分区的节点至关重要。
4. 修复 `kubelet_http_requests_duration_seconds` 指标记录错误（接近零）延迟值的问题 - [PR #135749](https://github.com/kubernetes/kubernetes/pull/135749) - **影响：** 恢复了 kubelet API 请求延迟监控的准确性，对性能排查和 SLO 衡量很重要。
5. 修复 kube-proxy 在所有端点都未就绪时产生日志垃圾信息的问题 - [PR #136743](https://github.com/kubernetes/kubernetes/pull/136743) - **影响：** 减少了在服务异常期间 kube-proxy 的不必要日志输出，避免日志系统压力。
6. 修复 `kubectl logs -f` 在 Pod 启动阶段抛出错误的问题 - [PR #136411](https://github.com/kubernetes/kubernetes/pull/136411) - **影响：** 改善了用户体验，`kubectl logs -f` 现在会等待 Pod 启动，而不是立即报错。
7. 修复 `PodCertificateRequest` 中错误的 `OwnerReference` 导致垃圾回收失效的问题 - [PR #137008](https://github.com/kubernetes/kubernetes/pull/137008) - **影响：** Pod 删除后，其关联的证书请求现在能被正确清理，避免资源泄漏。
8. 修复 client-go Reflector 不支持接收 Table 格式资源的问题 - [PR #136937](https://github.com/kubernetes/kubernetes/pull/136937) - **影响：** 当 API 服务器返回 Table 格式（用于 `kubectl get`）时，Informer 将明确报错而非静默失败，避免数据不同步。
9. 修复 kubeadm 将 etcd learner 成员错误添加到客户端端点列表的问题 - [PR #137251](https://github.com/kubernetes/kubernetes/pull/137251) - **影响：** 确保 etcd 客户端不会尝试连接 learner 节点，提升 etcd 集群稳定性。

## 💥 破坏性变更
1. 🚨 在 apiserver admission 子系统中将已弃用的 `sets.String` 替换为 `sets.Set[string]` - [PR #134044](https://github.com/kubernetes/kubernetes/pull/134044) - **影响：** 直接导入并使用 `k8s.io/apiserver/pkg/admission/plugin/namespace/lifecycle` 包中 `NewLifecycle` 等函数的客户端代码需要更新类型。
2. 🚨 kubeadm 移除 FlexVolume 自动挂载支持 - [PR #136423](https://github.com/kubernetes/kubernetes/pull/136423) - **影响：** 使用 FlexVolume 的 kubeadm 集群必须按照紧急升级说明进行手动配置迁移，否则升级后功能丢失。
3. 🚨 移除临时 `ProtoMessage` 方法 - [PR #137084](https://github.com/kubernetes/kubernetes/pull/137084) - **影响：** 任何直接调用这些内部方法的第三方代码（如 Karmada）将无法编译或运行，必须移除相关依赖。
4. 🚨 Pod 证书 API 弃用 `pkixPublicKey` 和 `proofOfPossession` 字段 - [PR #136729](https://github.com/kubernetes/kubernetes/pull/136729) - **影响：** 使用 Beta Pod 证书 API 并设置了这些字段的客户端或控制器，需要迁移到新的 `stubPKCS10Request` 字段。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 调度器 PostFilter 插件接口变更，为延迟抢占做准备 - [PR #136254](https://github.com/kubernetes/kubernetes/pull/136254) - **影响：** 自定义调度器插件的开发者需要更新 PostFilter 实现以返回被抢占的 Pod 列表，否则可能导致抢占逻辑异常。
2. kubeadm 移除对 FlexVolume 的内置支持 - [PR #136423](https://github.com/kubernetes/kubernetes/pull/136423) - **影响：** 仍在使用 FlexVolume 的 kubeadm 集群，在升级前需按说明手动配置 KCM 挂载卷，否则功能将失效。
3. MutatingAdmissionPolicy 升级至 v1 (GA) - [PR #136039](https://github.com/kubernetes/kubernetes/pull/136039) - **影响：** 提供稳定的、基于 CEL 的声明式变更准入控制，可替代部分 Mutating Webhook，降低运维复杂度。
4. 组件基础指标（如 rest_client_requests_total）从 Alpha 升级至 Beta - [PR #136154](https://github.com/kubernetes/kubernetes/pull/136154) - **影响：** 这些广泛使用的指标现在拥有更强的 API 和标签稳定性保证，更适合用于生产监控。
5. Pod 证书 Beta API 引入 `stubPKCS10Request` 字段并弃用旧字段 - [PR #136729](https://github.com/kubernetes/kubernetes/pull/136729) - **影响：** 提高了与外部 CA（如 Vault）的兼容性，使用旧字段 `pkixPublicKey` 和 `proofOfPossession` 的代码需要迁移。
6. 移除临时的、带构建标签的 `ProtoMessage` 方法 - [PR #137084](https://github.com/kubernetes/kubernetes/pull/137084) - **影响：** 直接依赖这些内部方法（如 `kubernetes_protomessage_one_more_release`）的客户端库（如 Karmada）需要更新，否则可能在编译或运行时出错。
7. 在 apiserver 内部 API 组中强制要求 `optional` 或 `required` 标签 - [PR #134675](https://github.com/kubernetes/kubernetes/pull/134675) - **影响：** 确保 API 定义的清晰性，对 API 代码生成工具有影响。
8. 将 `gitRepo` 卷驱动锁定为禁用状态 - [PR #136400](https://github.com/kubernetes/kubernetes/pull/136400) - **影响：** 这是该不安全卷类型被完全移除前的又一步，使用 `gitRepo` 卷的 Pod 将无法创建。

## 🚀 性能优化
1. 为线程安全存储添加资源版本查询和书签支持 - [PR #134827](https://github.com/kubernetes/kubernetes/pull/134827) - **提升：** 为未来优化大规模集群下的 List-Watch 性能奠定了基础。
2. 引入工作负载调度周期（KEP-4671） - [PR #136618](https://github.com/kubernetes/kubernetes/pull/136618) - **提升：** 旨在改进批处理作业和复杂工作负载的调度效率和公平性。
3. 将 `HonorPVReclaimPolicy` 特性门控锁定并移除 - [PR #135335](https://github.com/kubernetes/kubernetes/pull/135335) - **提升：** 简化了代码路径，该功能已稳定并默认启用。

## 🎯 风险评估
整体风险评估：**高（对于 Alpha 版本）**。此版本包含多个重大的 API 变更、一项未解决的严重崩溃 Bug（kube-proxy nftables）以及需要立即行动的废弃项（FlexVolume）。升级时机：仅限测试和实验集群。生产环境应等待至少 Beta 甚至 Release Candidate 版本，并密切关注上述关键问题的修复进展。需要特别关注的方面包括：自定义调度插件的兼容性、FlexVolume 迁移路径、nftables 版本与 kube-proxy 的兼容性，以及所有破坏性 API 变更对内部工具和库的影响。

## 📋 升级建议
1. **这是一个 Alpha 版本，绝对不要用于生产环境。** 仅适用于早期测试和开发人员评估新功能。
2. 如果您开发自定义调度器插件，请立即评估 PR #136254 对 `PostFilter` 接口的变更，并准备更新插件代码。
3. 如果您的 kubeadm 集群仍在使用 FlexVolume，请参考 PR #136423 中的说明，在升级到未来 1.36 稳定版前完成迁移或手动配置。
4. 关注 kube-proxy nftables 崩溃问题（Issue #136786）。如果您的基础设施使用较新的 nftables 版本，在升级到包含最终修复的 Kubernetes 版本前，存在网络中断风险。
5. 计划将使用已弃用 `sets.String` 的代码库迁移到 `sets.Set[string]`，并检查是否有代码依赖被移除的 `ProtoMessage` 方法。
6. 考虑在测试集群中启用并试用已 GA 的 `MutatingAdmissionPolicy`，评估其替代部分 Mutating Webhook 的可能性，以降低运维负担。

## 📋 Release 包含的变更

### PR #10: Move everything out of src and reorganize scripts.
- **链接：** https://github.com/kubernetes/kubernetes/pull/10
- **状态：** closed
- **已合并：** 是
- **作者：** jbeda
- **变更说明：**
  重构代码库，将内容移出src目录并重新组织脚本。改进脚本健壮性，将e2e测试实例类型改为g1-small，并禁用了未经充分测试的`curl | bash`集群启动方式。

### PR #134044: Replace deprecated sets.String with sets.Set[string] in apiserver
- **链接：** https://github.com/kubernetes/kubernetes/pull/134044
- **状态：** closed
- **已合并：** 是
- **作者：** mcallzbl
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  清理/API变更PR，在apiserver准入控制子系统中，将已弃用的`sets.String`类型替换为推荐的泛型类型`sets.Set[string]`，涉及7个文件并导致`NewLifecycle`函数签名发生破坏性变更。

### PR #134675: Enforce either optional or required tag on apiserverinternal API group
- **链接：** https://github.com/kubernetes/kubernetes/pull/134675
- **状态：** closed
- **已合并：** 是
- **作者：** JoelSpeed
- **标签：** lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  API变更PR，在apiserverinternal API组中强制执行字段标签（optional或required），这是提升API一致性和清晰度工作的一部分。

### PR #134827: Add Resource Version query and Bookmarks to thread safe store
- **链接：** https://github.com/kubernetes/kubernetes/pull/134827
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, lgtm, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  为线程安全的存储（thread safe store）添加了Resource Version查询和Bookmarks功能。这是一个特性增强，改进了API Machinery组件的数据存储和检索能力。

### PR #134937: Daemonset controller staleness detection
- **链接：** https://github.com/kubernetes/kubernetes/pull/134937
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, area/e2e-test-framework, triage/accepted, wg/device-management
- **变更说明：**
  特性PR，为DaemonSet控制器实现了陈旧性检测功能，旨在提高控制器对过时或无效状态的识别和处理能力。

### PR #134981: kubelet: drop cpu load metrics from container metrics test
- **链接：** https://github.com/kubernetes/kubernetes/pull/134981
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  从容器指标测试中移除CPU负载（cpu load）指标的检查。这是一个测试修复，因为该指标在某些环境下不稳定，导致测试失败。

### PR #135335: [1.36] Remove feature gate HonorPVReclaimPolicy
- **链接：** https://github.com/kubernetes/kubernetes/pull/135335
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/cleanup, lgtm, sig/storage, release-note, size/M, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  在Kubernetes 1.36版本中，移除了HonorPVReclaimPolicy特性门控。这是一个清理性质的PR，作为PR #129583的后续工作，标志着该功能已稳定或不再需要。

### PR #135502: Preempt pods in prebind phase without delete calls.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135502
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  允许在PreBind阶段抢占Pod，而无需向apiserver发出删除调用。被抢占的Pod将回到退避队列而非被完全删除，修复了Issue #132332，改变了抢占行为。

### PR #135749: Fix: Incorrect duration metric recording incorrect values
- **链接：** https://github.com/kubernetes/kubernetes/pull/135749
- **状态：** closed
- **已合并：** 是
- **作者：** novahe
- **标签：** kind/bug, area/kubelet, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/instrumentation, sig/architecture, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复持续时间指标记录错误值的问题。这是一个Bug修复，确保kubelet和调度器相关的耗时指标能准确反映实际操作时间。

### PR #135808: SeparateCacheWatchRPC LockToDefault set true
- **链接：** https://github.com/kubernetes/kubernetes/pull/135808
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  清理PR，将已弃用的SeparateCacheWatchRPC特性门锁定为其默认值（false），禁止覆盖。这是移除该特性门的前置步骤，未来版本将完全移除。

### PR #135965: set KEP-5440 to enabled by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/135965
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  特性PR，将KEP-5440设置为默认启用，并添加了两个e2e测试。

### PR #136039: Promote MutatingAdmissionPolicy to v1 (GA)
- **链接：** https://github.com/kubernetes/kubernetes/pull/136039
- **状态：** closed
- **已合并：** 是
- **作者：** lalitc375
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, sig/architecture, area/conformance, area/code-generation, needs-priority, api-review, needs-triage, sig/etcd
- **变更说明：**
  将 MutatingAdmissionPolicy 功能提升至正式发布 (GA) 状态，API 版本升级为 admissionregistration.k8s.io/v1。该功能提供基于 CEL 的声明式可变准入控制，是 Mutating Admission Webhook 的替代方案，降低了运维开销。

### PR #136154: Promote component-base metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136154
- **状态：** closed
- **已合并：** 是
- **作者：** bhope
- **标签：** area/test, sig/network, area/kubelet, sig/scalability, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, priority/important-longterm, sig/architecture, area/code-generation, sig/cloud-provider, ok-to-test, area/e2e-test-framework, area/dependency, triage/accepted, area/stable-metrics, sig/etcd, wg/device-management
- **变更说明：**
  将一组广泛使用的 component-base metrics 从 Alpha 提升至 Beta 稳定性。涉及指标包括 kubernetes_build_info、rest_client_requests_total、rest_client_request_duration_seconds 和 running_managed_controllers。此举为这些被仪表盘和工具依赖的指标提供了更强的 API 和标签稳定性保证。

### PR #136254: Extend PostFilterResult with a list of victim Pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/136254
- **状态：** closed
- **已合并：** 是
- **作者：** tosi3k
- **标签：** sig/scheduling, lgtm, size/L, kind/feature, release-note-action-required, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  扩展PostFilterResult结构体，新增被抢占Pod（victim Pods）列表字段。这是实现延迟抢占机制的第一步，为将抢占决策与执行解耦做准备。

### PR #136400: KEP:5040 Lock gitRepo Volume Driver to disabled.
- **链接：** https://github.com/kubernetes/kubernetes/pull/136400
- **状态：** closed
- **已合并：** 是
- **作者：** vinayakankugoyal
- **标签：** lgtm, sig/storage, release-note, size/S, approved, cncf-cla: yes, needs-priority, kind/deprecation, needs-triage
- **变更说明：**
  根据KEP-5040，将gitRepo卷驱动锁定为禁用状态。这是一个弃用相关的变更，正式禁止使用gitRepo卷类型。

### PR #136411: fix cli throwing an error when trying to tail the logs for a Pod
- **链接：** https://github.com/kubernetes/kubernetes/pull/136411
- **状态：** closed
- **已合并：** 是
- **作者：** olamilekan000
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  修复了 kubectl 在 Windows 系统上使用 `kubectl logs -f` 追踪 Pod 日志时抛出错误的问题。问题源于路径处理逻辑在跨平台环境下的不一致性，现已修正以确保命令在所有操作系统上正常工作。

### PR #136423: kubeadm: removed the built-in flex volume support
- **链接：** https://github.com/kubernetes/kubernetes/pull/136423
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/backlog, kind/cleanup, lgtm, sig/cluster-lifecycle, size/S, release-note-action-required, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  从 kubeadm 中移除了内置的 flex volume 支持。这是一项清理工作，因为 flex volume 驱动已被 CSI 驱动取代且自 Kubernetes 1.23 起已弃用。用户需确保节点已通过其他方式安装所需的 flex volume 驱动。

### PR #136618: KEP-4671: Introduce Workload Scheduling Cycle
- **链接：** https://github.com/kubernetes/kubernetes/pull/136618
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, area/workload-aware
- **变更说明：**
  实现KEP-4671，引入Workload Scheduling Cycle。这是一个大型特性，旨在为工作负载调度（包括延迟抢占）提供新的调度周期框架，涉及sig/scheduling。

### PR #136689: Fix kubectl plugin list overshadow detection on Windows
- **链接：** https://github.com/kubernetes/kubernetes/pull/136689
- **状态：** closed
- **已合并：** 是
- **作者：** kfess
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 `kubectl plugin list` 在 Windows 系统上检测插件覆盖（overshadow）功能失效的问题。问题源于代码使用 `/` 分割路径，未处理 Windows 的 `\` 路径分隔符，现已修正。

### PR #136716: Split from concurrent-node-syncs a separate flag for node status updates
- **链接：** https://github.com/kubernetes/kubernetes/pull/136716
- **状态：** closed
- **已合并：** 是
- **作者：** yonizxz
- **标签：** lgtm, area/cloudprovider, release-note, size/M, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  API变更/特性PR，从`concurrent-node-syncs`标志中分离出一个独立的标志，专门用于控制节点状态更新的并发度，以提供更精细的配置。

### PR #136729: Pod Certificates: Add StubPKCS10Request; migrate in-tree usages
- **链接：** https://github.com/kubernetes/kubernetes/pull/136729
- **状态：** closed
- **已合并：** 是
- **作者：** ahmedtd
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage
- **变更说明：**
  API变更/特性PR，在Pod Certificates（beta）API中添加`spec.stubPKCS10Request`字段，以提升与现有CA软件（如Vault）的兼容性，并弃用`pkixPublicKey`和`proofOfPossession`字段。

### PR #136734: Fix missing GetSharedDeviceIDs bug in GatherAllocatedState
- **链接：** https://github.com/kubernetes/kubernetes/pull/136734
- **状态：** closed
- **已合并：** 是
- **作者：** sunya-ch
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复在启用DRA（动态资源分配）ConsumableCapacity特性时，`pkg/scheduler/framework/plugins/noderesources`单元测试中发现的bug，具体涉及`GatherAllocatedState`函数中缺失`GetSharedDeviceIDs`调用。

### PR #136743: fix(kube-proxy): skip topology hints logging when no ready endpoints exist
- **链接：** https://github.com/kubernetes/kubernetes/pull/136743
- **状态：** closed
- **已合并：** 是
- **作者：** ansilh
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复kube-proxy在所有端点都未就绪（ready=false）时，错误地记录“忽略相同区域拓扑提示...”误导性日志的问题。修复方法是在没有就绪端点时提前返回，并添加了相应的测试用例。

### PR #136793: KEP-5073:  Declarative Validation Lifecycle Update
- **链接：** https://github.com/kubernetes/kubernetes/pull/136793
- **状态：** closed
- **已合并：** 是
- **作者：** yongruilin
- **标签：** sig/scheduling, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, needs-priority, needs-triage
- **变更说明：**
  实现KEP-5073，更新声明式验证（Declarative Validation）的生命周期。这是一个大型的API变更和特性引入，涉及代码生成和验证逻辑的更新。

### PR #136796: Fix kube-proxy nftables crash with newer nftables versions
- **链接：** https://github.com/kubernetes/kubernetes/pull/136796
- **状态：** closed
- **已合并：** 是
- **作者：** kairosci
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, sig/api-machinery, release-note, size/S, sig/auth, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  修复了 kube-proxy 在 nftables 1.1.3+ 版本系统上因 segmentation fault 而崩溃的问题。该修复使 kube-proxy 的 nftables 模式能够兼容新旧版本的 nftables，无需依赖 nftables 本身的补丁。

### PR #136802: Fix data race in PopulateRefs by copying Items and AdditionalProperties
- **链接：** https://github.com/kubernetes/kubernetes/pull/136802
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, area/test, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复了 apiserver 的 CEL OpenAPI resolver 中 `PopulateRefs` 函数的数据竞争问题。根本原因是浅拷贝导致对 `Items.Schema` 和 `AdditionalProperties.Schema` 的修改在多 goroutine 并发访问时产生竞争。修复方案是进行深拷贝。

### PR #136816: k8s.io/cloud-provider: Adds missing TLS flags to webhook serving options
- **链接：** https://github.com/kubernetes/kubernetes/pull/136816
- **状态：** closed
- **已合并：** 是
- **作者：** damdo
- **标签：** lgtm, area/cloudprovider, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  为 k8s.io/cloud-provider 中的 webhook 服务端选项添加了缺失的 TLS 配置标志，包括 --webhook-tls-cipher-suites、--webhook-tls-min-version 等。这使得运维人员可以独立于主服务端点，单独为 webhook 配置 TLS 安全策略。

### PR #136846: kubelet: defer the configurations flags (and the related fallback behavior) deprecation removal timeline from 1.36 to 1.37 to align with containerd v1.7 support
- **链接：** https://github.com/kubernetes/kubernetes/pull/136846
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  将kubelet配置标志（及相关回退行为）的弃用移除时间线从1.36版本推迟到1.37版本，以便与containerd v1.7的支持时间保持一致。

### PR #136892: Update/kubectl in kustomize to v5.8.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/136892
- **状态：** closed
- **已合并：** 是
- **作者：** koba1t
- **标签：** priority/important-soon, kind/cleanup, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, sig/architecture, needs-priority, area/dependency, needs-triage
- **变更说明：**
  更新kustomize中集成的kubectl版本至v5.8.1。这是一个依赖项更新和清理工作，确保使用最新的kubectl库。

### PR #136898: kubeadm:  bump the version in the ContainerRuntimeVersionCheck warning message from 1.36 to 1.37
- **链接：** https://github.com/kubernetes/kubernetes/pull/136898
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** lgtm, sig/cluster-lifecycle, release-note, size/XS, kind/feature, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将kubeadm中ContainerRuntimeVersionCheck警告信息的版本号从1.36更新至1.37。这是一个微小的更新，确保警告信息与目标发布版本一致。

### PR #136937: client-go/reflector: reject Table format resources in List and Watch paths
- **链接：** https://github.com/kubernetes/kubernetes/pull/136937
- **状态：** closed
- **已合并：** 是
- **作者：** p0lyn0mial
- **标签：** kind/bug, area/test, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复了 client-go reflector 在处理 Table 格式资源时的兼容性问题。现在，reflector 在 List 和 Watch 路径中会明确拒绝 Table 格式的资源响应，防止因格式不匹配导致的反序列化错误或意外行为。

### PR #136952: Add kubelet_metrics_provider metric
- **链接：** https://github.com/kubernetes/kubernetes/pull/136952
- **状态：** closed
- **已合并：** 是
- **作者：** dgrisonnet
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/M, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  为 kubelet 添加了一个名为 `kubelet_metrics_provider` 的新指标，用于监控 kubelet 指标提供者（如 cAdvisor、Pod 和节点资源指标）的健康状态与性能，增强了对 kubelet 指标采集系统的可观测性。

### PR #136982: Bump images and versions to go 1.25.7 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/136982
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, release-note, size/S, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  特性PR，将构建镜像和版本升级至Go 1.25.7，并使用distroless iptables基础镜像。

### PR #137008: [KEP 4317] Fix incorrect APIVersion in PodCertificateRequest OwnerReference
- **链接：** https://github.com/kubernetes/kubernetes/pull/137008
- **状态：** closed
- **已合并：** 是
- **作者：** srhppr
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复PodCertificateRequest对象中OwnerReference的apiVersion错误，从“core/v1”改为“v1”。此bug导致垃圾收集器无法清理已删除Pod关联的PodCertificateRequest。修复包含代码和测试更新。

### PR #137019: add show-secret flag to the diff command
- **链接：** https://github.com/kubernetes/kubernetes/pull/137019
- **状态：** closed
- **已合并：** 是
- **作者：** olamilekan000
- **标签：** area/kubectl, lgtm, release-note, size/L, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  为kubectl diff命令新增--show-secret标志。这是一个新特性，允许用户在diff输出中查看Secret资源的内容，便于调试和比较。

### PR #137063: Add group, version, resource labels to alpha metric apiserver_rerouted_request_total
- **链接：** https://github.com/kubernetes/kubernetes/pull/137063
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 alpha 阶段的指标 `apiserver_rerouted_request_total` 添加了 group、version、resource 标签。这些额外的维度信息能帮助更精确地追踪和分析被 API 服务器重定向的请求。

### PR #137065: Add more metrics for Mixed Version Proxy
- **链接：** https://github.com/kubernetes/kubernetes/pull/137065
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 API 服务器的 Mixed Version Proxy 功能添加了更多监控指标，以增强对集群中不同 API 版本间请求代理行为的可观测性，便于运维人员诊断和监控代理流量。

### PR #137084: KEP-5589: Drop temporary build-tagged ProtoMessage methods
- **链接：** https://github.com/kubernetes/kubernetes/pull/137084
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/cleanup, sig/scheduling, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, sig/architecture, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  根据 KEP-5589，移除了在 Kubernetes REST API 类型上临时添加的、带有构建标签的 `ProtoMessage()` 方法。这是一项清理工作，旨在消除对误导性/不正确标记方法的依赖，促进客户端库正确迁移。

### PR #137098: Fix container swap metrics
- **链接：** https://github.com/kubernetes/kubernetes/pull/137098
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复kubelet资源指标端点（/metrics/resource）中container_swap_usage_bytes始终为0的bug。原因是CRI不提供swap信息，且pkg/kubelet/stats/cri_stats_provider.go中的`addCadvisorContainerCPUAndMemoryStats`函数缺少从cAdvisor传播swap统计数据的逻辑。

### PR #137107: etcd: update etcd image to v3.6.8
- **链接：** https://github.com/kubernetes/kubernetes/pull/137107
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  清理/依赖更新PR，将etcd镜像升级到v3.6.8版本，以获取最新的修复和更新。

### PR #137157: Allow kube-apiserver to recover from an accidentally made connection to a wrong server
- **链接：** https://github.com/kubernetes/kubernetes/pull/137157
- **状态：** closed
- **已合并：** 是
- **作者：** bsalamat
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复kube-apiserver在意外连接到错误服务器后无法恢复的问题。通过可选地强制TLS验证和更优雅地处理连接错误，提高了API服务器的健壮性。

### PR #137169: Revert nftables fix for nftables 1.1.3
- **链接：** https://github.com/kubernetes/kubernetes/pull/137169
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, kind/failing-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  还原PR #136796中对nftables的修复。因为该修复在5000节点规模的测试中导致严重性能问题，使nft.List()操作基本失效，需要寻找其他解决方案。

### PR #137251: kubeadm: do not add learner member to etcd client endpoints
- **链接：** https://github.com/kubernetes/kubernetes/pull/137251
- **状态：** closed
- **已合并：** 是
- **作者：** pacoxu
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复kubeadm在添加etcd learner成员时，错误地将其客户端URL添加到c.Endpoints中的bug。因为learner成员不处理客户端流量，应被跳过。

---
*本报告由 Containerd Release Tracker 自动生成*
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
- **分析时间：** 2026-02-27 00:47:21
- **分析的 PR 数量：** 43
- **分析的 Issue 数量：** 12
- **重要项目数量：** 53

## 📊 版本概述
Kubernetes v1.36.0-alpha.2 是一个早期开发版本，核心价值在于推进多项API向稳定版演进（如MutatingAdmissionPolicy GA），并为未来的调度功能（如延迟抢占）奠定基础，同时包含多项重要的bug修复和一项关键的安全修复。

## 🔒 安全问题修复
1. ⚠️ 修复 APIService 因连接到错误端点且不验证证书而持续处于不健康状态的问题 - [PR #137157](https://github.com/kubernetes/kubernetes/pull/137157) - **风险级别：** 中 - 可能导致聚合 API 服务不可用，影响依赖该服务的功能。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kube-proxy 在 nftables 1.1.3+ 版本上因段错误而崩溃的问题 - [PR #136796](https://github.com/kubernetes/kubernetes/pull/136796) - **影响：** 使用 nftables 模式且系统版本较新的集群中，kube-proxy 会持续崩溃，导致网络功能中断。
2. 修复 `kubectl logs -f` 在 Pod 启动阶段抛出错误的问题 - [PR #136411](https://github.com/kubernetes/kubernetes/pull/136411) - **影响：** 用户体验下降，无法在 Pod 启动时自动跟踪日志。
3. 修复 kube-proxy 在所有端点都未就绪时产生误导性日志刷屏的问题 - [PR #136743](https://github.com/kubernetes/kubernetes/pull/136743) - **影响：** 日志系统可能因大量无用日志而承受压力。
4. 修复 `container_swap_usage_bytes` 容器交换内存指标始终为 0 的问题 - [PR #137098](https://github.com/kubernetes/kubernetes/pull/137098) - **影响：** 监控系统无法正确采集容器级别的交换内存使用量。
5. 修复 `kubelet_http_requests_duration_seconds` 指标记录值不准确的问题 - [PR #135749](https://github.com/kubernetes/kubernetes/pull/135749) - **影响：** 基于此指标的 Kubelet API 延迟监控和告警失效。
6. 修复 PodCertificateRequest 的 OwnerReference 中错误的 apiVersion 导致垃圾回收失效的问题 - [PR #137008](https://github.com/kubernetes/kubernetes/pull/137008) - **影响：** Pod 删除后，关联的 PodCertificateRequest 资源无法被自动清理，造成资源泄漏。
7. 修复 client-go Reflector 无法处理 Table 格式资源的问题 - [PR #136937](https://github.com/kubernetes/kubernetes/pull/136937) - **影响：** 依赖特定格式 API 的客户端可能无法正确同步资源。

## 💥 破坏性变更
1. 🚨 kubeadm 完全移除对 FlexVolume 的集成支持 - [PR #136423](https://github.com/kubernetes/kubernetes/pull/136423) - **影响：** 自 1.22 版本已废弃。仍在使用的用户必须在升级前，为 kube-controller-manager 创建包含 `--flex-volume-plugin-dir` 标志和对应目录挂载的自定义静态 Pod 配置。
2. 🚨 API 服务器 admission 子系统中将已废弃的 `sets.String` 类型替换为 `sets.Set[string]` - [PR #134044](https://github.com/kubernetes/kubernetes/pull/134044) - **影响：** 直接导入并使用 `k8s.io/apiserver/pkg/admission` 包中相关导出 API（如 `NewLifecycle`）的第三方代码需要更新类型引用。
3. 🚨 Pod 证书 Beta API 废弃 `pkixPublicKey` 和 `proofOfPossession` 字段，改用 `stubPKCS10Request` - [PR #136729](https://github.com/kubernetes/kubernetes/pull/136729) - **影响：** 使用 Pod 证书 Beta 功能的用户和签名器实现需要迁移到新的字段。
4. 🚨 移除临时构建标签保护的 `ProtoMessage()` 方法 - [PR #137084](https://github.com/kubernetes/kubernetes/pull/137084) - **影响：** 极少数依赖此错误标记方法的第三方库（如 Karmada）需要更新其代码，不再假设 API 类型实现 `ProtoMessage`。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 调度器 PostFilter 插件接口变更，为延迟抢占机制做准备 - [PR #136254](https://github.com/kubernetes/kubernetes/pull/136254)
2. MutatingAdmissionPolicy 功能正式进入 GA (v1) 稳定阶段 - [PR #136039](https://github.com/kubernetes/kubernetes/pull/136039)
3. Pod 证书 (Pod Certificates) Beta API 变更，引入 `stubPKCS10Request` 字段以提升与外部 CA 的兼容性 - [PR #136729](https://github.com/kubernetes/kubernetes/pull/136729)
4. 一组核心组件基础指标从 Alpha 提升至 Beta 稳定性级别 - [PR #136154](https://github.com/kubernetes/kubernetes/pull/136154)
5. kubeadm 移除对 FlexVolume 的内置支持，用户需自行配置 - [PR #136423](https://github.com/kubernetes/kubernetes/pull/136423)
6. 修复 kube-apiserver 错误连接到错误端点后无法恢复的问题 - [PR #137157](https://github.com/kubernetes/kubernetes/pull/137157)

## 🚀 性能优化
1. 调度器 PostFilter 结果扩展，为解耦抢占决策与执行（延迟抢占）铺平道路 - [PR #136254](https://github.com/kubernetes/kubernetes/pull/136254) - **提升：** 为未来实现更优的 workload 调度和减少不必要的 Pod 驱逐提供架构支持。
2. 减少 kube-proxy 在特定场景下的冗余日志输出 - [PR #136743](https://github.com/kubernetes/kubernetes/pull/136743) - **提升：** 降低日志系统的 I/O 和存储压力。

## 🎯 风险评估
整体风险评估：高（因为是 Alpha 版本）。此版本包含大量 API 变更、破坏性变更和实验性功能，稳定性无法保证。建议的升级时机：仅限开发、测试和概念验证环境。需要特别关注的方面：1) 调度器插件兼容性；2) 使用 FlexVolume 的 kubeadm 集群的迁移准备；3) 依赖已变更 API 的内部组件或库的编译错误。

## 📋 升级建议
1. **此版本为 Alpha 预览版，绝对禁止用于生产环境。** 仅适用于测试和早期评估。
2. 如果开发自定义调度器插件，请评估 PR #136254 对 PostFilter 插件接口的变更，并提前适配。
3. 如果集群仍在使用 FlexVolume，请参考 PR #136423 的描述，在升级到未来包含此变更的稳定版（如 1.36）前，完成 kube-controller-manager 的配置迁移。
4. 关注 MutatingAdmissionPolicy (GA) 和 Pod Certificates (Beta) 的 API 变化，评估在 CI 环境中测试这些新稳定功能的价值。
5. 检查内部工具或控制器是否直接引用了 `k8s.io/apiserver/pkg/admission` 包中涉及 `sets.String` 的 API，并计划更新。
6. 在测试集群中验证 nftables (PR #136796) 和 kube-proxy 日志 (PR #136743) 相关的修复效果。

## 📋 Release 包含的变更

### PR #10: Move everything out of src and reorganize scripts.
- **链接：** https://github.com/kubernetes/kubernetes/pull/10
- **状态：** closed
- **已合并：** 是
- **作者：** jbeda
- **变更说明：**
  早期PR，重构项目结构，将内容移出src目录并重组脚本。优化脚本健壮性，将e2e测试实例类型改为g1-small，并更新文档。

### PR #134044: Replace deprecated sets.String with sets.Set[string] in apiserver
- **链接：** https://github.com/kubernetes/kubernetes/pull/134044
- **状态：** closed
- **已合并：** 是
- **作者：** mcallzbl
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  清理性PR，在apiserver准入控制子系统中，将已弃用的`sets.String`类型替换为推荐的泛型类型`sets.Set[string]`，涉及API破坏性变更。

### PR #134675: Enforce either optional or required tag on apiserverinternal API group
- **链接：** https://github.com/kubernetes/kubernetes/pull/134675
- **状态：** closed
- **已合并：** 是
- **作者：** JoelSpeed
- **标签：** lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  API变更PR，在apiserverinternal API组中强制要求字段必须标记为`optional`或`required`，以加强API验证和一致性。

### PR #134827: Add Resource Version query and Bookmarks to thread safe store
- **链接：** https://github.com/kubernetes/kubernetes/pull/134827
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, lgtm, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  为线程安全存储（thread safe store）添加了Resource Version查询和Bookmarks支持。这是一个API机制的特性增强，提升了存储组件的查询能力。

### PR #134937: Daemonset controller staleness detection
- **链接：** https://github.com/kubernetes/kubernetes/pull/134937
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, area/e2e-test-framework, triage/accepted, wg/device-management
- **变更说明：**
  功能PR，为DaemonSet控制器引入陈旧性检测机制，旨在提高调度效率，属于大规模变更（size/XL）。

### PR #134981: kubelet: drop cpu load metrics from container metrics test
- **链接：** https://github.com/kubernetes/kubernetes/pull/134981
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  从容器指标测试中移除CPU负载指标。这是一个针对测试的bug修复，解决了因CPU负载指标不稳定导致的测试失败问题。

### PR #135335: [1.36] Remove feature gate HonorPVReclaimPolicy
- **链接：** https://github.com/kubernetes/kubernetes/pull/135335
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/cleanup, lgtm, sig/storage, release-note, size/M, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  在Kubernetes 1.36版本中，作为清理工作的一部分，移除了`HonorPVReclaimPolicy`特性门控。这是PR #129583的后续操作，表明该功能已稳定或不再需要门控保护。

### PR #135502: Preempt pods in prebind phase without delete calls.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135502
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  允许在PreBind阶段抢占Pod，而无需向apiserver发出删除调用。被抢占的Pod将被放回调度队列而非完全删除，行为略有变化，解决了issue #132332。

### PR #135749: Fix: Incorrect duration metric recording incorrect values
- **链接：** https://github.com/kubernetes/kubernetes/pull/135749
- **状态：** closed
- **已合并：** 是
- **作者：** novahe
- **标签：** kind/bug, area/kubelet, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/instrumentation, sig/architecture, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了持续时间指标记录错误值的问题。该bug影响kubelet和调度器相关的指标，修复确保了监控数据的准确性。

### PR #135808: SeparateCacheWatchRPC LockToDefault set true
- **链接：** https://github.com/kubernetes/kubernetes/pull/135808
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  清理性PR，将已弃用的SeparateCacheWatchRPC特性门锁定为其默认值（false），禁止用户覆盖。该特性门将在未来版本中移除。

### PR #135965: set KEP-5440 to enabled by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/135965
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  功能PR，将KEP-5440对应的功能默认启用，并增加了两个端到端（e2e）测试用例。

### PR #136039: Promote MutatingAdmissionPolicy to v1 (GA)
- **链接：** https://github.com/kubernetes/kubernetes/pull/136039
- **状态：** closed
- **已合并：** 是
- **作者：** lalitc375
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, sig/architecture, area/conformance, area/code-generation, needs-priority, api-review, needs-triage, sig/etcd
- **变更说明：**
  将 `MutatingAdmissionPolicy` 特性提升至正式发布（GA/v1）。该特性提供了一种基于 CEL 的声明式替代方案，用于执行常见的资源变更操作（如设置标签、注入 sidecar），而无需运维 mutating admission webhook。

### PR #136154: Promote component-base metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136154
- **状态：** closed
- **已合并：** 是
- **作者：** bhope
- **标签：** area/test, sig/network, area/kubelet, sig/scalability, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, priority/important-longterm, sig/architecture, area/code-generation, sig/cloud-provider, ok-to-test, area/e2e-test-framework, area/dependency, triage/accepted, area/stable-metrics, sig/etcd, wg/device-management
- **变更说明：**
  将四个广泛使用的 component-base 指标从 Alpha 提升至 Beta 稳定性，包括 `kubernetes_build_info`、`rest_client_requests_total`、`rest_client_request_duration_seconds` 和 `running_managed_controllers`。此举为这些生产环境中长期依赖的指标提供了更强的 API 和标签稳定性保证。

### PR #136254: Extend PostFilterResult with a list of victim Pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/136254
- **状态：** closed
- **已合并：** 是
- **作者：** tosi3k
- **标签：** sig/scheduling, lgtm, size/L, kind/feature, release-note-action-required, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  扩展`PostFilterResult`结构，新增包含被抢占Pod列表的字段。这是为实现延迟抢占机制（KEP）做准备的第一步，旨在将抢占决策的计算与执行解耦。

### PR #136400: KEP:5040 Lock gitRepo Volume Driver to disabled.
- **链接：** https://github.com/kubernetes/kubernetes/pull/136400
- **状态：** closed
- **已合并：** 是
- **作者：** vinayakankugoyal
- **标签：** lgtm, sig/storage, release-note, size/S, approved, cncf-cla: yes, needs-priority, kind/deprecation, needs-triage
- **变更说明：**
  根据KEP-5040，将`gitRepo`卷驱动程序锁定为禁用状态。这是一个废弃（deprecation）步骤，标志着该旧卷类型将被逐步淘汰。

### PR #136411: fix cli throwing an error when trying to tail the logs for a Pod
- **链接：** https://github.com/kubernetes/kubernetes/pull/136411
- **状态：** closed
- **已合并：** 是
- **作者：** olamilekan000
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  修复了 `kubectl logs` 命令在 Windows 平台上因路径分隔符处理不当而无法追踪 Pod 日志的错误。问题源于使用 `strings.Split(path, "/")` 未识别 Windows 的反斜杠 `\` 分隔符，导致命令执行失败。

### PR #136423: kubeadm: removed the built-in flex volume support
- **链接：** https://github.com/kubernetes/kubernetes/pull/136423
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/backlog, kind/cleanup, lgtm, sig/cluster-lifecycle, size/S, release-note-action-required, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  从 kubeadm 中移除了内置的 flex volume 支持。这是对已弃用功能的清理，用户应使用 CSI（Container Storage Interface）驱动作为替代方案。此变更需要用户注意并采取相应行动。

### PR #136618: KEP-4671: Introduce Workload Scheduling Cycle
- **链接：** https://github.com/kubernetes/kubernetes/pull/136618
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, area/workload-aware
- **变更说明：**
  引入KEP-4671：工作负载调度周期。这是一个大型特性，旨在改进调度器的工作负载感知能力，属于scheduling SIG的工作范围。

### PR #136689: Fix kubectl plugin list overshadow detection on Windows
- **链接：** https://github.com/kubernetes/kubernetes/pull/136689
- **状态：** closed
- **已合并：** 是
- **作者：** kfess
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 `kubectl plugin list` 在 Windows 系统上检测插件被遮蔽（overshadow）功能失效的问题。原代码使用 `strings.Split(path, "/")` 无法正确解析 Windows 路径分隔符 `\`，现已修正。

### PR #136716: Split from concurrent-node-syncs a separate flag for node status updates
- **链接：** https://github.com/kubernetes/kubernetes/pull/136716
- **状态：** closed
- **已合并：** 是
- **作者：** yonizxz
- **标签：** lgtm, area/cloudprovider, release-note, size/M, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  API变更/功能PR，从`--concurrent-node-syncs`标志中分离出一个独立的标志（`--concurrent-node-status-updates`），用于控制节点状态更新的并发度，以提供更精细的配置。

### PR #136729: Pod Certificates: Add StubPKCS10Request; migrate in-tree usages
- **链接：** https://github.com/kubernetes/kubernetes/pull/136729
- **状态：** closed
- **已合并：** 是
- **作者：** ahmedtd
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage
- **变更说明：**
  API变更/功能PR，在Pod Certificates（beta）API的`spec`中新增`stubPKCS10Request`字段，以提升与现有CA软件（如Vault）的兼容性，并弃用`pkixPublicKey`和`proofOfPossession`字段。

### PR #136734: Fix missing GetSharedDeviceIDs bug in GatherAllocatedState
- **链接：** https://github.com/kubernetes/kubernetes/pull/136734
- **状态：** closed
- **已合并：** 是
- **作者：** sunya-ch
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  Bug修复PR，修复了在启用`DRAConsumableCapacity`功能时，`pkg/scheduler/framework/plugins/noderesources`单元测试中发现的`GetSharedDeviceIDs`缺失问题。

### PR #136743: fix(kube-proxy): skip topology hints logging when no ready endpoints exist
- **链接：** https://github.com/kubernetes/kubernetes/pull/136743
- **状态：** closed
- **已合并：** 是
- **作者：** ansilh
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  Bug修复PR，修复kube-proxy在所有Service端点均为非就绪状态时，错误地记录关于拓扑提示的误导性日志信息的问题，通过添加检查避免日志刷屏。

### PR #136793: KEP-5073:  Declarative Validation Lifecycle Update
- **链接：** https://github.com/kubernetes/kubernetes/pull/136793
- **状态：** closed
- **已合并：** 是
- **作者：** yongruilin
- **标签：** sig/scheduling, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, needs-priority, needs-triage
- **变更说明：**
  实施KEP-5073：声明式验证生命周期更新。这是一个涉及API变更和代码生成的重大特性，旨在更新验证规则的生命周期管理。

### PR #136796: Fix kube-proxy nftables crash with newer nftables versions
- **链接：** https://github.com/kubernetes/kubernetes/pull/136796
- **状态：** closed
- **已合并：** 是
- **作者：** kairosci
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, sig/api-machinery, release-note, size/S, sig/auth, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  修复了 kube-proxy 在 nftables 1.1.3+ 版本上因列出支持 udata 的 nftables sets 时发生 segmentation fault 而崩溃的问题。该修复使 kube-proxy 的 nftables 模式能兼容不同版本的 nftables，无需对 nftables 本身打补丁。

### PR #136802: Fix data race in PopulateRefs by copying Items and AdditionalProperties
- **链接：** https://github.com/kubernetes/kubernetes/pull/136802
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, area/test, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复了 `PopulateRefs` 函数中的数据竞争问题。该函数对输入 schema 进行浅拷贝后，直接修改了指针字段 `Items.Schema` 和 `AdditionalProperties.Schema`，而这些指针仍指向原始共享数据结构，导致多 goroutine 并发调用时发生数据竞争。

### PR #136816: k8s.io/cloud-provider: Adds missing TLS flags to webhook serving options
- **链接：** https://github.com/kubernetes/kubernetes/pull/136816
- **状态：** closed
- **已合并：** 是
- **作者：** damdo
- **标签：** lgtm, area/cloudprovider, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  为 k8s.io/cloud-provider 中的 webhook 服务选项添加了缺失的 TLS 配置标志，包括 `--webhook-disable-http2-serving`、`--webhook-tls-cipher-suites`、`--webhook-tls-min-version` 和 `--webhook-tls-sni-cert-key`。这使得运维人员可以独立于主服务端点，完整配置 webhook 端点的 TLS。

### PR #136846: kubelet: defer the configurations flags (and the related fallback behavior) deprecation removal timeline from 1.36 to 1.37 to align with containerd v1.7 support
- **链接：** https://github.com/kubernetes/kubernetes/pull/136846
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  功能PR，将kubelet配置标志（及相关回退行为）的弃用移除时间线从1.36版本推迟到1.37版本，以便与containerd v1.7的支持时间对齐。

### PR #136892: Update/kubectl in kustomize to v5.8.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/136892
- **状态：** closed
- **已合并：** 是
- **作者：** koba1t
- **标签：** priority/important-soon, kind/cleanup, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, sig/architecture, needs-priority, area/dependency, needs-triage
- **变更说明：**
  将kustomize中集成的kubectl版本更新至v5.8.1。这是一个依赖项更新，属于常规维护和清理工作。

### PR #136898: kubeadm:  bump the version in the ContainerRuntimeVersionCheck warning message from 1.36 to 1.37
- **链接：** https://github.com/kubernetes/kubernetes/pull/136898
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** lgtm, sig/cluster-lifecycle, release-note, size/XS, kind/feature, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将kubeadm中`ContainerRuntimeVersionCheck`警告信息提及的版本号从1.36更新至1.37。这是一个与版本发布周期相关的微小更新。

### PR #136937: client-go/reflector: reject Table format resources in List and Watch paths
- **链接：** https://github.com/kubernetes/kubernetes/pull/136937
- **状态：** closed
- **已合并：** 是
- **作者：** p0lyn0mial
- **标签：** kind/bug, area/test, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复了 client-go reflector 在 List/Watch 路径中错误接受 `Table` 格式资源的问题。现在 reflector 会明确拒绝 `Table` 格式，确保只处理预期的资源对象列表，防止因格式不匹配导致的问题。

### PR #136952: Add kubelet_metrics_provider metric
- **链接：** https://github.com/kubernetes/kubernetes/pull/136952
- **状态：** closed
- **已合并：** 是
- **作者：** dgrisonnet
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/M, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  新增了一个名为 `kubelet_metrics_provider` 的指标，用于监控 kubelet 中 metrics provider 的运行状态和性能，增强了节点层面的可观测性。

### PR #136982: Bump images and versions to go 1.25.7 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/136982
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, release-note, size/S, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  功能PR，将构建镜像和版本升级至Go 1.25.7，并使用distroless iptables基础镜像，属于构建系统更新。

### PR #137008: [KEP 4317] Fix incorrect APIVersion in PodCertificateRequest OwnerReference
- **链接：** https://github.com/kubernetes/kubernetes/pull/137008
- **状态：** closed
- **已合并：** 是
- **作者：** srhppr
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了`PodCertificateRequest`对象中`OwnerReference`的`apiVersion`错误，从`"core/v1"`更正为`"v1"`。此错误导致垃圾收集器无法清理已删除Pod关联的证书请求。修复包含代码更改和测试断言补充。

### PR #137019: add show-secret flag to the diff command
- **链接：** https://github.com/kubernetes/kubernetes/pull/137019
- **状态：** closed
- **已合并：** 是
- **作者：** olamilekan000
- **标签：** area/kubectl, lgtm, release-note, size/L, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  为`kubectl diff`命令新增`--show-secret`标志。该特性允许用户在diff输出中查看Secret对象的内容，提高了调试和审查的便利性。

### PR #137063: Add group, version, resource labels to alpha metric apiserver_rerouted_request_total
- **链接：** https://github.com/kubernetes/kubernetes/pull/137063
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 alpha 指标 `apiserver_rerouted_request_total` 添加了 `group`、`version`、`resource` 标签。这些额外的维度有助于更精细地追踪和分析被 API 服务器重定向的请求。

### PR #137065: Add more metrics for Mixed Version Proxy
- **链接：** https://github.com/kubernetes/kubernetes/pull/137065
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 Mixed Version Proxy 功能添加了更多监控指标，以增强对 API 服务器在处理不同版本 API 请求时的代理行为的可观测性。

### PR #137084: KEP-5589: Drop temporary build-tagged ProtoMessage methods
- **链接：** https://github.com/kubernetes/kubernetes/pull/137084
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/cleanup, sig/scheduling, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, sig/architecture, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  根据 KEP-5589，移除了临时添加的、带有构建标签的 `ProtoMessage()` 方法实现。这些方法在 1.35 版本中作为临时缓解措施引入，现已清理，REST API 类型不再实现此标记方法。

### PR #137098: Fix container swap metrics
- **链接：** https://github.com/kubernetes/kubernetes/pull/137098
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复kubelet资源指标端点中`container_swap_usage_bytes`指标始终为0的bug。根本原因是CRI不提供swap信息，且`addCadvisorContainerCPUAndMemoryStats`函数未将cAdvisor的swap数据传播到容器指标对象。

### PR #137107: etcd: update etcd image to v3.6.8
- **链接：** https://github.com/kubernetes/kubernetes/pull/137107
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  清理性PR，将etcd镜像版本更新至v3.6.8，属于常规依赖项升级。

### PR #137157: Allow kube-apiserver to recover from an accidentally made connection to a wrong server
- **链接：** https://github.com/kubernetes/kubernetes/pull/137157
- **状态：** closed
- **已合并：** 是
- **作者：** bsalamat
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复kube-apiserver在意外连接到错误服务器时无法恢复的问题。通过可选地强制执行TLS验证并在连接建立后立即关闭无效连接来实现，增强了API服务器的健壮性。

### PR #137169: Revert nftables fix for nftables 1.1.3
- **链接：** https://github.com/kubernetes/kubernetes/pull/137169
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, kind/failing-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  恢复（Revert）了针对nftables 1.1.3的修复（PR #136796）。因为原修复在5000节点规模的测试中引发了严重的性能问题，需要寻找替代方案。

### PR #137251: kubeadm: do not add learner member to etcd client endpoints
- **链接：** https://github.com/kubernetes/kubernetes/pull/137251
- **状态：** closed
- **已合并：** 是
- **作者：** pacoxu
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  Bug修复PR，修复kubeadm在添加etcd学习者（learner）成员时，错误地将其客户端URL添加到etcd客户端端点列表的问题，因为学习者不处理客户端流量。

---
*本报告由 Containerd Release Tracker 自动生成*
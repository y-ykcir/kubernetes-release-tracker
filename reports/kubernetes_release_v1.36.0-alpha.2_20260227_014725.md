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
- **分析时间：** 2026-02-27 01:47:25
- **分析的 PR 数量：** 43
- **分析的 Issue 数量：** 12
- **重要项目数量：** 53

## 📊 版本概述
Kubernetes v1.36.0-alpha.2 是一个早期测试版本，核心价值在于引入了多项重要的 API 增强（如 MutatingAdmissionPolicy GA）、调度器改进以及修复了多个关键的生产环境 Bug（如 kube-proxy nftables 崩溃）。

## 🔒 安全问题修复
1. ⚠️ 修复 APIServer 在 APIService 健康检查中可能重用错误连接且不验证服务证书的问题 - [PR #137157](https://github.com/kubernetes/kubernetes/pull/137157) - **风险级别：** 中 - **影响：** 在特定部署顺序下，可能导致 APIService 被错误地标记为不健康，或潜在的安全风险。
2. ⚠️ 为云提供商 webhook 服务器添加独立的 TLS 配置标志（如密码套件、最小版本） - [PR #136816](https://github.com/kubernetes/kubernetes/pull/136816) - **风险级别：** 低 - **影响：** 允许管理员为 webhook 端点配置更强的 TLS 安全策略，与主服务端点解耦。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kube-proxy 在 nftables 1.1.3+ 版本上因列出集合导致的崩溃问题 - [PR #136796](https://github.com/kubernetes/kubernetes/pull/136796) - **影响：** 生产环境中使用 nftables 模式的 kube-proxy 可能发生持续崩溃，导致 Service 网络故障。
2. 修复 APIServer CEL 开放 API 解析器中的数据结构竞争问题 - [PR #136802](https://github.com/kubernetes/kubernetes/pull/136802) - **影响：** 在高并发场景下可能导致基于 CEL 的准入策略出现不可预测的行为或崩溃。
3. 修复 PodCertificateRequest 中 OwnerReference 的 apiVersion 错误，解决垃圾回收失效问题 - [PR #137008](https://github.com/kubernetes/kubernetes/pull/137008) - **影响：** Pod 删除后，其关联的 PodCertificateRequest 资源会泄漏，无法被自动清理。
4. 修复 kube-proxy 在所有端点都未就绪时误报拓扑提示日志的问题，减少日志噪音 - [PR #136743](https://github.com/kubernetes/kubernetes/pull/136743) - **影响：** 存在大量未就绪 Pod 时，kube-proxy 日志可能被刷屏，影响日志系统。
5. 修复 kubelet 容器交换内存指标 (`container_swap_usage_bytes`) 始终为 0 的问题 - [PR #137098](https://github.com/kubernetes/kubernetes/pull/137098) - **影响：** 监控系统无法正确获取容器级别的 Swap 使用量，影响资源监控和告警。
6. 修复 kubectl logs -f 在 Pod 启动阶段报错的问题，改善用户体验 - [PR #136411](https://github.com/kubernetes/kubernetes/pull/136411) - **影响：** 用户无法在 Pod 启动时自动跟随日志，需反复重试。

## 💥 破坏性变更
1. 🚨 将 apiserver admission 子系统中的 `sets.String` 类型替换为 `sets.Set[string]`，涉及导出的 API - [PR #134044](https://github.com/kubernetes/kubernetes/pull/134044) - **影响：** 直接导入并使用 `k8s.io/apiserver/pkg/admission/plugin/namespace/lifecycle` 等包中相关类型的客户端代码需要更新。
2. 🚨 kubeadm 移除内置的 FlexVolume 支持目录挂载 - [PR #136423](https://github.com/kubernetes/kubernetes/pull/136423) - **影响：** 依赖此功能的集群升级到 1.36 前，必须按照 PR 描述手动配置 Controller Manager 的卷挂载和启动参数。
3. 🚨 锁定并计划移除 `SeparateCacheWatchRPC` 特性门控，其默认值固定为 false - [PR #135808](https://github.com/kubernetes/kubernetes/pull/135808) - **影响：** 显式启用此特性门控的配置将不再生效，需评估对集群的影响。
4. 🚨 移除临时的、带构建标签的 `ProtoMessage()` 方法 - [PR #137084](https://github.com/kubernetes/kubernetes/pull/137084) - **影响：** 极少数依赖此方法的外部项目（如 Karmada）需要更新其代码，否则可能在编译或运行时出错。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 调度器 PostFilter 插件接口变更，需返回被抢占的 Pod 列表，为延迟抢占机制做准备 - [PR #136254](https://github.com/kubernetes/kubernetes/pull/136254) - **影响：** 自定义调度器插件的开发者需要更新 PostFilter 方法的实现。
2. MutatingAdmissionPolicy 功能正式发布 GA (v1)，提供声明式的 CEL 变更准入控制 - [PR #136039](https://github.com/kubernetes/kubernetes/pull/136039) - **影响：** 可以使用更稳定、运维成本更低的替代方案来替代部分 Mutating Webhook。
3. Pod 证书 (Pod Certificates) Beta API 增加 PKCS#10 请求支持，提升与外部 CA 的兼容性 - [PR #136729](https://github.com/kubernetes/kubernetes/pull/136729) - **影响：** 简化了与 Vault 等现有 CA 系统的集成。
4. kubeadm 移除对 FlexVolume 的内置支持，需用户自行配置 - [PR #136423](https://github.com/kubernetes/kubernetes/pull/136423) - **影响：** 仍在使用 FlexVolume 的 kubeadm 集群在升级前必须完成迁移或按说明进行额外配置。
5. 将一组核心组件指标从 Alpha 提升至 Beta 稳定性级别 - [PR #136154](https://github.com/kubernetes/kubernetes/pull/136154) - **影响：** 提升了 `rest_client_requests_total` 等关键监控指标的 API 和标签稳定性。

## 🚀 性能优化
1. 优化抢占逻辑，对处于 PreBind 阶段的 Pod 进行抢占时不再发起删除 API 调用 - [PR #135502](https://github.com/kubernetes/kubernetes/pull/135502) - **提升：** 减少了不必要的 API 调用，降低了 APIServer 负载，并使被抢占的 Pod 能重新排队。
2. 修复 kube-proxy 在无就绪端点时记录冗余拓扑提示日志的问题，减少 I/O 开销 - [PR #136743](https://github.com/kubernetes/kubernetes/pull/136743) - **提升：** 降低了日志系统的处理压力。

## 🎯 风险评估
整体风险评估：高（因为是 Alpha 版本）。升级风险级别：高，可能存在未知的不稳定性和 Bug。建议的升级时机：仅限开发和测试环境，用于早期功能验证和问题发现。生产环境应等待至少 Beta 甚至稳定版。需要特别关注的方面：1) 调度器行为变化，2) kube-proxy 网络稳定性（尤其是 nftables 模式），3) 所有破坏性变更对现有工作负载和工具链的影响。

## 📋 升级建议
1. **对于生产环境：** 此版本为 Alpha 版本，绝对不应用于生产。但应开始评估关键变更（如调度器插件、FlexVolume 移除）对自身环境的影响。
2. **对于开发/测试集群：** 可以部署此版本以测试新功能（如 MutatingAdmissionPolicy GA）和验证关键 Bug 修复（如 kube-proxy nftables 崩溃）。
3. **行动项：** 1) 检查是否使用自定义调度器插件，并评估 PR #136254 的影响。2) 检查集群是否仍在使用 FlexVolume，并开始制定迁移计划。3) 如果使用基于 CEL 的准入策略，关注相关数据竞争修复。
4. **升级前：** 务必在测试环境中充分验证，特别是网络（kube-proxy）、调度和证书相关功能。

## 📋 Release 包含的变更

### PR #10: Move everything out of src and reorganize scripts.
- **链接：** https://github.com/kubernetes/kubernetes/pull/10
- **状态：** closed
- **已合并：** 是
- **作者：** jbeda
- **变更说明：**
  重构脚本和目录结构，将内容移出src目录，优化脚本健壮性，将e2e测试实例改为g1-small，并禁用了未经充分测试的`curl | bash`集群启动方式。

### PR #134044: Replace deprecated sets.String with sets.Set[string] in apiserver
- **链接：** https://github.com/kubernetes/kubernetes/pull/134044
- **状态：** closed
- **已合并：** 是
- **作者：** mcallzbl
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  清理性PR，在apiserver准入控制子系统中，将已弃用的`sets.String`类型替换为推荐的泛型类型`sets.Set[string]`，涉及7个文件，并导致`NewLifecycle`函数签名发生破坏性变更。

### PR #134675: Enforce either optional or required tag on apiserverinternal API group
- **链接：** https://github.com/kubernetes/kubernetes/pull/134675
- **状态：** closed
- **已合并：** 是
- **作者：** JoelSpeed
- **标签：** lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  API变更PR，强化apiserverinternal API group的验证，要求字段必须标注`optional`或`required`标签。

### PR #134827: Add Resource Version query and Bookmarks to thread safe store
- **链接：** https://github.com/kubernetes/kubernetes/pull/134827
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, lgtm, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  为线程安全的存储（thread safe store）添加了Resource Version查询和Bookmarks功能。这是一个特性增强，提升了API Machinery组件在缓存和列表操作方面的能力。

### PR #134937: Daemonset controller staleness detection
- **链接：** https://github.com/kubernetes/kubernetes/pull/134937
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, area/e2e-test-framework, triage/accepted, wg/device-management
- **变更说明：**
  功能PR，为DaemonSet控制器引入了陈旧性检测机制。

### PR #134981: kubelet: drop cpu load metrics from container metrics test
- **链接：** https://github.com/kubernetes/kubernetes/pull/134981
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  从容器指标测试中移除了CPU负载（cpu load）指标的检查。这是一个测试修复，因为该指标并非在所有环境下都稳定存在，移除后可避免测试因环境差异而失败。

### PR #135335: [1.36] Remove feature gate HonorPVReclaimPolicy
- **链接：** https://github.com/kubernetes/kubernetes/pull/135335
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/cleanup, lgtm, sig/storage, release-note, size/M, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  在Kubernetes 1.36版本中，作为清理工作的一部分，移除了已稳定的特性门控 `HonorPVReclaimPolicy`。这是对PR #129583的后续跟进，标志着该功能已默认启用且不可回退。

### PR #135502: Preempt pods in prebind phase without delete calls.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135502
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  改进了抢占逻辑，允许抢占处于PreBind阶段的Pod，而无需向apiserver发起删除调用。被抢占的Pod将通过取消其PreBind上下文并返回调度队列，而非直接从集群存储中删除，行为有所变化。

### PR #135749: Fix: Incorrect duration metric recording incorrect values
- **链接：** https://github.com/kubernetes/kubernetes/pull/135749
- **状态：** closed
- **已合并：** 是
- **作者：** novahe
- **标签：** kind/bug, area/kubelet, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/instrumentation, sig/architecture, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了kubelet中持续时间指标（如`volume_manager_volume_operation_duration_seconds`）记录错误值的问题。问题在于指标记录完成后仍被更新，现已通过确保记录后不再修改来修正。

### PR #135808: SeparateCacheWatchRPC LockToDefault set true
- **链接：** https://github.com/kubernetes/kubernetes/pull/135808
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  清理性PR，将已弃用的SeparateCacheWatchRPC功能门锁定为默认值false，禁止用户覆盖，为未来版本中移除该功能门做准备。

### PR #135965: set KEP-5440 to enabled by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/135965
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  功能PR，将KEP-5440默认设置为启用状态，并添加了两个e2e测试。

### PR #136039: Promote MutatingAdmissionPolicy to v1 (GA)
- **链接：** https://github.com/kubernetes/kubernetes/pull/136039
- **状态：** closed
- **已合并：** 是
- **作者：** lalitc375
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, sig/architecture, area/conformance, area/code-generation, needs-priority, api-review, needs-triage, sig/etcd
- **变更说明：**
  将 MutatingAdmissionPolicy 特性提升至 General Availability (v1)。该特性提供基于 CEL 的声明式准入控制，作为 mutating admission webhook 的替代。API 类型升级至 admissionregistration.k8s.io/v1，特性门控在 1.36 版本中晋升为 GA。

### PR #136154: Promote component-base metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136154
- **状态：** closed
- **已合并：** 是
- **作者：** bhope
- **标签：** area/test, sig/network, area/kubelet, sig/scalability, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, priority/important-longterm, sig/architecture, area/code-generation, sig/cloud-provider, ok-to-test, area/e2e-test-framework, area/dependency, triage/accepted, area/stable-metrics, sig/etcd, wg/device-management
- **变更说明：**
  将一组广泛使用的 component-base 指标从 Alpha 提升至 Beta 稳定性。这些指标（包括 kubernetes_build_info、rest_client_requests_total 等）已在多个版本中生产使用，提升后提供更强的 API 和标签稳定性保证。

### PR #136254: Extend PostFilterResult with a list of victim Pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/136254
- **状态：** closed
- **已合并：** 是
- **作者：** tosi3k
- **标签：** sig/scheduling, lgtm, size/L, kind/feature, release-note-action-required, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  扩展了PostFilterResult结构体，新增了被抢占Pod（victim Pods）列表字段。这是实现延迟抢占机制的第一步，旨在将抢占决策的计算与执行解耦，为KEP-5730中的Workload Scheduling做准备。

### PR #136400: KEP:5040 Lock gitRepo Volume Driver to disabled.
- **链接：** https://github.com/kubernetes/kubernetes/pull/136400
- **状态：** closed
- **已合并：** 是
- **作者：** vinayakankugoyal
- **标签：** lgtm, sig/storage, release-note, size/S, approved, cncf-cla: yes, needs-priority, kind/deprecation, needs-triage
- **变更说明：**
  根据KEP-5040，将gitRepo卷驱动锁定为禁用状态。这是一个弃用步骤，意味着该功能将不再可用，为未来完全移除该卷类型做准备。

### PR #136411: fix cli throwing an error when trying to tail the logs for a Pod
- **链接：** https://github.com/kubernetes/kubernetes/pull/136411
- **状态：** closed
- **已合并：** 是
- **作者：** olamilekan000
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  修复 kubectl logs 命令在尝试跟踪 Pod 日志时抛出错误的问题。此问题与 Windows 平台上的路径分隔符处理有关，导致插件检测失败。

### PR #136423: kubeadm: removed the built-in flex volume support
- **链接：** https://github.com/kubernetes/kubernetes/pull/136423
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/backlog, kind/cleanup, lgtm, sig/cluster-lifecycle, size/S, release-note-action-required, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  从 kubeadm 中移除内置的 flex volume 支持。这是一项清理工作，因为 flex volume 驱动已被 CSI 取代，移除后简化了 kubeadm 的代码和依赖。

### PR #136618: KEP-4671: Introduce Workload Scheduling Cycle
- **链接：** https://github.com/kubernetes/kubernetes/pull/136618
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, area/workload-aware
- **变更说明：**
  实现KEP-4671，为调度框架引入Workload Scheduling Cycle。这是一个大型功能，旨在支持工作负载感知调度，通过新的调度周期来优化Pod的调度决策。

### PR #136689: Fix kubectl plugin list overshadow detection on Windows
- **链接：** https://github.com/kubernetes/kubernetes/pull/136689
- **状态：** closed
- **已合并：** 是
- **作者：** kfess
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复 kubectl plugin list 在 Windows 系统上检测插件被覆盖（overshadow）功能失效的问题。原代码使用 `/` 分割路径，未处理 Windows 的 `\` 分隔符。

### PR #136716: Split from concurrent-node-syncs a separate flag for node status updates
- **链接：** https://github.com/kubernetes/kubernetes/pull/136716
- **状态：** closed
- **已合并：** 是
- **作者：** yonizxz
- **标签：** lgtm, area/cloudprovider, release-note, size/M, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  API变更/功能PR，旨在从`concurrent-node-syncs`标志中拆分出一个独立的标志，专门用于控制节点状态更新。

### PR #136729: Pod Certificates: Add StubPKCS10Request; migrate in-tree usages
- **链接：** https://github.com/kubernetes/kubernetes/pull/136729
- **状态：** closed
- **已合并：** 是
- **作者：** ahmedtd
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage
- **变更说明：**
  API变更/功能PR，在Pod Certificates beta API中添加`spec.stubPKCS10Request`字段，以提升与现有CA软件（如Vault）的兼容性，并弃用了`spec.pkixPublicKey`和`spec.proofOfPossession`字段。

### PR #136734: Fix missing GetSharedDeviceIDs bug in GatherAllocatedState
- **链接：** https://github.com/kubernetes/kubernetes/pull/136734
- **状态：** closed
- **已合并：** 是
- **作者：** sunya-ch
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复bug，解决了在启用DRAConsumableCapacity特性时，`pkg/scheduler/framework/plugins/noderesources`单元测试中发现的`GatherAllocatedState`函数缺失`GetSharedDeviceIDs`调用的问题。

### PR #136743: fix(kube-proxy): skip topology hints logging when no ready endpoints exist
- **链接：** https://github.com/kubernetes/kubernetes/pull/136743
- **状态：** closed
- **已合并：** 是
- **作者：** ansilh
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复bug，解决当Service的所有端点均未就绪时，kube-proxy错误记录“Ignoring same-zone topology hints...”日志刷屏的问题。修复方法是在未处理任何就绪端点时提前返回。

### PR #136793: KEP-5073:  Declarative Validation Lifecycle Update
- **链接：** https://github.com/kubernetes/kubernetes/pull/136793
- **状态：** closed
- **已合并：** 是
- **作者：** yongruilin
- **标签：** sig/scheduling, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, needs-priority, needs-triage
- **变更说明：**
  实现了KEP-5073，对声明式验证（Declarative Validation）的生命周期进行了更新。这是一个大型的API变更和功能增强，涉及代码生成和apiserver验证逻辑的改进。

### PR #136796: Fix kube-proxy nftables crash with newer nftables versions
- **链接：** https://github.com/kubernetes/kubernetes/pull/136796
- **状态：** closed
- **已合并：** 是
- **作者：** kairosci
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, sig/api-machinery, release-note, size/S, sig/auth, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  修复 kube-proxy 在 nftables 1.1.3+ 版本上因列出支持 udata 的 nftables 集时发生段错误而崩溃的问题。该修复无需修改 nftables 本身，确保与不同版本的兼容性。

### PR #136802: Fix data race in PopulateRefs by copying Items and AdditionalProperties
- **链接：** https://github.com/kubernetes/kubernetes/pull/136802
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, area/test, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 apiserver 中 PopulateRefs 函数的数据竞争问题。该函数对 schema 进行浅拷贝后直接修改其 Items.Schema 和 AdditionalProperties.Schema 指针，导致多 goroutine 并发访问时数据竞争。

### PR #136816: k8s.io/cloud-provider: Adds missing TLS flags to webhook serving options
- **链接：** https://github.com/kubernetes/kubernetes/pull/136816
- **状态：** closed
- **已合并：** 是
- **作者：** damdo
- **标签：** lgtm, area/cloudprovider, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  为 k8s.io/cloud-provider 的 webhook 服务选项添加缺失的 TLS 配置标志（如 --webhook-tls-cipher-suites、--webhook-tls-min-version 等），使 webhook 端点的 TLS 配置能够独立于主服务端点。

### PR #136846: kubelet: defer the configurations flags (and the related fallback behavior) deprecation removal timeline from 1.36 to 1.37 to align with containerd v1.7 support
- **链接：** https://github.com/kubernetes/kubernetes/pull/136846
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  功能PR，将kubelet配置标志（及相关回退行为）的弃用移除时间线从1.36版本推迟到1.37版本，以便与containerd v1.7的支持时间保持一致。

### PR #136892: Update/kubectl in kustomize to v5.8.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/136892
- **状态：** closed
- **已合并：** 是
- **作者：** koba1t
- **标签：** priority/important-soon, kind/cleanup, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, sig/architecture, needs-priority, area/dependency, needs-triage
- **变更说明：**
  更新kustomize组件中集成的kubectl版本至v5.8.1。这是一个依赖项更新和清理工作，旨在保持子模块与上游依赖的同步。

### PR #136898: kubeadm:  bump the version in the ContainerRuntimeVersionCheck warning message from 1.36 to 1.37
- **链接：** https://github.com/kubernetes/kubernetes/pull/136898
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** lgtm, sig/cluster-lifecycle, release-note, size/XS, kind/feature, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将kubeadm中ContainerRuntimeVersionCheck警告信息里提及的版本号从1.36更新为1.37。这是一个微小的更新，确保版本提示信息与即将发布的版本保持一致。

### PR #136937: client-go/reflector: reject Table format resources in List and Watch paths
- **链接：** https://github.com/kubernetes/kubernetes/pull/136937
- **状态：** closed
- **已合并：** 是
- **作者：** p0lyn0mial
- **标签：** kind/bug, area/test, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复 client-go reflector 在 List 和 Watch 路径中处理 Table 格式资源时可能引发的 panic。现在 reflector 会明确拒绝 Table 格式的资源。

### PR #136952: Add kubelet_metrics_provider metric
- **链接：** https://github.com/kubernetes/kubernetes/pull/136952
- **状态：** closed
- **已合并：** 是
- **作者：** dgrisonnet
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/M, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  为 kubelet 添加一个新的指标 kubelet_metrics_provider，用于监控 kubelet 内部指标提供者的状态和性能。

### PR #136982: Bump images and versions to go 1.25.7 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/136982
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, release-note, size/S, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  功能PR，更新构建基础镜像和版本，将Go版本升级至1.25.7，并使用distroless iptables镜像。

### PR #137008: [KEP 4317] Fix incorrect APIVersion in PodCertificateRequest OwnerReference
- **链接：** https://github.com/kubernetes/kubernetes/pull/137008
- **状态：** closed
- **已合并：** 是
- **作者：** srhppr
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了PodCertificateRequest对象中OwnerReference使用错误apiVersion（“core/v1”而非“v1”）的bug。此错误导致垃圾收集器无法在Pod删除时清理这些对象。修复包括代码更改和补充测试断言。

### PR #137019: add show-secret flag to the diff command
- **链接：** https://github.com/kubernetes/kubernetes/pull/137019
- **状态：** closed
- **已合并：** 是
- **作者：** olamilekan000
- **标签：** area/kubectl, lgtm, release-note, size/L, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  为kubectl diff命令新增了`--show-secret`标志。这是一个CLI功能增强，允许用户在diff输出中查看Secret资源的具体内容，便于调试和审计。

### PR #137063: Add group, version, resource labels to alpha metric apiserver_rerouted_request_total
- **链接：** https://github.com/kubernetes/kubernetes/pull/137063
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 alpha 指标 apiserver_rerouted_request_total 添加 group、version、resource 标签，以提供更细粒度的请求重定向监控维度。

### PR #137065: Add more metrics for Mixed Version Proxy
- **链接：** https://github.com/kubernetes/kubernetes/pull/137065
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 Mixed Version Proxy 功能添加更多指标，以增强对 API 请求在不同版本间代理行为的可观测性。

### PR #137084: KEP-5589: Drop temporary build-tagged ProtoMessage methods
- **链接：** https://github.com/kubernetes/kubernetes/pull/137084
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/cleanup, sig/scheduling, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, sig/architecture, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  根据 KEP-5589，移除临时添加的、带有构建标签的 ProtoMessage 方法实现。这些方法在 1.35 版本中作为临时缓解措施添加，现在正式移除，REST API 类型不再实现此标记方法。

### PR #137098: Fix container swap metrics
- **链接：** https://github.com/kubernetes/kubernetes/pull/137098
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复kubelet资源指标端点中container_swap_usage_bytes始终为0的bug。原因是CRI不提供swap信息，且cri_stats_provider.go中的`addCadvisorContainerCPUAndMemoryStats`函数未将cAdvisor的swap数据传播到容器指标对象。

### PR #137107: etcd: update etcd image to v3.6.8
- **链接：** https://github.com/kubernetes/kubernetes/pull/137107
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  清理性PR，将etcd镜像版本更新至v3.6.8。

### PR #137157: Allow kube-apiserver to recover from an accidentally made connection to a wrong server
- **链接：** https://github.com/kubernetes/kubernetes/pull/137157
- **状态：** closed
- **已合并：** 是
- **作者：** bsalamat
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复了一个bug，允许kube-apiserver在意外连接到错误服务器后能够恢复。通过修改http.Transport的TLS验证和连接池配置，使连接在握手失败后可被关闭和重建，避免了永久性阻塞。

### PR #137169: Revert nftables fix for nftables 1.1.3
- **链接：** https://github.com/kubernetes/kubernetes/pull/137169
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, kind/failing-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  回滚了PR #136796中对nftables的修复。因为该修复在大型集群（5000节点）测试中导致`nft.List()`效率严重下降，近乎失效，需要寻找替代方案。

### PR #137251: kubeadm: do not add learner member to etcd client endpoints
- **链接：** https://github.com/kubernetes/kubernetes/pull/137251
- **状态：** closed
- **已合并：** 是
- **作者：** pacoxu
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复bug，确保kubeadm在添加etcd learner成员时，不将其客户端URL添加到c.Endpoints中，因为learner不处理客户端流量。

---
*本报告由 Containerd Release Tracker 自动生成*
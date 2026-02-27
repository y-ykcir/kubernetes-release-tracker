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
- **分析时间：** 2026-02-27 00:47:25
- **分析的 PR 数量：** 43
- **分析的 Issue 数量：** 12
- **重要项目数量：** 53

## 📊 版本概述
Kubernetes v1.36.0-alpha.2 是一个早期预览版本，主要引入了 MutatingAdmissionPolicy GA、多项 API 改进、调度器优化，并继续推进废弃功能的移除，为生产环境升级提供了重要的早期信号。

## 🔒 安全问题修复
1. ⚠️ 修复 kube-apiserver 在错误连接到非预期服务器后无法恢复的问题，并开始验证服务器证书 - [PR #137157](https://github.com/kubernetes/kubernetes/pull/137157) - **风险级别：** 中 - **影响：** 在特定网络配置下（如 kube-proxy 未就绪），APIService 可能被误判为不健康且无法自动恢复。
2. ⚠️ 为云提供商 Webhook 服务器添加独立的 TLS 配置标志（如 cipher suites, min version），增强安全配置灵活性 - [PR #136816](https://github.com/kubernetes/kubernetes/pull/136816) - **风险级别：** 低 - **影响：** 允许管理员为 webhook 端点配置与主 API 服务器不同的、更严格的安全策略。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kube-proxy 在 nftables 1.1.3+ 版本上因段错误而崩溃的问题 - [PR #136796](https://github.com/kubernetes/kubernetes/pull/136796) - **影响：** 使用 nftables 模式且系统版本较新的集群，kube-proxy 会持续崩溃，导致服务网络故障。**注意：** 此修复在 PR #137169 中被回退，问题在 Alpha.2 中依然存在。
2. 修复 APIServer CEL 验证器中的数据结构竞争问题 - [PR #136802](https://github.com/kubernetes/kubernetes/pull/136802) - **影响：** 在高并发场景下可能导致数据不一致或程序崩溃。
3. 修复 kubelet 创建的 PodCertificateRequest 中 OwnerReference apiVersion 错误，导致垃圾回收失效的问题 - [PR #137008](https://github.com/kubernetes/kubernetes/pull/137008) - **影响：** Pod 删除后，关联的 PodCertificateRequest 资源无法被自动清理，造成资源泄漏。
4. 修复 kubelet 容器交换内存使用量指标 (`container_swap_usage_bytes`) 始终为 0 的问题 - [PR #137098](https://github.com/kubernetes/kubernetes/pull/137098) - **影响：** 监控系统无法正确获取容器级别的 Swap 使用情况。
5. 修复 kubectl logs -f 在 Pod 启动阶段抛出错误的问题，改善用户体验 - [PR #136411](https://github.com/kubernetes/kubernetes/pull/136411) - **影响：** 用户无法在 Pod 启动时自动跟随日志，需手动重试。
6. 修复 kube-proxy 在所有端点都未就绪时产生误导性日志刷屏的问题 - [PR #136743](https://github.com/kubernetes/kubernetes/pull/136743) - **影响：** 增加日志存储压力，干扰问题排查。

## 💥 破坏性变更
1. 🚨 将 API 服务器 admission 子系统中的 `sets.String` 类型替换为 `sets.Set[string]`，相关导出 API 发生变更 - [PR #134044](https://github.com/kubernetes/kubernetes/pull/134044) - **影响：** 直接导入并使用这些 API 的自定义控制器或扩展代码需要更新类型引用。
2. 🚨 kubeadm 移除对 FlexVolume 的内置支持，相关目录挂载需用户手动配置 - [PR #136423](https://github.com/kubernetes/kubernetes/pull/136423) - **影响：** 仍在使用 FlexVolume 的 kubeadm 集群，在升级前必须按照说明创建自定义控制器管理器镜像并配置卷挂载，否则功能失效。
3. 🚨 将 `gitRepo` 卷驱动锁定为禁用状态，使用该卷类型的 Pod 将无法创建 - [PR #136400](https://github.com/kubernetes/kubernetes/pull/136400) - **影响：** 必须将现有使用 `gitRepo` 卷的负载迁移到其他卷类型（如 Git 侧车容器或 CSI 驱动）。
4. 🚨 移除临时的、带构建标签的 `ProtoMessage()` 方法，依赖此方法的客户端库需要更新 - [PR #137084](https://github.com/kubernetes/kubernetes/pull/137084) - **影响：** 少数直接依赖此内部方法的第三方工具或库（如已发现的 Karmada）需要修改其实现。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. MutatingAdmissionPolicy 正式 GA，提供声明式 CEL 变异策略，减少对变异 Webhook 的依赖 - [PR #136039](https://github.com/kubernetes/kubernetes/pull/136039)
2. Pod 证书 (Beta) API 更新，引入 `stubPKCS10Request` 字段以提升与外部 CA 的兼容性，并废弃 `pkixPublicKey` 和 `proofOfPossession` - [PR #136729](https://github.com/kubernetes/kubernetes/pull/136729)
3. 多项核心组件指标从 Alpha 提升至 Beta，提供更强的 API 和标签稳定性保证 - [PR #136154](https://github.com/kubernetes/kubernetes/pull/136154)
4. 调度器 PostFilter 插件接口变更，为支持延迟抢占机制做准备 - [PR #136254](https://github.com/kubernetes/kubernetes/pull/136254)
5. 移除已废弃的 `HonorPVReclaimPolicy` 特性门控 - [PR #135335](https://github.com/kubernetes/kubernetes/pull/135335)
6. 锁定 `gitRepo` 卷驱动为禁用状态，推进其废弃进程 - [PR #136400](https://github.com/kubernetes/kubernetes/pull/136400)

## 🚀 性能优化
1. 优化抢占逻辑，对处于 PreBind 阶段的 Pod 进行抢占时不再发出删除 API 调用，而是将其重新放回队列 - [PR #135502](https://github.com/kubernetes/kubernetes/pull/135502) - **提升：** 减少不必要的 API 调用，降低 API 服务器负载，并使抢占行为更优雅。
2. 为线程安全存储添加资源版本查询和书签支持，提升大规模集群下的 List/Watch 效率 - [PR #134827](https://github.com/kubernetes/kubernetes/pull/134827) - **提升：** 改善 Informer 和 Reflector 在特定场景下的性能和资源使用。

## 🎯 风险评估
整体风险评估：**高（因为是 Alpha 版本）**。此版本包含多项破坏性变更和核心组件的重要修改，虽然修复了许多关键 Bug，但也引入了新的复杂变更（如调度器接口）。建议的升级时机：仅用于早期测试和特性验证。需要特别关注的方面：1) FlexVolume 和 gitRepo 卷的迁移；2) 自定义调度插件的兼容性；3) nftables 相关稳定性；4) 所有 API 变更对现有工具链的影响。

## 📋 升级建议
1. **对于生产环境：** 此版本为 Alpha，绝对不应用于生产。建议等待 Beta 或稳定版发布。
2. **评估废弃功能影响：** 立即检查集群是否仍在使用 `FlexVolume` 或 `gitRepo` 卷，并制定迁移计划。
3. **测试自定义调度插件：** 如果使用了自定义的 PostFilter 调度插件，需要根据 PR #136254 更新插件实现，返回被抢占的 Pod 列表。
4. **关注 nftables 问题：** 使用 nftables 模式且系统版本较新的集群，需密切关注后续版本对 kube-proxy 崩溃问题的最终修复。
5. **利用新特性：** 计划评估并使用 GA 的 `MutatingAdmissionPolicy`，以简化配置变异并降低对 Webhook 的运维负担。
6. **升级客户端库：** 如果开发的自定义控制器或工具直接引用了 `sets.String` 或 `ProtoMessage()` 等变更的 API，需提前适配。

## 📋 Release 包含的变更

### PR #10: Move everything out of src and reorganize scripts.
- **链接：** https://github.com/kubernetes/kubernetes/pull/10
- **状态：** closed
- **已合并：** 是
- **作者：** jbeda
- **变更说明：**
  重组代码库结构，将所有内容移出src目录并重新组织脚本。优化脚本健壮性，将e2e测试实例类型改为g1-small，更新文档以反映新脚本位置，并暂时禁用未经充分测试的'curl | bash'集群启动方式。

### PR #134044: Replace deprecated sets.String with sets.Set[string] in apiserver
- **链接：** https://github.com/kubernetes/kubernetes/pull/134044
- **状态：** closed
- **已合并：** 是
- **作者：** mcallzbl
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  在apiserver的准入控制子系统中，将所有已弃用的sets.String类型用法替换为推荐的泛型类型sets.Set[string]。这是一个代码现代化清理，但包含对导出API的破坏性变更。

### PR #134675: Enforce either optional or required tag on apiserverinternal API group
- **链接：** https://github.com/kubernetes/kubernetes/pull/134675
- **状态：** closed
- **已合并：** 是
- **作者：** JoelSpeed
- **标签：** lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  在apiserverinternal API组上强制执行字段标签（optional或required）。这是涉及多个SIG（storage, node, api-machinery等）的API变更，旨在提高API定义的一致性和清晰度。

### PR #134827: Add Resource Version query and Bookmarks to thread safe store
- **链接：** https://github.com/kubernetes/kubernetes/pull/134827
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, lgtm, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  为线程安全存储（thread safe store）添加了Resource Version查询和Bookmarks支持。这是一个功能增强，提升了API Machinery在测试场景下的能力。

### PR #134937: Daemonset controller staleness detection
- **链接：** https://github.com/kubernetes/kubernetes/pull/134937
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, area/e2e-test-framework, triage/accepted, wg/device-management
- **变更说明：**
  为DaemonSet控制器添加陈旧性检测功能。这是一个大型功能变更，涉及调度、节点、API机制等多个SIG，并与设备管理工作组相关。

### PR #134981: kubelet: drop cpu load metrics from container metrics test
- **链接：** https://github.com/kubernetes/kubernetes/pull/134981
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  从容器指标测试中移除CPU负载指标。因为该指标不稳定且已弃用，移除后可避免测试因该指标波动而失败。

### PR #135335: [1.36] Remove feature gate HonorPVReclaimPolicy
- **链接：** https://github.com/kubernetes/kubernetes/pull/135335
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/cleanup, lgtm, sig/storage, release-note, size/M, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  在Kubernetes 1.36版本中，移除了`HonorPVReclaimPolicy`特性门控。这是一个清理性质的PR，表明该功能已稳定并默认启用，无需再通过特性门控控制。

### PR #135502: Preempt pods in prebind phase without delete calls.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135502
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  允许调度器在PreBind阶段抢占Pod，而无需向apiserver发出删除调用。被抢占的Pod将被放回调度队列，而不是从集群存储中完全删除，行为更优雅。

### PR #135749: Fix: Incorrect duration metric recording incorrect values
- **链接：** https://github.com/kubernetes/kubernetes/pull/135749
- **状态：** closed
- **已合并：** 是
- **作者：** novahe
- **标签：** kind/bug, area/kubelet, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/instrumentation, sig/architecture, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了kubelet中持续时间指标记录错误值的问题。确保`volume_manager_volume_operation_duration_seconds`等指标能准确反映实际操作的延迟。

### PR #135808: SeparateCacheWatchRPC LockToDefault set true
- **链接：** https://github.com/kubernetes/kubernetes/pull/135808
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  将已弃用的SeparateCacheWatchRPC特性门锁定为其默认值(false)，禁止用户覆盖。这是移除该特性门前的清理步骤，未来版本将完全删除。

### PR #135965: set KEP-5440 to enabled by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/135965
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  将KEP-5440对应的功能默认启用，并为此添加了两个e2e测试。

### PR #136039: Promote MutatingAdmissionPolicy to v1 (GA)
- **链接：** https://github.com/kubernetes/kubernetes/pull/136039
- **状态：** closed
- **已合并：** 是
- **作者：** lalitc375
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, sig/architecture, area/conformance, area/code-generation, needs-priority, api-review, needs-triage, sig/etcd
- **变更说明：**
  将 `MutatingAdmissionPolicy` 特性提升至 General Availability (GA) 状态，API 版本为 `admissionregistration.k8s.io/v1`。该特性提供了一种基于 CEL 的声明式替代方案，用于执行常见的资源变更操作，无需运维 Mutating Admission Webhook。

### PR #136154: Promote component-base metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136154
- **状态：** closed
- **已合并：** 是
- **作者：** bhope
- **标签：** area/test, sig/network, area/kubelet, sig/scalability, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, priority/important-longterm, sig/architecture, area/code-generation, sig/cloud-provider, ok-to-test, area/e2e-test-framework, area/dependency, triage/accepted, area/stable-metrics, sig/etcd, wg/device-management
- **变更说明：**
  将一组广泛使用的 component-base 指标从 Alpha 提升至 Beta 稳定性。涉及指标包括 `kubernetes_build_info`、`rest_client_requests_total`、`rest_client_request_duration_seconds` 和 `running_managed_controllers`。此举为这些生产环境中已使用多个版本的指标提供了更强的 API 和标签稳定性保证。

### PR #136254: Extend PostFilterResult with a list of victim Pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/136254
- **状态：** closed
- **已合并：** 是
- **作者：** tosi3k
- **标签：** sig/scheduling, lgtm, size/L, kind/feature, release-note-action-required, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  扩展`PostFilterResult`结构，增加被抢占Pod（victim Pods）列表字段。这是为实现延迟抢占机制（KEP）做准备的第一步，旨在将抢占决策的计算与执行解耦。

### PR #136400: KEP:5040 Lock gitRepo Volume Driver to disabled.
- **链接：** https://github.com/kubernetes/kubernetes/pull/136400
- **状态：** closed
- **已合并：** 是
- **作者：** vinayakankugoyal
- **标签：** lgtm, sig/storage, release-note, size/S, approved, cncf-cla: yes, needs-priority, kind/deprecation, needs-triage
- **变更说明：**
  根据KEP-5040，将gitRepo卷驱动程序锁定为禁用状态。这是弃用该不安全卷类型过程的一部分。

### PR #136411: fix cli throwing an error when trying to tail the logs for a Pod
- **链接：** https://github.com/kubernetes/kubernetes/pull/136411
- **状态：** closed
- **已合并：** 是
- **作者：** olamilekan000
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  修复了 `kubectl logs --tail` 命令在尝试跟踪 Pod 日志时抛出错误的问题。这是一个针对 kubectl 的 bug 修复，确保了日志跟踪功能的正常使用。

### PR #136423: kubeadm: removed the built-in flex volume support
- **链接：** https://github.com/kubernetes/kubernetes/pull/136423
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/backlog, kind/cleanup, lgtm, sig/cluster-lifecycle, size/S, release-note-action-required, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  从 kubeadm 中移除了内置的 flex volume 支持。这是一项清理工作，因为 flex volume 已被弃用，用户需迁移至 CSI（容器存储接口）。此变更需要用户注意并采取相应行动。

### PR #136618: KEP-4671: Introduce Workload Scheduling Cycle
- **链接：** https://github.com/kubernetes/kubernetes/pull/136618
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, area/workload-aware
- **变更说明：**
  实现了KEP-4671，引入Workload Scheduling Cycle。这是一个大型功能，旨在改进调度器，使其能够感知工作负载特性并进行更智能的调度决策。

### PR #136689: Fix kubectl plugin list overshadow detection on Windows
- **链接：** https://github.com/kubernetes/kubernetes/pull/136689
- **状态：** closed
- **已合并：** 是
- **作者：** kfess
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 `kubectl plugin list` 在 Windows 系统上检测被遮蔽（overshadowed）插件时失效的问题。原代码使用 `/` 分割路径，未正确处理 Windows 的 `\` 路径分隔符。

### PR #136716: Split from concurrent-node-syncs a separate flag for node status updates
- **链接：** https://github.com/kubernetes/kubernetes/pull/136716
- **状态：** closed
- **已合并：** 是
- **作者：** yonizxz
- **标签：** lgtm, area/cloudprovider, release-note, size/M, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  从现有的concurrent-node-syncs标志中拆分出一个独立的标志，用于控制节点状态更新的并发度。这是一个API变更和功能增强，旨在为云提供商组件提供更精细的配置。

### PR #136729: Pod Certificates: Add StubPKCS10Request; migrate in-tree usages
- **链接：** https://github.com/kubernetes/kubernetes/pull/136729
- **状态：** closed
- **已合并：** 是
- **作者：** ahmedtd
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage
- **变更说明：**
  在Pod Certificates beta API中添加spec.stubPKCS10Request字段，以提升与现有CA实现（如Vault）的兼容性。同时弃用spec.pkixPublicKey和spec.proofOfPossession字段，并迁移所有内部使用。

### PR #136734: Fix missing GetSharedDeviceIDs bug in GatherAllocatedState
- **链接：** https://github.com/kubernetes/kubernetes/pull/136734
- **状态：** closed
- **已合并：** 是
- **作者：** sunya-ch
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复在启用DRAConsumableCapacity特性时，pkg/scheduler/framework/plugins/noderesources单元测试中发现的GatherAllocatedState函数缺少GetSharedDeviceIDs调用的bug。

### PR #136743: fix(kube-proxy): skip topology hints logging when no ready endpoints exist
- **链接：** https://github.com/kubernetes/kubernetes/pull/136743
- **状态：** closed
- **已合并：** 是
- **作者：** ansilh
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复当Service的所有端点均未就绪时，kube-proxy错误记录“Ignoring same-zone topology hints...”日志的问题。修复方法是在topologyModeFromHints函数中添加就绪端点跟踪，若无就绪端点则提前返回，避免误导性日志。

### PR #136793: KEP-5073:  Declarative Validation Lifecycle Update
- **链接：** https://github.com/kubernetes/kubernetes/pull/136793
- **状态：** closed
- **已合并：** 是
- **作者：** yongruilin
- **标签：** sig/scheduling, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, needs-priority, needs-triage
- **变更说明：**
  实现了KEP-5073：声明式验证生命周期更新。这是一个大型API变更，引入了验证表达式的生命周期管理，改进了CRD的验证逻辑。

### PR #136796: Fix kube-proxy nftables crash with newer nftables versions
- **链接：** https://github.com/kubernetes/kubernetes/pull/136796
- **状态：** closed
- **已合并：** 是
- **作者：** kairosci
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, sig/api-machinery, release-note, size/S, sig/auth, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  修复了 kube-proxy 在 nftables 1.1.3+ 系统上因列出支持 udata 的 nftables sets 而导致段错误并崩溃的问题。该修复使 kube-proxy 的 nftables 模式能在不同 nftables 版本上稳定运行，无需依赖 nftables 本身的补丁。

### PR #136802: Fix data race in PopulateRefs by copying Items and AdditionalProperties
- **链接：** https://github.com/kubernetes/kubernetes/pull/136802
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, area/test, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复了 `staging/src/k8s.io/apiserver/pkg/cel/openapi/resolver/refs.go` 中 `PopulateRefs` 函数的数据竞争问题。问题根源在于浅拷贝导致 `Items.Schema` 和 `AdditionalProperties.Schema` 指针被多个 goroutine 共享修改。修复方案是对这些字段进行深拷贝。

### PR #136816: k8s.io/cloud-provider: Adds missing TLS flags to webhook serving options
- **链接：** https://github.com/kubernetes/kubernetes/pull/136816
- **状态：** closed
- **已合并：** 是
- **作者：** damdo
- **标签：** lgtm, area/cloudprovider, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  为 `k8s.io/cloud-provider` 中的 webhook 服务选项添加了缺失的 TLS 配置标志，包括 `--webhook-disable-http2-serving`、`--webhook-tls-cipher-suites`、`--webhook-tls-min-version` 和 `--webhook-tls-sni-cert-key`。这使得 webhook 端点的 TLS 配置可以独立于主服务端点进行管理。

### PR #136846: kubelet: defer the configurations flags (and the related fallback behavior) deprecation removal timeline from 1.36 to 1.37 to align with containerd v1.7 support
- **链接：** https://github.com/kubernetes/kubernetes/pull/136846
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  将kubelet配置标志（及相关回退行为）的弃用移除时间线从1.36版本推迟到1.37版本，以便与containerd v1.7的支持时间线对齐。

### PR #136892: Update/kubectl in kustomize to v5.8.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/136892
- **状态：** closed
- **已合并：** 是
- **作者：** koba1t
- **标签：** priority/important-soon, kind/cleanup, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, sig/architecture, needs-priority, area/dependency, needs-triage
- **变更说明：**
  更新kustomize工具中集成的kubectl依赖版本至v5.8.1。这是一个依赖更新和清理操作。

### PR #136898: kubeadm:  bump the version in the ContainerRuntimeVersionCheck warning message from 1.36 to 1.37
- **链接：** https://github.com/kubernetes/kubernetes/pull/136898
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** lgtm, sig/cluster-lifecycle, release-note, size/XS, kind/feature, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  更新kubeadm中容器运行时版本检查的警告信息，将提及的版本号从1.36更新为1.37。这是一个微小的版本更新。

### PR #136937: client-go/reflector: reject Table format resources in List and Watch paths
- **链接：** https://github.com/kubernetes/kubernetes/pull/136937
- **状态：** closed
- **已合并：** 是
- **作者：** p0lyn0mial
- **标签：** kind/bug, area/test, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复了 client-go reflector 在 List 和 Watch 路径中处理 `Table` 格式资源时可能导致 panic 的问题。现在 reflector 会明确拒绝 `Table` 格式的资源。

### PR #136952: Add kubelet_metrics_provider metric
- **链接：** https://github.com/kubernetes/kubernetes/pull/136952
- **状态：** closed
- **已合并：** 是
- **作者：** dgrisonnet
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/M, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  新增了 `kubelet_metrics_provider` 指标，用于监控 kubelet metrics provider 的健康状态和性能。

### PR #136982: Bump images and versions to go 1.25.7 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/136982
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, release-note, size/S, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将Kubernetes构建基础镜像和版本升级至Go 1.25.7，并使用distroless iptables镜像。这是发布工程相关的更新。

### PR #137008: [KEP 4317] Fix incorrect APIVersion in PodCertificateRequest OwnerReference
- **链接：** https://github.com/kubernetes/kubernetes/pull/137008
- **状态：** closed
- **已合并：** 是
- **作者：** srhppr
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了`PodCertificateRequest`对象中`OwnerReference`的`apiVersion`字段错误（从`"core/v1"`改为`"v1"`）。此错误导致垃圾收集器无法在Pod删除时清理这些对象。同时修复了测试中遗漏的验证。

### PR #137019: add show-secret flag to the diff command
- **链接：** https://github.com/kubernetes/kubernetes/pull/137019
- **状态：** closed
- **已合并：** 是
- **作者：** olamilekan000
- **标签：** area/kubectl, lgtm, release-note, size/L, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  为`kubectl diff`命令新增`--show-secret`标志。该功能允许用户在查看配置差异时选择性地显示Secret的内容，便于调试。

### PR #137063: Add group, version, resource labels to alpha metric apiserver_rerouted_request_total
- **链接：** https://github.com/kubernetes/kubernetes/pull/137063
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 alpha 指标 `apiserver_rerouted_request_total` 添加了 `group`、`version`、`resource` 标签，提升了该指标在监控 API 请求重定向时的可观察性和细分能力。

### PR #137065: Add more metrics for Mixed Version Proxy
- **链接：** https://github.com/kubernetes/kubernetes/pull/137065
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 Mixed Version Proxy 功能添加了更多监控指标，以增强对 API 请求在不同版本间代理情况的观察能力。

### PR #137084: KEP-5589: Drop temporary build-tagged ProtoMessage methods
- **链接：** https://github.com/kubernetes/kubernetes/pull/137084
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/cleanup, sig/scheduling, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, sig/architecture, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  根据 KEP-5589，移除了临时添加的、带有构建标签的 `ProtoMessage()` 方法实现。这些方法是在 1.35 版本中为兼容性而引入的，现已确认仅有极少数外部依赖，故进行清理。

### PR #137098: Fix container swap metrics
- **链接：** https://github.com/kubernetes/kubernetes/pull/137098
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复kubelet资源指标端点中container_swap_usage_bytes始终为0的bug。根本原因是CRI不提供swap信息，且addCadvisorContainerCPUAndMemoryStats函数未将cAdvisor的swap统计传播到容器指标对象。修复后容器级swap使用量可正确上报。

### PR #137107: etcd: update etcd image to v3.6.8
- **链接：** https://github.com/kubernetes/kubernetes/pull/137107
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将etcd镜像版本更新至v3.6.8。这是一个依赖项更新和清理操作，涉及测试、云提供商、集群生命周期等多个领域。

### PR #137157: Allow kube-apiserver to recover from an accidentally made connection to a wrong server
- **链接：** https://github.com/kubernetes/kubernetes/pull/137157
- **状态：** closed
- **已合并：** 是
- **作者：** bsalamat
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复kube-apiserver在意外连接到错误服务器时无法恢复的问题。通过可选地强制执行TLS验证并在连接失败时关闭连接，提高了组件的健壮性。

### PR #137169: Revert nftables fix for nftables 1.1.3
- **链接：** https://github.com/kubernetes/kubernetes/pull/137169
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, kind/failing-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  回退了PR #136796中对nftables的修复。因为原修复在5000节点规模的测试中导致`nft.List()`性能严重下降，需要寻找替代方案。

### PR #137251: kubeadm: do not add learner member to etcd client endpoints
- **链接：** https://github.com/kubernetes/kubernetes/pull/137251
- **状态：** closed
- **已合并：** 是
- **作者：** pacoxu
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复kubeadm在添加etcd learner成员时，错误地将其客户端URL添加到c.Endpoints中的bug。因为learner成员不处理客户端流量，所以不应加入端点列表。

---
*本报告由 Containerd Release Tracker 自动生成*
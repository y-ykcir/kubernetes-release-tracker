# Kubernetes 版本发布分析报告
## v1.37.0-rc.0 (v1.37.0-rc.0)

### 📋 版本信息
- **版本标签：** v1.37.0-rc.0
- **版本名称：** v1.37.0-rc.0
- **发布时间：** 2026-08-06T12:04:57Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.37.0-rc.0

### 🔍 分析统计
- **分析时间：** 2026-08-06 13:47:41
- **分析的 PR 数量：** 41
- **分析的 Issue 数量：** 13
- **重要项目数量：** 52

## 📊 版本概述
Kubernetes v1.37 是一个功能丰富的版本，核心价值在于引入了声明式的 Pod 驱逐 API、显著提升了 DRA（动态资源分配）功能的成熟度与性能，并修复了多个关键的安全与稳定性问题。

## 🔒 安全问题修复
1. ⚠️ 放宽对包含 `CAP_SYSADMIN` 能力但 `allowPrivilegeEscalation: false` 的 Pod 的验证 - [PR #138834](https://github.com/kubernetes/kubernetes/pull/138834) - **风险级别：** 中 - **影响：** 此变更修复了之前过于严格的验证（Issue #119568），允许了原本被错误拒绝的安全配置。但需重新评估集群安全策略，确保此变更符合预期。
2. ⚠️ 识别 `allowPrivilegeEscalation: false` 无法完全防止通过危险能力（如 CAP_NET_ADMIN）进行权限提升的问题 - [Issue #131336](https://github.com/kubernetes/kubernetes/issues/131336) - **风险级别：** 中 - **影响：** 这是一个已知限制，用户需意识到仅设置 `allowPrivilegeEscalation: false` 不足以防御所有权限提升途径，应结合其他安全措施。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 DRA 设备分配重试时可能导致设备列表重复的 bug - [PR #140274](https://github.com/kubernetes/kubernetes/pull/140274) - **影响：** 防止容器启动失败或设备被重复挂载。
2. 修复 cgroup v2 下 Pod 级别 CPU 请求状态读取错误的问题 - [PR #137660](https://github.com/kubernetes/kubernetes/pull/137660) - **影响：** 确保资源监控和报告的数据准确性。
3. 修复 In-Place Pod 垂直伸缩时，MemoryQoS 保护可能丢失的问题 - [PR #140262](https://github.com/kubernetes/kubernetes/pull/140262) - **影响：** 保障 Pod 内存服务质量在资源调整期间不受影响。
4. 修复旧版本客户端通过 `pods/status` 更新时可能误清空 DRA 状态字段，导致 Pod 卡在 Terminating 的问题 - [PR #139876](https://github.com/kubernetes/kubernetes/pull/139876) - **影响：** 解决与旧客户端（如某些 CNI 插件）交互时的 Pod 终止阻塞问题。
5. 修复 kubelet 重启后，Pod 初始化检测逻辑可能导致 init 容器未正确重启的问题 - [PR #138514](https://github.com/kubernetes/kubernetes/pull/138514) - **影响：** 提升节点重启后 Pod 恢复的可靠性。

## 💥 破坏性变更
1. 🚨 client-go 完成 Context 支持，移除了绝大多数 `context.TODO()` 调用，引入了新的上下文感知 API - [PR #129125](https://github.com/kubernetes/kubernetes/pull/129125) - **影响：** 直接使用底层 client-go 库的代码可能需要适配新的 API 签名以传递 Context。
2. 🚨 `PodAndContainerStatsFromCRI` 特性门控在 Beta 阶段默认被禁用 - [PR #140081](https://github.com/kubernetes/kubernetes/pull/140081) - **影响：** 依赖此功能获取容器统计信息的用户需要显式启用该门控。
3. 🚨 `DRAPrioritizedList` 特性门控（已在 1.36 GA）被锁定为默认启用且不可禁用 - [PR #139110](https://github.com/kubernetes/kubernetes/pull/139110) - **影响：** 升级后无法再关闭此功能。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 引入声明式 EvictionRequest API，支持优雅驱逐 Pod - [PR #137050](https://github.com/kubernetes/kubernetes/pull/137050) - **影响：** 为自动化运维提供了新的 API 原语，可替代部分 `kubectl drain` 的使用场景。
2. DRA 调度器性能优化：为 ResourceClaim 事件添加 PreQueueingHint 扩展点，将 O(N) 的 Pod 重评估优化为 O(1) - [PR #138916](https://github.com/kubernetes/kubernetes/pull/138916) - **影响：** 大幅提升大规模集群中使用 DRA 时的调度器响应速度。
3. kube-proxy nftables 模式默认启用 netlink 支持以提升性能 - [PR #137536](https://github.com/kubernetes/kubernetes/pull/137536) - **影响：** 减少规则同步时的命令执行开销，提升网络代理性能。
4. 支持内存卷（如 tmpfs）的动态在线扩容 - [PR #139425](https://github.com/kubernetes/kubernetes/pull/139425) - **影响：** 允许在不重启 Pod 的情况下调整内存卷大小，提升应用灵活性。
5. KubeletInUserNamespace 功能升级至 Beta - [PR #134639](https://github.com/kubernetes/kubernetes/pull/134639) - **影响：** 改善在用户命名空间（如 rootless 模式）下运行 Kubelet 的支持。
6. HostnameOverride 功能门控升级至 GA - [PR #139116](https://github.com/kubernetes/kubernetes/pull/139116) - **影响：** 功能稳定，可安全用于覆盖节点主机名。

## 🚀 性能优化
1. 调度器为仅使用 `kubernetes.io/hostname` 拓扑的 Pod 间亲和性/反亲和性规则启用快速评估路径 - [PR #138198](https://github.com/kubernetes/kubernetes/pull/138198) - **提升：** 将 O(N*M) 的集群范围扫描优化为仅检查当前节点，显著降低调度延迟。
2. kube-proxy nftables 模式优化，为单端点 Service 避免使用 numgen map，减少规则集映射数量以提升同步速度 - [PR #140723](https://github.com/kubernetes/kubernetes/pull/140723) - **提升：** 缓解 Service 数量增长时同步时间超线性增长的问题（Issue #139513）。
3. API Server 默认启用 `ConcurrentWatchObjectDecode` 特性门控（Beta），支持并行解码 Watch 事件 - [PR #139679](https://github.com/kubernetes/kubernetes/pull/139679) - **提升：** Watch 缓存初始化性能提升约 45%。
4. 为 nftables 模式的本地主机 NodePorts 提供支持 - [PR #138427](https://github.com/kubernetes/kubernetes/pull/138427) - **提升：** 改善了本地开发测试和本地镜像仓库等场景的体验。

## 🎯 风险评估
整体风险评估：**中等**。此版本引入了重要的新 API 和大量优化，但同时也包含对核心组件（kubelet、调度器、kube-proxy）的深度修改。DRA 功能快速演进，相关修复较多，表明该区域仍处于活跃状态。建议的升级时机是在 v1.37 稳定版发布后，经过至少 2-4 周的测试环境验证。需要特别关注的方面包括：DRA 设备管理的正确性、Pod 终止流程、调度器性能变化，以及任何依赖 client-go 上下文的自定义控制器/工具的兼容性。

## 📋 升级建议
1. **升级前必须测试：** 由于包含大量 API 变更和 DRA 相关改动，请在非生产环境充分测试工作负载的兼容性与稳定性，特别是使用了 DRA、Pod 垂直伸缩或自定义调度器插件的集群。
2. **评估安全策略：** 仔细审查 PR #138834 关于 `CAP_SYSADMIN` 验证的变更，确认其是否会影响您现有的 Pod 安全策略或合规要求。
3. **检查客户端兼容性：** 如果集群中运行着使用旧版 client-go（早于引入 DRA 字段版本）的控制器或插件（如某些 CNI），升级前请参考 PR #139876 评估 Pod 终止风险，并考虑更新这些组件。
4. **关注性能监控：** 升级后，密切关注调度器（特别是 DRA 相关）、kube-proxy（nftables 模式）和 API Server 的性能指标，验证性能改进效果并发现潜在问题。
5. **利用新功能：** 计划使用新的 EvictionRequest API 来优化节点维护等自动化流程，替代传统的 `kubectl drain` 命令调用。

## 📋 Release 包含的变更

### PR #129125: client-go: finish context support
- **链接：** https://github.com/kubernetes/kubernetes/pull/129125
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** area/test, sig/network, area/kubelet, kind/cleanup, area/apiserver, lgtm, area/logging, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, sig/cloud-provider, needs-priority, area/dependency, needs-triage, wg/structured-logging, wg/device-management
- **变更说明：**
  清理client-go代码，将大部分`context.TODO()`替换为调用方传递的context，并支持上下文日志。这是一个代码重构，旨在提升API的上下文感知能力和日志可追溯性。

### PR #134037: KEP-3926: implement dry-run support for unsafe corrupt object deletion
- **链接：** https://github.com/kubernetes/kubernetes/pull/134037
- **状态：** closed
- **已合并：** 是
- **作者：** ibihim
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  为不安全的损坏对象删除功能（KEP-3926）添加 dry-run 支持，允许管理员在执行前安全测试删除操作，该功能受 AllowUnsafeMalformedObjectDeletion 特性门控。

### PR #134639: KEP-2033: promote KubeletInUserNamespace feature to beta (v1.37)
- **链接：** https://github.com/kubernetes/kubernetes/pull/134639
- **状态：** closed
- **已合并：** 是
- **作者：** AkihiroSuda
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  将 `KubeletInUserNamespace` 特性门禁晋升至Beta阶段（1.37版）。该特性允许kubelet在用户命名空间（user namespace）中运行，提升了在非特权容器或隔离环境中的部署能力。

### PR #135735: client-go: kubectl#1644 make relative path check cross platform
- **链接：** https://github.com/kubernetes/kubernetes/pull/135735
- **状态：** closed
- **已合并：** 是
- **作者：** bliles
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  修复client-go中相对路径检查的跨平台兼容性问题。这是一个bug修复，确保路径检查逻辑在不同操作系统上一致工作。

### PR #137050: EvictionRequest API
- **链接：** https://github.com/kubernetes/kubernetes/pull/137050
- **状态：** closed
- **已合并：** 是
- **作者：** atiratree
- **标签：** area/test, priority/important-soon, area/apiserver, area/kubectl, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, sig/architecture, area/conformance, area/code-generation, api-review, triage/accepted, sig/etcd, wg/node-lifecycle
- **变更说明：**
  引入新的声明式 EvictionRequest API，包括 Pod 的 .spec.evictionResponders 字段及 Eviction 资源，用于协调 Pod 的优雅驱逐。

### PR #137536: kube-proxy: Enable netlink support for nftables mode by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/137536
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, needs-rebase, size/XL, approved, cncf-cla: yes, sig/testing, needs-priority, area/dependency, needs-triage, kind/dependency
- **变更说明：**
  kube-proxy 在 nftables 模式下默认启用 netlink 支持，通过直接使用 netlink 而非解析 `nft` 命令输出来提升性能，可通过 NFTablesNetlink 特性门控禁用。

### PR #137546: [KEP-4817] DRAResourceClaimDeviceStatus to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/137546
- **状态：** closed
- **已合并：** 是
- **作者：** LionelJouin
- **标签：** area/test, lgtm, sig/node, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将 DRAResourceClaimDeviceStatus 特性门控升级到 GA 并默认启用，标志着 DRA 资源声明设备状态功能已稳定。

### PR #137660: fix cgroup v2 pod level cpu request readback issue
- **链接：** https://github.com/kubernetes/kubernetes/pull/137660
- **状态：** closed
- **已合并：** 是
- **作者：** pacoxu
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复kubelet在cgroup v2下读取Pod级别CPU请求状态时出现的错误。这是一个bug修复，确保从cgroup v2正确读回Pod的CPU请求值。

### PR #137762: kubelet : Add TLS support for gRPC probe
- **链接：** https://github.com/kubernetes/kubernetes/pull/137762
- **状态：** closed
- **已合并：** 是
- **作者：** amritansh1502
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  为kubelet的gRPC探针添加TLS支持。这是一个功能特性，增强了gRPC健康检查的安全性，支持加密通信。

### PR #138198: Fast-track evaluation path for host-scoped affinity/anti-affinity
- **链接：** https://github.com/kubernetes/kubernetes/pull/138198
- **状态：** closed
- **已合并：** 是
- **作者：** tetianakh
- **标签：** area/test, area/kubelet, sig/scheduling, lgtm, sig/node, release-note, size/XXL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  为使用 `kubernetes.io/hostname` 拓扑键的Pod间亲和性/反亲和性规则引入“快速路径”评估优化。当仅涉及该拓扑时，调度器Filter阶段只需检查当前节点，避免O(N*M)的集群范围扫描，提升性能。优化由 `InterPodAffinityHostnameFastPath` 特性门禁控制。

### PR #138427: kube-proxy: serve localhost NodePorts in nftables mode
- **链接：** https://github.com/kubernetes/kubernetes/pull/138427
- **状态：** closed
- **已合并：** 是
- **作者：** AustinAbro321
- **标签：** area/test, sig/network, area/kube-proxy, lgtm, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, area/ipvs, ok-to-test, needs-priority, api-review, needs-triage
- **变更说明：**
  使kube-proxy在nftables模式下支持通过localhost访问NodePort服务。这是一个功能增强，扩展了nftables代理模式的功能，使其行为与其他模式一致。

### PR #138456: DRA: add ResourceSlice field selector for pool name
- **链接：** https://github.com/kubernetes/kubernetes/pull/138456
- **状态：** closed
- **已合并：** 是
- **作者：** yaroslavborbat
- **标签：** area/test, lgtm, sig/node, sig/api-machinery, release-note, needs-rebase, size/XL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, area/code-generation, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  为`ResourceSlice` API添加对`spec.pool.name`的字段选择器支持。这是一个功能特性，允许客户端高效地按资源池名称列出和监视ResourceSlice对象。

### PR #138514: kubelet: use ActiveContainerStatuses to detect pod initialization
- **链接：** https://github.com/kubernetes/kubernetes/pull/138514
- **状态：** closed
- **已合并：** 是
- **作者：** chez-shanpu
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, kind/regression, triage/accepted
- **变更说明：**
  修复 kubelet 在检测 Pod 初始化时，错误使用 AllContainers 而非 ActiveContainerStatuses 的回归问题，确保初始化状态判断准确。

### PR #138738: [PodLevelResourceManagers] Report pod-level exclusive resources in PodResources API
- **链接：** https://github.com/kubernetes/kubernetes/pull/138738
- **状态：** closed
- **已合并：** 是
- **作者：** KevinTMtz
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, priority/important-longterm, triage/accepted
- **变更说明：**
  扩展PodResources API，使其能够报告Pod级别的独占资源（exclusive resources）。这是PodLevelResourceManagers功能的一部分，为外部组件（如监控、设备插件）提供更细粒度的资源分配信息。

### PR #138808: KEP-4222: Cbor encoder supports streaming for collection objects
- **链接：** https://github.com/kubernetes/kubernetes/pull/138808
- **状态：** closed
- **已合并：** 是
- **作者：** chenk008
- **标签：** sig/network, area/kubelet, sig/scalability, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/provider/gcp, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, sig/autoscaling, size/XXL, kind/api-change, sig/contributor-experience, kind/feature, area/release-eng, sig/auth, sig/apps, approved, sig/windows, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, sig/release, area/code-generation, area/ipvs, sig/cloud-provider, ok-to-test, needs-priority, area/dependency, triage/accepted, area/stable-metrics, wg/device-management
- **变更说明：**
  引入`StreamingCollectionEncodingToCbor`特性门控，使CBOR序列化器支持对集合对象进行流式编码。支持确定性和非确定性模式，旨在提升序列化性能。

### PR #138834: api: relax validation on CAP_SYSADMIN pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/138834
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** lgtm, release-note, size/L, kind/api-change, sig/apps, approved, cncf-cla: yes, needs-priority, api-review, needs-triage
- **变更说明：**
  放松API对具有`CAP_SYSADMIN`能力的Pod的验证规则。这是一个API变更，旨在提供更灵活的权限配置。

### PR #138916: scheduler: add PreQueueingHint extension point to narrow pod evaluation on events
- **链接：** https://github.com/kubernetes/kubernetes/pull/138916
- **状态：** closed
- **已合并：** 是
- **作者：** geetasg
- **标签：** area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/windows, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, area/e2e-test-framework, area/dependency, needs-triage, wg/device-management
- **变更说明：**
  为调度框架新增`PreQueueingHint`扩展点。允许插件（如DRA插件）在事件触发时指定需要重新评估的特定Pod，将部分场景下的重新调度复杂度从O(N)降至O(1)，优化性能。

### PR #139110: DRA PrioritizedList: lock to default-on
- **链接：** https://github.com/kubernetes/kubernetes/pull/139110
- **状态：** closed
- **已合并：** 是
- **作者：** mortent
- **标签：** area/test, priority/important-soon, kind/cleanup, sig/scheduling, lgtm, sig/node, release-note, needs-rebase, size/L, approved, cncf-cla: yes, sig/testing, triage/accepted, wg/device-management
- **变更说明：**
  将已稳定且默认启用的 DRAPrioritizedList 特性门控锁定为“默认开启且不可禁用”，该功能自 1.36 版本 GA。

### PR #139116: KEP-4762: Promote HostnameOverride feature gate to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/139116
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, needs-triage
- **变更说明：**
  将 HostnameOverride 特性门控升级到 GA 并默认启用，该功能允许覆盖节点向 API 服务器报告的主机名。

### PR #139262: EventedPLEG: Narrow the scope to apply only to container termination scenarios
- **链接：** https://github.com/kubernetes/kubernetes/pull/139262
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/XL, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  优化 EventedPLEG 功能，将其应用范围从所有容器事件缩小到仅容器终止场景，以减少不必要的开销并提升 kubelet 性能。

### PR #139425: feat: Support dynamically resizing memory-backed volumes
- **链接：** https://github.com/kubernetes/kubernetes/pull/139425
- **状态：** closed
- **已合并：** 是
- **作者：** natasha41575
- **标签：** area/test, priority/important-soon, area/kubelet, sig/scheduling, area/kubectl, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, sig/autoscaling, size/XXL, kind/api-change, kind/feature, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, area/code-generation, api-review, area/e2e-test-framework, triage/accepted
- **变更说明：**
  支持动态调整内存支持型卷（如`emptyDir`）的容量。这是一个API变更和功能增强，允许在线扩展内存卷，无需重启Pod。

### PR #139522: kubelet: fix in-place pod resize with non-admitted pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/139522
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复 kubelet 在 Pod 未准入（non-admitted）时错误地跳过原地（in-place）资源调整的问题，确保资源调整能正确进行。

### PR #139604: TAS Monitoring Metrics for Placement Phases
- **链接：** https://github.com/kubernetes/kubernetes/pull/139604
- **状态：** closed
- **已合并：** 是
- **作者：** alimaazamat
- **标签：** area/test, priority/important-soon, sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/testing, tide/merge-method-squash, triage/accepted, wg/workload-aware-scheduling
- **变更说明：**
  为拓扑感知调度（TAS）添加三个 Alpha 监控指标，用于观测 Pod 组放置（placement）的生成数量、评估结果和延迟，受 TopologyAwareWorkloadScheduling 特性门控。

### PR #139679: ConcurrentWatchObjectDecode enablement
- **链接：** https://github.com/kubernetes/kubernetes/pull/139679
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, kind/feature, approved, cncf-cla: yes, priority/important-longterm, triage/accepted, sig/etcd
- **变更说明：**
  将 `ConcurrentWatchObjectDecode` 特性门禁默认启用（Beta，1.37版），旨在启用CI测试并收集基准数据。基准测试显示，Pod的watch cache初始化速度提升约45%（从7.3秒降至4.0秒，处理15万个Pod）。

### PR #139726: Feat: kubectl top support v1.metrics.k8s.io
- **链接：** https://github.com/kubernetes/kubernetes/pull/139726
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** priority/backlog, area/kubectl, lgtm, release-note, size/XXL, kind/feature, approved, sig/cli, cncf-cla: yes, sig/instrumentation, area/code-generation, tide/merge-method-squash, triage/accepted
- **变更说明：**
  为 `kubectl top` 命令添加对 `v1.metrics.k8s.io` API的支持，以配合metrics.k8s.io API晋升至GA（正式可用）状态。这是KEP-5207的一部分。

### PR #139862: kubectl: add support for `--proxy-url` flag
- **链接：** https://github.com/kubernetes/kubernetes/pull/139862
- **状态：** closed
- **已合并：** 是
- **作者：** Mujib-Ahasan
- **标签：** priority/backlog, lgtm, release-note, size/XS, kind/feature, approved, sig/cli, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  为kubectl添加`--proxy-url`标志支持。这是一个小型功能，允许用户通过指定的代理URL访问Kubernetes API服务器。

### PR #139876: apiserver/pod: preserve DRA status fields when old clients clear them via pods/status
- **链接：** https://github.com/kubernetes/kubernetes/pull/139876
- **状态：** closed
- **已合并：** 是
- **作者：** ashishpatel26
- **标签：** area/test, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, needs-kind, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复当旧版本客户端通过`pods/status`更新Pod状态时，无意中清除DRA相关状态字段的问题。通过在`PrepareForUpdate`中恢复`ResourceClaimStatuses`等字段，防止Pod卡在Terminating状态。

### PR #139921: kubelet: populate Node UID on recorded node events (best-effort)
- **链接：** https://github.com/kubernetes/kubernetes/pull/139921
- **状态：** closed
- **已合并：** 是
- **作者：** harche
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复kubelet记录的节点事件中`involvedObject.uid`字段缺失的问题。通过从节点缓存中动态获取UID并填充到事件引用中，确保事件能被`kubectl describe node`等工具正确显示。

### PR #140081: features: move PodAndContainerStatsFromCRI to off by default beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/140081
- **状态：** closed
- **已合并：** 是
- **作者：** dgrisonnet
- **标签：** lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  将 PodAndContainerStatsFromCRI 特性门控从默认开启的 Beta 状态改为默认关闭，以收集更多稳定性数据。

### PR #140122: [InPlacePodVerticalScaling] add metrics to determine deferred resize duration and priority
- **链接：** https://github.com/kubernetes/kubernetes/pull/140122
- **状态：** closed
- **已合并：** 是
- **作者：** natasha41575
- **标签：** priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/instrumentation, needs-triage
- **变更说明：**
  为原地 Pod 垂直伸缩（InPlacePodVerticalScaling）增强可观测性，新增度量延迟调整（Deferred）持续时间和优先级的 Alpha 指标。

### PR #140147: feat(ccm): add labels to route_sync_total metric
- **链接：** https://github.com/kubernetes/kubernetes/pull/140147
- **状态：** closed
- **已合并：** 是
- **作者：** lukasmetzner
- **标签：** lgtm, area/cloudprovider, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/cloud-provider, needs-priority, triage/accepted
- **变更说明：**
  为云控制器管理器（CCM）的 Alpha 指标 `route_controller_route_sync_total` 添加 `trigger` 和 `outcome` 标签，以区分同步触发原因和结果。

### PR #140193: DRA: resource slice tracker informer
- **链接：** https://github.com/kubernetes/kubernetes/pull/140193
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/cleanup, lgtm, sig/node, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, area/code-generation, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将DRA（设备资源分配）的ResourceSlice跟踪器切换至类型安全的informer API，简化代码并修复一个潜在崩溃问题：当OnDelete事件发生时，若被删除的DeviceTaintRule对象未知，查找相关ResourceSlices的代码会崩溃。修复后调度器无需重启即可恢复。

### PR #140262: Fix MemoryQoS protection lost during IPPR resize and PodLevelResources memory.high miscalculation
- **链接：** https://github.com/kubernetes/kubernetes/pull/140262
- **状态：** closed
- **已合并：** 是
- **作者：** sohankunkerkar
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  修复两个bug：1) 在InPlace Pod Resize（IPPR）过程中MemoryQoS保护可能丢失；2) PodLevelResources中 `memory.high` 值计算错误。确保cgroup v2内存保护在资源调整和Pod级别资源管理中的正确性。

### PR #140274: kubelet/dra: reset devices before processing gRPC response
- **链接：** https://github.com/kubernetes/kubernetes/pull/140274
- **状态：** closed
- **已合并：** 是
- **作者：** bart0sh
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复kubelet中DRA（设备资源分配）的一个bug：当 `PrepareResources` 批处理中部分驱动成功、部分失败后重试时，可能导致成功的驱动返回的CDI设备ID在缓存中重复，进而引发容器启动失败。修复方法是在处理gRPC响应前重置设备列表，确保响应具有权威性。

### PR #140286: kubelet: harden and promote PodsAPI feature to Beta in 1.37
- **链接：** https://github.com/kubernetes/kubernetes/pull/140286
- **状态：** closed
- **已合并：** 是
- **作者：** briansonnenberg
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/testing, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  将 `PodsAPI` 特性门禁晋升至Beta（1.37版默认启用）。增强包括：无条件初始化gRPC服务器、修复拦截器链注册以阻止启动panic、新增ListPods/WatchPods错误计数指标，并修复相关E2E测试。

### PR #140289: Opportunistic batching rescore
- **链接：** https://github.com/kubernetes/kubernetes/pull/140289
- **状态：** closed
- **已合并：** 是
- **作者：** romanbaron
- **标签：** area/test, kind/cleanup, sig/scheduling, area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, area/release-eng, approved, cncf-cla: yes, sig/instrumentation, sig/testing, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  PR内容不完整，无法提取有效技术要点。

### PR #140437: DRA: skip the counter check for a persisted shared device
- **链接：** https://github.com/kubernetes/kubernetes/pull/140437
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRA结构化分配器中，对已持久化的共享设备进行计数器重复检查的bug。通过让`deviceCapacityInUse`也识别`AllocatedSharedDeviceIDs`，避免错误拒绝共享该设备的后续资源请求。

### PR #140442: DRA: reject an out-of-range consumable-capacity request
- **链接：** https://github.com/kubernetes/kubernetes/pull/140442
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, lgtm, sig/node, release-note, size/XL, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRA中处理超出`int64`表示范围的可消耗容量请求时可能导致的溢出问题。在`roundUpRange`函数中添加错误处理，拒绝无法安全表示的请求，防止调度器进入错误状态。

### PR #140641: Return succes from podgroup preemption if one is ongoing
- **链接：** https://github.com/kubernetes/kubernetes/pull/140641
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, release-note, size/XL, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复 PodGroup 抢占问题：当检测到正在进行抢占时，返回 Success 而非 Unschedulable，以防止清除 Pod 组的节点提名信息（NNN）。

### PR #140661: admission/namespace/lifecycle: allow updates to resources in deleted namespaces
- **链接：** https://github.com/kubernetes/kubernetes/pull/140661
- **状态：** closed
- **已合并：** 是
- **作者：** sanchezl
- **标签：** kind/bug, area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复 NamespaceLifecycle 准入控制器：允许对已删除命名空间中的现有资源进行更新（Update）操作，同时仍阻止创建（Create）操作，以解决存储版本迁移器的问题。

### PR #140723: kube-proxy/nftables: avoid numgen map for single-endpoint service DNAT
- **链接：** https://github.com/kubernetes/kubernetes/pull/140723
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** sig/network, kind/cleanup, area/kube-proxy, lgtm, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  优化kube-proxy的nftables模式，对于单端点的Service，避免使用numgen映射。由于nftables表中映射过多会显著增加规则添加成本，此优化旨在减少映射数量，提升规则编程速度，缓解相关问题。

---
*本报告由 Containerd Release Tracker 自动生成*
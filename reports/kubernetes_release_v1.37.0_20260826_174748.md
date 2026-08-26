# Kubernetes 版本发布分析报告
## v1.37.0 (v1.37.0)

### 📋 版本信息
- **版本标签：** v1.37.0
- **版本名称：** v1.37.0
- **发布时间：** 2026-08-26T16:29:12Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.37.0

### 🔍 分析统计
- **分析时间：** 2026-08-26 17:47:48
- **分析的 PR 数量：** 48
- **分析的 Issue 数量：** 24
- **重要项目数量：** 69

## 📊 版本概述
Kubernetes v1.37.0 是一个包含重要API变更、性能改进和关键Bug修复的版本，重点关注存储（SELinuxMount GA）、调度API升级和稳定性提升，但包含多个需要立即关注的破坏性变更。

## 🔒 安全问题修复
1. ⚠️ 未在此版本发布说明中识别到公开的 CVE 或高危安全问题。但条件授权机制的引入（Conditional Authz）可能影响现有的授权策略评估逻辑，建议审查 - [PR #137513](https://github.com/kubernetes/kubernetes/pull/137513) - **风险级别：** 低

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 StatefulSet 使用 OnDelete 策略时 CurrentRevision 不更新的问题 - [PR #136833](https://github.com/kubernetes/kubernetes/pull/136833) - **影响：** 修复了长期存在的 Bug，确保状态准确反映当前版本，影响所有使用 OnDelete 策略的 StatefulSet。
2. 修复 CronJob 控制器在获取现有 Job 时使用空命名空间的问题 - [PR #136920](https://github.com/kubernetes/kubernetes/pull/136920) - **影响：** 修复了 CronJob 控制器无法正确采用现有 Job 的问题，可能导致 Job 重复创建或状态不一致。
3. 修复节点关机管理器中导致线程耗尽的 dbus 连接泄漏 - [PR #137141](https://github.com/kubernetes/kubernetes/pull/137141) - **影响：** 防止因连接泄漏导致 kubelet 线程耗尽并崩溃，提升节点稳定性。
4. 修复 kubectl drain --disable-eviction --dry-run=server 命令无限挂起的问题 - [PR #137543](https://github.com/kubernetes/kubernetes/pull/137543) - **影响：** 修复了 drain 命令在特定参数组合下的阻塞问题，影响运维操作。
5. 修复 Binding API 不验证节点名称导致 Pod 卡在删除状态的问题 - [PR #136776](https://github.com/kubernetes/kubernetes/pull/136776) - **影响：** 防止绑定到无效节点名的 Pod 因终结器而无法删除，需手动介入清理。
6. 修复 ImageVolume 验证允许空引用导致运行时失败的问题 - [PR #135989](https://github.com/kubernetes/kubernetes/pull/135989) - **影响：** API 验证通过但 Pod 创建失败，修复后提前在 API 层拒绝无效配置。

## 💥 破坏性变更
1. 🚨 scheduling.k8s.io/v1alpha2 API 版本被移除 - [PR #138572](https://github.com/kubernetes/kubernetes/pull/138572) - **影响：** 升级前必须使用 kubectl 或 API 删除所有 v1alpha2 对象（如 Workload, PodGroup），否则 kube-apiserver 将无法启动。
2. 🚨 SELinuxMount 功能门默认启用且无法禁用 - [PR #139956](https://github.com/kubernetes/kubernetes/pull/139956) - **影响：** 在启用 SELinux 的集群中，任何依赖旧卷挂载行为的 Pod 可能无法启动。必须按照官方博客指南预先识别和修复问题工作负载。
3. 🚨 client-go 中广泛移除 context.TODO()，引入新的上下文感知 API - [PR #129125](https://github.com/kubernetes/kubernetes/pull/129125) - **影响：** 直接使用 client-go 底层接口的应用程序可能需要更新代码以传递上下文，否则可能遇到编译错误或警告。
4. 🚨 移除未使用的 PodStatusResult 类型 - [PR #136271](https://github.com/kubernetes/kubernetes/pull/136271) - **影响：** 任何直接导入此内部类型的代码将无法编译，但该类型从未在公共 API 中使用，影响范围有限。
5. 🚨 废弃并锁定 DeclarativeValidationTakeover 功能门 - [PR #139212](https://github.com/kubernetes/kubernetes/pull/139212) - **影响：** 该功能门被锁定为默认值，显式启用或禁用它将不再生效，需移除相关配置。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. SELinuxMount 功能门升级至 GA 并默认启用，可能破坏启用 SELinux 集群中的现有工作负载 - [PR #139956](https://github.com/kubernetes/kubernetes/pull/139956) - **影响：** 启用 SELinux 的集群中，现有 Pod 可能因卷标签不匹配而无法启动，需在升级前评估和修复。
2. scheduling.k8s.io API 组从 v1alpha2 升级到 v1alpha3，并完全移除 v1alpha2 - [PR #138572](https://github.com/kubernetes/kubernetes/pull/138572) - **影响：** 所有 v1alpha2 对象必须在升级前从 API Server 中删除，否则升级将失败。
3. 修复 kubelet 配置 eventRecordQPS 设置为 0 时仍有限制的问题 - [PR #117119](https://github.com/kubernetes/kubernetes/pull/117119) - **影响：** 之前设置为 0 表示“无限制”，但实际限制为 5 QPS，修复后行为符合预期。
4. StatefulSet 新增 Recreate 更新策略 - [PR #137187](https://github.com/kubernetes/kubernetes/pull/137187) - **影响：** 为有状态应用提供了类似 Deployment 的重建更新方式，增强了更新灵活性。
5. 引入声明式的 EvictionRequest API 用于 Pod 优雅驱逐 - [PR #137050](https://github.com/kubernetes/kubernetes/pull/137050) - **影响：** 提供了更可控的 Pod 驱逐机制，可用于构建自定义的节点排空和工作负载管理工具。

## 🚀 性能优化
1. kube-proxy 在 nftables 模式下默认启用 netlink 支持以提升性能 - [PR #137536](https://github.com/kubernetes/kubernetes/pull/137536) - **提升：** 通过直接使用 netlink 列出规则，避免执行和解析 `nft` 命令行二进制文件，提升规则处理性能。
2. 引入 EtcdRangeStream Beta 功能门，优化 watch 缓存初始化 - [PR #136915](https://github.com/kubernetes/kubernetes/pull/136915) - **提升：** 通过单次流式 RPC 而非分页请求初始化 watch 缓存，显著减少大型集群的 API Server 启动时间。
3. 优化 GangScheduling 插件的事件处理，减少不必要的队列提示函数执行 - [PR #135905](https://github.com/kubernetes/kubernetes/pull/135905) - **提升：** 减少调度器在 Pod 添加事件时的无效处理开销，提升调度性能。
4. 多项指标从 Alpha 升级到 Beta，提供更强的稳定性保证 - [PR #136189](https://github.com/kubernetes/kubernetes/pull/136189), [PR #137072](https://github.com/kubernetes/kubernetes/pull/137072), [PR #136894](https://github.com/kubernetes/kubernetes/pull/136894) - **提升：** 为存储操作、ServiceAccount Token 和工具类指标提供稳定的监控数据源。

## 🎯 风险评估
**整体风险评估：中等偏高**。此版本包含两个高影响的破坏性变更（SELinuxMount GA 和 v1alpha2 API 移除），处理不当可直接导致集群升级失败或工作负载中断。然而，它也修复了多个影响稳定性的关键 Bug（如 StatefulSet 状态、CronJob 控制器、kubelet 连接泄漏）。建议的升级时机是在充分测试后，选择维护窗口进行。需要特别关注的方面包括：SELinux 环境兼容性、遗留的 v1alpha2 对象清理、client-go 依赖项的兼容性，以及所有有状态工作负载（StatefulSet、CronJob）升级后的行为验证。

## 📋 升级建议
1. **升级前必须操作：** 1) 如果集群启用 SELinux，务必阅读官方博客并运行检测工具，修复或豁免受影响的工作负载。2) 清理所有 scheduling.k8s.io/v1alpha2 资源对象。
2. **测试建议：** 在非生产环境充分测试，重点验证：1) 所有 StatefulSet（特别是使用 OnDelete 策略的）的状态更新。2) CronJob 的 Job 创建和管理。3) 使用自定义调度器或 Binding API 的流程。
3. **客户端更新：** 检查并更新所有使用 client-go 库的应用程序、控制器或工具，确保它们能适配新的上下文感知 API。
4. **监控与观察：** 升级后，密切关注 kubelet 事件速率限制、kube-proxy 在 nftables 模式下的性能，以及 API Server 的 watch 缓存初始化时间。
5. **配置清理：** 从 kubeadm 配置、kubelet 配置文件和功能门列表中移除已锁定或删除的配置项，如 DeclarativeValidationTakeover 和 AnyVolumeDataSource。
6. **长期规划：** 注意 kubectl run --filename/-f 标志已被废弃，未来版本将移除，应迁移到 kubectl create -f 或 kubectl apply -f。

## 📋 Release 包含的变更

### PR #117119: kubelet: fix eventRecordQPS can't be set no limit enforced
- **链接：** https://github.com/kubernetes/kubernetes/pull/117119
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, sig/api-machinery, size/XS, release-note-action-required, sig/auth, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, ok-to-test, triage/accepted
- **变更说明：**
  修复 kubelet 中 eventRecordQPS 配置无法设置为无限制的问题。确保当 eventRecordQPS 设置为 0 时，事件记录速率限制被正确禁用。

### PR #121873: Log the actual host path volume mount type
- **链接：** https://github.com/kubernetes/kubernetes/pull/121873
- **状态：** closed
- **已合并：** 是
- **作者：** skitt
- **标签：** lgtm, sig/storage, release-note, size/M, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  PR #121873 改进了主机路径（host path）卷挂载失败时的日志信息。当挂载失败原因是主机路径类型与期望类型不匹配时，日志现在会同时记录实际路径类型和期望类型，便于问题诊断。

### PR #129109: restmapper + discovery: add context-aware APIs
- **链接：** https://github.com/kubernetes/kubernetes/pull/129109
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** area/test, area/kubelet, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, needs-priority, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  为 restmapper 和 discovery 组件添加上下文感知 API。主要目的是替换 context.TODO 并启用上下文日志记录。为避免破坏现有接口，采用创建 *WithContext 变体方法的新接口，原有方法作为新方法的包装器实现。

### PR #129125: client-go: finish context support
- **链接：** https://github.com/kubernetes/kubernetes/pull/129125
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** area/test, sig/network, area/kubelet, kind/cleanup, area/apiserver, lgtm, area/logging, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, sig/cloud-provider, needs-priority, area/dependency, needs-triage, wg/structured-logging, wg/device-management
- **变更说明：**
  完成 client-go 的上下文支持。主要移除 context.TODO 调用，通过引入调用者传递上下文的新 API 来实现。次要目的是启用上下文日志记录，使用调用者提供的 logger。

### PR #131176: Update po, mo files for kubectl Japanese translation
- **链接：** https://github.com/kubernetes/kubernetes/pull/131176
- **状态：** closed
- **已合并：** 是
- **作者：** yude
- **标签：** area/test, kind/documentation, area/kubectl, lgtm, release-note, size/XL, approved, sig/cli, cncf-cla: yes, sig/testing, priority/important-longterm, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  更新 kubectl 的日语翻译文件（po, mo 文件）。这是一个文档更新 PR，旨在完善 kubectl 命令的本地化支持。

### PR #131599: Enhance `kubectl get crd` output to include extra metadata beyond Name and Created-At
- **链接：** https://github.com/kubernetes/kubernetes/pull/131599
- **状态：** closed
- **已合并：** 是
- **作者：** jaehanbyun
- **标签：** lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  增强 kubectl get crd 命令的输出信息。在现有名称和创建时间的基础上，额外包含 CRD 的所属组、版本、作用域（Scope）和简称等元数据，提升可读性。

### PR #133313: check the job owner reference in the cronjob reconcile loop
- **链接：** https://github.com/kubernetes/kubernetes/pull/133313
- **状态：** closed
- **已合并：** 是
- **作者：** kei01234kei
- **标签：** kind/bug, priority/backlog, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  修复 CronJob 协调循环中的 bug。在协调循环中检查 Job 的所有者引用，防止因引用不匹配导致 Job 泄漏（未被正确清理）。

### PR #134037: KEP-3926: implement dry-run support for unsafe corrupt object deletion
- **链接：** https://github.com/kubernetes/kubernetes/pull/134037
- **状态：** closed
- **已合并：** 是
- **作者：** ibihim
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  PR #134037 为 KEP-3926 引入的“不安全损坏对象删除”功能实现了 dry-run 支持。管理员现在可以在实际执行这个可能破坏集群的操作前进行安全测试。该功能由 `AllowUnsafeMalformedObjectDeletion` 功能门控制。

### PR #134151: apiserver: Clean up the obsolete `DefaultWatchCacheSize` etcd option
- **链接：** https://github.com/kubernetes/kubernetes/pull/134151
- **状态：** closed
- **已合并：** 是
- **作者：** ialidzhikov
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/S, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  PR #134151 执行代码清理，移除了 apiserver 中已过时的 `DefaultWatchCacheSize` 等与 etcd 相关的配置选项。这些选项不再使用，删除它们有助于简化代码库。

### PR #134639: KEP-2033: promote KubeletInUserNamespace feature to beta (v1.37)
- **链接：** https://github.com/kubernetes/kubernetes/pull/134639
- **状态：** closed
- **已合并：** 是
- **作者：** AkihiroSuda
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  将 KubeletInUserNamespace 功能从 Alpha 升级至 Beta 阶段（v1.37）。该功能允许 Kubelet 在用户命名空间（user namespace）中运行，是 KEP-2033 的实现。

### PR #135160: support multi conditions in apicall
- **链接：** https://github.com/kubernetes/kubernetes/pull/135160
- **状态：** closed
- **已合并：** 是
- **作者：** KunWuLuan
- **标签：** sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  在 API 调用中支持指定多个条件（conditions）。此功能允许在单个 API 请求（如 List/Watch）中组合多个过滤条件，提高了查询的灵活性和效率，与调度（scheduling）等相关功能关联。

### PR #135300: kubelet: add diagnostic message to PodReadyToStartContainers condition
- **链接：** https://github.com/kubernetes/kubernetes/pull/135300
- **状态：** closed
- **已合并：** 是
- **作者：** harche
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复 kubelet 中 PodReadyToStartContainers 条件的问题，为其添加诊断消息。此改进有助于用户和调试工具更清晰地了解 Pod 容器无法启动的具体原因。

### PR #135336: [1.37] Remove feature gate AnyVolumeDataSource
- **链接：** https://github.com/kubernetes/kubernetes/pull/135336
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, kind/cleanup, lgtm, sig/storage, sig/api-machinery, release-note, size/L, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  在 1.37 版本中移除 AnyVolumeDataSource 特性门控。该特性已进入稳定阶段，因此执行清理工作，移除相关的特性门控代码。

### PR #135735: client-go: kubectl#1644 make relative path check cross platform
- **链接：** https://github.com/kubernetes/kubernetes/pull/135735
- **状态：** closed
- **已合并：** 是
- **作者：** bliles
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  修复 client-go 中相对路径检查的跨平台兼容性问题。确保路径检查逻辑在 Windows 和 Unix 系统上都能正确工作，解决相关问题。

### PR #135905: Execute GangScheduling plugin only for requeuing unschedulable pods on Add/Pod
- **链接：** https://github.com/kubernetes/kubernetes/pull/135905
- **状态：** closed
- **已合并：** 是
- **作者：** iomarsayed
- **标签：** area/test, sig/scheduling, lgtm, sig/storage, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  PR #135905 优化调度器性能，通过将集群事件中的 Pod 资源细分为 `AssignedPod`、`UnscheduledPod` 和 `TargetPod` 三种类型，使插件能更精确地订阅事件。这避免了像 GangScheduling 插件这样的场景下，无关插件执行无用的排队提示函数，从而减少性能损耗。

### PR #135925: Docs: event cache key generation functions require non-nil inputs
- **链接：** https://github.com/kubernetes/kubernetes/pull/135925
- **状态：** closed
- **已合并：** 是
- **作者：** jianzhangbjz
- **标签：** kind/documentation, lgtm, sig/api-machinery, release-note, size/S, approved, cncf-cla: yes, lifecycle/stale, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  PR #135925 是一个文档更新，明确指出事件缓存（event cache）的键生成函数要求输入参数非空（non-nil）。这是一个重要的使用说明，防止因传递空值而导致错误。

### PR #135964: fix: show only effective default StorageClass in kubectl output
- **链接：** https://github.com/kubernetes/kubernetes/pull/135964
- **状态：** closed
- **已合并：** 是
- **作者：** jaehanbyun
- **标签：** kind/bug, lgtm, sig/storage, release-note, size/L, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  PR #135964 修复了 `kubectl get storageclass` 命令的一个 bug。当多个 StorageClass 被标记为默认时，该命令现在只显示实际生效的那个默认 StorageClass，而不是列出所有，避免了输出上的混淆。

### PR #135989: Fix ImageVolume validation for empty reference in Pod templates
- **链接：** https://github.com/kubernetes/kubernetes/pull/135989
- **状态：** closed
- **已合并：** 是
- **作者：** Okabe-Junya
- **标签：** kind/bug, lgtm, sig/node, release-note, size/S, sig/apps, approved, cncf-cla: yes, tide/merge-method-squash, needs-priority, api-review, needs-triage
- **变更说明：**
  PR #135989 修复了 Pod 模板（如 Deployment、StatefulSet）中 `ImageVolume` 字段的验证漏洞。当 `image.reference` 为空时，现在会正确触发验证错误，防止创建引用无效镜像的 Pod。

### PR #136189: Promote volume metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136189
- **状态：** closed
- **已合并：** 是
- **作者：** bhope
- **标签：** lgtm, sig/storage, release-note, size/L, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/instrumentation, ok-to-test, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  PR #136189 将一组 kubelet 卷指标从 Alpha 稳定性提升到 Beta。涉及的指标包括 `storage_operation_duration_seconds` 和 `volume_operation_total_seconds`。升级到 Beta 为监控仪表板和告警提供了更强的向后兼容性保证。

### PR #136271: cleanup: Remove unused PodStatusResult type
- **链接：** https://github.com/kubernetes/kubernetes/pull/136271
- **状态：** closed
- **已合并：** 是
- **作者：** adityasharmawork
- **标签：** area/test, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, lifecycle/rotten, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  PR #136271 移除了 API 中未使用的 `PodStatusResult` 类型。该类型自 2015 年 kubelet 架构变更后已废弃超过 10 年，从未通过 REST API 暴露。删除它减少了不必要的测试维护和代码复杂度。

### PR #136436: Fix incorrect constant in VolumeError message validation
- **链接：** https://github.com/kubernetes/kubernetes/pull/136436
- **状态：** closed
- **已合并：** 是
- **作者：** Okabe-Junya
- **标签：** kind/bug, lgtm, sig/storage, release-note, size/XS, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  PR #136436 修复了 `VolumeAttachment` 验证中的一个 bug。验证函数错误地使用了 `maxAttachedVolumeMetadataSize` 常量（256 KB）来生成错误信息，而实际限制是 `maxVolumeErrorMessageSize`（1024 字节）。现已更正，错误信息将显示正确的限制值。

### PR #136709: DRA: improve CEL error message for "no such key" errors
- **链接：** https://github.com/kubernetes/kubernetes/pull/136709
- **状态：** closed
- **已合并：** 是
- **作者：** gzb1128
- **标签：** kind/documentation, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  改进 DRA（设备资源分配）中 CEL 选择器访问不存在设备属性时的错误信息。通过字符串匹配检测 'no such key' 错误，并在三个不同成熟度级别的分配器文件中应用此改进，为用户提供更清晰的调试指引。

### PR #136776: Validate node name in Binding API
- **链接：** https://github.com/kubernetes/kubernetes/pull/136776
- **状态：** closed
- **已合并：** 是
- **作者：** yakir-shriker
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, api-review, needs-triage
- **变更说明：**
  修复 Binding API 未验证节点名称的 Bug。此前绑定 Pod 到无效节点名（如含大写字符）会导致带 Finalizer 的 Pod 无法删除。现通过 ValidateNodeName 函数在 ValidatePodBinding 中添加前置验证。

### PR #136833: StatefulSet: Fix OnDelete strategy not updating CurrentRevision
- **链接：** https://github.com/kubernetes/kubernetes/pull/136833
- **状态：** closed
- **已合并：** 是
- **作者：** zhijun42
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  修复 StatefulSet 使用 OnDelete 更新策略时，CurrentRevision 字段不更新的 Bug。确保手动删除 Pod 后，StatefulSet 的状态版本信息能正确反映当前配置。

### PR #136894: Update util metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136894
- **状态：** closed
- **已合并：** 是
- **作者：** LoginovIlia
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/testing, ok-to-test, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将一组实用指标（util metrics）从 Alpha 阶段升级至 Beta 阶段，标志着这些指标的稳定性和可靠性得到提升。

### PR #136915: KEP 5966: Implement RangeStream for watch cache
- **链接：** https://github.com/kubernetes/kubernetes/pull/136915
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, kind/feature, sig/auth, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, sig/cloud-provider, needs-priority, area/dependency, triage/accepted, sig/etcd, wg/device-management
- **变更说明：**
  实现 KEP-5966，引入 Beta 特性门控 `EtcdRangeStream`。通过单个 etcd `RangeStream` RPC 流式初始化 watch cache，替代分页的 `Range` 请求，以减少初始化时间。

### PR #136920: Fix empty namespace when fetching existing job in cronjob controller
- **链接：** https://github.com/kubernetes/kubernetes/pull/136920
- **状态：** closed
- **已合并：** 是
- **作者：** ysam12345
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/M, sig/apps, approved, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  修复 CronJob 控制器在获取已存在 Job 时使用空命名空间的问题。现改为使用 CronJob 对象自身的命名空间，确保控制器能正确识别和采用现有 Job。

### PR #137050: EvictionRequest API
- **链接：** https://github.com/kubernetes/kubernetes/pull/137050
- **状态：** closed
- **已合并：** 是
- **作者：** atiratree
- **标签：** area/test, priority/important-soon, area/apiserver, area/kubectl, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, sig/architecture, area/conformance, area/code-generation, api-review, triage/accepted, sig/etcd, wg/node-lifecycle
- **变更说明：**
  引入新的声明式 EvictionRequest API（KEP-4563）。新增 Pod 的 `.spec.evictionResponders` 字段、EvictionRequest 和 Eviction 资源，用于协调 Pod 的优雅驱逐。

### PR #137072: Graduate old alpha ServiceAccount metric to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/137072
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** area/test, lgtm, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, sig/instrumentation, sig/testing, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将三个陈旧的 Alpha 版 ServiceAccount 指标升级至 Beta 版：`serviceaccount_legacy_tokens_total`、`serviceaccount_stale_tokens_total`、`serviceaccount_valid_tokens_total`。

### PR #137141: Fix dbus connection leak in node shutdown manager causing thread exhaustion
- **链接：** https://github.com/kubernetes/kubernetes/pull/137141
- **状态：** closed
- **已合并：** 是
- **作者：** harche
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, priority/important-longterm, lifecycle/rotten, triage/accepted
- **变更说明：**
  修复节点关闭管理器（Node Shutdown Manager）中的 dbus 连接泄漏问题。该问题会导致 goroutine 不断累积最终耗尽线程。修复方法包括：错误时正确关闭连接，重连时关闭旧连接，并使用可安全关闭的私有 dbus 连接。

### PR #137150: [PodLevelResources] Fix handling of empty pod-level resources
- **链接：** https://github.com/kubernetes/kubernetes/pull/137150
- **状态：** closed
- **已合并：** 是
- **作者：** KevinTMtz
- **标签：** sig/scheduling, area/kubectl, lgtm, sig/node, release-note, size/XL, kind/api-change, sig/apps, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复 PodLevelResources 功能中处理空 Pod 级别资源时的问题。确保在计算 Pod 资源请求时，能正确处理资源列表为空的情况，避免逻辑错误。

### PR #137187: Add recreate update strategy to statefulsets
- **链接：** https://github.com/kubernetes/kubernetes/pull/137187
- **状态：** closed
- **已合并：** 是
- **作者：** galal-hussein
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/XXL, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, tide/merge-method-squash, ok-to-test, api-review, area/e2e-test-framework, triage/accepted
- **变更说明：**
  为 StatefulSet 添加了 `Recreate` 更新策略。这是一个新的 API 特性，允许用户在更新 StatefulSet 时选择一次性删除所有旧 Pod 再创建新 Pod 的策略，作为现有 `RollingUpdate` 策略的补充。该改动涉及 API 定义、代码生成、控制器逻辑及广泛的测试。

### PR #137204: Conditional Authz [1/n]: Add conditional capabilities to the authorizer interface
- **链接：** https://github.com/kubernetes/kubernetes/pull/137204
- **状态：** closed
- **已合并：** 是
- **作者：** luxas
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  为授权器（Authorizer）接口添加了条件能力支持，这是实现条件授权功能系列工作的第一部分（预重构）。此变更扩展了核心授权接口，为后续支持基于动态条件（如 Pod 特征）的授权决策奠定基础，涉及多个 SIG（如 auth、api-machinery）。

### PR #137513: Conditional Authz [2/n]: Implementation of core Conditional Authorization machinery
- **链接：** https://github.com/kubernetes/kubernetes/pull/137513
- **状态：** closed
- **已合并：** 是
- **作者：** luxas
- **标签：** area/test, area/kubelet, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  实现条件授权（Conditional Authorization）的核心机制。这是该特性的第二部分，引入了新的 API 类型和评估逻辑，允许基于动态条件进行授权决策。

### PR #137536: kube-proxy: Enable netlink support for nftables mode by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/137536
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, needs-rebase, size/XL, approved, cncf-cla: yes, sig/testing, needs-priority, area/dependency, needs-triage, kind/dependency
- **变更说明：**
  kube-proxy 在 nftables 模式下默认启用 netlink 支持。通过 NFTablesNetlink 特性门控（Beta，默认启用）控制，使用 netlink 直接列出规则以提升性能，替代解析 nft 命令输出。

### PR #137543: Fix: kubectl drain --disable-eviction --dry-run=server hanging indefinitely
- **链接：** https://github.com/kubernetes/kubernetes/pull/137543
- **状态：** closed
- **已合并：** 是
- **作者：** kfess
- **标签：** kind/bug, area/test, priority/backlog, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  修复 kubectl drain --disable-eviction --dry-run=server 命令无限挂起的 bug。问题在于 deletePods 路径未像 evictPods 路径那样在 DryRunServer 模式下跳过等待，现已添加相应检查。

### PR #137699: DRA: KEP-5304: add e2e test for discoverable device metadata
- **链接：** https://github.com/kubernetes/kubernetes/pull/137699
- **状态：** closed
- **已合并：** 是
- **作者：** alaypatel07
- **标签：** area/test, priority/backlog, sig/scheduling, lgtm, sig/node, release-note, size/L, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  为 DRA（动态资源分配）的可发现设备元数据功能添加端到端（e2e）测试。此 PR 对应 KEP-5304，用于验证该特性的功能正确性。

### PR #138351: optional tracking and documentation of breaking Go API changes in client-go
- **链接：** https://github.com/kubernetes/kubernetes/pull/138351
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/documentation, lgtm, sig/api-machinery, release-note, size/XXL, approved, cncf-cla: yes, needs-priority, area/dependency, needs-triage
- **变更说明：**
  PR #138351 为 client-go 和 apimachinery 包引入了可选的破坏性 Go API 变更跟踪和文档机制。通过 `hack/apidiff.sh` 脚本和 `hack/update-go-apidocs.sh` 脚本，旨在提高代码审查中对破坏性变更的警觉性，并自动在 CHANGELOG 中记录变更信息。

### PR #138572: Converts the DisruptionMode enum field to struct as v1alpha3 and drops v1alpha2
- **链接：** https://github.com/kubernetes/kubernetes/pull/138572
- **状态：** closed
- **已合并：** 是
- **作者：** dom4ha
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, area/kubectl, lgtm, sig/node, sig/api-machinery, size/XXL, kind/api-change, kind/feature, release-note-action-required, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, needs-triage, sig/etcd, wg/device-management
- **变更说明：**
  PR #138572 将 `scheduling.k8s.io` API 组中的 `DisruptionMode` 字段从枚举（enum）转换为结构体（struct），以支持未来扩展。由于此变更不向后兼容，API 组版本从 `v1alpha2` 升级到 `v1alpha3`，并完全删除了 `v1alpha2`。管理员需在集群升级前清理所有 `v1alpha2` 对象。

### PR #138671: kubectl: deprecate run filename flag
- **链接：** https://github.com/kubernetes/kubernetes/pull/138671
- **状态：** closed
- **已合并：** 是
- **作者：** Suknna
- **标签：** area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, kind/deprecation, triage/accepted
- **变更说明：**
  PR #138671 开始弃用 `kubectl run` 命令中无效的 `--filename`/`-f` 标志。该标志通过 `DeleteFlags` 被注册，但 `run` 命令实际并不使用它来读取文件，而是通过命令行参数生成 Pod。此 PR 标志着该标志的弃用过程开始。

### PR #138940: Fix kube-proxy metrics-bind-address doc string inconsistency
- **链接：** https://github.com/kubernetes/kubernetes/pull/138940
- **状态：** closed
- **已合并：** 是
- **作者：** kairosci
- **标签：** kind/bug, sig/network, kind/documentation, area/kube-proxy, lgtm, release-note, size/XS, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修正 kube-proxy 的 `--metrics-bind-address` 标志文档。移除关于设置空字符串即可禁用指标服务器的错误描述，因为实际行为会回退到默认地址 `127.0.0.1:10249`。

### PR #139057: Store pod nomination before adding the pod to scheduling queue
- **链接：** https://github.com/kubernetes/kubernetes/pull/139057
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/L, approved, cncf-cla: yes, kind/failing-test, needs-priority, needs-triage
- **变更说明：**
  修复调度队列中的竞争条件：在将 Pod 加入调度队列之前，先存储其节点提名信息。确保提名信息在 Pod 被调度时可用，避免因顺序问题导致调度失败。

### PR #139067: kubeadm: warn if the user has configured kube-proxy with 'ipvs'
- **链接：** https://github.com/kubernetes/kubernetes/pull/139067
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/XS, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, kind/deprecation, triage/accepted
- **变更说明：**
  kubeadm 增加警告：当用户配置 kube-proxy 使用 'ipvs' 模式时发出警告，提示该模式即将被弃用，引导用户转向替代方案。

### PR #139212: Lock deprecated DeclarativeValidationTakeover to default in 1.37
- **链接：** https://github.com/kubernetes/kubernetes/pull/139212
- **状态：** closed
- **已合并：** 是
- **作者：** yongruilin
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, needs-priority, kind/deprecation, needs-triage
- **变更说明：**
  在 Kubernetes 1.37 版本中，将已弃用的 `DeclarativeValidationTakeover` 特性门控锁定为默认值（通常为关闭），以推进其淘汰流程，确保API验证行为的稳定性。

### PR #139651: Align DeviceTaintRule informer API version with handlers
- **链接：** https://github.com/kubernetes/kubernetes/pull/139651
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** kind/bug, area/test, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, kind/failing-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DeviceTaintRule informer 使用的 API 版本与处理器不匹配的问题。这是一个 bug 修复，旨在解决因版本不一致导致的测试失败。

### PR #139777: kubeadm: explicitly set the kube-proxy mode to 'iptables'
- **链接：** https://github.com/kubernetes/kubernetes/pull/139777
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/important-soon, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, kind/deprecation, triage/accepted
- **变更说明：**
  kubeadm 显式将 kube-proxy 模式设置为 'iptables'。这是一项清理和弃用准备工作，因为 'iptables' 是当前默认且唯一支持的模式，为未来移除模式选择逻辑做准备。

### PR #139837: Dump full config on kubelet startup instead of command line arguments
- **链接：** https://github.com/kubernetes/kubernetes/pull/139837
- **状态：** closed
- **已合并：** 是
- **作者：** SergeyKanzhelev
- **标签：** area/test, area/kubelet, lgtm, sig/node, size/L, kind/feature, release-note-action-required, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  PR #139837 修改 kubelet 启动日志，不再记录原始命令行参数，改为记录合并了所有来源（默认值、--config 文件、--config-dir 文件、命令行标志优先级）后的完整有效 KubeletConfiguration。这解决了之前参数可能显示过时值的问题，日志格式与 /configz 端点一致。管理员需注意审查 nodes/logs 集群角色的权限。

### PR #139956: Graduate SELinuxMount to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/139956
- **状态：** closed
- **已合并：** 是
- **作者：** jsafrane
- **标签：** area/kubelet, lgtm, sig/node, sig/api-machinery, size/M, kind/api-change, kind/feature, release-note-action-required, sig/apps, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, needs-triage
- **变更说明：**
  PR #139956 将 `SELinuxMount` 功能门（Feature Gate）从 Beta 升级到 GA（正式可用）。在 Kubernetes 1.37 中该功能将默认启用，可能对已启用 SELinux 的集群中的现有工作负载造成破坏。管理员需参考博客文章检查并修复问题，或在升级前选择退出。

---
*本报告由 Containerd Release Tracker 自动生成*
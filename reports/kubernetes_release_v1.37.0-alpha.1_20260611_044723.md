# Kubernetes 版本发布分析报告
## v1.37.0-alpha.1 (v1.37.0-alpha.1)

### 📋 版本信息
- **版本标签：** v1.37.0-alpha.1
- **版本名称：** v1.37.0-alpha.1
- **发布时间：** 2026-06-11T03:25:52Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.37.0-alpha.1

### 🔍 分析统计
- **分析时间：** 2026-06-11 04:47:23
- **分析的 PR 数量：** 45
- **分析的 Issue 数量：** 26
- **重要项目数量：** 66

## 📊 版本概述
Kubernetes v1.37.0-alpha.1 是一个早期测试版本，主要包含多项API变更、功能废弃、重要Bug修复和性能改进，重点关注kubelet配置修复、API清理和调度器优化。

## 🔒 安全问题修复
1. ⚠️ 加强kubelet日志相关端点的HTTP方法限制 - [PR #138088](https://github.com/kubernetes/kubernetes/pull/138088) - **风险级别：** 低 - 明确限制只读端点仅允许GET方法
2. ⚠️ 修复etcd不安全删除路径的数据损坏问题 - [PR #137582](https://github.com/kubernetes/kubernetes/pull/137582) - **风险级别：** 中 - 确保数据一致性，防止潜在的数据损坏

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复StatefulSet OnDelete策略不更新CurrentRevision的问题 - [PR #136833](https://github.com/kubernetes/kubernetes/pull/136833) - **影响：** 影响使用OnDelete更新策略的StatefulSet状态准确性
2. 修复并行Pod管理中maxUnavailable计算错误的问题 - [PR #137666](https://github.com/kubernetes/kubernetes/pull/137666) - **影响：** 修复v1.35引入的回归问题，确保StatefulSet滚动更新正常进行
3. 恢复通过环境变量传递二进制数据的能力（修复1.34+的回归） - [PR #139168](https://github.com/kubernetes/kubernetes/pull/139168) - **影响：** 修复Secret中包含非UTF-8数据时容器创建失败的问题
4. 修复CronJob控制器获取已存在Job时空命名空间的问题 - [PR #136920](https://github.com/kubernetes/kubernetes/pull/136920) - **影响：** 修复CronJob无法正确采用现有Job的问题
5. 修复kubectl drain --disable-eviction --dry-run=server无限挂起的问题 - [PR #137543](https://github.com/kubernetes/kubernetes/pull/137543) - **影响：** 影响使用dry-run模式的运维操作
6. 修复Windows kube-proxy在IP重用场景下的远程端点清理问题 - [PR #138000](https://github.com/kubernetes/kubernetes/pull/138000) - **影响：** 解决Windows节点上因IP重用导致的网络连接问题

## 💥 破坏性变更
1. 🚨 废弃kubectl run的--filename/-f标志（该标志原本被忽略） - [PR #138671](https://github.com/kubernetes/kubernetes/pull/138671) - **影响：** 使用该标志将收到废弃警告，需要移除
2. 🚨 移除kubeadm v1beta3 API和PublicKeysECDSA特性门控 - [PR #136016](https://github.com/kubernetes/kubernetes/pull/136016) - **影响：** 需要更新kubeadm配置
3. 🚨 移除AnyVolumeDataSource特性门控（功能已稳定） - [PR #135336](https://github.com/kubernetes/kubernetes/pull/135336) - **影响：** 相关功能默认启用，无需配置特性门控
4. 🚨 移除SidecarContainers特性门控（功能已稳定） - [PR #137755](https://github.com/kubernetes/kubernetes/pull/137755) - **影响：** 相关功能默认启用
5. 🚨 清理已废弃的DefaultWatchCacheSize等etcd选项 - [PR #134151](https://github.com/kubernetes/kubernetes/pull/134151) - **影响：** 需要更新相关配置

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 紧急修复：kubelet配置eventRecordQPS=0的行为变更，现在0表示无限制（之前被当作默认值50） - [PR #117119](https://github.com/kubernetes/kubernetes/pull/117119) - **影响：** 如果配置中设置了eventRecordQPS=0且希望保持之前的行为，需要手动改为50
2. API变更：将DisruptionMode从枚举改为结构体，并废弃scheduling.k8s.io/v1alpha2 API版本 - [PR #138572](https://github.com/kubernetes/kubernetes/pull/138572) - **影响：** 升级时需要清理所有v1alpha2对象
3. 功能提升：DRA（动态资源分配）扩展资源功能正式GA - [PR #138488](https://github.com/kubernetes/kubernetes/pull/138488) - **影响：** 相关API和功能进入稳定状态
4. API清理：移除未使用的PodStatusResult类型 - [PR #136271](https://github.com/kubernetes/kubernetes/pull/136271) - **影响：** 内部API清理，不影响用户
5. CRI API变更：重命名Signal枚举键以避免C++宏冲突 - [PR #139251](https://github.com/kubernetes/kubernetes/pull/139251) - **影响：** 需要重新编译使用CRI API的组件

## 🚀 性能优化
1. 实现watch cache的RangeStream以提升初始化性能 - [PR #136915](https://github.com/kubernetes/kubernetes/pull/136915) - **提升：** 通过单次RPC流式传输替代分页请求，减少watch cache初始化时间
2. 优化GangScheduling插件仅在需要时执行 - [PR #135905](https://github.com/kubernetes/kubernetes/pull/135905) - **提升：** 减少不必要的插件执行，提升调度器性能
3. 多项指标从Alpha提升到Beta稳定性 - [PR #136189](https://github.com/kubernetes/kubernetes/pull/136189)、[PR #137072](https://github.com/kubernetes/kubernetes/pull/137072)、[PR #136894](https://github.com/kubernetes/kubernetes/pull/136894)、[PR #137116](https://github.com/kubernetes/kubernetes/pull/137116) - **提升：** 提供更稳定的监控指标

## 🎯 风险评估
整体风险评估：中等。这是一个alpha版本，包含多个API变更和破坏性变更，不建议在生产环境使用。主要风险包括：1) kubelet配置行为变更可能导致事件记录限制意外变化；2) API版本废弃需要迁移工作；3) Windows网络修复可能影响现有配置。建议仅在测试环境中评估，重点关注StatefulSet、CronJob和Windows节点的功能验证。升级时机：等待beta或稳定版本发布后再考虑生产环境升级。

## 📋 升级建议
1. **重要：** 如果kubelet配置中设置了eventRecordQPS=0，升级前请检查是否需要改为50以保持原有行为
2. **API迁移：** 如果使用scheduling.k8s.io/v1alpha2 API，升级前需要迁移到v1alpha3并清理v1alpha2对象
3. **测试建议：** 在测试环境中充分验证StatefulSet滚动更新、CronJob管理和Windows网络功能
4. **监控更新：** 更新监控仪表板以使用新的Beta指标，确保兼容性
5. **工具链更新：** 如果使用CRI API开发容器运行时，需要重新编译以适应Signal枚举键的变更

## 📋 Release 包含的变更

### PR #117119: kubelet: fix eventRecordQPS can't be set no limit enforced
- **链接：** https://github.com/kubernetes/kubernetes/pull/117119
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, sig/api-machinery, size/XS, release-note-action-required, sig/auth, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, ok-to-test, triage/accepted
- **变更说明：**
  修复 kubelet 中 `eventRecordQPS` 设置为 0（表示无限制）时，速率限制未正确生效的问题。

### PR #131176: Update po, mo files for kubectl Japanese translation
- **链接：** https://github.com/kubernetes/kubernetes/pull/131176
- **状态：** closed
- **已合并：** 是
- **作者：** yude
- **标签：** area/test, kind/documentation, area/kubectl, lgtm, release-note, size/XL, approved, sig/cli, cncf-cla: yes, sig/testing, priority/important-longterm, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  更新了kubectl命令行工具的日语翻译文件（po/mo文件），属于本地化文档更新。

### PR #131599: Enhance `kubectl get crd` output to include extra metadata beyond Name and Created-At
- **链接：** https://github.com/kubernetes/kubernetes/pull/131599
- **状态：** closed
- **已合并：** 是
- **作者：** jaehanbyun
- **标签：** lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  增强了`kubectl get crd`命令的输出，在默认显示的Name和Created-At之外包含了更多元数据信息，提升了用户对CRD的可见性。

### PR #133313: check the job owner reference in the cronjob reconcile loop
- **链接：** https://github.com/kubernetes/kubernetes/pull/133313
- **状态：** closed
- **已合并：** 是
- **作者：** kei01234kei
- **标签：** kind/bug, priority/backlog, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  修复了CronJob控制器在协调循环中未能正确检查Job的所有者引用（OwnerReference）的问题，确保能准确识别和清理非自己创建的Job，防止状态不一致。

### PR #134151: apiserver: Clean up the obsolete `DefaultWatchCacheSize` etcd option
- **链接：** https://github.com/kubernetes/kubernetes/pull/134151
- **状态：** closed
- **已合并：** 是
- **作者：** ialidzhikov
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/S, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  清理了apiserver中过时的DefaultWatchCacheSize等etcd相关配置选项，移除了不再使用的代码以简化实现。这是一个清理性质的变更。

### PR #135160: support multi conditions in apicall
- **链接：** https://github.com/kubernetes/kubernetes/pull/135160
- **状态：** closed
- **已合并：** 是
- **作者：** KunWuLuan
- **标签：** sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  在调度框架的 `apicall` 插件中增加对多个过滤条件（Conditions）的支持，增强了插件在调度决策时的过滤能力。

### PR #135336: [1.37] Remove feature gate AnyVolumeDataSource
- **链接：** https://github.com/kubernetes/kubernetes/pull/135336
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, kind/cleanup, lgtm, sig/storage, sig/api-machinery, release-note, size/L, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  在1.37版本中移除了已稳定的AnyVolumeDataSource特性门控。这是一个清理和API变更，该功能现已默认启用。

### PR #135905: Execute GangScheduling plugin only for requeuing unschedulable pods on Add/Pod
- **链接：** https://github.com/kubernetes/kubernetes/pull/135905
- **状态：** closed
- **已合并：** 是
- **作者：** iomarsayed
- **标签：** area/test, sig/scheduling, lgtm, sig/storage, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  优化调度插件性能，将集群事件中的Pod资源细分为AssignedPod、UnscheduledPod和TargetPod三种类型。这使得插件（如GangScheduling）可以更精确地订阅特定事件，避免在Pod添加等事件中所有插件都执行其排队提示函数，从而减少不必要的性能损耗。

### PR #135925: Docs: event cache key generation functions require non-nil inputs
- **链接：** https://github.com/kubernetes/kubernetes/pull/135925
- **状态：** closed
- **已合并：** 是
- **作者：** jianzhangbjz
- **标签：** kind/documentation, lgtm, sig/api-machinery, release-note, size/S, approved, cncf-cla: yes, lifecycle/stale, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  文档更新，明确指出事件缓存键生成函数（如`keyFunc`、`metaNamespaceKeyFunc`）要求输入参数不能为nil。这是一个重要的使用前提说明。

### PR #135964: fix: show only effective default StorageClass in kubectl output
- **链接：** https://github.com/kubernetes/kubernetes/pull/135964
- **状态：** closed
- **已合并：** 是
- **作者：** jaehanbyun
- **标签：** kind/bug, lgtm, sig/storage, release-note, size/L, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  修复`kubectl get storageclass`的输出问题。当多个StorageClass被标记为默认时，命令现在只显示实际生效的那个（即`storageclass.kubernetes.io/is-default-class`注解为`"true"`的类），而不是显示所有带有默认注解的类。

### PR #135989: Fix ImageVolume validation for empty reference in Pod templates
- **链接：** https://github.com/kubernetes/kubernetes/pull/135989
- **状态：** closed
- **已合并：** 是
- **作者：** Okabe-Junya
- **标签：** kind/bug, lgtm, sig/node, release-note, size/S, sig/apps, approved, cncf-cla: yes, tide/merge-method-squash, needs-priority, api-review, needs-triage
- **变更说明：**
  修复Pod模板（如Deployment、StatefulSet）中ImageVolume的验证漏洞。当`image.reference`字段为空时，验证应失败。此PR确保了在Pod模板创建和更新时，会对ImageVolume进行正确的验证。

### PR #136016: kubeadm: remove the v1beta3 API and PublicKeysECDSA feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/136016
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/important-soon, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/XXL, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  清理kubeadm代码，移除已弃用的`v1beta3` API版本以及与之关联的`PublicKeysECDSA`特性门控。这是版本迭代后的常规清理工作。

### PR #136189: Promote volume metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136189
- **状态：** closed
- **已合并：** 是
- **作者：** bhope
- **标签：** lgtm, sig/storage, release-note, size/L, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/instrumentation, ok-to-test, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将 kubelet 卷操作监控指标 `storage_operation_duration_seconds` 和 `volume_operation_total_seconds` 从 Alpha 稳定性提升至 Beta，为存储可靠性监控提供更强的兼容性保证。

### PR #136271: cleanup: Remove unused PodStatusResult type
- **链接：** https://github.com/kubernetes/kubernetes/pull/136271
- **状态：** closed
- **已合并：** 是
- **作者：** adityasharmawork
- **标签：** area/test, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, lifecycle/rotten, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  移除了十年未使用的PodStatusResult API类型（自2015年kubelet架构变更后废弃）。此清理工作减少了维护负担和测试开销，是一个API变更。

### PR #136436: Fix incorrect constant in VolumeError message validation
- **链接：** https://github.com/kubernetes/kubernetes/pull/136436
- **状态：** closed
- **已合并：** 是
- **作者：** Okabe-Junya
- **标签：** kind/bug, lgtm, sig/storage, release-note, size/XS, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复VolumeAttachment验证中错误使用常量的问题。验证函数实际检查消息长度是否超过1024字节（maxVolumeErrorMessageSize），但错误信息中错误地引用了256KB的限制（maxAttachedVolumeMetadataSize）。此PR更正了错误信息，使其准确反映1024字节的限制。

### PR #136709: DRA: improve CEL error message for "no such key" errors
- **链接：** https://github.com/kubernetes/kubernetes/pull/136709
- **状态：** closed
- **已合并：** 是
- **作者：** gzb1128
- **标签：** kind/documentation, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  改进了DRA中CEL表达式访问不存在设备属性时的错误信息。通过strings.HasPrefix检测"no such key"错误（因cel-go错误类型未导出），并在allocator_stable.go、allocator_incubating.go、allocator_experimental.go三个文件中添加了更清晰的修复指引。

### PR #136833: StatefulSet: Fix OnDelete strategy not updating CurrentRevision
- **链接：** https://github.com/kubernetes/kubernetes/pull/136833
- **状态：** closed
- **已合并：** 是
- **作者：** zhijun42
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  修复了StatefulSet使用OnDelete更新策略时，CurrentRevision字段不会随PodTemplate更新而变化的bug。修复后，CurrentRevision能正确反映最新的Pod规格。

### PR #136894: Update util metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136894
- **状态：** closed
- **已合并：** 是
- **作者：** LoginovIlia
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/testing, ok-to-test, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将apiserver utility相关的指标从alpha稳定性升级为beta，标志着这些指标已可用于生产环境。

### PR #136915: KEP 5966: Implement RangeStream for watch cache
- **链接：** https://github.com/kubernetes/kubernetes/pull/136915
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, kind/feature, sig/auth, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, sig/cloud-provider, needs-priority, area/dependency, triage/accepted, sig/etcd, wg/device-management
- **变更说明：**
  实现了KEP 5966，新增EtcdRangeStream beta特性门控。启用后，watch cache初始化时使用etcd的单次RangeStream RPC替代分页Range请求，旨在减少延迟并提升性能，支持回退到原有分页方式。

### PR #136920: Fix empty namespace when fetching existing job in cronjob controller
- **链接：** https://github.com/kubernetes/kubernetes/pull/136920
- **状态：** closed
- **已合并：** 是
- **作者：** ysam12345
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/M, sig/apps, approved, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  修复了CronJob控制器在获取已存在Job时错误地使用空命名空间的问题（Issue #136918）。现改为使用CronJob对象自身的命名空间，确保能正确采用现有Job。

### PR #137072: Graduate old alpha ServiceAccount metric to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/137072
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** area/test, lgtm, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, sig/instrumentation, sig/testing, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将三个 ServiceAccount 令牌相关指标 `serviceaccount_legacy_tokens_total`、`serviceaccount_stale_tokens_total` 和 `serviceaccount_valid_tokens_total` 从 Alpha 稳定性提升至 Beta。

### PR #137116: Promote `apiserver_watch_events_total` and `apiserver_watch_events_sizes` to BETA
- **链接：** https://github.com/kubernetes/kubernetes/pull/137116
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** area/test, kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/instrumentation, sig/testing, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将 API Server 监控指标 `apiserver_watch_events_total` 和 `apiserver_watch_events_sizes` 从 Alpha 稳定性提升至 Beta。

### PR #137204: Conditional Authz [1/n]: Add conditional capabilities to the authorizer interface
- **链接：** https://github.com/kubernetes/kubernetes/pull/137204
- **状态：** closed
- **已合并：** 是
- **作者：** luxas
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  为授权器（Authorizer）接口添加条件授权能力，这是实现细粒度、基于运行时属性（如资源名称）进行访问控制系列更改的第一步。

### PR #137543: Fix: kubectl drain --disable-eviction --dry-run=server hanging indefinitely
- **链接：** https://github.com/kubernetes/kubernetes/pull/137543
- **状态：** closed
- **已合并：** 是
- **作者：** kfess
- **标签：** kind/bug, area/test, priority/backlog, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  修复`kubectl drain --disable-eviction --dry-run=server`命令无限挂起的问题。根本原因是`deletePods`路径（当使用`--disable-eviction`时）缺少对`DryRunStrategy == DryRunServer`的检查，导致命令等待永远不会被删除的Pod。PR添加了相应的检查。

### PR #137547: feature: add ServiceName, PodManagementPolicy, and PersistentVolumeClaimRetentionPolicy to kubectl describe statefulset output
- **链接：** https://github.com/kubernetes/kubernetes/pull/137547
- **状态：** closed
- **已合并：** 是
- **作者：** kfess
- **标签：** priority/backlog, area/kubectl, lgtm, release-note, size/M, kind/feature, approved, sig/cli, cncf-cla: yes, triage/accepted
- **变更说明：**
  增强`kubectl describe statefulset`命令的输出信息。新增显示`ServiceName`、`PodManagementPolicy`和`PersistentVolumeClaimRetentionPolicy`这三个字段，为用户提供更完整的StatefulSet配置视图。

### PR #137582: KEP-3926: Ensure corruption at latest revision for "unsafe delete" path.
- **链接：** https://github.com/kubernetes/kubernetes/pull/137582
- **状态：** closed
- **已合并：** 是
- **作者：** benluddy
- **标签：** kind/bug, area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  根据 KEP-3926，增强 etcd 损坏检测测试，确保在 'unsafe delete' 路径下，即使是最新修订版本也能检测到数据损坏。

### PR #137666: Parallel pod management should not count old, broken pods for maxUnavailable budget
- **链接：** https://github.com/kubernetes/kubernetes/pull/137666
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/XL, sig/apps, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 v1.35 中 StatefulSet 使用 Parallel Pod 管理策略时的回归问题：不可用的旧版本 Pod 不再被错误计入 `maxUnavailable` 预算，从而允许滚动更新继续进行。

### PR #137755: Remove SidecarContainers feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/137755
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** area/test, kind/cleanup, sig/scheduling, lgtm, sig/node, release-note, size/L, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, api-review, needs-triage
- **变更说明：**
  移除了已稳定的SidecarContainers特性门控（Feature Gate）。Sidecar容器功能现在默认启用，无需通过门控开启。

### PR #137767: Adding prometheues metrics for Kubeproxy failed loadbalancer operations.
- **链接：** https://github.com/kubernetes/kubernetes/pull/137767
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** sig/network, area/kube-proxy, lgtm, release-note, size/L, kind/feature, approved, sig/windows, cncf-cla: yes, sig/instrumentation, ok-to-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  为Windows kube-proxy（winkernel）的负载均衡器操作失败新增了三个ALPHA稳定性Prometheus计数器指标，分别追踪创建、更新、删除失败，并附带ip_family、lb_type、error标签以增强可观测性。

### PR #137883: add support for invariant testing in integration testing
- **链接：** https://github.com/kubernetes/kubernetes/pull/137883
- **状态：** closed
- **已合并：** 是
- **作者：** lalitc375
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  在集成测试框架中增加了不变性（invariant）测试支持。StartTestServer在测试结束时自动验证不变性指标，可通过DisableInvariantChecks选项禁用。

### PR #138000: Delete remote endpoint if it has same ip as local endpoint in the system.
- **链接：** https://github.com/kubernetes/kubernetes/pull/138000
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/XL, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复Windows L2Bridge网络下IP地址重用导致的端点重复问题。当本地与远程端点IP相同时，kube-proxy会错误地增加陈旧远程端点的引用计数。解决方案是在`getAllEndpointsByNetwork`中，如果发现远程端点与本地端点IP相同，则删除该远程端点。

### PR #138003: pkg/registry/core/pod/storage: add PDB-specific CauseType to eviction forbidden errors
- **链接：** https://github.com/kubernetes/kubernetes/pull/138003
- **状态：** closed
- **已合并：** 是
- **作者：** shady0503
- **标签：** lgtm, sig/node, release-note, size/M, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  为Pod Disruption Budget (PDB)相关的驱逐禁止错误添加两个新的`CauseType`常量：`DisruptionBudgetNegativeAllowedDisruptions`和`DisruptionBudgetTooManyDisruptedPods`。这使得客户端无需解析错误信息字符串，即可通过`errors.HasStatusCause`方法以类型安全的方式区分具体的错误原因。

### PR #138088: kubelet: enforce explicit HTTP method restrictions for logs-related endpoints
- **链接：** https://github.com/kubernetes/kubernetes/pull/138088
- **状态：** closed
- **已合并：** 是
- **作者：** amritansh1502
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  加强kubelet日志相关HTTP端点的安全性，明确限制允许的HTTP方法。对于只读端点（如`/pods`， `/containerLogs/...`）强制仅允许`GET`方法；对于NodeLogQuery (`/logs`) 端点明确允许`GET`和`POST`方法，并对其他方法返回405状态码及正确的`Allow`头部。

### PR #138090: kubeadm: add kubeproxydaemonset patch target
- **链接：** https://github.com/kubernetes/kubernetes/pull/138090
- **状态：** closed
- **已合并：** 是
- **作者：** SataQiu
- **标签：** priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, kind/feature, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubeadm 新增 `kubeproxydaemonset` 补丁目标，允许用户通过 `kubeadm upgrade` 或 `kubeadm config` 命令直接对 kube-proxy DaemonSet 进行配置管理。

### PR #138094: kubectl: honor --label-columns with custom-columns
- **链接：** https://github.com/kubernetes/kubernetes/pull/138094
- **状态：** closed
- **已合并：** 是
- **作者：** ahmadmaha02
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  修复 kubectl get 命令中 `--label-columns` 与 `-o custom-columns` 同时使用时被静默忽略的问题，现在会在 `GetOptions.Validate` 中验证并返回明确错误。

### PR #138260: use `json:""` consistently for inlined fields
- **链接：** https://github.com/kubernetes/kubernetes/pull/138260
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XXL, kind/api-change, sig/auth, sig/apps, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, sig/cloud-provider, needs-priority, area/dependency, triage/accepted, sig/etcd, wg/device-management
- **变更说明：**
  将API Go类型中内联的TypeMeta字段的json标签从",inline"统一更改为""。因为"inline"并非合法的JSON序列化选项，此举需更新kube-openapi、gengo等依赖，影响范围广泛。

### PR #138488: DRA Extended Resource: promote to GA in 1.37
- **链接：** https://github.com/kubernetes/kubernetes/pull/138488
- **状态：** closed
- **已合并：** 是
- **作者：** yliaog
- **标签：** area/test, area/kubelet, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-sig, area/code-generation, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将Dynamic Resource Allocation (DRA) Extended Resource功能从Beta提升至GA（正式可用）状态，计划在Kubernetes 1.37版本中发布。这是一个API变更。

### PR #138572: Converts the DisruptionMode enum field to struct as v1alpha3 and drops v1alpha2
- **链接：** https://github.com/kubernetes/kubernetes/pull/138572
- **状态：** closed
- **已合并：** 是
- **作者：** dom4ha
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, area/kubectl, lgtm, sig/node, sig/api-machinery, size/XXL, kind/api-change, kind/feature, release-note-action-required, sig/apps, approved, sig/cli, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, needs-triage, sig/etcd, wg/device-management
- **变更说明：**
  将`scheduling.k8s.io` API组中的`DisruptionMode`枚举字段转换为结构体，以支持未来的扩展性。由于此变更为破坏性更改，API组版本从`v1alpha2`升级至`v1alpha3`，并完全移除`v1alpha2`。用户升级时需注意清理旧的`v1alpha2`对象。

### PR #138653: HPA: Set ObservedGeneration in HPA conditions
- **链接：** https://github.com/kubernetes/kubernetes/pull/138653
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** area/test, priority/important-soon, kind/cleanup, lgtm, sig/api-machinery, release-note, sig/autoscaling, size/L, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, api-review, triage/accepted
- **变更说明：**
  在 HorizontalPodAutoscaler (HPA) 的 Status Conditions 中添加 `ObservedGeneration` 字段，以增强状态跟踪和可观察性。

### PR #138671: kubectl: deprecate run filename flag
- **链接：** https://github.com/kubernetes/kubernetes/pull/138671
- **状态：** closed
- **已合并：** 是
- **作者：** Suknna
- **标签：** area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, kind/deprecation, triage/accepted
- **变更说明：**
  开始弃用 `kubectl run` 命令中无效的 `--filename`/`-f` 标志，该标志被注册但实际未使用，命令仍从命令行参数生成 Pod。

### PR #139057: Store pod nomination before adding the pod to scheduling queue
- **链接：** https://github.com/kubernetes/kubernetes/pull/139057
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/L, approved, cncf-cla: yes, kind/failing-test, needs-priority, needs-triage
- **变更说明：**
  修复调度队列中的数据竞争问题。调整了Pod提名信息的存储时机，确保在将Pod添加到调度队列`之前`就存储其提名信息，从而避免因时序问题导致提名信息丢失或不一致。

### PR #139067: kubeadm: warn if the user has configured kube-proxy with 'ipvs'
- **链接：** https://github.com/kubernetes/kubernetes/pull/139067
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/XS, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, kind/deprecation, triage/accepted
- **变更说明：**
  kubeadm清理与弃用警告。当用户配置kube-proxy使用`ipvs`模式时，kubeadm会在初始化或升级过程中输出警告信息，提示该模式即将被弃用。

### PR #139168: Restore ability to plumb binary data through envvar values
- **链接：** https://github.com/kubernetes/kubernetes/pull/139168
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, kind/api-change, approved, cncf-cla: yes, sig/testing, sig/architecture, kind/regression, triage/accepted
- **变更说明：**
  修复 v1.34 引入的回归问题，恢复通过 Secret API 对象中的二进制（非 UTF-8）数据设置容器环境变量的能力，将 CRI API 相关字段类型从 `string` 改为 `bytes`。

### PR #139212: Lock deprecated DeclarativeValidationTakeover to default in 1.37
- **链接：** https://github.com/kubernetes/kubernetes/pull/139212
- **状态：** closed
- **已合并：** 是
- **作者：** yongruilin
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, needs-priority, kind/deprecation, needs-triage
- **变更说明：**
  在 Kubernetes 1.37 版本中，将已弃用的 `DeclarativeValidationTakeover` 功能门锁定为默认值。

### PR #139251: rename signal enum keys
- **链接：** https://github.com/kubernetes/kubernetes/pull/139251
- **状态：** closed
- **已合并：** 是
- **作者：** SergeyKanzhelev
- **标签：** area/test, area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/XL, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  重命名 CRI API 中 `Signal` 枚举的键名，为其添加 `SIGNAL_` 前缀（如 `SIGNAL_SIGABRT`），以避免与 C++ 宏命名冲突，此更改不影响线格式。

---
*本报告由 Containerd Release Tracker 自动生成*
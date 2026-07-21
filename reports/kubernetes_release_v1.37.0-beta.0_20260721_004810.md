# Kubernetes 版本发布分析报告
## v1.37.0-beta.0 (v1.37.0-beta.0)

### 📋 版本信息
- **版本标签：** v1.37.0-beta.0
- **版本名称：** v1.37.0-beta.0
- **发布时间：** 2026-07-20T23:21:18Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.37.0-beta.0

### 🔍 分析统计
- **分析时间：** 2026-07-21 00:48:10
- **分析的 PR 数量：** 42
- **分析的 Issue 数量：** 14
- **重要项目数量：** 54

## 📊 版本概述
Kubernetes v1.37.0-beta.0 是一个功能丰富的版本，重点关注调度增强（PodGroup、Workload-Aware Preemption）、DRA（Dynamic Resource Allocation）稳定性和关键 Bug 修复，包含多项 API 升级和重要的安全修复。

## 🔒 安全问题修复
1. ⚠️ 修复 kubectl cluster-info dump 输出文件权限过宽，可能泄露 Pod 日志中敏感信息的问题 - [PR #140189](https://github.com/kubernetes/kubernetes/pull/140189) - **风险级别：** 高 - 之前文件默认创建为 0644（全局可读），Pod 日志常包含令牌、凭证等敏感信息
2. ⚠️ 更新 kube-proxy 镜像中的 nftables 到 1.0.6.1，修复与系统上较新 nftables 版本不兼容导致的崩溃 - [PR #140405](https://github.com/kubernetes/kubernetes/pull/140405) - **风险级别：** 中 - 可能导致 kube-proxy 持续崩溃，影响集群网络

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kube-apiserver 在身份 Lease 无法创建时（如主机名超过 63 字节）收到 SIGTERM 后死锁无法关闭的问题 - [PR #140241](https://github.com/kubernetes/kubernetes/pull/140241) - **影响：** 导致 apiserver 无法正常关闭，只能通过 SIGKILL 强制终止，影响集群维护和滚动升级
2. 修复 kube-proxy 在节点 IP 变更或节点删除后不重启，导致网络状态过时的问题 - [PR #138183](https://github.com/kubernetes/kubernetes/pull/138183) - **影响：** 节点网络配置变更后 kube-proxy 可能使用旧的网络信息，导致服务流量路由错误
3. 修复 DRA 结构化分配器在拒绝或回溯候选设备时泄漏预留计数器和约束的问题 - [PR #140431](https://github.com/kubernetes/kubernetes/pull/140431) - **影响：** 可能导致可调度的 Pod 因资源计数错误而持续处于 Pending 状态
4. 修复 CEL 准入控制器在处理三键类型 Map 列表时可能 panic 的问题 - [PR #140386](https://github.com/kubernetes/kubernetes/pull/140386) - **影响：** 特定 CEL 验证规则可能导致 apiserver 崩溃
5. 修复 Burstable QoS Pod 的 memory.low cgroup 设置因缺少祖先覆盖而无效的问题 - [PR #140267](https://github.com/kubernetes/kubernetes/pull/140267) - **影响：** Burstable Pod 的内存保护可能不生效，在内存压力下被过早驱逐
6. 修复 kubelet 在跨资源设备 ID 冲突时将设备健康更新路由到错误 Pod 的问题 - [PR #140323](https://github.com/kubernetes/kubernetes/pull/140323) - **影响：** 设备健康状态更新可能影响错误的 Pod，导致不必要的状态同步和潜在调度问题
7. 修复 DRA ResourceSlice 控制器在快速删除后更新时使用 MutationCache 中过时副本的问题 - [PR #140063](https://github.com/kubernetes/kubernetes/pull/140063) - **影响：** DRA 驱动重启更新期间，kubelet 删除 ResourceSlice 后控制器可能无法正确重新创建
8. 修复容器状态中 Linux UID 大于 INT32_MAX 时被错误拒绝的问题 - [PR #138574](https://github.com/kubernetes/kubernetes/pull/138574) - **影响：** 使用高 UID（> 2,147,483,647）的容器会卡在 ContainerCreating 状态
9. 修复启用 DRAListTypeAttributes 时，matchAttribute 约束在回溯期间交集计算错误导致设备分配失败的问题 - [PR #140325](https://github.com/kubernetes/kubernetes/pull/140325) - **影响：** 存在有效设备组合时调度失败
10. 修复 CEL 对 'set' 和 'map' 列表的相等性和连接操作语义 - [PR #140293](https://github.com/kubernetes/kubernetes/pull/140293) - **影响：** CEL 验证规则中涉及列表相等和连接的操作可能产生意外结果

## 💥 破坏性变更
1. 🚨 CEL 表达式对 'set' 和 'map' 类型列表的相等性（==）和连接（+）操作语义变更 - [PR #140293](https://github.com/kubernetes/kubernetes/pull/140293) - **影响：** 需要检查并更新所有使用 CEL 进行列表比较或连接的验证规则，确保新语义下仍能正确工作
2. 🚨 MutatingAdmissionPolicy 存储版本覆盖在 v1.37 中移除 - [Issue #138283](https://github.com/kubernetes/kubernetes/issues/138283) - **影响：** 使用 MutatingAdmissionPolicy 的用户需确保客户端兼容 v1 API 版本
3. 🚨 kubectl cluster-info dump 输出文件权限从 0644 改为 0600，目录权限从 0755 改为 0700 - [PR #140189](https://github.com/kubernetes/kubernetes/pull/140189) - **影响：** 自动化脚本若依赖其他用户读取 dump 输出需调整，或修改脚本以适当权限运行
4. 🚨 kube-proxy --metrics-bind-address 文档修正：空字符串不再禁用指标服务器，而是回退到默认地址 - [PR #138940](https://github.com/kubernetes/kubernetes/pull/138940) - **影响：** 依赖文档中“设为空以禁用”行为的用户需改用其他方法禁用指标服务器

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. metrics.k8s.io API 从 v1beta1 升级到 GA (v1) - [PR #139223](https://github.com/kubernetes/kubernetes/pull/139223)
2. ClusterTrustBundles 功能升级到 GA 并默认启用 - [PR #139437](https://github.com/kubernetes/kubernetes/pull/139437)
3. 为 StatefulSet 新增 Recreate 更新策略 - [PR #137187](https://github.com/kubernetes/kubernetes/pull/137187)
4. 引入 Node 生命周期条件（GracefulNodeShutdownInProgress, DrainInProgress 等） - [PR #139993](https://github.com/kubernetes/kubernetes/pull/139993)
5. PodGroup 核心 API 实现（KEP-6012） - [PR #139596](https://github.com/kubernetes/kubernetes/pull/139596)
6. 为 PodGroup 调度新增 PodGroupPostFilter 扩展点 - [PR #139674](https://github.com/kubernetes/kubernetes/pull/139674)
7. 支持原地 Pod 垂直扩缩容的调度器抢占（Alpha 特性） - [PR #140000](https://github.com/kubernetes/kubernetes/pull/140000)
8. PersistentVolumeClaimUnusedSinceTime 字段升级到 Beta - [PR #139620](https://github.com/kubernetes/kubernetes/pull/139620)
9. EtcdRangeStream 特性门默认启用（Beta），提升 watch-cache 初始化性能 - [PR #140085](https://github.com/kubernetes/kubernetes/pull/140085)
10. NativeHistograms 特性门升级到 Beta - [PR #140124](https://github.com/kubernetes/kubernetes/pull/140124)

## 🚀 性能优化
1. 在 kube-proxy informer 中剥离 managedFields 以减少缓存大小 - [PR #140056](https://github.com/kubernetes/kubernetes/pull/140056) - **提升：** 显著减少 kube-proxy 内存使用，特别是大型集群
2. 默认启用 EtcdRangeStream 特性门，优化 watch-cache 初始化 - [PR #140085](https://github.com/kubernetes/kubernetes/pull/140085) - **提升：** watch-cache 初始化速度提升约 30%，内存使用减少约 9%
3. 调度器指标 plugin_execution_duration_seconds 和 scheduling_algorithm_duration_seconds 升级到 BETA - [PR #138176](https://github.com/kubernetes/kubernetes/pull/138176) - **提升：** 提供更稳定的调度性能监控指标
4. 新增 PodGroup 级别调度队列指标 - [PR #139840](https://github.com/kubernetes/kubernetes/pull/139840) - **提升：** 增强对 Gang Scheduling 工作负载的监控能力

## 🎯 风险评估
整体风险评估：中等。此版本包含多个关键稳定性修复和安全补丁，建议升级。主要风险来自 CEL 语义变更可能破坏现有验证规则，以及 DRA 相关改动可能影响设备感知调度。建议的升级时机：在充分测试 CEL 策略和 DRA 功能后，尽快安排升级以获取安全修复。需要特别关注的方面：1) CEL 验证规则测试；2) DRA 设备分配功能验证；3) 调度器行为变化对工作负载的影响；4) kubectl 权限变更对自动化流程的影响。

## 📋 升级建议
1. **立即行动：** 如果使用 kubectl cluster-info dump 进行故障排查，升级到该版本以修复敏感信息泄露漏洞。检查现有 dump 文件权限并清理。
2. **测试重点：** 升级前在测试环境中充分验证 CEL 准入策略，特别是涉及列表操作的部分。
3. **DRA 用户：** 如果使用 Dynamic Resource Allocation 和设备插件，仔细测试设备分配和健康监控功能，确保修复生效。
4. **调度优化：** 关注 PodGroup 和 Workload-Aware Preemption 相关功能，评估其对批处理工作负载调度的影响。
5. **监控更新：** 利用新的调度器 BETA 指标和 PodGroup 级别指标优化监控和告警。
6. **升级准备：** 确保主机名不超过 63 字节，避免触发 kube-apiserver 关闭死锁问题（虽已修复，但仍建议规范命名）。
7. **权限检查：** 审查所有依赖 kubectl cluster-info dump 输出的自动化流程，确保有适当权限读取新创建的文件。

## 📋 Release 包含的变更

### PR #134037: KEP-3926: implement dry-run support for unsafe corrupt object deletion
- **链接：** https://github.com/kubernetes/kubernetes/pull/134037
- **状态：** closed
- **已合并：** 是
- **作者：** ibihim
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  为 KEP-3926 的不安全损坏对象删除功能实现 dry-run 支持。允许管理员在执行前安全测试删除操作，遵循标准 dry-run 模式，需启用 AllowUnsafeMalformedObjectDeletion 特性门控。

### PR #137150: [PodLevelResources] Fix handling of empty pod-level resources
- **链接：** https://github.com/kubernetes/kubernetes/pull/137150
- **状态：** closed
- **已合并：** 是
- **作者：** KevinTMtz
- **标签：** sig/scheduling, area/kubectl, lgtm, sig/node, release-note, size/XL, kind/api-change, sig/apps, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  **PR #137150:** [PodLevelResources] Fix handling of empty pod-level resources
**标签:** sig/scheduling, area/kubectl, lgtm, sig/node, release-note, size/XL, kind/api-change, sig/apps, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contr...

### PR #137187: Add recreate update strategy to statefulsets
- **链接：** https://github.com/kubernetes/kubernetes/pull/137187
- **状态：** closed
- **已合并：** 是
- **作者：** galal-hussein
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/XXL, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, tide/merge-method-squash, ok-to-test, api-review, area/e2e-test-framework, triage/accepted
- **变更说明：**
  为StatefulSet添加了 `Recreate` 更新策略，这是一个新的API变更和功能。该策略允许StatefulSet在更新时一次性删除所有旧Pod再创建新Pod，类似于Deployment的行为，增强了StatefulSet的更新灵活性。

### PR #137375: apiserver: fix autocalculation of emulated version
- **链接：** https://github.com/kubernetes/kubernetes/pull/137375
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** area/test, kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted, sig/etcd
- **变更说明：**
  修复 apiserver 模拟版本自动计算问题，涉及 MutatingAdmissionPolicy 和 MutatingAdmissionPolicyBinding 的 GA 迁移 (v1.36)。确保在模拟版本 1.34 时存储版本正确选择 v1beta1，并跳过 alpha 版本进行 n-1 兼容性搜索。

### PR #137699: DRA: KEP-5304: add e2e test for discoverable device metadata
- **链接：** https://github.com/kubernetes/kubernetes/pull/137699
- **状态：** closed
- **已合并：** 是
- **作者：** alaypatel07
- **标签：** area/test, priority/backlog, sig/scheduling, lgtm, sig/node, release-note, size/L, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  为KEP-5304（Dynamic Resource Allocation， DRA）添加了端到端（e2e）测试，用于验证可发现的设备元数据（discoverable device metadata）功能。这是一个测试增强和清理工作。

### PR #137981: Feature/pod group as victim
- **链接：** https://github.com/kubernetes/kubernetes/pull/137981
- **状态：** closed
- **已合并：** 是
- **作者：** vshkrabkov
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  增强了标准Pod-by-Pod抢占流程，使其支持将PodGroup视为一个原子抢占受害者（victim）。通过引入 `Victim` 和 `DomainVictim` 接口抽象，抢占算法可以按组进行决策，这是工作负载感知调度（WAS）功能的一部分。

### PR #138176: scheduler: graduate plugin_execution_duration_seconds and scheduling_algorithm_duration_seconds metrics to BETA
- **链接：** https://github.com/kubernetes/kubernetes/pull/138176
- **状态：** closed
- **已合并：** 是
- **作者：** abhay1999
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/testing, ok-to-test, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将调度器的两个指标从 ALPHA 升级到 BETA 稳定性级别：`scheduler_plugin_execution_duration_seconds`（插件执行时长）和 `scheduler_scheduling_algorithm_duration_seconds`（调度算法延迟）。这是 #136311 工作的一部分，标志着所有调度器核心指标均已进入 BETA 阶段。

### PR #138183: Restart kube-proxy on node IP changes and deletion
- **链接：** https://github.com/kubernetes/kubernetes/pull/138183
- **状态：** closed
- **已合并：** 是
- **作者：** abishekgiri
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复 kube-proxy 在监听的 Node IP 变更或 Node 对象被删除时不会重启的问题。此前 NodeManager 中的退出路径被注释掉，导致 kube-proxy 可能使用过时的网络状态。本次修复恢复了该重启逻辑，确保 kube-proxy 能及时更新节点网络信息。

### PR #138188: Improve error messages for invalid restart policy and image pull policy
- **链接：** https://github.com/kubernetes/kubernetes/pull/138188
- **状态：** closed
- **已合并：** 是
- **作者：** ogormans-deptstack
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  改进 kubectl 中 `--restart` 和 `--image-pull-policy` 标志的错误信息。当用户输入无效值时，错误信息现在会列出所有有效值（例如 `Always, OnFailure, Never`），帮助用户快速纠正，无需查阅文档。

### PR #138363: Address DRA controller feedback from DRAWorkloadResourceClaims implementation
- **链接：** https://github.com/kubernetes/kubernetes/pull/138363
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** area/test, kind/cleanup, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management, wg/workload-aware-scheduling
- **变更说明：**
  基于对DRAWorkloadResourceClaims实现的反馈，对DRA（Dynamic Resource Allocation）控制器逻辑进行了一系列清理和改进。涉及多个SIG（如scheduling, node, api-machinery），属于代码优化。

### PR #138574: pkg/apis/core: allow uint32 Linux UIDs in container status
- **链接：** https://github.com/kubernetes/kubernetes/pull/138574
- **状态：** closed
- **已合并：** 是
- **作者：** Kunalbehbud
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/M, kind/api-change, sig/apps, approved, cncf-cla: yes, tide/merge-method-squash, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复容器状态中 Linux UID 的验证范围。Linux UID 为 32 位无符号整数，但此前 pod status 验证沿用 pod spec 的 int32 范围，导致大于 2147483647 的有效 UID 被拒绝。现保持 pod spec `runAsUser` 验证不变，仅放宽容器状态中 `containerStatus.user.linux.uid` 的验证范围至 uint32。

### PR #138809: kubectl explain: add --max-depth flag
- **链接：** https://github.com/kubernetes/kubernetes/pull/138809
- **状态：** closed
- **已合并：** 是
- **作者：** shady0503
- **标签：** area/test, priority/backlog, area/kubectl, lgtm, release-note, size/XL, kind/feature, approved, sig/cli, cncf-cla: yes, sig/testing, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  为 kubectl explain 添加 --max-depth=N 标志，用于限制递归输出深度。当 N>0 时隐含 --recursive，便于查看大型资源（如 Pod、Deployment）的模式概览，支持 OpenAPIv2 和 v3。

### PR #138940: Fix kube-proxy metrics-bind-address doc string inconsistency
- **链接：** https://github.com/kubernetes/kubernetes/pull/138940
- **状态：** closed
- **已合并：** 是
- **作者：** kairosci
- **标签：** kind/bug, sig/network, kind/documentation, area/kube-proxy, lgtm, release-note, size/XS, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复 kube-proxy 中 `--metrics-bind-address` 标志的文档错误。原文档错误地声称设置为空字符串会禁用 metrics server，实际上由于 v1alpha1 配置和命令行标志默认机制，空字符串会导致回退到默认地址 `127.0.0.1:10249`。本次修改移除了误导性描述，解决了文档不一致问题。

### PR #139223: KEP-5207: Promote metrics.k8s.io to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/139223
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** lgtm, release-note, size/XL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/instrumentation, area/code-generation, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  将 `metrics.k8s.io` API 从 v1beta1 升级到 v1，正式进入 GA（General Availability）阶段。这是 KEP-5207 的实现，API 本身功能没有变化，标志着该 API 已稳定。

### PR #139373: Add metrics related to workload-aware preemption
- **链接：** https://github.com/kubernetes/kubernetes/pull/139373
- **状态：** closed
- **已合并：** 是
- **作者：** brejman
- **标签：** sig/scheduling, lgtm, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/instrumentation, needs-priority, triage/accepted, area/stable-metrics, wg/workload-aware-scheduling
- **变更说明：**
  添加了与工作负载感知抢占（workload-aware preemption）相关的新监控指标。这是一个功能增强，旨在为调度器的抢占决策提供更丰富的可观测性数据。

### PR #139437: ClusterTrustBundles - GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/139437
- **状态：** closed
- **已合并：** 是
- **作者：** stlaz
- **标签：** area/test, area/kubelet, area/apiserver, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, sig/architecture, area/conformance, area/code-generation, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将 ClusterTrustBundles 和 ClusterTrustBundleProjection 特性升级至 GA (稳定版) 并默认启用。这是一个涉及多个 SIG 的大型 API 变更。

### PR #139596: KEP-6012: Implement core CompositePodGroup API [WAS]
- **链接：** https://github.com/kubernetes/kubernetes/pull/139596
- **状态：** closed
- **已合并：** 是
- **作者：** jdzikowski
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, ok-to-test, needs-priority, needs-triage, sig/etcd, wg/device-management, wg/workload-aware-scheduling
- **变更说明：**
  **PR #139596:** KEP-6012: Implement core CompositePodGroup API [WAS]
**标签:** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, ok-to-test, needs-priority, needs-triage, sig/etcd, wg/device-management, wg/workload-aware-s...

### PR #139613: On successful scheduling of podgroup, requeue remaining pods directly to active queue.
- **链接：** https://github.com/kubernetes/kubernetes/pull/139613
- **状态：** closed
- **已合并：** 是
- **作者：** iomarsayed
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  优化 PodGroup 调度逻辑：当一个 PodGroup 成功调度后，其剩余未调度的 Pod 将被直接重新排队到 active 队列（而非 backoff 队列），并保留原有的时间戳。这确保了这些 Pod 能在下一个调度周期中立即参与调度或抢占，除非有更高优先级的实体介入。

### PR #139620: Promote PersistentVolumeClaimUnusedSinceTime to Beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/139620
- **状态：** closed
- **已合并：** 是
- **作者：** RomanBednar
- **标签：** lgtm, release-note, size/S, kind/api-change, sig/apps, approved, cncf-cla: yes, api-review
- **变更说明：**
  将 `PersistentVolumeClaimUnusedSinceTime` 字段从Alpha阶段提升至Beta阶段。这是一个API变更，该字段用于标记持久卷声明（PVC）自何时起未被使用，有助于资源清理。

### PR #139674: Feature: Add PodGroupPostFilter extension point
- **链接：** https://github.com/kubernetes/kubernetes/pull/139674
- **状态：** closed
- **已合并：** 是
- **作者：** GFilipek
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, area/code-generation, ok-to-test, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  引入新的调度器框架扩展点 PodGroupPostFilter。该扩展点在 PostFilter 之后运行，但操作对象是 PodGroup (用于 GangScheduling)，为工作负载感知抢占 (KEP-5710) 提供可配置接口。

### PR #139840: Add podgroup level metrics
- **链接：** https://github.com/kubernetes/kubernetes/pull/139840
- **状态：** closed
- **已合并：** 是
- **作者：** iomarsayed
- **标签：** sig/network, sig/scheduling, area/kube-proxy, lgtm, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/instrumentation, area/ipvs, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  为调度器引入两个新的 podgroup 级别指标：`queued_entities`（当前队列中待处理的实体数）和 `queue_incoming_entities_total`（进入队列的实体总数）。这两个指标通过 `entity_type` 标签区分统计的是单个 Pod 还是 PodGroup，增强了调度队列的监控能力。

### PR #139929: dra: add standard numaNode device attribute with SLIT-based helpers
- **链接：** https://github.com/kubernetes/kubernetes/pull/139929
- **状态：** closed
- **已合并：** 是
- **作者：** johnahull
- **标签：** lgtm, sig/node, release-note, size/XL, kind/feature, approved, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted, wg/device-management
- **变更说明：**
  为 DRA 添加标准 resource.kubernetes.io/numaNode 设备属性 (KEP-6072)，支持通过 matchAttribute 实现跨驱动 NUMA 协同放置。提供辅助函数根据 PCI Bus ID 或 CPU 核心获取 NUMA 节点属性，需配置 AttributeForm 参数。

### PR #139980: Reimplement WAP with in place filter reprieval
- **链接：** https://github.com/kubernetes/kubernetes/pull/139980
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  根据 KEP-5710 重新实现 Workload-Aware Preemption (WAP)。主要变更包括：移除受害者后仅运行一次调度算法、重用调度算法的 CycleState 进行受害者恢复、为每个抢占者运行 Filter 插件。虽然存在已知的 Snapshot 状态更新问题，但不影响功能实现。

### PR #139993: Introduce Node Lifecycle Conditions
- **链接：** https://github.com/kubernetes/kubernetes/pull/139993
- **状态：** closed
- **已合并：** 是
- **作者：** rthallisey
- **标签：** priority/backlog, lgtm, sig/node, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, api-review, triage/accepted, wg/node-lifecycle
- **变更说明：**
  为 Node 对象引入一组标准的生命周期条件，包括：`GracefulNodeShutdownInProgress`、`DrainInProgress`、`Drained`、`MaintenancePlanned`、`MaintenanceInProgress`。这些条件提供了 Node 在关机、排水、维护等关键生命周期事件中的状态信息。

### PR #140000: feat: Scheduler Preemption for In-Place Pod Resize (alpha)
- **链接：** https://github.com/kubernetes/kubernetes/pull/140000
- **状态：** closed
- **已合并：** 是
- **作者：** natasha41575
- **标签：** area/test, priority/important-soon, area/kubelet, sig/scheduling, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, api-review, needs-triage, wg/device-management
- **变更说明：**
  为原地Pod垂直扩缩容（In-Place Pod Resize）实现了调度器抢占（Scheduler Preemption）功能，作为Alpha特性通过特性门控 `InPlacePodVerticalScalingSchedulerPreemption` 启用。根据相关讨论，kubelet端的关键Pod抢占将不适用于resize操作，转而依赖调度器端的抢占逻辑。

### PR #140019: Implement Exclusion of Virtual Resources from Admission Webhooks
- **链接：** https://github.com/kubernetes/kubernetes/pull/140019
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  实现了从准入Webhook调用中排除虚拟资源（如 `PodMetrics`）的功能。这是一个新特性，旨在避免对不真实存在的资源对象进行不必要的Webhook验证，提升性能与兼容性。

### PR #140056: Strip managedFields in kube-proxy informers to reduce informer cache size
- **链接：** https://github.com/kubernetes/kubernetes/pull/140056
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** sig/network, kind/cleanup, area/kube-proxy, lgtm, release-note, size/S, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  优化 kube-proxy 内存使用，通过从 informer 接收的对象中剥离 .metadata.managedFields 字段来减少缓存大小，该字段 kube-proxy 不需要。

### PR #140063: DRA resourceslice controller: fix update after quick delete
- **链接：** https://github.com/kubernetes/kubernetes/pull/140063
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, area/test, lgtm, sig/node, sig/api-machinery, release-note, size/XL, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DRA ResourceSlice 控制器在快速删除后更新时的问题。MutationCache 缓存了过时副本导致控制器未重新创建已删除的 ResourceSlice。通过让缓存响应底层存储的变化来修复，用户需在事件处理程序中通知缓存。

### PR #140085: Enable EtcdRangeStream feature gate by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/140085
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将 EtcdRangeStream 特性门控默认启用 (进入 Beta 阶段)。该特性使 watch-cache 初始化速度提升约 1.4 倍，内存使用减少约 8.85%。

### PR #140124: Graduate NativeHistograms feature gate to Beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/140124
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** lgtm, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/architecture, needs-priority, needs-triage
- **变更说明：**
  将 `NativeHistograms` 特性门控从 Alpha 升级到 Beta 阶段。该特性用于增强 Prometheus 指标中的直方图功能。

### PR #140189: kubectl: create cluster-info dump output with owner-only permissions
- **链接：** https://github.com/kubernetes/kubernetes/pull/140189
- **状态：** closed
- **已合并：** 是
- **作者：** ashvinctrl
- **标签：** kind/bug, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, sig/security, triage/accepted
- **变更说明：**
  修复 kubectl cluster-info dump --output-directory 命令的文件权限问题。现在创建的目录权限为 0700，文件权限为 0600，确保转储的集群状态（可能包含敏感信息）仅对运行命令的用户可读。

### PR #140241: :bug: fix:(kube-apiserver): hanging forever on SIGTERM when its identity Lease cannot be created (e.g. hostname longer than 63 bytes)
- **链接：** https://github.com/kubernetes/kubernetes/pull/140241
- **状态：** closed
- **已合并：** 是
- **作者：** camilamacedo86
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复 kube-apiserver 在无法创建身份 Lease（如主机名超过 63 字节）时，收到 SIGTERM 信号会永久挂起的回归问题。问题源于 lease 控制器在持有锁时无限重试创建。通过添加 `stopCh` 使重试在关闭时及时返回，确保优雅关机能正常进行。

### PR #140267: Fix burstable memory.low being ineffective due to missing ancestor coverage
- **链接：** https://github.com/kubernetes/kubernetes/pull/140267
- **状态：** closed
- **已合并：** 是
- **作者：** sohankunkerkar
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  修复了Burstable QoS Pod的 `memory.low` cgroup设置因缺少祖先cgroup覆盖而无效的问题。此bug导致Burstable Pod在内存压力下无法获得预期的内存保护，影响kubelet的内存管理。

### PR #140293: CEL reflective wrappers (5): Keep set-list union semantics on CEL concatenation results
- **链接：** https://github.com/kubernetes/kubernetes/pull/140293
- **状态：** closed
- **已合并：** 是
- **作者：** jpbetz
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复 CEL 中 set 和 map 列表的相等性 (==) 和连接 (+) 操作。相等性不再匹配包含重复项的列表，连接操作现在正确应用 set/map 合并语义到追加元素，确保顺序不敏感的并集相等性。

### PR #140311: Propagate preemption status message to pod group status
- **链接：** https://github.com/kubernetes/kubernetes/pull/140311
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  将工作负载感知抢占 (Workload Aware Preemption) 运行时的状态消息传播到 PodGroup 状态。当为 PodGroup 找到放置位置时，状态消息会包含抢占的受害者数量信息。

### PR #140323: kubelet: fix device health updates being routed to the wrong pod when device IDs collide across resources
- **链接：** https://github.com/kubernetes/kubernetes/pull/140323
- **状态：** closed
- **已合并：** 是
- **作者：** harche
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, kind/flake, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复设备健康更新可能被路由到错误 Pod 的问题。当不同资源下设备 ID 冲突时，设备管理器查找会出错。修复方法是在 getPodAndContainerForDevice 中同时匹配资源名称和设备 ID。

### PR #140325: KEP-5491: restore the intersection on backtrack in `matchAttribute` constraint when DRAListTypeAttributes is enabled
- **链接：** https://github.com/kubernetes/kubernetes/pull/140325
- **状态：** closed
- **已合并：** 是
- **作者：** everpeace
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 KEP-5491 实现中的 bug：当 DRAListTypeAttributes 启用时，在回溯过程中恢复 matchAttribute 约束的交集操作，确保列表类型属性约束在搜索中正确应用。

### PR #140359: KEP-5710: Validate matching preemption policy across all pods when scheduling pod groups [WAS]
- **链接：** https://github.com/kubernetes/kubernetes/pull/140359
- **状态：** closed
- **已合并：** 是
- **作者：** ania-borowiec
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  **PR #140359:** KEP-5710: Validate matching preemption policy across all pods when scheduling pod groups [WAS]
**标签:** area/test, sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/workload-aware-scheduling

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first tim...

### PR #140386: fix: Prevent CEL Admission Panics on Three-Key Typed Map Lists
- **链接：** https://github.com/kubernetes/kubernetes/pull/140386
- **状态：** closed
- **已合并：** 是
- **作者：** weizhoublue
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了apiserver中CEL准入控制在处理具有三个 `listMapKey` 字段的 `listType=map` 列表时可能引发的panic问题。这是一个针对特定数据结构的bug修复。

### PR #140405: Use new distroless-iptables v0.9.4 with nft 1.0.6.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/140405
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, area/test, lgtm, release-note, size/XS, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  将kube-proxy镜像中的基础镜像更新为包含 nftables 1.0.6.1 的 distroless-iptables v0.9.4，以修复在已存在由新版nftables（如1.1.3）创建规则的系统上，kube-proxy在nftables模式下同步失败并崩溃的问题（修复Issue #136786）。

### PR #140431: DRA: roll back reserved state in allocateDevice
- **链接：** https://github.com/kubernetes/kubernetes/pull/140431
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, lgtm, sig/node, release-note, size/XL, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复结构化 DRA 分配器在拒绝候选设备时可能遗留预留状态的问题。通过引入 deviceRollbackState 记录突变并统一回滚，确保设备计数器预留不会泄漏，避免可调度 Pod 调度失败。

### PR #140654: Fix status wiping api definition test and fix gaps
- **链接：** https://github.com/kubernetes/kubernetes/pull/140654
- **状态：** closed
- **已合并：** 是
- **作者：** jpbetz
- **标签：** area/test, kind/cleanup, sig/scheduling, lgtm, sig/api-machinery, release-note, size/M, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复了API定义测试中的一个排序bug，该bug导致测试无法正确检测 `GetResetFields` 方法的错误实现。同时修复了PodGroup、PodCompositeGroup和PodCertificateRequest资源在Server-Side Apply中状态字段（status）未被正确清除的问题。

---
*本报告由 Containerd Release Tracker 自动生成*
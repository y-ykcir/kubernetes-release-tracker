# Kubernetes 版本发布分析报告
## v1.38.0-alpha.1 (v1.38.0-alpha.1)

### 📋 版本信息
- **版本标签：** v1.38.0-alpha.1
- **版本名称：** v1.38.0-alpha.1
- **发布时间：** 2026-09-29T08:46:22Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.38.0-alpha.1

### 🔍 分析统计
- **分析时间：** 2026-09-29 09:47:25
- **分析的 PR 数量：** 45
- **分析的 Issue 数量：** 14
- **重要项目数量：** 54

## 📊 版本概述
Kubernetes v1.38.0-alpha.1 是一个早期预发布版本，主要聚焦于清理已毕业的特性门控、修复多个关键Bug、增强调度器稳定性与安全性，并移除部分已废弃的API。

## 🔒 安全问题修复
1. ⚠️ 修复 kube-scheduler 在日志级别 `-v=2` 时，将调度器扩展器配置中的TLS私钥（keyData）以base64形式记录到日志中 - [PR #140519](https://github.com/kubernetes/kubernetes/pull/140519) - **风险级别：** 中 - 仅影响配置了扩展器TLS内联证书且开启`-v=2`日志的场景
2. ⚠️ 修复 kubelet 在启动时，将 `--manifest-url-header` 配置的头部值（如Authorization令牌）以明文记录到日志中 - [PR #140220](https://github.com/kubernetes/kubernetes/pull/140220) - **风险级别：** 中 - 影响使用静态Pod URL并配置了认证头部的kubelet
3. ⚠️ 修复 kubectl debug 的 sysadmin 配置文件，使其能感知Windows节点并应用正确的Host Process Container配置，而非Linux特权模式 - [PR #138182](https://github.com/kubernetes/kubernetes/pull/138182) - **风险级别：** 低 - 增强了Windows节点调试的安全性

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复调度器预抢占时，使用过滤器扩展器（filter extenders）导致的错误 - [PR #135486](https://github.com/kubernetes/kubernetes/pull/135486) - **影响：** 使用调度器扩展器的集群，预抢占可能失败，影响高优先级Pod的调度
2. 修复设备管理器（Device Manager）在重建 allocatedDevices 时可能丢失进行中（in-flight）的设备预留，导致同一设备被分配给多个Pod - [PR #137534](https://github.com/kubernetes/kubernetes/pull/137534) - **影响：** 使用GPU、FPGA等扩展资源的集群可能出现设备分配冲突，导致Pod启动失败或设备访问错误
3. 修复调度队列中因竞争条件导致Pod被永久忽略的Bug - [PR #139450](https://github.com/kubernetes/kubernetes/pull/139450) - **影响：** 极少数情况下，Pod可能卡在调度队列中无法被调度，且无错误日志
4. 修复 CPUManager 在跨NUMA节点分配独占CPU时，错误地缩小了 TopologyManager 提供的NUMA亲和性范围 - [PR #139456](https://github.com/kubernetes/kubernetes/pull/139456) - **影响：** 配置了 `distribute-cpus-across-numa: "true"` 和 `prefer-closest-numa-nodes: "true"` 的节点，可能无法获得最优的NUMA亲和性，影响性能敏感型工作负载
5. 修复 PersistentVolume 指标 `pv_collector_total_pv_count` 对所有CSI卷错误地报告插件名称为 `N/A` - [PR #139356](https://github.com/kubernetes/kubernetes/pull/139356) - **影响：** 基于此指标的监控和告警（如 `kube_persistentvolume_plugin_type_counts`）会丢失CSI卷的准确分类信息
6. 修复 NodeRestriction 准入插件在解析Pod的CSI卷源失败时，未正确回退检查授权，导致特定情况下节点服务账户令牌请求被错误拒绝 - [PR #140607](https://github.com/kubernetes/kubernetes/pull/140607) - **影响：** 当集群中存在未找到的CSIDriver、PVC或PV时，节点的令牌请求可能失败
7. 修复 code-generator 生成的客户端会覆盖用户传入的 config.NegotiatedSerializer - [PR #140317](https://github.com/kubernetes/kubernetes/pull/140317) - **影响：** 依赖自定义 NegotiatedSerializer 的客户端（如为了保留未知字段）将无法正常工作

## 💥 破坏性变更
1. 🚨 外部调度器插件必须更新：`NominatedPodsForNode` 方法的第一个参数现在必须是 `logger klog.Logger` - [PR #142118](https://github.com/kubernetes/kubernetes/pull/142118) - **影响：** 所有实现此接口的自定义调度器插件需要重新编译并适配新签名，否则升级后会导致调度器崩溃
2. 🚨 移除 metrics.k8s.io/v1alpha1 API - [PR #140862](https://github.com/kubernetes/kubernetes/pull/140862) - **影响：** 任何直接调用此API版本的客户端或工具将失效，应迁移至 metrics.k8s.io/v1beta1
3. 🚨 移除 apidiscovery.k8s.io/v2beta1 API 及 AggregatedDiscoveryRemoveBetaType 特性门控 - [PR #141208](https://github.com/kubernetes/kubernetes/pull/141208) - **影响：** 依赖此API版本的客户端代码需要更新导入路径和类型到 v2
4. 🚨 废弃并重命名指标 `endpoint_slice_controller_changes` 为 `endpoint_slice_controller_changes_total` - [PR #140447](https://github.com/kubernetes/kubernetes/pull/140447) - **影响：** 监控仪表板和告警规则如果使用了旧指标名，需要更新。新版本中两个指标同时存在，旧指标已被标记为废弃
5. 🚨 修复 Quantity 类型中负值舍入逻辑和超大DecimalSI值字符串表示的Bug，可能改变序列化/反序列化行为 - [PR #138510](https://github.com/kubernetes/kubernetes/pull/138510), [PR #140459](https://github.com/kubernetes/kubernetes/pull/140459) - **影响：** 极少数处理极端数值边界或依赖特定字符串表示格式的应用程序可能观察到行为变化

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 移除 PodSchedulingReadiness 特性门控，该功能已永久启用 - [PR #141741](https://github.com/kubernetes/kubernetes/pull/141741)
2. 移除 SeparateTaintEvictionController 特性门控，污点驱逐现在由独立控制器永久处理 - [PR #141789](https://github.com/kubernetes/kubernetes/pull/141789)
3. 外部调度器插件（Out-of-tree kube-scheduler plugins）的 NominatedPodsForNode 方法签名变更，需添加 logger 参数 - [PR #142118](https://github.com/kubernetes/kubernetes/pull/142118)
4. 移除已废弃的 metrics.k8s.io/v1alpha1 API - [PR #140862](https://github.com/kubernetes/kubernetes/pull/140862)
5. 移除已废弃的 apidiscovery.k8s.io/v2beta1 API 及相关特性门控 - [PR #141208](https://github.com/kubernetes/kubernetes/pull/141208)
6. 移除已锁定GA的特性门控 CustomResourceFieldSelectors 和 CRDValidationRatcheting - [PR #141207](https://github.com/kubernetes/kubernetes/pull/141207)
7. 调度器支持在 Topology-Aware Scheduling (TAS) 中尊重 NominatedNodeName - [PR #139472](https://github.com/kubernetes/kubernetes/pull/139472)
8. 为 CompositePodGroup 的 MinGroupCount 字段添加可变性支持，允许动态调整 - [PR #141023](https://github.com/kubernetes/kubernetes/pull/141023)

## 🚀 性能优化
1. 调度器队列指标现在支持 CompositePodGroup - [PR #141800](https://github.com/kubernetes/kubernetes/pull/141800) - **提升：** 为基于CompositePodGroup的工作负载调度提供了可观测性
2. API Server 为聚合的 OpenAPI v2 端点 (`/openapi/v2`) 添加请求指标 - [PR #140888](https://github.com/kubernetes/kubernetes/pull/140888) - **提升：** 完善了API Server的监控覆盖
3. 将 `volume_operation_errors_total` 指标从Alpha升级到Beta稳定性 - [PR #141536](https://github.com/kubernetes/kubernetes/pull/141536) - **提升：** 增强了存储操作错误监控的可靠性

## 🎯 风险评估
整体风险评估：**中高**（对于Alpha版本而言属正常范围）。此版本包含多项破坏性API变更和关键Bug修复，对调度器、设备管理、资源计算等核心子系统有实质性改动。虽然修复了许多严重问题，但新引入的变更本身需要充分测试。建议的升级时机：仅限具备完整回滚方案的开发或集成测试环境。需要特别关注的方面包括：自定义调度器插件的兼容性、扩展资源管理、以及任何对已移除API的隐性依赖。

## 📋 升级建议
1. **对于生产环境：** 此版本为Alpha，**绝对不应用于生产**。仅用于早期集成测试和评估变更影响。
2. **升级前检查清单：** 1) 检查是否使用自定义的、实现了 `NominatedPodsForNode` 的调度器插件，并准备更新。2) 从 kube-controller-manager 的 `--feature-gates` 中移除 `SeparateTaintEvictionController`（如果显式设置过）。3) 审查代码和工具是否依赖已被移除的 `metrics.k8s.io/v1alpha1` 或 `apidiscovery.k8s.io/v2beta1` API。
3. **测试重点：** 在测试集群中，重点验证：1) 调度器扩展器（extender）在预抢占场景下的功能。2) 设备（如GPU）的分配是否正常，无冲突。3) 使用了 `distribute-cpus-across-numa` 和 `prefer-closest-numa-nodes` 的工作负载性能。4) 所有涉及 `resource.Quantity` 类型处理的边缘用例。
4. **监控与日志：** 升级测试环境后，检查调度器、kubelet日志中是否还有敏感信息泄露。更新监控仪表板，将 `endpoint_slice_controller_changes` 指标引用替换为 `endpoint_slice_controller_changes_total`。

## 📋 Release 包含的变更

### PR #10: Move everything out of src and reorganize scripts.
- **链接：** https://github.com/kubernetes/kubernetes/pull/10
- **状态：** closed
- **已合并：** 是
- **作者：** jbeda
- **变更说明：**
  早期代码重组PR。将文件移出src目录，重组脚本，增强脚本健壮性，将e2e测试实例类型改为g1-small，并禁用了未经充分测试的`curl | bash`集群启动方式。

### PR #135338: remove feature gate ServiceAccountTokenPodNodeInfo
- **链接：** https://github.com/kubernetes/kubernetes/pull/135338
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, kind/cleanup, lgtm, sig/node, release-note, size/L, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted, wg/device-management
- **变更说明：**
  清理PR。移除了已稳定且默认启用的`ServiceAccountTokenPodNodeInfo`特性门控及相关代码。

### PR #135486: Fix default-preemption error when using filter extenders
- **链接：** https://github.com/kubernetes/kubernetes/pull/135486
- **状态：** closed
- **已合并：** 是
- **作者：** FouoF
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/L, kind/api-change, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  调度器Bug修复：修复当调度器配置了filter extender且该extender拒绝Pod时，DefaultPreemption插件可能因未正确处理Pod状态而报错的问题。确保抢占逻辑能正确传播和处理extender的过滤结果。

### PR #135870: Build kubelet as a static binary (CGO_ENABLED=0)
- **链接：** https://github.com/kubernetes/kubernetes/pull/135870
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** area/test, area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, sig/testing, sig/architecture, needs-priority, needs-triage
- **变更说明：**
  清理PR。将kubelet加入`KUBE_STATIC_BINARIES`，默认构建为静态二进制（CGO_ENABLED=0），提升跨Linux发行版的移植性。同时修复了静态构建下kubelet通过`getent`命令进行用户命名空间ID查找，以支持NSS服务。

### PR #137534: kubelet/devicemanager: preserve in-flight reservations across allocatedDevices rebuilds
- **链接：** https://github.com/kubernetes/kubernetes/pull/137534
- **状态：** closed
- **已合并：** 是
- **作者：** trozet
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XL, approved, cncf-cla: yes, sig/testing, priority/important-longterm, lifecycle/stale, ok-to-test, triage/accepted
- **变更说明：**
  Kubelet设备管理器Bug修复：修复了在UpdateAllocatedDevices重置allocatedDevices时，可能丢失进行中(in-flight)的设备预留，导致同一设备ID被同时分配给多个Pod的竞态条件。通过引入pendingAllocations跟踪未完成的预留来解决。

### PR #138182: kubectl debug: make sysadmin profile OS-aware for Windows node debugging
- **链接：** https://github.com/kubernetes/kubernetes/pull/138182
- **状态：** closed
- **已合并：** 是
- **作者：** rzlink
- **标签：** priority/backlog, area/kubectl, lgtm, release-note, size/L, kind/feature, approved, sig/windows, sig/cli, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  扩展 kubectl debug 的 sysadmin 配置文件，使其能自动检测 Windows 节点并应用 Windows Host Process Container 设置（如 HostProcess=true, RunAsUserName），而 Linux 节点行为保持不变。

### PR #138219: fix: apiserver return JSON Status 404 for unregistered paths instead of plain text
- **链接：** https://github.com/kubernetes/kubernetes/pull/138219
- **状态：** closed
- **已合并：** 是
- **作者：** yashsingh74
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/S, kind/feature, approved, cncf-cla: yes, sig/testing, lifecycle/stale, needs-priority, needs-triage
- **变更说明：**
  修复 API 服务器对未注册路径返回 404 状态时格式不一致的问题。现在统一返回符合 Kubernetes API 约定的 JSON 格式 Status 对象，而非纯文本。

### PR #138510: [Quantity] Fix scaledValue to round negative Quantity values away from zero
- **链接：** https://github.com/kubernetes/kubernetes/pull/138510
- **状态：** closed
- **已合并：** 是
- **作者：** qflen
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, api-review, needs-triage
- **变更说明：**
  Bug修复：修复resource.Quantity的Value()和MilliValue()方法在处理极小负值时舍入方向错误的问题。修正了scaledValue函数中int64快速路径和big.Int路径的舍入逻辑，确保符合‘远离零’的文档化行为，并修复了负值可能触发int64溢出的边界检查。

### PR #138724: Allow for ResourceVersion to be passed on delete api calls
- **链接：** https://github.com/kubernetes/kubernetes/pull/138724
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, triage/accepted, sig/etcd, wg/device-management
- **变更说明：**
  扩展 Kubernetes API，允许在删除（Delete）操作中传递 ResourceVersion 参数。这增强了删除操作的并发控制能力，与已有的更新（Update）操作行为保持一致。

### PR #139115: Promote Envfiles feature gate to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/139115
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/S, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将 Envfiles 特性门（feature gate）从 Beta 升级为 GA（正式可用）。该功能现已默认启用且稳定，无需再通过特性门控制。

### PR #139356: Fix: pv_collector_total_pv_count reporting N/A plugin for all CSI-provisioned PVs
- **链接：** https://github.com/kubernetes/kubernetes/pull/139356
- **状态：** closed
- **已合并：** 是
- **作者：** dfajmon
- **标签：** kind/bug, lgtm, sig/storage, sig/api-machinery, release-note, size/M, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  Bug修复/回归修复PR。修复了`pv_collector_total_pv_count`指标对所有CSI置备的PersistentVolume错误报告`plugin_name="N/A"`的问题。根本原因是CSI插件因未实现特定接口而被过滤，解决方案是为指标收集初始化一个专用的`volumePluginMgr`。

### PR #139450: scheduler: call Done before requeueing pod in AddUnschedulablePodIfNotPresent
- **链接：** https://github.com/kubernetes/kubernetes/pull/139450
- **状态：** closed
- **已合并：** 是
- **作者：** rsd-darshan
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/XS, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  Bug修复PR。修复了调度器队列中`AddUnschedulablePodIfNotPresent`函数的一个竞态条件：通过调整`Done()`的调用时机，确保在广播唤醒`Pop`之前完成，防止Pod从队列中永久丢失。

### PR #139456: Fix/cpumanager preserve numa affinity
- **链接：** https://github.com/kubernetes/kubernetes/pull/139456
- **状态：** closed
- **已合并：** 是
- **作者：** yong-jie-gong
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  Bug修复PR。修复了CPUManager在启用`distribute-cpus-across-numa`策略选项时，`takeByTopologyNUMADistributed`函数错误选择最小NUMA节点数，导致NUMA亲和性丢失的问题。

### PR #139472: scheduler: respect NominatedNodeName in TAS placement selection
- **链接：** https://github.com/kubernetes/kubernetes/pull/139472
- **状态：** closed
- **已合并：** 是
- **作者：** mboersma
- **标签：** area/test, priority/important-soon, sig/scheduling, lgtm, sig/api-machinery, release-note, size/XL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, area/code-generation, tide/merge-method-squash, triage/accepted, wg/workload-aware-scheduling
- **变更说明：**
  功能PR。使拓扑感知调度（TAS）在为PodGroup选择放置位置时尊重`NominatedNodeName`。调度器会优先评估与提名节点匹配的放置位置，若可行则直接选用，否则回退到正常的基于分数的选择，确保被提名的Gang调度到预期节点。

### PR #139561: KEP-5958: Add server-side opt-out for metadata.managedFields
- **链接：** https://github.com/kubernetes/kubernetes/pull/139561
- **状态：** closed
- **已合并：** 是
- **作者：** yongruilin
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  API服务器功能：根据KEP-5958实现服务器端选择不返回metadata.managedFields的机制。通过添加?fieldManager=、?fieldValidation=等查询参数，允许客户端请求省略该字段，以减少大型资源（如ConfigMap、Secret）的响应体积。

### PR #139728: authorization: enable optionalorrequired kube-api-linter rule
- **链接：** https://github.com/kubernetes/kubernetes/pull/139728
- **状态：** closed
- **已合并：** 是
- **作者：** krishhna24
- **标签：** lgtm, release-note, size/M, kind/api-change, sig/auth, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, api-review, needs-triage
- **变更说明：**
  为 authorization API 组启用 kube-api-linter 的 optionalorrequired 和 nonpointerstructs 规则。标记所有字段为 +optional 或 +required，确保 API 规范性和代码生成准确性。

### PR #140010: batch: enable optionalorrequired kube-api-linter rule
- **链接：** https://github.com/kubernetes/kubernetes/pull/140010
- **状态：** closed
- **已合并：** 是
- **作者：** krishhna24
- **标签：** lgtm, release-note, size/S, kind/api-change, sig/apps, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, api-review, needs-triage
- **变更说明：**
  API规范与代码生成：为batch API组（v1和v1beta1）启用optionalorrequired和nonpointerstructs kube-api-linter规则。根据实际验证逻辑为字段添加+optional或+required标记，并调整了Job.spec等字段的OpenAPI required集合，确保API规范与运行时行为一致。

### PR #140058: kubectl explain: add auto completion
- **链接：** https://github.com/kubernetes/kubernetes/pull/140058
- **状态：** closed
- **已合并：** 是
- **作者：** oscrx
- **标签：** area/kubectl, lgtm, release-note, size/XL, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  用户体验增强：为kubectl explain命令添加自动补全功能，提升命令行操作的便捷性。

### PR #140108: admission: handle empty runtimeClassName
- **链接：** https://github.com/kubernetes/kubernetes/pull/140108
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/bug, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  RuntimeClass准入插件Bug修复：允许RuntimeClass准入插件接受spec.runtimeClassName为空的Pod。这与核心验证逻辑保持一致，该逻辑允许该字段为空但要求其为有效的DNS子域名。修复了之前因此返回500错误的问题。

### PR #140220: kubelet: log StaticPodURLHeader key names only, not values
- **链接：** https://github.com/kubernetes/kubernetes/pull/140220
- **状态：** closed
- **已合并：** 是
- **作者：** rithwik-01
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复 kubelet 启动时日志泄露 StaticPodURLHeader 凭证值的安全问题。修改日志逻辑，仅记录 header 键名而不记录值，并添加回归测试确保凭证不再泄露。

### PR #140230: kubectl: prevent kuberc defaults from matching unrelated commands
- **链接：** https://github.com/kubernetes/kubernetes/pull/140230
- **状态：** closed
- **已合并：** 是
- **作者：** Mujib-Ahasan
- **标签：** kind/bug, priority/backlog, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  修复 kubectl 配置默认值可能错误匹配不相关命令的问题。提高了配置匹配的准确性，防止无关命令意外应用默认配置。

### PR #140233: flagz: note that endpoint reflects flag layer, not effective config
- **链接：** https://github.com/kubernetes/kubernetes/pull/140233
- **状态：** closed
- **已合并：** 是
- **作者：** ashishpatel26
- **标签：** kind/documentation, area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, sig/instrumentation, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  为 /flagz 调试端点添加文档说明，明确指出其仅显示命令行标志值（或默认值），而非有效的运行时配置。有效配置应查看 /configz 端点。

### PR #140256: Lock DRADeviceTaints and DRADeviceTaintRules feature gates to GA in 1.38, remove in 1.41
- **链接：** https://github.com/kubernetes/kubernetes/pull/140256
- **状态：** closed
- **已合并：** 是
- **作者：** SamWangEng
- **标签：** priority/backlog, lgtm, sig/node, release-note, size/M, kind/feature, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-triage, wg/device-management
- **变更说明：**
  将 DRADeviceTaints 和 DRADeviceTaintRules 特性门在 v1.38 版本锁定为 true（GA）。用户若在 --feature-gates 中显式设置为 false 需移除，这两个门计划在 v1.41 版本删除。

### PR #140317: code-generator: don't overwrite NegotiatedSerializer
- **链接：** https://github.com/kubernetes/kubernetes/pull/140317
- **状态：** closed
- **已合并：** 是
- **作者：** npinaeva
- **标签：** kind/bug, area/kubectl, lgtm, sig/api-machinery, release-note, size/L, sig/auth, approved, sig/cli, cncf-cla: yes, sig/instrumentation, area/code-generation, needs-priority, needs-triage
- **变更说明：**
  Bug修复PR。修复了code-generator中一个会错误覆盖客户端`NegotiatedSerializer`字段的问题，确保生成的客户端能正确使用自定义的序列化器。

### PR #140447: Rename endpoint_slice_controller_changes to add _total suffix
- **链接：** https://github.com/kubernetes/kubernetes/pull/140447
- **状态：** closed
- **已合并：** 是
- **作者：** cipheraxat
- **标签：** sig/network, lgtm, release-note, size/M, kind/api-change, approved, cncf-cla: yes, sig/instrumentation, sig/architecture, tide/merge-method-squash, ok-to-test, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  清理/API变更PR。将计数器指标`endpoint_slice_controller_changes`重命名为符合规范的`endpoint_slice_controller_changes_total`（Alpha阶段），并废弃旧名称，为未来升级至Beta做准备。

### PR #140459: Fix Quantity.String() dropping the suffix for DecimalSI values above 10^18
- **链接：** https://github.com/kubernetes/kubernetes/pull/140459
- **状态：** closed
- **已合并：** 是
- **作者：** semx
- **标签：** kind/bug, priority/important-soon, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  Bug修复PR。修复了`resource.Quantity.String()`在处理`DecimalSI`格式且数值超过10^18时，静默丢弃数量级后缀导致数据损坏的问题。修复了`CanonicalizeBytes`中忽略的错误返回值。

### PR #140519: kube-scheduler: redact extender TLS key data from the component config log
- **链接：** https://github.com/kubernetes/kubernetes/pull/140519
- **状态：** closed
- **已合并：** 是
- **作者：** UditDewan
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  安全修复：修复kube-scheduler在日志记录配置时可能泄露extender TLS私钥(keyData)的问题。通过创建并记录一个脱敏的配置副本来解决，keyData被替换为‘REDACTED’占位符，但--write-config-to仍输出完整配置。

### PR #140607: Fix NodeRestriction audience authz fallback on volume lookup error
- **链接：** https://github.com/kubernetes/kubernetes/pull/140607
- **状态：** closed
- **已合并：** 是
- **作者：** aramase
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, release-note, size/L, sig/auth, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  NodeRestriction插件Bug修复：修复当启用ServiceAccountNodeAudienceRestriction特性时，若Pod的CSI卷源解析失败（如CSIDriver/PVC/PV未找到），插件会提前返回而不会咨询授权器，导致基于request-serviceaccounts-token-audience授权的绕过路径失效的问题。现在即使卷查找出错，也会回退到授权检查。

### PR #140674: [Quantity] Add resource.MaxMilliQuantity and fix the Quantity docs
- **链接：** https://github.com/kubernetes/kubernetes/pull/140674
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/cleanup, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复 Quantity 类型中 MaxMilliValue 检查不可靠的问题。添加 MaxMilliQuantity() 函数，并更新文档，推荐使用 Quantity.Cmp 方法进行安全比较，避免因 Value() 溢出导致的误判。

### PR #140800: Document scheduler profile label and clean up scheduler metric help texts
- **链接：** https://github.com/kubernetes/kubernetes/pull/140800
- **状态：** closed
- **已合并：** 是
- **作者：** alimaazamat
- **标签：** kind/documentation, sig/scheduling, lgtm, release-note, size/L, approved, cncf-cla: yes, sig/instrumentation, needs-priority, needs-triage, area/stable-metrics
- **变更说明：**
  文档清理PR。为kube-scheduler所有带有`profile`标签的指标在`# HELP`文本中添加了`scheduler profile`维度说明，使其可从文档直接发现。同时修复了`store_schedule_results_duration_seconds`指标的错误描述和`unschedulable_pods`的语法错误。

### PR #140803: Use queue for node authorization controller in APIServer
- **链接：** https://github.com/kubernetes/kubernetes/pull/140803
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, kind/feature, sig/auth, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  功能PR。在APIServer的节点授权控制器中引入队列机制，以优化请求处理。

### PR #140862: Remove dead metrics.k8s.io/v1alpha1 API
- **链接：** https://github.com/kubernetes/kubernetes/pull/140862
- **状态：** closed
- **已合并：** 是
- **作者：** dalaoqi
- **标签：** lgtm, release-note, size/XXL, kind/api-change, approved, cncf-cla: yes, sig/instrumentation, area/code-generation, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  清理PR。移除了自Kubernetes 1.8起已被`v1beta1`取代的`metrics.k8s.io/v1alpha1` API相关死代码。

### PR #140888: Add request metric for the aggregated OpenAPI v2 endpoint
- **链接：** https://github.com/kubernetes/kubernetes/pull/140888
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** kind/cleanup, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  清理/增强PR。为聚合的`/openapi/v2`端点添加请求计数指标`apiserver_request_total`，使其与OpenAPI v3端点行为一致。

### PR #141023: Make MinGroupCount mutable for CompositePodGroups
- **链接：** https://github.com/kubernetes/kubernetes/pull/141023
- **状态：** closed
- **已合并：** 是
- **作者：** jdzikowski
- **标签：** area/test, sig/scheduling, lgtm, sig/api-machinery, release-note, needs-rebase, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  API变更与调度器插件增强：允许CompositePodGroup.Spec.SchedulingPolicy.Gang.MinGroupCount字段在v1alpha3和v1beta1版本中可变，支持动态调整层次化Gang调度需求，无需重建父对象。同时在gangscheduling插件中实现了isSchedulableAfterCompositePodGroupUpdated队列提示，当MinGroupCount减少时，重新调度相关Pod。

### PR #141032: etcd: update etcd image to v3.7.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/141032
- **状态：** closed
- **已合并：** 是
- **作者：** humblec
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  基础组件更新：将etcd镜像版本升级至v3.7.1，涉及构建依赖、kubeadm默认配置、GCE清单、测试清单及sample-apiserver部署的全面更新。

### PR #141207: Remove locked GA feature gates CustomResourceFieldSelectors and CRDValidationRatcheting
- **链接：** https://github.com/kubernetes/kubernetes/pull/141207
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** area/test, kind/cleanup, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  清理已锁定的 GA 特性门。移除 CustomResourceFieldSelectors（v1.32锁定）和 CRDValidationRatcheting（v1.33锁定），这两个特性门已锁定默认值超过3个版本。

### PR #141208: Remove apidiscovery.k8s.io/v2beta1
- **链接：** https://github.com/kubernetes/kubernetes/pull/141208
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, approved, cncf-cla: yes, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  移除 apidiscovery.k8s.io/v2beta1 API 版本及相关代码。同时移除 AggregatedDiscoveryRemoveBetaType 特性门，这是对 PR #134230 的后续清理工作。

### PR #141460: [conformance] extend pod lifecycle test to cover PodReadyToStartContainers
- **链接：** https://github.com/kubernetes/kubernetes/pull/141460
- **状态：** closed
- **已合并：** 是
- **作者：** Priyankasaggu11929
- **标签：** area/test, priority/important-soon, lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  功能PR。扩展了现有的Pod生命周期一致性测试，以覆盖在v1.37 GA的`PodReadyToStartContainers` Pod状态条件，这是KEP-3085的一部分。

### PR #141536: metrics: graduate volume_operation_total_errors to BETA
- **链接：** https://github.com/kubernetes/kubernetes/pull/141536
- **状态：** closed
- **已合并：** 是
- **作者：** obarisk
- **标签：** lgtm, sig/storage, release-note, size/M, kind/feature, sig/apps, approved, cncf-cla: yes, sig/instrumentation, ok-to-test, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  指标稳定性升级：将kube-controller-manager中的volume_operation_errors_total指标从ALPHA提升至BETA稳定性，完成了#136310的剩余工作项。

### PR #141557: implement generateWorkloadName and generatePodGroupName in builder library
- **链接：** https://github.com/kubernetes/kubernetes/pull/141557
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** priority/important-soon, sig/scheduling, lgtm, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, triage/accepted, wg/workload-aware-scheduling
- **变更说明：**
  功能增强：在builder库中实现了generateWorkloadName和generatePodGroupName方法，用于辅助生成Workload和PodGroup资源名称。

### PR #141656: kubectl top pod: add field-selector example for filtering by node
- **链接：** https://github.com/kubernetes/kubernetes/pull/141656
- **状态：** closed
- **已合并：** 是
- **作者：** Pratik-Redhat-Tech
- **标签：** kind/documentation, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  文档更新：为kubectl top pod命令的--field-selector参数添加了按节点过滤的示例（spec.nodeName=NODE_NAME），以文档化现有功能，回应用户对按节点过滤指标的需求。此PR不引入新功能或标志。

### PR #141741: Remove PodSchedulingReadiness feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/141741
- **状态：** closed
- **已合并：** 是
- **作者：** wasylkowski-a
- **标签：** kind/cleanup, sig/scheduling, lgtm, size/S, release-note-action-required, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  移除 PodSchedulingReadiness 特性门。该特性已在 v1.30 版本 GA 并锁定，现已完成版本模拟弃用窗口，从 kube-scheduler 及相关组件中永久启用。

### PR #141789: Remove SeparateTaintEvictionController feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/141789
- **状态：** closed
- **已合并：** 是
- **作者：** wasylkowski-a
- **标签：** area/test, kind/cleanup, sig/scheduling, lgtm, sig/node, sig/api-machinery, size/L, release-note-action-required, sig/apps, approved, cncf-cla: yes, sig/testing, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  移除 SeparateTaintEvictionController 特性门。该特性已在 v1.34 版本 GA，现移除旧版内嵌的污点管理器代码，并更新相关单元测试和集成测试。

### PR #141800: scheduler: support CompositePodGroup in queue metrics
- **链接：** https://github.com/kubernetes/kubernetes/pull/141800
- **状态：** closed
- **已合并：** 是
- **作者：** dom4ha
- **标签：** sig/scheduling, lgtm, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/instrumentation, needs-priority, needs-triage
- **变更说明：**
  扩展调度器队列指标，新增对 CompositePodGroup 实体类型的支持。更新相关指标（如 scheduler_queued_entities）和记录逻辑，并添加了全面的单元测试。

### PR #142118: Use HandleErrorWithLogger instead of HandleError in workload_forest
- **链接：** https://github.com/kubernetes/kubernetes/pull/142118
- **状态：** closed
- **已合并：** 是
- **作者：** jdzikowski
- **标签：** area/test, kind/cleanup, sig/scheduling, lgtm, size/L, release-note-action-required, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  代码清理与日志改进：将workload_forest中的错误处理从utilruntime.HandleError改为utilruntime.HandleErrorWithLogger，以传递上下文日志器。同时将SchedulingQueue.GetPod的签名从接受klog.Logger改为context.Context，便于内部提取日志器和未来上下文传播。

---
*本报告由 Containerd Release Tracker 自动生成*
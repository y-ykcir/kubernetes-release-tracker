# Kubernetes 版本发布分析报告
## v1.36.0-beta.0 (v1.36.0-beta.0)

### 📋 版本信息
- **版本标签：** v1.36.0-beta.0
- **版本名称：** v1.36.0-beta.0
- **发布时间：** 2026-03-20T04:33:40Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.36.0-beta.0

### 🔍 分析统计
- **分析时间：** 2026-03-20 04:47:32
- **分析的 PR 数量：** 45
- **分析的 Issue 数量：** 19
- **重要项目数量：** 57

## 📊 版本概述
Kubernetes v1.36.0-beta.0 是一个以稳定性和性能优化为主的版本，包含多项功能毕业（GA/Beta）、重要 Bug 修复、内存泄漏修复以及一个需要立即关注的监控指标变更。

## 🔒 安全问题修复
1. ⚠️ 修复 client-go CA 证书重载问题，提升 CA 轮换安全性 - [PR #132922](https://github.com/kubernetes/kubernetes/pull/132922) - **风险级别：** 中
2. ⚠️ 修复 client-go TLS 缓存内存泄漏，无直接安全风险但影响稳定性 - [PR #136355](https://github.com/kubernetes/kubernetes/pull/136355) - **风险级别：** 低

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 client-go 在集群 CA 轮换时无法重新加载信任根证书的问题 - [PR #132922](https://github.com/kubernetes/kubernetes/pull/132922) - **影响：** 修复了 CA 轮换期间客户端连接永久中断的关键问题，需关注升级。
2. 修复 client-go TLS 缓存内存泄漏问题，添加自动垃圾回收 - [PR #136355](https://github.com/kubernetes/kubernetes/pull/136355) - **影响：** 解决长期运行进程连接多个集群时的内存持续增长问题。
3. 修复垃圾收集器（GC）在外部删除对象后记录大量 NotFound 错误日志的问题 - [PR #136817](https://github.com/kubernetes/kubernetes/pull/136817) - **影响：** 减少控制平面日志噪音，提升可观测性。
4. 修复高核数机器上 nf_conntrack 限制计算过高导致内存过度消耗的问题 - [PR #137002](https://github.com/kubernetes/kubernetes/pull/137002) - **影响：** 防止拥有大量 CPU 核心的节点因网络配置消耗过多内存。
5. 修复 `kubelet_pod_start_sli_duration_seconds` 指标未正确排除初始化容器运行时间的问题 - [PR #131950](https://github.com/kubernetes/kubernetes/pull/131950) - **影响：** 使 Pod 启动 SLI 指标更准确，影响 SLO 监控。
6. 修复 `kubectl attach` 命令不支持 `--detach-keys` 参数的问题 - [PR #134997](https://github.com/kubernetes/kubernetes/pull/134997) - **影响：** 提升运维人员使用体验。

## 💥 破坏性变更
1. 🚨 破坏性变更：kube-controller-manager 指标重命名 `volume_operation_total_errors` -> `volume_operation_errors_total` - [PR #136399](https://github.com/kubernetes/kubernetes/pull/136399) - **影响：** 必须更新所有相关的监控仪表板、告警规则和自动化脚本。
2. 🚨 API 变更：将 kuberc 凭证插件白名单条目的 `name` 字段重命名为 `command` 以与 kubeconfig 保持一致 - [PR #137272](https://github.com/kubernetes/kubernetes/pull/137272) - **影响：** 使用此 Beta API 的配置文件需要更新字段名。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 紧急变更：kube-controller-manager 指标 `volume_operation_total_errors` 重命名为 `volume_operation_errors_total` - [PR #136399](https://github.com/kubernetes/kubernetes/pull/136399) - **影响：** 所有使用此指标的自定义监控仪表板或告警规则必须更新。
2. API 废弃：开始废弃 `Service.spec.externalIPs` 字段，未来版本将移除 - [PR #137293](https://github.com/kubernetes/kubernetes/pull/137293) - **影响：** 使用此字段的服务将收到警告，需规划迁移至 LoadBalancer 或 Ingress。
3. 功能毕业：动态资源分配（DRA）扩展资源功能升级至 Beta - [PR #135048](https://github.com/kubernetes/kubernetes/pull/135048) - **影响：** 为设备管理（如 GPU、FPGA）提供了更稳定的 API。
4. 功能毕业：节点声明功能（NodeDeclaredFeatures）升级至 Beta，作为多个功能（如原地垂直伸缩、WebSocket 直连）的基础 - [PR #136042](https://github.com/kubernetes/kubernetes/pull/136042)
5. 新功能：HPA 支持基于条件的缩放到零（Alpha） - [PR #135118](https://github.com/kubernetes/kubernetes/pull/135118) - **影响：** 允许根据自定义条件将副本数缩至零，节省资源。
6. API 变更：废弃直接访问 `fieldsV1.Raw` 字段，推荐使用封装访问器 - [PR #137304](https://github.com/kubernetes/kubernetes/pull/137304) - **影响：** 使用 Server-Side Apply 并直接操作 Raw 字段的客户端库需要更新。

## 🚀 性能优化
1. 优化：`kubectl describe` 在描述多个对象时默认跳过查询事件，大幅减少 API 调用 - [PR #137145](https://github.com/kubernetes/kubernetes/pull/137145) - **提升：** 描述含 500 个 Pod 的命名空间可减少 500 次 API 调用。
2. 优化：DRA 资源切片控制器引入基于索引的命名和字典序排序，提升调度器选择设备的可预测性和性能 - [PR #136641](https://github.com/kubernetes/kubernetes/pull/136641)
3. 优化：为原地 Pod 垂直伸缩创建准入插件，在 API 层提前进行节点容量和 OS 检查，避免无效请求下发到 kubelet - [PR #136043](https://github.com/kubernetes/kubernetes/pull/136043) - **提升：** 失败更快，减少不必要的工作负载。

## 🎯 风险评估
整体风险评估：**中等**。此版本包含一个必须处理的紧急指标变更（ACTION REQUIRED）和一个重要的 API 废弃开端。同时，修复了 CA 轮换和内存泄漏等关键稳定性问题。建议在非生产环境充分测试后，规划升级。需要特别关注监控系统的兼容性更新和 `Service.spec.externalIPs` 的迁移准备。对于大规模集群，PR #137145 的性能优化将带来显著收益。

## 📋 升级建议
1. **立即行动：** 检查并更新所有监控系统中引用的 `volume_operation_total_errors` 指标，改为 `volume_operation_errors_total`。
2. **规划迁移：** 评估集群中是否使用 `Service.spec.externalIPs`，并开始规划迁移至 LoadBalancer 或 Ingress 控制器。
3. **测试重点：** 在测试环境中重点验证 client-go CA 重载修复（PR #132922）和 TLS 缓存 GC（PR #136355），特别是涉及多集群连接和证书轮换的场景。
4. **升级前检查：** 如果使用 Server-Side Apply 并直接操作 `fieldsV1.Raw`，确认客户端库已适配新的访问器接口。
5. **性能评估：** 在高核数节点上验证 nf_conntrack 内存使用是否恢复正常。
6. **利用新功能：** 考虑试用 HPA 基于条件的缩放到零功能，以优化资源成本。

## 📋 Release 包含的变更

### PR #5055: Start cluster management doc
- **链接：** https://github.com/kubernetes/kubernetes/pull/5055
- **状态：** closed
- **已合并：** 是
- **作者：** lavalamp
- **变更说明：**
  **PR #5055:** Start cluster management doc

### PR #131744: Add ResourceSlices field to kubectl describe node
- **链接：** https://github.com/kubernetes/kubernetes/pull/131744
- **状态：** closed
- **已合并：** 是
- **作者：** ArangoGutierrez
- **标签：** area/kubectl, lgtm, release-note, size/L, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  为 `kubectl describe node` 命令的输出添加了 **ResourceSlices** 字段。这是一个新功能，旨在增强节点资源信息的可观测性。

### PR #131950: PodStartSLIDuration should exclude init container runtime, image pulling time, stateful pods, not immediately schedulable pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/131950
- **状态：** closed
- **已合并：** 是
- **作者：** alimaazamat
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/XL, approved, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, ok-to-test, area/dependency, triage/accepted
- **变更说明：**
  修复 PodStartSLIDuration 指标计算，现在会排除 init 容器的运行时间、镜像拉取时间、StatefulSet Pod 以及不可立即调度的 Pod，使指标更准确地反映 Pod 启动延迟。

### PR #132922: Fix the client-go issue of reloading trust root CAs.
- **链接：** https://github.com/kubernetes/kubernetes/pull/132922
- **状态：** closed
- **已合并：** 是
- **作者：** yt2985
- **标签：** kind/bug, area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/node, sig/api-machinery, release-note, size/XXL, area/release-eng, sig/auth, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, sig/release, sig/architecture, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  修复了 client-go 在运行时无法重新加载信任根 CA 证书的问题，确保了证书轮换场景下的连接安全性。

### PR #134290: Do not get PV for externally deleting volume
- **链接：** https://github.com/kubernetes/kubernetes/pull/134290
- **状态：** closed
- **已合并：** 是
- **作者：** huww98
- **标签：** kind/cleanup, lgtm, sig/storage, release-note, size/M, sig/apps, approved, cncf-cla: yes, lifecycle/stale, needs-priority, needs-triage
- **变更说明：**
  清理优化：当检测到 PersistentVolume（PV）已被外部删除时，避免在清理流程中再次尝试获取该 PV 对象，减少不必要的 API 调用。

### PR #134627: [KEP-4188] New Kubelet gRPC API returning node-local Pod info
- **链接：** https://github.com/kubernetes/kubernetes/pull/134627
- **状态：** closed
- **已合并：** 是
- **作者：** briansonnenberg
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, priority/important-longterm, ok-to-test, api-review, area/dependency, triage/accepted
- **变更说明：**
  根据 KEP-4188，在 Kubelet 中引入一个新的 gRPC API 端点，用于查询运行在该节点上的 Pod 信息。

### PR #134660: [KEP-3085] kubelet - extend RuntimeHelper interface with `OnPodSandboxReady` to update `PodReadyToStartContainers` condition correctly
- **链接：** https://github.com/kubernetes/kubernetes/pull/134660
- **状态：** closed
- **已合并：** 是
- **作者：** Priyankasaggu11929
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/XL, sig/apps, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  修复 kubelet 中 PodReadyToStartContainers 条件更新不准确的问题。通过扩展 RuntimeHelper 接口，新增 OnPodSandboxReady 方法，确保 Pod 沙箱就绪时正确触发条件更新。属于 KEP-3085 的一部分。

### PR #134768: [PodLevelResourceManagers] Pod Level Resource Managers - Alpha
- **链接：** https://github.com/kubernetes/kubernetes/pull/134768
- **状态：** closed
- **已合并：** 是
- **作者：** KevinTMtz
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  新特性（Alpha）：引入 Pod 级别资源管理器（Pod Level Resource Managers）的 Alpha 实现。该特性允许对 Pod 内的容器进行更精细化的资源管理。

### PR #134997: Add `--detach-keys` for `kubectl attach` command
- **链接：** https://github.com/kubernetes/kubernetes/pull/134997
- **状态：** closed
- **已合并：** 是
- **作者：** yangjunmyfm192085
- **标签：** kind/bug, priority/important-soon, area/kubectl, lgtm, sig/api-machinery, release-note, size/L, approved, sig/cli, cncf-cla: yes, needs-triage
- **变更说明：**
  为 `kubectl attach` 命令新增了 `--detach-keys` 选项，允许用户自定义用于分离（detach）容器的键序列。

### PR #135048: DRA Extended Resource: promote to Beta in 1.36
- **链接：** https://github.com/kubernetes/kubernetes/pull/135048
- **状态：** closed
- **已合并：** 是
- **作者：** yliaog
- **标签：** area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, sig/architecture, area/code-generation, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将 DRA (Dynamic Resource Allocation) Extended Resource 功能从 Alpha 提升至 Beta 阶段，计划在 Kubernetes 1.36 版本中发布。

### PR #135118: KEP-2021: HPA condition based scaling to zero
- **链接：** https://github.com/kubernetes/kubernetes/pull/135118
- **状态：** closed
- **已合并：** 是
- **作者：** johanneswuerbach
- **标签：** area/test, priority/backlog, lgtm, release-note, sig/autoscaling, size/XL, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, ok-to-test, api-review, triage/accepted
- **变更说明：**
  实现了 KEP-2021: HPA 基于条件的缩放到零功能。HorizontalPodAutoscaler 现在可以根据 `ScaledToZero` 条件将副本数减少到零。

### PR #135297: Remove CRD stored versions from status upon SVM migration
- **链接：** https://github.com/kubernetes/kubernetes/pull/135297
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  新特性：在 CRD 的存储版本迁移（SVM）完成后，自动从其状态（status）中清理已迁移的存储版本（storedVersions）。这是存储版本管理流程的优化。

### PR #136042: Node Declared Features beta changes
- **链接：** https://github.com/kubernetes/kubernetes/pull/136042
- **状态：** closed
- **已合并：** 是
- **作者：** pravk03
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  实现了 Node Declared Features 的 Beta 版本变更，包括在 Node 状态中新增 `declaredFeatures` 字段，并添加了相应的验证和准入逻辑。

### PR #136043: [InPlacePodVerticalScaling] create an admission plugin to perform the OS and node capacity checks
- **链接：** https://github.com/kubernetes/kubernetes/pull/136043
- **状态：** closed
- **已合并：** 是
- **作者：** natasha41575
- **标签：** area/test, priority/important-soon, area/kubelet, kind/cleanup, sig/scheduling, area/apiserver, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XL, kind/api-change, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  为 InPlacePodVerticalScaling 创建一个 admission plugin，用于执行 OS 和节点容量检查。当 Pod 垂直扩展请求超过节点可分配容量或节点 OS 不支持扩展时，该插件能更快地使请求失败。这是针对 issue #135341 的优化。

### PR #136044: added API Version and Kind in /configz serailized objects
- **链接：** https://github.com/kubernetes/kubernetes/pull/136044
- **状态：** closed
- **已合并：** 是
- **作者：** SergeyKanzhelev
- **标签：** kind/bug, area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, lgtm, area/cloudprovider, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XL, kind/api-change, approved, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, api-review, needs-triage
- **变更说明：**
  修复了 kubelet、scheduler、cloud controller manager 和 kube-proxy 的 /configz 端点序列化问题。现在会正确包含 APIVersion 和 Kind 字段，并使用公共类型而非内部类型。

### PR #136155: Promote scheduler metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136155
- **状态：** closed
- **已合并：** 是
- **作者：** bhope
- **标签：** sig/scheduling, lgtm, release-note, size/L, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/instrumentation, ok-to-test, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将一组调度器指标从 Alpha 提升至 Beta 稳定性，包括 `scheduler_goroutines`、`scheduler_permit_wait_duration_seconds`、`scheduler_plugin_evaluation_total` 和 `scheduler_unschedulable_pods`，提供更强的兼容性保证。

### PR #136178: promote HPA metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136178
- **状态：** closed
- **已合并：** 是
- **作者：** omerap12
- **标签：** kind/cleanup, lgtm, release-note, sig/autoscaling, size/M, sig/apps, approved, cncf-cla: yes, sig/instrumentation, priority/important-longterm, triage/accepted, area/stable-metrics
- **变更说明：**
  将 HorizontalPodAutoscaler (HPA) 的相关指标从 Alpha 提升至 Beta 稳定性，作为指标毕业工作的一部分。

### PR #136230: Promote sig-storage feature `MutableCSINodeAllocatableCount` to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/136230
- **状态：** closed
- **已合并：** 是
- **作者：** torredil
- **标签：** lgtm, sig/storage, sig/api-machinery, release-note, size/S, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, tide/merge-method-squash, needs-priority, needs-triage
- **变更说明：**
  特性升级：将 sig-storage 的特性门控 MutableCSINodeAllocatableCount 提升至 GA。该特性允许动态更新 CSI 驱动的节点可分配资源数量。

### PR #136256: Extend WebSocket Streaming Protocol to the Kubelet for Exec/Attach/PortForward
- **链接：** https://github.com/kubernetes/kubernetes/pull/136256
- **状态：** closed
- **已合并：** 是
- **作者：** seans3
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, sig/autoscaling, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, area/dependency, triage/accepted
- **变更说明：**
  新特性（Alpha）：将 WebSocket 流协议扩展至 kubelet，用于 exec、attach 和 portforward 操作。当特性启用且节点支持时，流直接代理至 kubelet，减少 API Server 开销。依赖 NodeDeclaredFeatures 特性，并引入新的 ALPHA 指标。

### PR #136279: controller-manager: Add ControllerManagerReleaseLeaderElectionLockOnCancel feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/136279
- **状态：** closed
- **已合并：** 是
- **作者：** tchap
- **标签：** lgtm, sig/api-machinery, release-note, size/S, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  新特性：新增 ControllerManagerReleaseLeaderElectionLockOnCancel 特性门控，用于控制 kube-controller-manager 在退出时是否释放其领导者选举锁。为后续条件启用该功能做准备。

### PR #136314: Graduate etcd metric 'apiserver_storage_events_received_total' to BETA
- **链接：** https://github.com/kubernetes/kubernetes/pull/136314
- **状态：** closed
- **已合并：** 是
- **作者：** petern48
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, kind/api-change, approved, cncf-cla: yes, sig/instrumentation, sig/testing, ok-to-test, needs-priority, triage/accepted, area/stable-metrics, sig/etcd
- **变更说明：**
  指标稳定性提升：将 etcd 相关指标 `apiserver_storage_events_received_total` 从 Alpha 提升至 BETA 稳定性等级。

### PR #136355: Add GC to client-go TLS cache
- **链接：** https://github.com/kubernetes/kubernetes/pull/136355
- **状态：** closed
- **已合并：** 是
- **作者：** enj
- **标签：** kind/bug, area/test, area/kubelet, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, sig/auth, approved, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, needs-priority, area/dependency, triage/accepted
- **变更说明：**
  修复了 k8s.io/client-go/transport 中的 TLS 缓存内存泄漏问题。引入了垃圾回收机制，通过 `ClientsAllowTLSCacheGC` 特性门控控制，并新增了 `rest_client_transport_cert_rotation_gc_calls_total` 等监控指标。

### PR #136360: Add metric component and endpoint to metric reference docs
- **链接：** https://github.com/kubernetes/kubernetes/pull/136360
- **状态：** closed
- **已合并：** 是
- **作者：** skl
- **标签：** area/test, kind/documentation, lgtm, release-note, size/XXL, approved, cncf-cla: yes, sig/instrumentation, sig/testing, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  为自动生成的指标参考文档添加了指标所属的组件（component）和端点（endpoint）信息，以改进文档的完整性和可读性。

### PR #136367: Promote job controller metrics to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136367
- **状态：** closed
- **已合并：** 是
- **作者：** bhope
- **标签：** lgtm, release-note, size/L, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/instrumentation, priority/important-longterm, ok-to-test, triage/accepted, area/stable-metrics
- **变更说明：**
  将 Job 控制器的两个指标 `job_controller_pod_failures_handled_by_failure_policy_total` 和 `job_controller_terminated_pods_tracking_finalizer_total` 从 Alpha 稳定性提升至 Beta。

### PR #136399: Rename metric `volume_operation_total_errors` to `volume_operation_errors_total`
- **链接：** https://github.com/kubernetes/kubernetes/pull/136399
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** area/test, lgtm, sig/storage, size/M, kind/feature, release-note-action-required, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将 kube-controller-manager 的指标 `volume_operation_total_errors` 重命名为 `volume_operation_errors_total` 以符合命名规范，原指标被标记为弃用。这是一个破坏性变更，需要用户更新监控配置。

### PR #136548: [KEP 4205] GA the KubeletPSI FeatureGate
- **链接：** https://github.com/kubernetes/kubernetes/pull/136548
- **状态：** closed
- **已合并：** 是
- **作者：** mariafromano-25
- **标签：** lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  将 `KubeletPSI` 特性门控提升至 GA（正式发布），这意味着 Kubelet 的 PSI（Pressure Stall Information）指标功能现已默认启用。

### PR #136585: Improve error message for immutable job.status.startTime
- **链接：** https://github.com/kubernetes/kubernetes/pull/136585
- **状态：** closed
- **已合并：** 是
- **作者：** zhzhuang-zju
- **标签：** kind/bug, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  改进了 Job 状态中不可变字段 `status.startTime` 的错误信息，使其对用户更清晰易懂。

### PR #136633: issue: setcap build image shouldn't require a shell
- **链接：** https://github.com/kubernetes/kubernetes/pull/136633
- **状态：** closed
- **已合并：** 是
- **作者：** addyess
- **标签：** lgtm, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/release, tide/merge-method-squash, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  减少了 kube-apiserver 的 `setcap` 构建镜像对 shell 的依赖，该镜像不再需要包含 `sh`、`dash` 或 `bash`。

### PR #136641: DRA: Introduce index-based naming in resourceslice controller and sort slices and pools lexicographically
- **链接：** https://github.com/kubernetes/kubernetes/pull/136641
- **状态：** closed
- **已合并：** 是
- **作者：** troychiu
- **标签：** area/test, lgtm, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  为 DRA (Dynamic Resource Allocation) 引入基于索引的命名方式，并让 ResourceSlice 控制器和分配器按名称字典序对切片和资源池进行排序，使驱动程序能通过命名控制分配优先级。

### PR #136663: Add timezone to kubectl describe cronjob output
- **链接：** https://github.com/kubernetes/kubernetes/pull/136663
- **状态：** closed
- **已合并：** 是
- **作者：** kfess
- **标签：** area/kubectl, lgtm, release-note, size/XS, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  在 `kubectl describe cronjob` 的输出中添加了 `timezone` 字段（当设置时），便于调试 CronJob 调度问题。该字段自 v1.27 起已 GA。

### PR #136681: Graduate RestartAllContainers to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/136681
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  将 `RestartAllContainersOnContainerExits` 功能提升至 Beta 阶段，并默认启用其功能门控。该功能依赖于同期毕业至 Beta 的 `NodeDeclaredFeature`。

### PR #136728: KEP-3695: FG kubeletPodResources GA update
- **链接：** https://github.com/kubernetes/kubernetes/pull/136728
- **状态：** closed
- **已合并：** 是
- **作者：** guptaNswati
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/testing, priority/important-longterm, ok-to-test, triage/accepted, wg/device-management
- **变更说明：**
  特性升级：将 KubeletPodResourcesDynamicResources 和 KubeletPodResourcesGet 两个特性门控提升至 GA 阶段，并在 1.36 版本中默认锁定启用。这是 KEP-3695 的 GA 更新。

### PR #136759: Remove `GuaranteedQoSPodCPUResize` declared feature
- **链接：** https://github.com/kubernetes/kubernetes/pull/136759
- **状态：** closed
- **已合并：** 是
- **作者：** pravk03
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  Bug 修复：移除已声明但实际不存在的特性门控 GuaranteedQoSPodCPUResize。该门控已被移除，但其声明残留于代码中，此 PR 进行清理以避免混淆。

### PR #136817: Handle NotFound errors in garbage collector
- **链接：** https://github.com/kubernetes/kubernetes/pull/136817
- **状态：** closed
- **已合并：** 是
- **作者：** kairosci
- **标签：** kind/bug, area/test, lgtm, sig/api-machinery, release-note, size/L, sig/apps, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  Bug 修复：修复垃圾收集器（GC）在处理外部已删除对象时记录虚假 NotFound 错误日志的问题。通过显式处理 NotFound 错误并触发虚拟删除事件，使行为与现有逻辑一致。

### PR #136912: Promote SELinuxChangePolicy & SELinuxMountReadWriteOncePod to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/136912
- **状态：** closed
- **已合并：** 是
- **作者：** dfajmon
- **标签：** area/test, kind/cleanup, lgtm, sig/storage, release-note, size/M, sig/apps, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, api-review, needs-triage
- **变更说明：**
  将 `SELinuxChangePolicy` 和 `SELinuxMountReadWriteOncePod` 两个特性从 Beta 提升至 GA（正式发布），现在已无条件启用。

### PR #136945: Reflect expected replica count to the output of kubectl scale
- **链接：** https://github.com/kubernetes/kubernetes/pull/136945
- **状态：** closed
- **已合并：** 是
- **作者：** ardaguclu
- **标签：** kind/bug, area/test, priority/backlog, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  修复了 `kubectl scale` 命令的输出，使其能正确显示内置资源（如 Deployment）的期望副本数，但不适用于 CustomResourceDefinitions。

### PR #136964: Fix LastTerminationStatus for RestartAllContainers
- **链接：** https://github.com/kubernetes/kubernetes/pull/136964
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-triage
- **变更说明：**
  修复了通过 `RestartAllContainers` 操作重启容器时，`lastTerminationStatus` 状态未被保留的问题，确保了容器重启的可观测性。

### PR #137001: fix: remove duplicate SSH execution in masterExec function
- **链接：** https://github.com/kubernetes/kubernetes/pull/137001
- **状态：** closed
- **已合并：** 是
- **作者：** kairosci
- **标签：** kind/bug, area/test, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  修复了 `test/e2e/apimachinery/etcd_failure.go` 中 `masterExec` 函数重复执行相同 SSH 命令的问题，移除了冗余的执行。

### PR #137002: Cap nf_conntrack limits to prevent excessive memory usage on high-core machines
- **链接：** https://github.com/kubernetes/kubernetes/pull/137002
- **状态：** closed
- **已合并：** 是
- **作者：** kairosci
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/M, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  为自动计算的 `nf_conntrack_max` 值设置了 1,048,576 的上限，以防止在高核数（如 512 核）机器上因默认计算规则导致内存使用过量。

### PR #137145: Skip events for multi-object kubectl describe
- **链接：** https://github.com/kubernetes/kubernetes/pull/137145
- **状态：** closed
- **已合并：** 是
- **作者：** mark-liu
- **标签：** kind/cleanup, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  优化 `kubectl describe` 性能：当描述多个对象且用户未显式设置 `--show-events` 时，默认不查询事件（`ShowEvents=false`），以减少大量 API 调用。单对象描述行为不变。

### PR #137220: DRA: Make GetPCIeRootAttributeByPCIBusID filesystem-independent
- **链接：** https://github.com/kubernetes/kubernetes/pull/137220
- **状态：** closed
- **已合并：** 是
- **作者：** ffromani
- **标签：** kind/cleanup, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  清理：使 DRA 组件中的 GetPCIeRootAttributeByPCIBusID 辅助函数与文件系统解耦。通过接受可选的 fs.ReadLinkFS 参数，使其不再依赖主机文件系统，保持向后兼容。

### PR #137272: Rename `name` to `command` in kuberc credentialPluginAllowlist entries
- **链接：** https://github.com/kubernetes/kubernetes/pull/137272
- **状态：** closed
- **已合并：** 是
- **作者：** pmengelbert
- **标签：** area/test, priority/important-soon, kind/cleanup, area/kubectl, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, sig/auth, approved, sig/cli, cncf-cla: yes, sig/testing, area/code-generation, kind/deprecation, triage/accepted
- **变更说明：**
  API 变更与清理：将 kuberc 凭证插件白名单配置中的字段名从 `name` 重命名为 `command`，以提高语义清晰度。此变更可能涉及弃用旧字段。

### PR #137293: KEP-5707: Deprecate Service.spec.externalIPs
- **链接：** https://github.com/kubernetes/kubernetes/pull/137293
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** sig/network, area/kube-proxy, lgtm, release-note, size/M, kind/api-change, sig/apps, approved, sig/windows, cncf-cla: yes, area/ipvs, needs-priority, kind/deprecation, needs-triage
- **变更说明：**
  弃用：根据 KEP-5707 启动弃用 Service.spec.externalIPs 字段的第一阶段，为其添加警告和弃用标记。主要出于安全考虑。

### PR #137304: refactor: fieldsv1 encapsulation via accessors and deprecation of direct "Raw" field usage
- **链接：** https://github.com/kubernetes/kubernetes/pull/137304
- **状态：** closed
- **已合并：** 是
- **作者：** aaron-prindle
- **标签：** area/test, kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, kind/deprecation, triage/accepted
- **变更说明：**
  API 变更与清理：通过引入访问器封装 fieldsv1 的操作，并弃用直接使用 `Raw` 字段。旨在提升代码封装性，为未来变更做准备，属于重构和弃用性质。

### PR #137909: Switch PLEGOnDemandRelist default to `false` for 1.36
- **链接：** https://github.com/kubernetes/kubernetes/pull/137909
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/S, kind/flake, approved, cncf-cla: yes, kind/failing-test, needs-priority, needs-triage
- **变更说明：**
  在 Kubernetes 1.36 版本中，将 `PLEGOnDemandRelist` 特性的默认值改回 `false`。这是因为该特性加剧了与 containerd 上游已知问题相关的测试失败。

---
*本报告由 Containerd Release Tracker 自动生成*
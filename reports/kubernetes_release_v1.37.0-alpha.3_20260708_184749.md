# Kubernetes 版本发布分析报告
## v1.37.0-alpha.3 (v1.37.0-alpha.3)

### 📋 版本信息
- **版本标签：** v1.37.0-alpha.3
- **版本名称：** v1.37.0-alpha.3
- **发布时间：** 2026-07-08T18:11:06Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.37.0-alpha.3

### 🔍 分析统计
- **分析时间：** 2026-07-08 18:47:49
- **分析的 PR 数量：** 37
- **分析的 Issue 数量：** 12
- **重要项目数量：** 46

## 📊 版本概述
Kubernetes v1.37.0-alpha.3 是一个早期预发布版本，核心价值在于将多个关键功能（SVM、DRA设备污点、SELinuxMount等）推进至GA状态，并修复了包括kubelet内存泄漏在内的多个重要Bug，同时引入了PodGroup调度API的显著改进。

## 🔒 安全问题修复
1. ⚠️ Kubelet启动日志现在包含完整配置，可能暴露敏感信息，需确保`nodes/logs`权限仅授予受信用户 - [PR #139837](https://github.com/kubernetes/kubernetes/pull/139837) - **风险级别：** 中
2. ⚠️ NodeRestriction准入插件增强了对PodCertificateRequests的检查，增加了纵深防御 - [PR #140006](https://github.com/kubernetes/kubernetes/pull/140006) - **风险级别：** 低

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复kubelet在每次Pod同步时因未取消旧上下文导致的内存泄漏回归问题 - [PR #139850](https://github.com/kubernetes/kubernetes/pull/139850) - **影响：** 在1.36集群中可能导致kubelet内存持续增长，影响节点稳定性
2. 修复Binding API不验证节点名，导致绑定到无效节点名的Pod（如有Finalizer）卡在删除状态的问题 - [PR #136776](https://github.com/kubernetes/kubernetes/pull/136776) - **影响：** 可能导致Pod无法删除，需手动介入清理
3. 修复调度器快照（Snapshot）中AssumePod/ForgetPod未正确更新Pod亲和性、反亲和性及PVC索引的问题 - [PR #139054](https://github.com/kubernetes/kubernetes/pull/139054) - **影响：** 在PodGroup调度周期中，可能导致亲和性规则和卷限制评估错误
4. 修复DRA ResourceSlice验证在`validRange.step`为零时引发panic的问题 - [PR #139698](https://github.com/kubernetes/kubernetes/pull/139698) - **影响：** 启用`DRAConsumableCapacity`特性门时，提交错误配置的ResourceSlice会导致API服务器panic
5. 修复kubelet/DRA在删除Pod时可能错误地释放仍被其他Pod使用的资源的问题 - [PR #140212](https://github.com/kubernetes/kubernetes/pull/140212) - **影响：** 共享DRA资源声明的Pod可能因资源被意外释放而运行失败
6. 修复驱逐信号未考虑大页内存，导致可用内存计算虚高，延迟驱逐触发的问题 - [PR #138127](https://github.com/kubernetes/kubernetes/pull/138127) - **影响：** 配置了大页内存的节点可能因内存压力引发OOM而非优雅驱逐
7. 修复client-go配置文件迁移时，目标文件权限可能比源文件更宽松的安全问题 - [PR #138142](https://github.com/kubernetes/kubernetes/pull/138142) - **影响：** 可能意外暴露kubeconfig中的凭据给系统其他用户

## 💥 破坏性变更
1. 🚨 SELinuxMount特性门升级至GA并默认启用。在启用SELinux的集群中，某些依赖特定卷挂载行为的工作负载可能失败。升级前必须按照官方博客指南检查和修复。 - [PR #139956](https://github.com/kubernetes/kubernetes/pull/139956) - **影响：** 需要审计并可能修改工作负载的SELinux上下文配置，或选择禁用该特性门
2. 🚨 PodGroup API字段重命名：`PodGroupTemplateRef` 改为 `WorkloadRef`。使用alpha版PodGroup API的客户端需要更新。 - [PR #140080](https://github.com/kubernetes/kubernetes/pull/140080) - **影响：** 需要更新自定义控制器或脚本以使用新字段名
3. 🚨 移除PreventStaticPodAPIReferences特性门。相关行为现已固化，无法通过特性门禁用。 - [PR #140226](https://github.com/kubernetes/kubernetes/pull/140226) - **影响：** 依赖此特性门禁用相关验证的集群需适应新行为

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. SELinuxMount功能门升级至GA，默认启用，可能破坏启用SELinux的集群中的现有工作负载 - [PR #139956](https://github.com/kubernetes/kubernetes/pull/139956)
2. Kubelet启动时记录完整的有效配置（而非命令行参数），集群管理员需审查`nodes/logs` ClusterRole权限 - [PR #139837](https://github.com/kubernetes/kubernetes/pull/139837)
3. PodGroup API 将 `PodGroupTemplateRef` 字段重命名为 `WorkloadRef` - [PR #140080](https://github.com/kubernetes/kubernetes/pull/140080)
4. 条件授权（Conditional Authorization）核心机制实现 - [PR #137513](https://github.com/kubernetes/kubernetes/pull/137513)
5. 存储版本管理器（SVM）功能升级至GA - [PR #138560](https://github.com/kubernetes/kubernetes/pull/138560)
6. DRA（动态资源分配）设备污点和容忍度功能升级至GA - [PR #138676](https://github.com/kubernetes/kubernetes/pull/138676)
7. 节点声明功能（Node Declared Features）升级至GA - [PR #139763](https://github.com/kubernetes/kubernetes/pull/139763)

## 🚀 性能优化
1. 启用WatchListCompression特性门，减少API服务器在List/Watch操作中的网络带宽和内存使用 - [PR #140140](https://github.com/kubernetes/kubernetes/pull/140140) - **提升：** 减少大规模集群中控制平面的负载
2. 调度器优化：PodGroup成功调度后，其剩余未调度Pod直接进入活跃队列（而非退避队列），加速调度 - [PR #139613](https://github.com/kubernetes/kubernetes/pull/139613) - **提升：** 改善PodGroup（Gang Scheduling）的调度延迟
3. 调度器内部缓存和快照PodGroup API对象，减少API调用 - [PR #140077](https://github.com/kubernetes/kubernetes/pull/140077) - **提升：** 提高调度器在处理PodGroup时的性能

## 🎯 风险评估
整体风险评估：**高（对于Alpha版本）**。此版本包含破坏性变更（尤其是SELinuxMount GA）、API变更和大量新功能代码，不适合生产环境。建议的升级时机：等待至少beta版本发布，并在完整的非生产环境中进行详尽测试。需要特别关注的方面：1) SELinux工作负载的兼容性；2) 使用PodGroup alpha API的自定义调度器或控制器；3) 启用SELinux和DRA功能的集群的升级后验证。

## 📋 升级建议
1. **生产环境暂勿升级**：这是alpha版本，包含实验性API和不稳定变更，仅用于早期测试和评估。
2. **重点评估SELinuxMount影响**：如果集群启用SELinux，计划升级至1.37前，务必在1.36集群中运行检查工具，识别并修复可能受影响的工作负载。参考官方博客指南。
3. **审查集群角色绑定**：检查并确保`system:node`角色或任何绑定到`nodes/logs`资源的ClusterRole仅包含必要的最小权限，防止配置信息泄露。
4. **关注PodGroup API用户**：如果您正在试用PodGroup（Gang Scheduling）alpha功能，请注意`PodGroupTemplateRef`到`WorkloadRef`的字段重命名，提前更新代码。
5. **测试DRA相关功能**：如果使用动态资源分配，在测试环境中验证设备污点、ResourceSlice验证等GA功能，以及相关Bug修复。
6. **为kube-proxy模式变更做准备**：注意kube-proxy将在未来版本默认切换为`nftables`，现在开始明确配置`proxy-mode`以避免未来警告和变更。

## 📋 Release 包含的变更

### PR #121873: Log the actual host path volume mount type
- **链接：** https://github.com/kubernetes/kubernetes/pull/121873
- **状态：** closed
- **已合并：** 是
- **作者：** skitt
- **标签：** lgtm, sig/storage, release-note, size/M, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  改进host path volume mount失败时的日志记录。当挂载失败是因为host path类型不匹配时，现在会记录实际路径类型和期望类型，便于调试。

### PR #129109: restmapper + discovery: add context-aware APIs
- **链接：** https://github.com/kubernetes/kubernetes/pull/129109
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** area/test, area/kubelet, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, needs-priority, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  为 restmapper 和 discovery 客户端接口添加了上下文感知（context-aware）的 API 变体（*WithContext 方法），以支持传入调用者上下文并启用上下文日志记录，同时保持对旧接口的向后兼容。

### PR #136705: Added warning in kubelet for invalid static pod priority and priorityClassNames
- **链接：** https://github.com/kubernetes/kubernetes/pull/136705
- **状态：** closed
- **已合并：** 是
- **作者：** sreeram-venkitesh
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, tide/merge-method-squash, needs-priority, needs-triage
- **变更说明：**
  在kubelet中为静态Pod的无效priority和priorityClassName配置添加警告。当静态Pod配置了这些字段时，kubelet会发出警告，但不会阻止Pod创建，以帮助用户发现配置问题。

### PR #136776: Validate node name in Binding API
- **链接：** https://github.com/kubernetes/kubernetes/pull/136776
- **状态：** closed
- **已合并：** 是
- **作者：** yakir-shriker
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, api-review, needs-triage
- **变更说明：**
  修复了 Binding API（pods/binding 端点）未验证节点名称的问题。此前绑定到无效节点名（如包含大写字符）会导致带有 finalizer 的 Pod 卡在删除状态。现添加验证，使用 ValidateNodeName 函数提前拒绝无效名称。

### PR #137513: Conditional Authz [2/n]: Implementation of core Conditional Authorization machinery
- **链接：** https://github.com/kubernetes/kubernetes/pull/137513
- **状态：** closed
- **已合并：** 是
- **作者：** luxas
- **标签：** area/test, area/kubelet, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  实现条件授权的核心机制。引入ConditionalAuthorizationRule API和评估逻辑，为基于动态条件的细粒度访问控制奠定基础。

### PR #138127: Make the eviction signal hugepages aware.
- **链接：** https://github.com/kubernetes/kubernetes/pull/138127
- **状态：** closed
- **已合并：** 是
- **作者：** jingczhang
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  使驱逐信号感知hugepages。kubelet在计算内存压力驱逐时，现在会考虑hugepages的使用量，避免因忽略hugepages而导致过早或过晚驱逐Pod。

### PR #138142: Migrate: use source file permission when writing destination file
- **链接：** https://github.com/kubernetes/kubernetes/pull/138142
- **状态：** closed
- **已合并：** 是
- **作者：** brianpursley
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/S, approved, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, triage/accepted
- **变更说明：**
  改进client-go的kubeconfig迁移功能。迁移时使用源文件的权限创建目标文件，避免目标文件权限超过源文件，减少凭证意外暴露的风险。

### PR #138351: optional tracking and documentation of breaking Go API changes in client-go
- **链接：** https://github.com/kubernetes/kubernetes/pull/138351
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/documentation, lgtm, sig/api-machinery, release-note, size/XXL, approved, cncf-cla: yes, needs-priority, area/dependency, needs-triage
- **变更说明：**
  引入可选机制跟踪和记录client-go及apimachinery中的破坏性Go API变更，通过apidiff在CHANGELOG.md中记录，提高透明度和开发者意识。

### PR #138432: Only warn about missing pull secrets if image pull fails
- **链接：** https://github.com/kubernetes/kubernetes/pull/138432
- **状态：** closed
- **已合并：** 是
- **作者：** Jamstah
- **标签：** kind/bug, priority/backlog, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  优化了关于缺失镜像拉取密钥（pull secret）的警告逻辑：现在仅在实际发生镜像拉取失败时才发出 FailedToRetrieveImagePullSecret 事件，避免了无关警告。

### PR #138560: Promote SVM to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/138560
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, sig/architecture, area/conformance, area/code-generation, needs-priority, triage/accepted, sig/etcd
- **变更说明：**
  将 SVM（推测为 ServiceAccount Volume Mount）功能从 Beta 阶段毕业为 GA（Generally Available）。

### PR #138676: DRA: Device Taints and Tolerations GA graduation
- **链接：** https://github.com/kubernetes/kubernetes/pull/138676
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** area/test, sig/scheduling, area/apiserver, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, sig/architecture, area/conformance, area/code-generation, needs-priority, needs-triage, sig/etcd, wg/device-management
- **变更说明：**
  DRA（动态资源分配）的 Device Taints and Tolerations 功能已正式毕业为 GA（Generally Available），并通过 resource.k8s.io/v1 API 提供。

### PR #138875: Add progress to conditions for migrations in SVM
- **链接：** https://github.com/kubernetes/kubernetes/pull/138875
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** lgtm, sig/api-machinery, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  为Storage Version Migrations（SVM）的conditions添加progress字段，允许跟踪迁移进度，增强可观察性。

### PR #139054: scheduler: fix snapshot AssumePod/ForgetPod affinity and PVC indexes
- **链接：** https://github.com/kubernetes/kubernetes/pull/139054
- **状态：** closed
- **已合并：** 是
- **作者：** net0pyr
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, release-note, size/XL, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  修复调度器快照中AssumePod/ForgetPod的亲和性和PVC索引问题。确保在PodGroup调度周期内，inter-pod affinity/anti-affinity和VolumeRestrictions插件观察到正确的状态。

### PR #139240: KEP-5710: Add PreemptionPolicy field to PodGroup [WAS]
- **链接：** https://github.com/kubernetes/kubernetes/pull/139240
- **状态：** closed
- **已合并：** 是
- **作者：** ania-borowiec
- **标签：** area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, sig/autoscaling, size/XL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/windows, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, sig/cloud-provider, needs-priority, area/dependency, needs-triage, sig/etcd, wg/device-management, wg/workload-aware-scheduling
- **变更说明：**
  根据KEP-5710，在PodGroup API中添加PreemptionPolicy字段，以支持Workload-Aware Scheduling（WAS），允许自定义抢占策略。

### PR #139395: KEP-5491: list-type attribute should be able to evaluate in StoredExpressions env (e.g., scheduler) even if the feature gate is disabled
- **链接：** https://github.com/kubernetes/kubernetes/pull/139395
- **状态：** closed
- **已合并：** 是
- **作者：** everpeace
- **标签：** kind/bug, lgtm, sig/node, release-note, size/XL, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复KEP-5491中list-type属性在StoredExpressions环境（如调度器）中的评估问题。即使相关feature gate被禁用，list-type属性现在也能在StoredExpressions中被正确评估。

### PR #139419: Fix CBOR apply patch request audit
- **链接：** https://github.com/kubernetes/kubernetes/pull/139419
- **状态：** closed
- **已合并：** 是
- **作者：** hoskeri
- **标签：** kind/bug, area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, sig/auth, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, kind/regression, triage/accepted
- **变更说明：**
  修复CBOR apply patch请求的审计日志问题。现在使用正确的内容类型记录审计事件，避免因RequestObject包含二进制数据导致序列化失败。

### PR #139602: scheduler: Add resourceVersion to Pod status patch
- **链接：** https://github.com/kubernetes/kubernetes/pull/139602
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/L, kind/flake, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  调度器在通过 PATCH 更新 Pod 状态时，现在会在请求体中包含 Pod 的 resourceVersion。这有助于解决因条件竞争导致的更新冲突问题。

### PR #139613: On successful scheduling of podgroup, requeue remaining pods directly to active queue.
- **链接：** https://github.com/kubernetes/kubernetes/pull/139613
- **状态：** closed
- **已合并：** 是
- **作者：** iomarsayed
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  优化了 PodGroup 调度行为：当一个 PodGroup 成功调度后，其剩余的未调度 Pod 会被直接重新排队（requeue）到活动队列（active queue）而非退避队列（backoff queue），并保留原有时间戳以尽快尝试调度，从而减少调度延迟。

### PR #139623: DRA kubeletplugin: use hashed registrar socket name for rolling updates
- **链接：** https://github.com/kubernetes/kubernetes/pull/139623
- **状态：** closed
- **已合并：** 是
- **作者：** vishalanarase
- **标签：** kind/bug, area/test, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRA kubelet插件在滚动更新时的问题，通过使用哈希化的registrar socket名称来避免冲突，确保Dynamic Resource Allocation插件的平滑更新。

### PR #139698: Reject a zero step in ResourceSlice validRange
- **链接：** https://github.com/kubernetes/kubernetes/pull/139698
- **状态：** closed
- **已合并：** 是
- **作者：** wilmerdooley
- **标签：** kind/bug, lgtm, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted, wg/device-management
- **变更说明：**
  修复了当 DRAConsumableCapacity 特性门启用且容量请求策略设置 validRange.step 为 0 时，ResourceSlice 验证会触发整数除以零的 panic 问题。通过添加验证拒绝非正的 step 值并添加回归测试来解决。

### PR #139763: Promote Node Declared Features to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/139763
- **状态：** closed
- **已合并：** 是
- **作者：** pravk03
- **标签：** area/test, area/kubelet, sig/scheduling, lgtm, sig/node, release-note, sig/autoscaling, size/L, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, api-review, needs-triage
- **变更说明：**
  将Node Declared Features功能从beta提升到GA，使其成为稳定API，用于节点声明特性管理。

### PR #139837: Dump full config on kubelet startup instead of command line arguments
- **链接：** https://github.com/kubernetes/kubernetes/pull/139837
- **状态：** closed
- **已合并：** 是
- **作者：** SergeyKanzhelev
- **标签：** area/test, area/kubelet, lgtm, sig/node, size/L, kind/feature, release-note-action-required, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  kubelet 启动时不再记录可能不准确的原始命令行参数，改为记录反映所有配置源（默认值、配置文件、命令行标志优先级）合并后的完整有效 KubeletConfiguration。管理员需审查 nodes/logs 集群角色权限。

### PR #139850: kubelet startPodSync: reuse the previous context to fix memory leak regression
- **链接：** https://github.com/kubernetes/kubernetes/pull/139850
- **状态：** closed
- **已合并：** 是
- **作者：** compumike
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复了 Kubernetes 1.36 中引入的 kubelet 内存泄漏回归问题。该问题源于每次 Pod 同步（SyncPod）时，startPodSync 函数会创建新的 context 而未取消旧的，导致 context 累积。修复方法是重用并取消前一个 context。

### PR #139920: Validate matching priorities when scheduling pod groups
- **链接：** https://github.com/kubernetes/kubernetes/pull/139920
- **状态：** closed
- **已合并：** 是
- **作者：** brejman
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  在调度PodGroup时，验证组内Pod的优先级是否与PodGroup的优先级匹配。防止因优先级不一致导致的调度问题，确保PodGroup内调度行为一致。

### PR #139952: Introduce incompletePodGroupPods to store pods waiting for their PodGroup to appear
- **链接：** https://github.com/kubernetes/kubernetes/pull/139952
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management, wg/workload-aware-scheduling
- **变更说明：**
  引入incompletePodGroupPods存储等待其PodGroup出现的Pods。改进PodGroup调度，允许Pod在PodGroup创建前排队等待，避免因PodGroup未就绪导致调度失败。

### PR #139956: Graduate SELinuxMount to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/139956
- **状态：** closed
- **已合并：** 是
- **作者：** jsafrane
- **标签：** area/kubelet, lgtm, sig/node, sig/api-machinery, size/M, kind/api-change, kind/feature, release-note-action-required, sig/apps, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, needs-triage
- **变更说明：**
  将 SELinuxMount 特性门毕业为 GA 并默认启用。在 Kubernetes 1.37 中，启用 SELinux 的集群可能因此破坏现有工作负载，管理员需按 ACTION REQUIRED 提示进行审查和调整。

### PR #139957: Warn about upcoming default change when defaulting kube-proxy mode
- **链接：** https://github.com/kubernetes/kubernetes/pull/139957
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** sig/network, area/kube-proxy, lgtm, release-note, size/XS, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  当 kube-proxy 启动时未显式指定代理模式（iptables、ipvs 或 nftables）而使用默认值（iptables）时，现在会发出警告，提示默认值将在未来版本（1.40）切换为 nftables。

### PR #139989: kubeadm: avoid contradictory kube-proxy bindAddress warnings
- **链接：** https://github.com/kubernetes/kubernetes/pull/139989
- **状态：** closed
- **已合并：** 是
- **作者：** vinayakray19
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, approved, area/kubeadm, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  改进了 kubeadm 中关于 kube-proxy bindAddress 的警告逻辑。当用户显式设置标准绑定地址（0.0.0.0 或 ::）时，不再发出矛盾的默认值警告。

### PR #140006: Pod Certificates: Node-restriction support for signer names
- **链接：** https://github.com/kubernetes/kubernetes/pull/140006
- **状态：** closed
- **已合并：** 是
- **作者：** ahmedtd
- **标签：** kind/bug, area/test, lgtm, release-note, size/XL, kind/api-change, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  NodeRestriction admission plugin新增对PodCertificateRequests的防御深度检查，限制Kubelet只能请求Pod中mount的podCertificate projected volume source指定的signer name，或通过授权检查（verb=request-podcertificate-signer）绕过。这是API变更，增强安全性。

### PR #140075: Add PodGroup object to PodGroupInfo for scheduling cycle consistency
- **链接：** https://github.com/kubernetes/kubernetes/pull/140075
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  将PodGroup对象添加到PodGroupInfo中。确保在调度周期内PodGroup信息的一致性，避免因API对象变化导致调度决策不一致。

### PR #140076: Promote KYAML printer to stable
- **链接：** https://github.com/kubernetes/kubernetes/pull/140076
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** priority/backlog, area/kubectl, lgtm, release-note, size/S, kind/feature, approved, sig/cli, cncf-cla: yes, triage/accepted
- **变更说明：**
  将KYAML printer提升为稳定功能。kubectl get -o kyaml输出格式现在标记为稳定，用户可放心使用。

### PR #140077: Cache and snapshot PodGroup API objects in kube-scheduler
- **链接：** https://github.com/kubernetes/kubernetes/pull/140077
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, sig/node, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management, wg/workload-aware-scheduling
- **变更说明：**
  在kube-scheduler中缓存和快照PodGroup API对象。通过缓存减少API服务器负载，通过快照确保调度周期内数据一致性，提升PodGroup调度性能。

### PR #140080: rename PodGroupTemplateRef to WorkloadRef
- **链接：** https://github.com/kubernetes/kubernetes/pull/140080
- **状态：** closed
- **已合并：** 是
- **作者：** dom4ha
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage, sig/etcd, wg/device-management, wg/workload-aware-scheduling
- **变更说明：**
  将PodGroup API中的PodGroupTemplateRef重命名为WorkloadRef。这是API重构，为CompositePodGroup的未来变更做准备，使命名更简洁直接。

### PR #140140: Enable WatchListCompression feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/140140
- **状态：** closed
- **已合并：** 是
- **作者：** p0lyn0mial
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  启用WatchListCompression功能门，压缩API服务器watch列表的数据传输，减少网络带宽使用。

### PR #140180: Add a message when preemption succeeds
- **链接：** https://github.com/kubernetes/kubernetes/pull/140180
- **状态：** closed
- **已合并：** 是
- **作者：** Argh4k
- **标签：** sig/scheduling, lgtm, release-note, size/S, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  为抢占成功的情况添加消息。当默认抢占插件找到潜在节点时，FailedScheduling事件和PodScheduled PodCondition现在会包含“preemption: found a potential placement...”消息，提高事件可读性。

### PR #140212: kubelet/dra: skip unprepareResources when claimInfo doesn't reference the pod
- **链接：** https://github.com/kubernetes/kubernetes/pull/140212
- **状态：** closed
- **已合并：** 是
- **作者：** bart0sh
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复了 kubelet/DRA 中的一个 bug：当 Pod 的 PrepareResources 验证失败时，该 Pod 不会被添加到 claimInfo 的 PodUIDs 中。后续删除此 Pod 时，会错误地 unprepared 仍被其他 Pod 共享使用的资源。修复方法是在 claimInfo 未引用该 Pod 时提前返回。

### PR #140226: Remove PreventStaticPodAPIReferences feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/140226
- **状态：** closed
- **已合并：** 是
- **作者：** sreeram-venkitesh
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  清理代码：移除了已毕业的 PreventStaticPodAPIReferences 特性门控。

---
*本报告由 Containerd Release Tracker 自动生成*
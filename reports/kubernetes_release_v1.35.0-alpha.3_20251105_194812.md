# Kubernetes 版本发布分析报告
## Kubernetes v1.35.0-alpha.3 (v1.35.0-alpha.3)

### 📋 版本信息
- **版本标签：** v1.35.0-alpha.3
- **版本名称：** Kubernetes v1.35.0-alpha.3
- **发布时间：** 2025-11-05T17:52:41Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.0-alpha.3

### 🔍 分析统计
- **分析时间：** 2025-11-05 19:48:12
- **分析的 PR 数量：** 44
- **分析的 Issue 数量：** 13
- **重要项目数量：** 55

## 📊 版本概述
Kubernetes v1.35.0-alpha.3 引入了多项重要变更，包括 cgroups v1 的强制废弃、DRA 功能增强、多个 API 升级到 GA/Beta，以及重要的安全修复和性能优化。

## 🔒 安全问题修复
1. ⚠️ 消除 MD5 使用，阻止新用途以符合 FIPS 标准 - [PR #133511](https://github.com/kubernetes/kubernetes/pull/133511) - **风险级别：** 中 - 影响需要 FIPS 合规的环境
2. ⚠️ CSI 驱动通过 secrets 字段选择加入服务账户令牌 - [PR #134826](https://github.com/kubernetes/kubernetes/pull/134826) - **风险级别：** 低 - 改善敏感信息处理

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复调度器缓存竞争：Pod 删除后立即从缓存中移除 - [PR #134157](https://github.com/kubernetes/kubernetes/pull/134157) - **影响：** 避免重复抢占和资源浪费
2. 修复 kubelet NodeAffinity 检查因缓存陈旧数据导致的 Pod 拒绝 - [PR #134445](https://github.com/kubernetes/kubernetes/pull/134445) - **影响：** 确保 Pod 在节点标签更新后能够正确调度
3. 修复 DRA 可消耗容量分配：允许同一设备多次分配 - [PR #134103](https://github.com/kubernetes/kubernetes/pull/134103) - **影响：** 提高设备资源利用率
4. 修复 Job 控制器在恢复挂起作业时的 startTime 更新错误 - [PR #134769](https://github.com/kubernetes/kubernetes/pull/134769) - **影响：** 避免控制器日志中出现重复错误
5. 修复 kubectl api-resources 在发现客户端失败时的 panic - [PR #134833](https://github.com/kubernetes/kubernetes/pull/134833) - **影响：** 提高命令行工具稳定性
6. 修复 kubelet configz 端点中 cgroupDriver 显示不正确 - [PR #134743](https://github.com/kubernetes/kubernetes/pull/134743) - **影响：** 确保监控工具获取准确的配置信息
7. 修复 DRA 分配器配置字段缺失问题 - [PR #134793](https://github.com/kubernetes/kubernetes/pull/134793) - **影响：** 改善设备驱动配置管理

## 💥 破坏性变更
1. 🚨 cgroups v1 支持废弃：在 kubelet 1.35+ 上会抛出错误 - [PR #134744](https://github.com/kubernetes/kubernetes/pull/134744) - **影响：** 必须迁移到 cgroups v2，否则集群初始化会失败
2. 🚨 移除 pod-infra-container-image 标志 - [PR #133779](https://github.com/kubernetes/kubernetes/pull/133779) - **影响：** 需要更新配置，通过 CRI 实现指定
3. 🚨 Pod 证书 API 从 v1alpha1 移除 - [PR #134624](https://github.com/kubernetes/kubernetes/pull/134624) - **影响：** 使用旧 API 的应用需要迁移到 v1beta1

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. cgroups v1 现在在 kubelet 1.35+ 上会抛出错误而非警告 - [PR #134744](https://github.com/kubernetes/kubernetes/pull/134744)
2. 移除已弃用的 pod-infra-container-image 标志 - [PR #133779](https://github.com/kubernetes/kubernetes/pull/133779)
3. DRA 设备污点功能：新增 ResourceSlice API 和设备健康监控 - [PR #134152](https://github.com/kubernetes/kubernetes/pull/134152)
4. 结构化 statusz 端点 - [PR #134313](https://github.com/kubernetes/kubernetes/pull/134313)
5. 约束模拟功能实现 - [PR #134803](https://github.com/kubernetes/kubernetes/pull/134803)
6. Pod 证书功能升级到 Beta - [PR #134624](https://github.com/kubernetes/kubernetes/pull/134624)
7. InPlacePodVerticalScaling 升级到 GA - [PR #134949](https://github.com/kubernetes/kubernetes/pull/134949)
8. Pod Generation 升级到 GA - [PR #134948](https://github.com/kubernetes/kubernetes/pull/134948)
9. PreferSameTrafficDistribution 升级到 GA - [PR #134457](https://github.com/kubernetes/kubernetes/pull/134457)

## 🚀 性能优化
1. RealFIFO 批量处理：显著提高控制器吞吐量 - [PR #132240](https://github.com/kubernetes/kubernetes/pull/132240) - **提升：** 在大规模集群中减少锁竞争，改善缓存新鲜度
2. 调度器缓存优化：立即移除已删除 Pod - [PR #134157](https://github.com/kubernetes/kubernetes/pull/134157) - **提升：** 减少抢占竞争和资源浪费
3. kubelet 镜像管理新增指标监控 - [PR #132644](https://github.com/kubernetes/kubernetes/pull/132644) - **提升：** 提供更细粒度的性能监控能力

## 🎯 风险评估
整体风险评估：中高风险。作为 alpha 版本，不建议在生产环境使用。主要风险点：cgroups v1 的强制废弃可能导致现有集群无法升级，需要提前规划迁移。建议在测试环境充分验证所有变更，特别是 DRA 相关功能和调度器修复。

## 📋 升级建议
1. 升级前必须验证节点 cgroups 版本，确保使用 cgroups v2
2. 检查并移除所有使用已废弃标志的配置，特别是 pod-infra-container-image
3. 对于使用 DRA 的环境，测试新功能和修复，确保设备分配正常工作
4. 生产环境升级建议等待 beta 或稳定版本，alpha 版本存在较大风险
5. 关注 etcd 版本兼容性，建议升级到 v3.5.24
6. 启用新的监控指标以跟踪性能改进效果

## 📋 Release 包含的变更

### PR #123642: Add JWKS fetch metrics for jwt authenticator
- **链接：** https://github.com/kubernetes/kubernetes/pull/123642
- **状态：** closed
- **已合并：** 是
- **作者：** aramase
- **标签：** area/test, priority/important-soon, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  为JWT认证器新增JWKS获取指标（如apiserver_authentication_jwt_authenticator_jwks_fetch_last_timestamp_seconds），需启用StructuredAuthenticationConfiguration特性。

### PR #125912: Migrate cpumanager to contextual logging
- **链接：** https://github.com/kubernetes/kubernetes/pull/125912
- **状态：** closed
- **已合并：** 是
- **作者：** ffromani
- **标签：** area/kubelet, kind/cleanup, lgtm, area/logging, sig/node, release-note, size/XL, approved, cncf-cla: yes, priority/important-longterm, triage/accepted, wg/structured-logging
- **变更说明：**
  将cpumanager迁移到上下文日志，提升日志可读性和调试能力，部分解决issue 123037和130069。

### PR #132157: drop UserNamespacesPodSecurityStandards feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/132157
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** area/test, kind/cleanup, lgtm, sig/node, release-note, size/XXL, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  删除UserNamespacesPodSecurityStandards功能门。由于kubelet 1.30+已支持用户命名空间，现在无条件放宽PodSecurityAdmission策略。

### PR #132240: Adding batch handling for popping items from RealFIFO
- **链接：** https://github.com/kubernetes/kubernetes/pull/132240
- **状态：** closed
- **已合并：** 是
- **作者：** yue9944882
- **标签：** sig/scheduling, lgtm, sig/storage, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  为RealFIFO添加批量处理功能，通过批量处理watch事件减少DeltaFIFO写锁竞争，显著提升控制器吞吐量。

### PR #132644: kubelet: add metrics for EnsureImageExists
- **链接：** https://github.com/kubernetes/kubernetes/pull/132644
- **状态：** closed
- **已合并：** 是
- **作者：** stlaz
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为kubelet的EnsureImageExists函数添加监控指标kubelet_image_manager_ensure_image_requests_total，包含present_locally、pull_policy等维度。

### PR #133087: promote DeploymentReplicaSetTerminatingReplicas to Beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/133087
- **状态：** closed
- **已合并：** 是
- **作者：** atiratree
- **标签：** area/test, lgtm, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, priority/important-longterm, area/code-generation, api-review, triage/accepted
- **变更说明：**
  将DeploymentReplicaSetTerminatingReplicas特性提升至beta，改进Deployment和ReplicaSet的终止副本计数功能。

### PR #133511: eliminate md5 usage, block new usage
- **链接：** https://github.com/kubernetes/kubernetes/pull/133511
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** area/test, sig/network, area/kubelet, kind/cleanup, area/kubectl, lgtm, sig/storage, sig/node, sig/cluster-lifecycle, release-note, size/L, sig/apps, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/testing, sig/architecture, needs-priority, area/code-organization, sig/security, triage/accepted
- **变更说明：**
  消除md5使用并阻止新用法，提升安全性，涉及kubelet、kubectl等多个组件清理。

### PR #133779: Remove deprecated pod-infra-container-image flag
- **链接：** https://github.com/kubernetes/kubernetes/pull/133779
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, size/XS, release-note-action-required, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  移除kubelet已弃用的pod-infra-container-image标志，完成清理工作。

### PR #133980: [KEP-4330] add min-compatibility-version to control plane.
- **链接：** https://github.com/kubernetes/kubernetes/pull/133980
- **状态：** closed
- **已合并：** 是
- **作者：** siyuanfoundation
- **标签：** area/test, sig/scheduling, area/apiserver, lgtm, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, sig/architecture, ok-to-test, needs-priority, triage/accepted, sig/etcd
- **变更说明：**
  基于KEP-4330在控制平面添加min-compatibility-version字段，支持API兼容性管理，涉及多个SIG组件。

### PR #134103: [DRA] Fix ConsumableCapacity to be able to allocate the same device that previously consumed the counterSet
- **链接：** https://github.com/kubernetes/kubernetes/pull/134103
- **状态：** closed
- **已合并：** 是
- **作者：** sunya-ch
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, area/dependency, needs-triage, wg/device-management
- **变更说明：**
  修复DRA中ConsumableCapacity无法分配先前消耗counterSet的相同设备的问题。调整分配逻辑确保设备可重复分配。

### PR #134152: DRA: device taints: new ResourceSlice API, new features
- **链接：** https://github.com/kubernetes/kubernetes/pull/134152
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, area/release-eng, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, sig/release, area/code-generation, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  实现DRA设备污点功能，引入ResourceSlice API，移除DeviceTaintRule中不支持的DeviceClass和CEL selectors字段，新增'None'效果用于预览设备污点行为。

### PR #134157: Forget pod from scheduler's cache immediately when it's deleted
- **链接：** https://github.com/kubernetes/kubernetes/pull/134157
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, release-note, size/XL, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  优化调度器性能，Pod删除后立即从缓存移除，避免缓存残留影响调度。

### PR #134263: Add given namespace in dryrun=client output of HPA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134263
- **状态：** closed
- **已合并：** 是
- **作者：** ardaguclu
- **标签：** kind/bug, area/test, priority/backlog, area/kubectl, lgtm, release-note, size/S, approved, sig/cli, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  修复kubectl autoscale在dry-run=client时输出无效HPA对象的问题。显式为dry-run=client场景添加namespace字段，确保输出对象格式正确。

### PR #134313: [KEP:4827] Structured statusz
- **链接：** https://github.com/kubernetes/kubernetes/pull/134313
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, needs-priority, needs-triage
- **变更说明：**
  实现KEP-4827结构化statusz端点，为apiserver、kubelet等组件提供机器可读的状态信息。

### PR #134378: Introduce --as-user-extra persistent flag in kubectl
- **链接：** https://github.com/kubernetes/kubernetes/pull/134378
- **状态：** closed
- **已合并：** 是
- **作者：** ardaguclu
- **标签：** area/test, priority/backlog, lgtm, release-note, size/L, kind/feature, approved, sig/cli, cncf-cla: yes, sig/testing, tide/merge-method-squash, triage/accepted
- **变更说明：**
  kubectl新增--as-user-extra持久标志，支持在模拟时传递额外用户参数，增强权限管理灵活性。

### PR #134445: kubelet: synchronously fetch node and retry on NodeAffinity admission errors
- **链接：** https://github.com/kubernetes/kubernetes/pull/134445
- **状态：** closed
- **已合并：** 是
- **作者：** natasha41575
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/XL, approved, cncf-cla: yes, needs-triage
- **变更说明：**
  修复kubelet因informer缓存过时导致的NodeAffinity admission错误。当admission handler遇到节点亲和性问题时，同步从api服务器获取节点并更新缓存后重试。包含简化getNodeAnyway函数和更新predicate admit handler两个提交。

### PR #134452: DRA: lock to default-on
- **链接：** https://github.com/kubernetes/kubernetes/pull/134452
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** area/test, kind/cleanup, sig/scheduling, lgtm, sig/node, release-note, size/M, kind/api-change, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将DynamicResourceAllocation（DRA）核心功能的功能门锁定为默认启用。该功能在1.34版本GA后运行稳定，现已无法禁用。

### PR #134457: KEP-3015: update PreferSameTrafficDistribution to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134457
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** area/test, priority/important-soon, sig/network, area/kube-proxy, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, triage/accepted
- **变更说明：**
  将Service的trafficDistribution字段值PreferSameZone和PreferSameNode提升为GA状态。弃用原有PreferClose值，推荐使用更明确的PreferSameZone。基于KEP-3015。

### PR #134466: DRA: Allow AllocationMode: All from multi-node resource pools
- **链接：** https://github.com/kubernetes/kubernetes/pull/134466
- **状态：** closed
- **已合并：** 是
- **作者：** mortent
- **标签：** kind/bug, priority/important-soon, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, triage/accepted, wg/device-management
- **变更说明：**
  修复DRA中AllocationMode: All在多节点资源池中的失败问题。调整资源池完整性检查逻辑，避免因忽略非当前节点的ResourceSlices而误判池不完整。

### PR #134493: Promote KEP-5311 (Relaxed validation for Services names) to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/134493
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** sig/network, lgtm, release-note, size/S, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将服务名称宽松验证(RelaxedServiceNameValidation)特性提升至beta阶段，默认启用NameIsDNSLabel()验证规则。

### PR #134523: KEP-5004: DRAExtendedResource metrics
- **链接：** https://github.com/kubernetes/kubernetes/pull/134523
- **状态：** closed
- **已合并：** 是
- **作者：** bitoku
- **标签：** sig/scheduling, lgtm, sig/node, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, sig/instrumentation, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  基于KEP-5004添加DRA扩展资源相关指标，增强Dynamic Resource Allocation的监控能力。

### PR #134624: Promote Pod Certificates feature to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/134624
- **状态：** closed
- **已合并：** 是
- **作者：** yt2985
- **标签：** area/test, area/kubelet, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, ok-to-test, needs-priority, api-review, needs-triage, area/stable-metrics, sig/etcd
- **变更说明：**
  Pod Certificates特性升级至beta，引入v1beta1 API并移除v1alpha1 API，特性门控默认关闭。

### PR #134647: Enable `MutableCSINodeAllocatableCount` by default in Beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/134647
- **状态：** closed
- **已合并：** 是
- **作者：** torredil
- **标签：** lgtm, sig/storage, release-note, size/XS, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  在beta阶段默认启用MutableCSINodeAllocatableCount特性，支持动态调整CSI节点可分配资源计数。

### PR #134691: Lock SystemdWatchdog feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/134691
- **状态：** closed
- **已合并：** 是
- **作者：** SergeyKanzhelev
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  锁定SystemdWatchdog特性门控至默认开启状态，后续版本将移除该门控，功能可通过系统直接控制。

### PR #134709: kubectl: Add support for tracing
- **链接：** https://github.com/kubernetes/kubernetes/pull/134709
- **状态：** closed
- **已合并：** 是
- **作者：** tchap
- **标签：** priority/backlog, area/kubectl, lgtm, release-note, size/M, kind/feature, approved, sig/cli, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  为kubectl新增追踪支持，添加--profile=trace选项。同时修复性能分析初始化的资源泄漏问题，确保输出文件正确关闭。

### PR #134730: Verify if pod has ongoing async preemption before evicting pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/134730
- **状态：** closed
- **已合并：** 是
- **作者：** ania-borowiec
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, release-note, size/XL, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  在驱逐pod前添加异步抢占状态检查。确保pod没有正在进行异步抢占时才执行驱逐，防止错误驱逐操作。

### PR #134740: remove taint values from unschedulable messages in pod status
- **链接：** https://github.com/kubernetes/kubernetes/pull/134740
- **状态：** closed
- **已合并：** 是
- **作者：** hoskeri
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/S, approved, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  kube-scheduler不再在pod状态中显示具体的taint键值信息。改用通用消息描述调度失败原因，敏感信息仅记录在日志中。

### PR #134743: kubelet: fix kubeletconfig.cgroupDriver in configz
- **链接：** https://github.com/kubernetes/kubernetes/pull/134743
- **状态：** closed
- **已合并：** 是
- **作者：** marquiz
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复kubelet configz端点中cgroupDriver配置显示不准确的问题。延迟初始化configz处理器以确保正确反映来自CRI的设置。

### PR #134744: vendor: update system-validators to v1.12.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/134744
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/important-soon, lgtm, sig/node, sig/cluster-lifecycle, size/M, kind/feature, release-note-action-required, approved, area/kubeadm, cncf-cla: yes, area/dependency, triage/accepted
- **变更说明：**
  更新system-validators依赖至v1.12.1版本。改进kubeadm等相关组件的系统验证能力。

### PR #134746: KEP-4781: Restarting kubelet does not change pod status
- **链接：** https://github.com/kubernetes/kubernetes/pull/134746
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-triage
- **变更说明：**
  实现KEP-4781功能：kubelet重启时不再改变pod状态。提升kubelet重启过程中的pod状态稳定性。

### PR #134760: Add step field in SizeRange struct for volume_expand tests
- **链接：** https://github.com/kubernetes/kubernetes/pull/134760
- **状态：** closed
- **已合并：** 是
- **作者：** Rishita-Golla
- **标签：** area/test, kind/cleanup, lgtm, sig/storage, release-note, size/S, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, area/e2e-test-framework, needs-triage
- **变更说明：**
  在volume_expand测试的SizeRange结构中添加step字段，优化存储卷扩展测试的粒度控制。

### PR #134769: fix: allow job startTime updates on resume from suspended state
- **链接：** https://github.com/kubernetes/kubernetes/pull/134769
- **状态：** closed
- **已合并：** 是
- **作者：** dejanzele
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, sig/testing, api-review, triage/accepted
- **变更说明：**
  修复Job从暂停状态恢复时startTime更新被错误阻止的问题，确保Job控制器正确处理暂停操作。

### PR #134777: Promote KUBECTL_COMMAND_HEADERS to stable
- **链接：** https://github.com/kubernetes/kubernetes/pull/134777
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** area/test, kind/cleanup, area/kubectl, lgtm, release-note, size/M, kind/feature, approved, sig/cli, cncf-cla: yes, sig/testing, priority/important-longterm, triage/accepted
- **变更说明：**
  将KUBECTL_COMMAND_HEADERS功能提升为稳定版。基于KEP-859，支持为kubectl命令添加自定义头部。

### PR #134779: etcd: Bump supported etcd version to v3.5.24 for release v1.32, v1.33, and v1.34
- **链接：** https://github.com/kubernetes/kubernetes/pull/134779
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XS, area/release-eng, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将etcd支持版本升级至v3.5.24，适用于Kubernetes v1.32、v1.33和v1.34版本。

### PR #134784: SVM: bump the API to beta, remove unused fields
- **链接：** https://github.com/kubernetes/kubernetes/pull/134784
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, size/XXL, kind/api-change, kind/feature, release-note-action-required, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, needs-triage, sig/etcd
- **变更说明：**
  将SVM API升级至beta版本，移除未使用字段，涉及API变更和功能增强。

### PR #134793: DRA allocator: Add the requests corresponding to the config FromClass
- **链接：** https://github.com/kubernetes/kubernetes/pull/134793
- **状态：** closed
- **已合并：** 是
- **作者：** LionelJouin
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRA分配器bug，确保FromClass配置正确映射到资源请求。

### PR #134803: KEP-5284: Implement Constrained Impersonation
- **链接：** https://github.com/kubernetes/kubernetes/pull/134803
- **状态：** closed
- **已合并：** 是
- **作者：** enj
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  实现KEP-5284受限模拟功能（Constrained Impersonation），增强API安全控制能力。

### PR #134826: CSI driver opt-in for service account tokens via secrets field
- **链接：** https://github.com/kubernetes/kubernetes/pull/134826
- **状态：** closed
- **已合并：** 是
- **作者：** aramase
- **标签：** area/test, lgtm, sig/storage, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  CSI驱动可通过spec.secrets字段选择加入服务账户令牌功能，增强令牌管理安全性。

### PR #134833: Return error in case of discovery client failure
- **链接：** https://github.com/kubernetes/kubernetes/pull/134833
- **状态：** closed
- **已合并：** 是
- **作者：** rikatz
- **标签：** kind/bug, priority/important-soon, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复kubectl api-resources在Discovery Client失败时的panic问题。当无法连接Kubernetes服务器时（如未设置KUBECONFIG），改为返回错误而非在数组迭代时panic。

### PR #134875: Fix bug in reporting health for templated and renamed DRA claims
- **链接：** https://github.com/kubernetes/kubernetes/pull/134875
- **状态：** closed
- **已合并：** 是
- **作者：** Jpsassine
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRA声明在模板化和重命名后健康报告错误的bug，提升设备管理可靠性。

### PR #134905: scheduler: KEP-5007 Add BindingTimeout args to DynamicResources plugin
- **链接：** https://github.com/kubernetes/kubernetes/pull/134905
- **状态：** closed
- **已合并：** 是
- **作者：** fj-naji
- **标签：** sig/scheduling, lgtm, sig/node, release-note, size/L, kind/api-change, kind/feature, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  基于KEP-5007为DynamicResources插件添加bindingTimeout参数，允许配置DRA设备绑定等待超时（默认600秒）。

### PR #134906: kubeadm: added container runtime version check to preflight
- **链接：** https://github.com/kubernetes/kubernetes/pull/134906
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** lgtm, sig/cluster-lifecycle, release-note, size/L, kind/feature, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  kubeadm预检阶段新增容器运行时版本检查功能，增强集群初始化时的运行时兼容性验证。

### PR #134948: Promote Pod Generation to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134948
- **状态：** closed
- **已合并：** 是
- **作者：** natasha41575
- **标签：** area/test, priority/important-soon, area/kubelet, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-triage
- **变更说明：**
  将Pod Generation功能（KEP-5067）提升至GA，正式稳定Pod生成追踪能力。

### PR #134949: Promote InPlacePodVerticalScaling to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134949
- **状态：** closed
- **已合并：** 是
- **作者：** natasha41575
- **标签：** priority/important-soon, area/kubelet, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/M, kind/feature, approved, cncf-cla: yes, needs-triage
- **变更说明：**
  将InPlacePodVerticalScaling功能（KEP-1287）提升至GA，支持原地Pod垂直伸缩。

---
*本报告由 Containerd Release Tracker 自动生成*
# Kubernetes 版本发布分析报告
## Kubernetes v1.35.0-alpha.2 (v1.35.0-alpha.2)

### 📋 版本信息
- **版本标签：** v1.35.0-alpha.2
- **版本名称：** Kubernetes v1.35.0-alpha.2
- **发布时间：** 2025-10-22T22:03:54Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.0-alpha.2

### 🔍 分析统计
- **分析时间：** 2025-10-23 03:09:24
- **分析的 PR 数量：** 34
- **分析的 Issue 数量：** 9
- **重要项目数量：** 43

## 📊 版本概述
Kubernetes v1.35.0-alpha.2 引入了多项 API 推广、关键 Bug 修复和安全增强，包括 cgroupV1 和 IPVS 的废弃警告。

## 🔒 安全问题修复
1. ⚠️ 修复客户端 CA 和请求头 CA 验证重叠问题 - [PR #131411](https://github.com/kubernetes/kubernetes/pull/131411) - **风险级别：** 中 - 可能允许权限提升
2. ⚠️ 客户端 CA 和请求头 CA 可能共享同一 CA 的安全风险 - [Issue #119267](https://github.com/kubernetes/kubernetes/issues/119267) - **风险级别：** 高 - 错误配置可能导致集群管理员权限提升

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 CRD 缺少 openAPIV3Schema 时的 panic 问题 - [PR #133721](https://github.com/kubernetes/kubernetes/pull/133721) - **影响：** 可能导致 API Server 崩溃，影响集群稳定性
2. 修复嵌套 map 段错误导致的崩溃 - [PR #134381](https://github.com/kubernetes/kubernetes/pull/134381) - **影响：** 处理复杂配置时可能触发段错误
3. 修复 DRA 设备污点的 NoExecute 容忍问题 - [PR #134479](https://github.com/kubernetes/kubernetes/pull/134479) - **影响：** 使用 DRA 的设备可能被错误驱逐
4. 修复 IPv6 /64 CIDR 分配器越界分配问题 - [PR #134193](https://github.com/kubernetes/kubernetes/pull/134193) - **影响：** 可能导致网络地址冲突
5. 修复 sidecar 容器 startup probe worker 错误终止问题 - [PR #133072](https://github.com/kubernetes/kubernetes/pull/133072) - **影响：** 可能导致主容器卡在 Initializing 状态
6. 修复 APF 座位计数不准确问题 - [PR #134601](https://github.com/kubernetes/kubernetes/pull/134601) - **影响：** API Server 可能面临 CPU 过载风险
7. 修复 DRA 可消耗容量调度多个设备的问题 - [PR #133706](https://github.com/kubernetes/kubernetes/pull/133706) - **影响：** 影响设备资源分配的正确性

## 💥 破坏性变更
1. 🚨 为 exec、attach、portforward 添加合成 create 权限检查 - [PR #134577](https://github.com/kubernetes/kubernetes/pull/134577) - **影响：** 需要更新 RBAC 规则，确保相关角色包含 create 权限
2. 🚨 废弃 cgroupV1 支持 - [PR #134298](https://github.com/kubernetes/kubernetes/pull/134298) - **影响：** 必须迁移到 cgroupV2
3. 🚨 移除 policyv1beta1 PodDisruptionBudget 支持 - [PR #134685](https://github.com/kubernetes/kubernetes/pull/134685) - **影响：** 需要更新到 policy/v1 API
4. 🚨 停止提供 storage.k8s.io/v1alpha1 VolumeAttributesClass API - [PR #134625](https://github.com/kubernetes/kubernetes/pull/134625) - **影响：** 需要迁移到稳定版本 API

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 废弃 cgroupV1 支持 - [PR #134298](https://github.com/kubernetes/kubernetes/pull/134298)
2. 标记 IPVS 模式为废弃 - [PR #134539](https://github.com/kubernetes/kubernetes/pull/134539)
3. HPA 可配置容忍度推广到 Beta - [PR #133128](https://github.com/kubernetes/kubernetes/pull/133128)
4. StatefulSet MaxUnavailable 推广到 Beta - [PR #133153](https://github.com/kubernetes/kubernetes/pull/133153)
5. 删除 gogo protobuf 运行时依赖 - [PR #134256](https://github.com/kubernetes/kubernetes/pull/134256)
6. ContainerRestartRules 推广到 Beta - [PR #134631](https://github.com/kubernetes/kubernetes/pull/134631)
7. StrictCPUReservationOption 推广到 GA - [PR #134388](https://github.com/kubernetes/kubernetes/pull/134388)
8. 拓扑管理器 max-allowable-numa-nodes 推广到 GA - [PR #134614](https://github.com/kubernetes/kubernetes/pull/134614)

## 🚀 性能优化
1. 优化 APF 座位计数准确性 - [PR #134601](https://github.com/kubernetes/kubernetes/pull/134601) - **提升：** 防止 API Server CPU 过载
2. 改进 pod 控制器索引维度 - [PR #134654](https://github.com/kubernetes/kubernetes/pull/134654) - **提升：** 提高控制器处理效率
3. 升级到 Go 1.25.3 - [PR #134598](https://github.com/kubernetes/kubernetes/pull/134598) - **提升：** 包含性能优化和安全修复

## 🎯 风险评估
整体风险评估：中等风险。主要风险来自废弃功能迁移和权限模型变更。建议在测试环境中充分验证所有工作负载，特别是涉及 DRA、sidecar 容器和网络策略的场景。建议等待 beta 版本发布后再考虑生产环境升级。

## 📋 升级建议
1. 升级前检查所有自定义 RBAC 规则，确保为 pods/exec、pods/attach、pods/portforward 包含 create 权限
2. 立即开始规划从 cgroupV1 和 IPVS 迁移到替代方案
3. 在测试环境中充分验证 DRA 相关功能，特别是设备污点和容量分配
4. 监控 API Server 日志中的废弃警告，及时处理相关配置
5. 确保 etcd 版本升级到 v3.5.23 或 v3.5.24
6. 对于使用 sidecar 容器和 startup probe 的应用，进行回归测试

## 📋 Release 包含的变更

### PR #131411: Fix overlapping client CA and requestheader CA validation with proper certificate checking
- **链接：** https://github.com/kubernetes/kubernetes/pull/131411
- **状态：** closed
- **已合并：** 是
- **作者：** ballista01
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, sig/security, triage/accepted
- **变更说明：**
  修复客户端CA和requestheader CA重叠验证问题，通过正确的证书检查防止潜在安全风险。这是一个安全修复。

### PR #132927: DRA API: implement ResourceClaim strategy for DRADeviceTaints
- **链接：** https://github.com/kubernetes/kubernetes/pull/132927
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, lgtm, release-note, size/XXL, approved, cncf-cla: yes, needs-priority, api-review, needs-triage, wg/device-management
- **变更说明：**
  实现ResourceClaim策略以处理DRADeviceTaints，修复未正确丢弃Tolerations字段的问题，关联KEP #5055。

### PR #133072: Fix startup probe worker termination for sidecar containers
- **链接：** https://github.com/kubernetes/kubernetes/pull/133072
- **状态：** closed
- **已合并：** 是
- **作者：** AadiDev005
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, ok-to-test, triage/accepted
- **变更说明：**
  修复sidecar容器启动探针worker终止问题。当Pod restartPolicy=Never且sidecar容器restartPolicy=Always时，主容器卡在"Initializing"状态。解决方案是添加容器级重启策略检查。

### PR #133128: Promote HPAConfigurableTolerance gate to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/133128
- **状态：** closed
- **已合并：** 是
- **作者：** jm-franc
- **标签：** lgtm, sig/api-machinery, release-note, sig/autoscaling, size/S, kind/api-change, kind/feature, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted
- **变更说明：**
  将HPAConfigurableTolerance特性门提升至beta阶段并默认启用，允许配置HPA容忍度，关联KEP #4951。

### PR #133153: Update MaxUnavailableStatefulSet feature gate to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/133153
- **状态：** closed
- **已合并：** 是
- **作者：** helayoty
- **标签：** lgtm, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted
- **变更说明：**
  将MaxUnavailableStatefulSet特性门提升至beta阶段并默认启用，优化StatefulSet滚动更新，关联KEP #961。

### PR #133373: [Carry 133278] kubelet: Don't ignore idsPerPod config #133278
- **链接：** https://github.com/kubernetes/kubernetes/pull/133373
- **状态：** closed
- **已合并：** 是
- **作者：** AkihiroSuda
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  修复kubelet忽略`idsPerPod`配置的bug，通过将idsPerPod作为参数传递给MakeUserNsManager，确保user namespaces配置正确应用，避免默认值覆盖。

### PR #133706: Fix DRAConsumableCapacity to schedule more than one devices
- **链接：** https://github.com/kubernetes/kubernetes/pull/133706
- **状态：** closed
- **已合并：** 是
- **作者：** sunya-ch
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRAConsumableCapacity问题，使其能够调度多个设备。这是一个bug修复，涉及Dynamic Resource Allocation (DRA) 的容量计算问题，确保资源分配正确性。

### PR #133721: fix panic for the crd with subresource but lose openAPIV3Schema
- **链接：** https://github.com/kubernetes/kubernetes/pull/133721
- **状态：** closed
- **已合并：** 是
- **作者：** fusida
- **标签：** kind/bug, area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, area/provider/gcp, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, sig/autoscaling, size/L, kind/api-change, area/release-eng, sig/auth, sig/apps, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, sig/release, sig/architecture, area/conformance, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, area/e2e-test-framework, area/dependency, triage/accepted, area/stable-metrics, sig/etcd, wg/device-management
- **变更说明：**
  修复CRD带有子资源但缺少openAPIV3Schema时导致的panic问题。这是一个稳定性修复。

### PR #133778: Remove the --pod-infra-container-image flag from kubeadm and cluster/gce
- **链接：** https://github.com/kubernetes/kubernetes/pull/133778
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/cleanup, lgtm, area/provider/gcp, sig/cluster-lifecycle, release-note, size/L, approved, area/kubeadm, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  移除kubeadm和cluster/gce中无效的--pod-infra-container-image标志，清理无用参数。

### PR #134193: Fix IPv6 allocator for /64 CIDRs
- **链接：** https://github.com/kubernetes/kubernetes/pull/134193
- **状态：** closed
- **已合并：** 是
- **作者：** hoskeri
- **标签：** kind/bug, sig/network, lgtm, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复IPv6分配器在/64 CIDR中分配地址超出范围的问题，使用math/big.Int.SetUint64()替换不当类型转换。

### PR #134256: KEP-5589 - drop gogo runtime dependencies
- **链接：** https://github.com/kubernetes/kubernetes/pull/134256
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** sig/network, area/kubelet, kind/cleanup, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/architecture, area/code-generation, needs-priority, area/dependency, needs-triage, wg/device-management
- **变更说明：**
  移除对gogo protobuf的运行时依赖，完成KEP-5589第一阶段。包括丢弃未使用的protobuf方法和重定位ProtoMessage方法。

### PR #134298: [KEP-5573] Set failCgroupV1 to true
- **链接：** https://github.com/kubernetes/kubernetes/pull/134298
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/kubelet, lgtm, sig/node, size/M, kind/api-change, release-note-action-required, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, kind/deprecation, needs-triage
- **变更说明：**
  设置failCgroupV1为true，作为cgroup v1弃用计划的一部分（KEP-5573），需要用户关注相关变更。

### PR #134381: fix nested map segmentation fault
- **链接：** https://github.com/kubernetes/kubernetes/pull/134381
- **状态：** closed
- **已合并：** 是
- **作者：** kon-angelo
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/S, approved, sig/cli, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  修复嵌套map操作导致的段错误问题。这是一个稳定性修复，防止在某些操作条件下发生崩溃。

### PR #134388: KEP-4540: StrictCPUReservationOption moved to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134388
- **状态：** closed
- **已合并：** 是
- **作者：** psasnal
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  将CPU Manager静态策略选项`strict-cpu-reservation`提升至GA状态，基于KEP-4540，影响kubelet组件配置，用户可通过release-note获取更新信息。

### PR #134433: kubeadm: print errors during control-plane-wait retries
- **链接：** https://github.com/kubernetes/kubernetes/pull/134433
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/XS, kind/feature, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  在kubeadm的control-plane等待重试期间打印错误信息，改进调试体验。

### PR #134479: DRA device taints: fix toleration of NoExecute
- **链接：** https://github.com/kubernetes/kubernetes/pull/134479
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, sig/node, release-note, size/L, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRA设备污点容忍问题，特别是NoExecute污点。调度器未将容忍信息复制到状态，导致Pod被立即驱逐。修复后确保容忍正确应用。

### PR #134481: Update --chunk-size flag, dropping the beta information
- **链接：** https://github.com/kubernetes/kubernetes/pull/134481
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/documentation, kind/cleanup, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  将--chunk-size标志从beta状态提升为稳定状态。影响kubectl describe、get、drain和events命令，该功能自2017年引入现已正式稳定。

### PR #134510: build by running kube-cross directly
- **链接：** https://github.com/kubernetes/kubernetes/pull/134510
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** kind/cleanup, lgtm, release-note, size/L, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  构建系统清理，直接运行kube-cross进行构建，简化构建过程并优化依赖管理。

### PR #134539: KEP: 5495 - Add deprecation warning for ipvs
- **链接：** https://github.com/kubernetes/kubernetes/pull/134539
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** sig/network, area/kube-proxy, lgtm, release-note, size/XS, approved, cncf-cla: yes, needs-priority, kind/deprecation, triage/accepted
- **变更说明：**
  在kube-proxy的ipvs模式启动时添加弃用警告，ipvs将被弃用，建议用户迁移到nftables，基于KEP #5495。

### PR #134577: Implements synthetic create authz permission check for exec, attach, and portforward
- **链接：** https://github.com/kubernetes/kubernetes/pull/134577
- **状态：** closed
- **已合并：** 是
- **作者：** seans3
- **标签：** area/test, priority/important-soon, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  为exec、attach和portforward子资源实现WebSocket升级请求的合成授权create权限检查，新增AuthorizePodWebsocketUpgradeCreatePermission特性门（beta，默认启用），需更新ClusterRoles和Roles。

### PR #134588: go 1.25.2/1.24.8 related fixes
- **链接：** https://github.com/kubernetes/kubernetes/pull/134588
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, sig/auth, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-triage
- **变更说明：**
  修复Go 1.25.2/1.24.8相关问题：IPv6比较错误、证书中无效email和DNS SAN生成，并添加集成测试验证修复。

### PR #134598: bump to go 1.25.3
- **链接：** https://github.com/kubernetes/kubernetes/pull/134598
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** kind/cleanup, lgtm, release-note, size/XS, area/release-eng, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  将Go版本升级到1.25.3，属于常规版本更新。

### PR #134601: Properly account APF seats for legacy watches that compute init-events
- **链接：** https://github.com/kubernetes/kubernetes/pull/134601
- **状态：** closed
- **已合并：** 是
- **作者：** shyamjvs
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复APF（API Priority and Fairness）座位计数问题，针对legacy watch调用（RV=0或未设置）生成init-events的情况。这防止API服务器CPU过载，用户可能会看到这些调用被更多节流。

### PR #134611: [go] Bump images, dependencies and versions to go 1.25.3 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/134611
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, area/provider/gcp, sig/storage, release-note, size/M, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, sig/architecture, area/conformance, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  升级构建系统到Go 1.25.3，并更新debian-base、setcap和distroless iptables等依赖。

### PR #134614: KEP-4622: promote topology manager `max-allowable-numa-nodes` to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134614
- **状态：** closed
- **已合并：** 是
- **作者：** ffromani
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将Topology Manager策略选项max-allowable-numa-nodes提升到GA状态。该功能用于控制NUMA节点分配策略。

### PR #134625: Drop alphas no longer served in 1.35
- **链接：** https://github.com/kubernetes/kubernetes/pull/134625
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** area/test, kind/cleanup, lgtm, sig/storage, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted, sig/etcd
- **变更说明：**
  在Kubernetes 1.35中停止提供storage.k8s.io/v1alpha1 VolumeAttributesClass API。这是一个清理操作，移除不再服务的alpha API。

### PR #134631: Promote ContainerRestartRules to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/134631
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将ContainerRestartRules功能提升到beta，并修复一个bug（探针在容器终止后继续运行）。功能门默认启用。

### PR #134635: Locked the (generally available) feature gate `ExecProbeTimeout` to true. 
- **链接：** https://github.com/kubernetes/kubernetes/pull/134635
- **状态：** closed
- **已合并：** 是
- **作者：** vivzbansal
- **标签：** area/test, lgtm, sig/node, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  将ExecProbeTimeout功能门锁定为true，表示该功能已正式可用且不可禁用。

### PR #134654: Include relevant dimensions in pod controller indexing
- **链接：** https://github.com/kubernetes/kubernetes/pull/134654
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复pod控制器uid索引问题，索引现在包含ownerReference的namespace、kind和name，防止在uid不正确时控制器混淆，影响kube-controller-manager，需回溯至1.33和1.34版本。

### PR #134656: additional build simplification, drop rsync requirement
- **链接：** https://github.com/kubernetes/kubernetes/pull/134656
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** kind/cleanup, lgtm, release-note, size/L, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  简化构建过程，移除对rsync的依赖，属于清理性质PR，旨在提升构建系统效率。

### PR #134685: Drop support for policyv1beta1.PodDisruptionBudget in kubectl
- **链接：** https://github.com/kubernetes/kubernetes/pull/134685
- **状态：** closed
- **已合并：** 是
- **作者：** scaliby
- **标签：** kind/cleanup, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  在kubectl中移除对policyv1beta1 PodDisruptionBudget的支持，清理已弃用API版本。

### PR #134692: etcd: Bump supported etcd version to v3.5.23 for release v1.31, v1.32, and v1.33
- **链接：** https://github.com/kubernetes/kubernetes/pull/134692
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** priority/important-soon, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/XS, approved, area/kubeadm, cncf-cla: yes, triage/accepted, sig/etcd
- **变更说明：**
  将支持的etcd版本升级到v3.5.23，适用于Kubernetes v1.31、v1.32和v1.33版本。

### PR #134729: kep-4762: Promote HostnameOverride feature gate to beta stage
- **链接：** https://github.com/kubernetes/kubernetes/pull/134729
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** sig/network, lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将HostnameOverride特性门提升至beta阶段，基于KEP-4762。

### PR #134779: etcd: Bump supported etcd version to v3.5.24 for release v1.32, v1.33, and v1.34
- **链接：** https://github.com/kubernetes/kubernetes/pull/134779
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XS, area/release-eng, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将etcd支持版本升级至v3.5.24，适用于Kubernetes v1.32、v1.33和v1.34版本，涉及多个SIG（如api-machinery、cluster-lifecycle），确保组件兼容性。

---
*本报告由 Containerd Release Tracker 自动生成*
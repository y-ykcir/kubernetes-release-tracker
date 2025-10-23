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
- **分析时间：** 2025-10-23 03:56:59
- **分析的 PR 数量：** 34
- **分析的 Issue 数量：** 9
- **重要项目数量：** 43

## 📊 版本概述
Kubernetes v1.35.0-alpha.2 引入了多项 API 变更、功能提升和关键 Bug 修复，重点关注 cgroup v1 废弃、ipvs 废弃以及安全改进。

## 🔒 安全问题修复
1. ⚠️ 修复客户端 CA 和请求头 CA 使用相同证书机构时的验证问题 - [PR #131411](https://github.com/kubernetes/kubernetes/pull/131411) - **风险级别：** 中 - 可能允许权限提升
2. ⚠️ WebSocket 升级请求授权检查增强 - [PR #134577](https://github.com/kubernetes/kubernetes/pull/134577) - **风险级别：** 低 - 要求 exec/attach/portforward 子资源具有 create 权限 - [Issue #133515](https://github.com/kubernetes/kubernetes/issues/133515)

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 CRD 缺少 openAPIV3Schema 时的 panic 问题 - [PR #133721](https://github.com/kubernetes/kubernetes/pull/133721) - **影响：** 防止 API 服务器崩溃，确保集群稳定性
2. 修复客户端 CA 和请求头 CA 验证重叠问题 - [PR #131411](https://github.com/kubernetes/kubernetes/pull/131411) - **影响：** 解决潜在的安全漏洞，防止证书验证绕过
3. 修复 sidecar 容器启动探针工作器终止问题 - [PR #133072](https://github.com/kubernetes/kubernetes/pull/133072) - **影响：** 避免主容器卡在 Initializing 状态
4. 修复 IPv6 分配器超出 CIDR 范围的问题 - [PR #134193](https://github.com/kubernetes/kubernetes/pull/134193) - **影响：** 确保 IPv6 服务 CIDR 正确分配地址
5. 修复嵌套映射段错误 - [PR #134381](https://github.com/kubernetes/kubernetes/pull/134381) - **影响：** 防止 API 服务器在处理复杂对象时崩溃
6. 修复 DRA 设备污点 NoExecute 容忍问题 - [PR #134479](https://github.com/kubernetes/kubernetes/pull/134479) - **影响：** 避免 Pod 被立即驱逐，确保资源分配稳定性

## 💥 破坏性变更
1. 🚨 启动探针工作器终止逻辑变更 - [PR #133072](https://github.com/kubernetes/kubernetes/pull/133072) - **影响：** 需要验证 sidecar 容器行为，特别是 restartPolicy=Never 的场景
2. 🚨 kubectl 移除对 policyv1beta1 PodDisruptionBudget 的支持 - [PR #134685](https://github.com/kubernetes/kubernetes/pull/134685) - **影响：** 需要更新 PDB 资源到 policy/v1 API 版本
3. 🚨 ExecProbeTimeout 功能门锁定为 true - [PR #134635](https://github.com/kubernetes/kubernetes/pull/134635) - **影响：** 可能影响现有执行探针超时配置
4. 🚨 停止提供 storage.k8s.io/v1alpha1 VolumeAttributesClass API - [PR #134625](https://github.com/kubernetes/kubernetes/pull/134625) - **影响：** 需要迁移到稳定 API 版本

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. cgroup v1 支持废弃 - [PR #134298](https://github.com/kubernetes/kubernetes/pull/134298) - **影响：** 使用 cgroup v1 的环境需要迁移到 cgroup v2
2. IPVS 模式废弃警告 - [PR #134539](https://github.com/kubernetes/kubernetes/pull/134539) - **影响：** kube-proxy 用户需要逐步迁移到 nftables
3. HPA 可配置容忍度提升至 Beta - [PR #133128](https://github.com/kubernetes/kubernetes/pull/133128) - **影响：** 允许更精细的水平 Pod 自动扩缩容控制
4. StatefulSet 最大不可用提升至 Beta - [PR #133153](https://github.com/kubernetes/kubernetes/pull/133153) - **影响：** 提升 StatefulSet 滚动更新性能
5. 删除 gogo protobuf 运行时依赖 - [PR #134256](https://github.com/kubernetes/kubernetes/pull/134256) - **影响：** 移除不维护的依赖项，提高代码安全性

## 🚀 性能优化
1. APF 座位计算优化 - [PR #134601](https://github.com/kubernetes/kubernetes/pull/134601) - **提升：** 更准确地反映 API 服务器负载，防止 CPU 过载
2. 拓扑管理器 max-allowable-numa-nodes 提升至 GA - [PR #134614](https://github.com/kubernetes/kubernetes/pull/134614) - **提升：** 改进 NUMA 节点资源分配效率
3. StrictCPUReservationOption 提升至 GA - [PR #134388](https://github.com/kubernetes/kubernetes/pull/134388) - **提升：** 确保 CPU 资源预留准确性
4. 构建系统简化，移除 rsync 依赖 - [PR #134656](https://github.com/kubernetes/kubernetes/pull/134656) - **提升：** 加快构建速度，简化依赖管理

## 🎯 风险评估
整体风险评估：高（alpha 版本不建议用于生产环境）。建议在测试环境中充分验证后再考虑升级，特别需要关注废弃功能迁移、安全配置验证和性能监控。

## 📋 升级建议
1. 升级前全面测试集群，重点关注 sidecar 容器启动行为和探针配置
2. 检查并更新 RBAC 权限，确保 exec/attach/portforward 子资源包含 create 动词
3. 评估 cgroup v1 和 IPVS 使用情况，制定迁移计划
4. 验证所有 CRD 资源是否正确定义了 openAPIV3Schema
5. 监控 API 服务器性能，特别是 APF 座位使用情况，防止意外节流
6. 对于使用 DRA 功能的集群，测试设备分配和污点容忍行为

## 📋 Release 包含的变更

### PR #131411: Fix overlapping client CA and requestheader CA validation with proper certificate checking
- **链接：** https://github.com/kubernetes/kubernetes/pull/131411
- **状态：** closed
- **已合并：** 是
- **作者：** ballista01
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, sig/security, triage/accepted
- **变更说明：**
  修复API服务器中client CA和requestheader CA证书验证重叠的bug，通过正确检查证书确保安全性。

### PR #132927: DRA API: implement ResourceClaim strategy for DRADeviceTaints
- **链接：** https://github.com/kubernetes/kubernetes/pull/132927
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, lgtm, release-note, size/XXL, approved, cncf-cla: yes, needs-priority, api-review, needs-triage, wg/device-management
- **变更说明：**
  修复DRA API中ResourceClaim策略的实现缺失，确保tolerations字段正确处理。

### PR #133072: Fix startup probe worker termination for sidecar containers
- **链接：** https://github.com/kubernetes/kubernetes/pull/133072
- **状态：** closed
- **已合并：** 是
- **作者：** AadiDev005
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, ok-to-test, triage/accepted
- **变更说明：**
  修复sidecar容器启动探针worker错误终止bug，允许sidecar容器（restartPolicy=Always）在Pod（restartPolicy=Never）中重启时主容器正常启动，不影响常规容器行为。

### PR #133128: Promote HPAConfigurableTolerance gate to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/133128
- **状态：** closed
- **已合并：** 是
- **作者：** jm-franc
- **标签：** lgtm, sig/api-machinery, release-note, sig/autoscaling, size/S, kind/api-change, kind/feature, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted
- **变更说明：**
  将HPAConfigurableTolerance特性门提升至beta阶段，默认启用，允许配置HPA容忍度。

### PR #133153: Update MaxUnavailableStatefulSet feature gate to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/133153
- **状态：** closed
- **已合并：** 是
- **作者：** helayoty
- **标签：** lgtm, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted
- **变更说明：**
  将MaxUnavailableStatefulSet特性门提升至beta，默认启用，允许StatefulSet设置最大不可用副本数。

### PR #133373: [Carry 133278] kubelet: Don't ignore idsPerPod config #133278
- **链接：** https://github.com/kubernetes/kubernetes/pull/133373
- **状态：** closed
- **已合并：** 是
- **作者：** AkihiroSuda
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  修复kubelet中userns管理器忽略`idsPerPod`配置的bug。问题源于初始化顺序，配置在管理器创建后设置，解决方案是通过参数传递配置值。

### PR #133706: Fix DRAConsumableCapacity to schedule more than one devices
- **链接：** https://github.com/kubernetes/kubernetes/pull/133706
- **状态：** closed
- **已合并：** 是
- **作者：** sunya-ch
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRAConsumableCapacity组件bug，使其能够正确调度多个设备，解决了之前只能调度一个设备的限制。

### PR #133721: fix panic for the crd with subresource but lose openAPIV3Schema
- **链接：** https://github.com/kubernetes/kubernetes/pull/133721
- **状态：** closed
- **已合并：** 是
- **作者：** fusida
- **标签：** kind/bug, area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, area/provider/gcp, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, sig/autoscaling, size/L, kind/api-change, area/release-eng, sig/auth, sig/apps, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, sig/release, sig/architecture, area/conformance, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, area/e2e-test-framework, area/dependency, triage/accepted, area/stable-metrics, sig/etcd, wg/device-management
- **变更说明：**
  修复当CRD有子资源但缺失openAPIV3Schema时引发的panic问题。

### PR #133778: Remove the --pod-infra-container-image flag from kubeadm and cluster/gce
- **链接：** https://github.com/kubernetes/kubernetes/pull/133778
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/cleanup, lgtm, area/provider/gcp, sig/cluster-lifecycle, release-note, size/L, approved, area/kubeadm, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  移除kubeadm和cluster/gce中的无效标志--pod-infra-container-image。

### PR #134193: Fix IPv6 allocator for /64 CIDRs
- **链接：** https://github.com/kubernetes/kubernetes/pull/134193
- **状态：** closed
- **已合并：** 是
- **作者：** hoskeri
- **标签：** kind/bug, sig/network, lgtm, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复IPv6 ServiceCIDR分配器在/64 CIDR中分配地址超出子网范围的bug。

### PR #134256: KEP-5589 - drop gogo runtime dependencies
- **链接：** https://github.com/kubernetes/kubernetes/pull/134256
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** sig/network, area/kubelet, kind/cleanup, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/architecture, area/code-generation, needs-priority, area/dependency, needs-triage, wg/device-management
- **变更说明：**
  移除Kubernetes API类型对gogo protobuf的运行时依赖，删除未使用的protobuf方法，并重新定位ProtoMessage方法，作为KEP-5589第一阶段。

### PR #134298: [KEP-5573] Set failCgroupV1 to true
- **链接：** https://github.com/kubernetes/kubernetes/pull/134298
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/kubelet, lgtm, sig/node, size/M, kind/api-change, release-note-action-required, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, kind/deprecation, needs-triage
- **变更说明：**
  设置failCgroupV1为true，推进cgroup v1的弃用过程。

### PR #134381: fix nested map segmentation fault
- **链接：** https://github.com/kubernetes/kubernetes/pull/134381
- **状态：** closed
- **已合并：** 是
- **作者：** kon-angelo
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/S, approved, sig/cli, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  修复在处理嵌套map时引发的段错误问题。

### PR #134388: KEP-4540: StrictCPUReservationOption moved to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134388
- **状态：** closed
- **已合并：** 是
- **作者：** psasnal
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  将CPU Manager静态策略选项`strict-cpu-reservation`升级到GA版本，标志着该功能已稳定可用。关联KEP-4540，涉及kubelet组件。

### PR #134433: kubeadm: print errors during control-plane-wait retries
- **链接：** https://github.com/kubernetes/kubernetes/pull/134433
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/XS, kind/feature, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubeadm在控制平面等待重试期间打印错误信息，便于调试问题。

### PR #134479: DRA device taints: fix toleration of NoExecute
- **链接：** https://github.com/kubernetes/kubernetes/pull/134479
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, sig/node, release-note, size/L, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRA设备污点容忍bug，scheduler现在正确将NoExecute容忍信息复制到status，防止Pod被立即驱逐。

### PR #134481: Update --chunk-size flag, dropping the beta information
- **链接：** https://github.com/kubernetes/kubernetes/pull/134481
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/documentation, kind/cleanup, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  将kubectl命令的--chunk-size标志从beta状态正式稳定化，更新相关文档。

### PR #134510: build by running kube-cross directly
- **链接：** https://github.com/kubernetes/kubernetes/pull/134510
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** kind/cleanup, lgtm, release-note, size/L, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  优化构建过程，通过直接运行kube-cross而不是间接方式，简化流程。

### PR #134539: KEP: 5495 - Add deprecation warning for ipvs
- **链接：** https://github.com/kubernetes/kubernetes/pull/134539
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** sig/network, area/kube-proxy, lgtm, release-note, size/XS, approved, cncf-cla: yes, needs-priority, kind/deprecation, triage/accepted
- **变更说明：**
  标记kube-proxy的ipvs模式为弃用，添加启动警告，建议用户迁移到nftables。

### PR #134577: Implements synthetic create authz permission check for exec, attach, and portforward
- **链接：** https://github.com/kubernetes/kubernetes/pull/134577
- **状态：** closed
- **已合并：** 是
- **作者：** seans3
- **标签：** area/test, priority/important-soon, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  为pods/exec、pods/attach、pods/portforward子资源实现WebSocket升级请求的'create'权限检查，默认启用。

### PR #134588: go 1.25.2/1.24.8 related fixes
- **链接：** https://github.com/kubernetes/kubernetes/pull/134588
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, sig/auth, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-triage
- **变更说明：**
  修复Go 1.25.2/1.24.8升级引入的多个bug，包括IPv6比较、证书SAN生成等。

### PR #134598: bump to go 1.25.3
- **链接：** https://github.com/kubernetes/kubernetes/pull/134598
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** kind/cleanup, lgtm, release-note, size/XS, area/release-eng, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  将Kubernetes构建的Go版本升级到1.25.3。

### PR #134601: Properly account APF seats for legacy watches that compute init-events
- **链接：** https://github.com/kubernetes/kubernetes/pull/134601
- **状态：** closed
- **已合并：** 是
- **作者：** shyamjvs
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复APF座位计算问题，正确核算legacy watch calls（RV=0或未设置）生成init-events的成本，防止API服务器CPU过载，用户可能看到此类调用节流增加。

### PR #134611: [go] Bump images, dependencies and versions to go 1.25.3 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/134611
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, area/provider/gcp, sig/storage, release-note, size/M, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, sig/architecture, area/conformance, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将Kubernetes构建环境升级到Go 1.25.3，并更新相关镜像和依赖，如distroless iptables、debian-base和setcap。

### PR #134614: KEP-4622: promote topology manager `max-allowable-numa-nodes` to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134614
- **状态：** closed
- **已合并：** 是
- **作者：** ffromani
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将Topology Manager的max-allowable-numa-nodes策略选项从beta提升为GA，作为KEP-4622的一部分。

### PR #134625: Drop alphas no longer served in 1.35
- **链接：** https://github.com/kubernetes/kubernetes/pull/134625
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** area/test, kind/cleanup, lgtm, sig/storage, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted, sig/etcd
- **变更说明：**
  在Kubernetes 1.35中移除不再服务的alpha API，具体是storage.k8s.io/v1alpha1 VolumeAttributesClass。

### PR #134631: Promote ContainerRestartRules to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/134631
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将ContainerRestartRules功能提升为beta，默认启用，并修复探针在容器终止后仍运行的bug。

### PR #134635: Locked the (generally available) feature gate `ExecProbeTimeout` to true. 
- **链接：** https://github.com/kubernetes/kubernetes/pull/134635
- **状态：** closed
- **已合并：** 是
- **作者：** vivzbansal
- **标签：** area/test, lgtm, sig/node, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  将ExecProbeTimeout功能门锁定为true，使其一般可用，不再可配置。

### PR #134654: Include relevant dimensions in pod controller indexing
- **链接：** https://github.com/kubernetes/kubernetes/pull/134654
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复pod控制器索引仅使用ownerReference uid的问题，现在包括namespace、kind和name维度，统一键构建并防止控制器混淆。影响版本1.33和1.34。

### PR #134656: additional build simplification, drop rsync requirement
- **链接：** https://github.com/kubernetes/kubernetes/pull/134656
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** kind/cleanup, lgtm, release-note, size/L, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  简化构建过程，移除了对rsync的依赖，属于release engineering的清理工作。

### PR #134685: Drop support for policyv1beta1.PodDisruptionBudget in kubectl
- **链接：** https://github.com/kubernetes/kubernetes/pull/134685
- **状态：** closed
- **已合并：** 是
- **作者：** scaliby
- **标签：** kind/cleanup, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  在kubectl中移除对policy/v1beta1 PodDisruptionBudget的支持。

### PR #134692: etcd: Bump supported etcd version to v3.5.23 for release v1.31, v1.32, and v1.33
- **链接：** https://github.com/kubernetes/kubernetes/pull/134692
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** priority/important-soon, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/XS, approved, area/kubeadm, cncf-cla: yes, triage/accepted, sig/etcd
- **变更说明：**
  将etcd支持版本提升至v3.5.23，适用于Kubernetes v1.31, v1.32, v1.33版本。

### PR #134729: kep-4762: Promote HostnameOverride feature gate to beta stage
- **链接：** https://github.com/kubernetes/kubernetes/pull/134729
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** sig/network, lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将HostnameOverride特性门提升至beta阶段。

### PR #134779: etcd: Bump supported etcd version to v3.5.24 for release v1.32, v1.33, and v1.34
- **链接：** https://github.com/kubernetes/kubernetes/pull/134779
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XS, area/release-eng, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将支持的etcd版本升级到v3.5.24，适用于Kubernetes版本v1.32、v1.33和v1.34，以保持依赖项更新和兼容性。

---
*本报告由 Containerd Release Tracker 自动生成*
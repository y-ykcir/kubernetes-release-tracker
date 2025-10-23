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
- **分析时间：** 2025-10-23 03:37:11
- **分析的 PR 数量：** 34
- **分析的 Issue 数量：** 9
- **重要项目数量：** 43

## 📊 版本概述
Kubernetes v1.35.0-alpha.2 引入了多项 API 升级、关键 Bug 修复和安全增强，包括 cgroupV1 和 IPVS 的废弃警告。

## 🔒 安全问题修复
1. ⚠️ 修复客户端 CA 和请求头 CA 重叠验证问题，加强证书检查 - [PR #131411](https://github.com/kubernetes/kubernetes/pull/131411) - **风险级别：** 中 - 防止权限提升风险
2. ⚠️ 升级到 Go 1.25.3 包含安全修复 - [PR #134598](https://github.com/kubernetes/kubernetes/pull/134598) - **风险级别：** 中 - 修复潜在 CVE 漏洞
3. ⚠️ 为 WebSocket 升级请求实现合成创建授权权限检查 - [PR #134577](https://github.com/kubernetes/kubernetes/pull/134577) - **风险级别：** 中 - 统一 SPDY 和 WebSocket 的权限要求

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 CRD 缺少 openAPIV3Schema 时导致的 panic 问题 - [PR #133721](https://github.com/kubernetes/kubernetes/pull/133721) - **影响：** 防止 API Server 崩溃，确保集群稳定性
2. 修复嵌套映射导致的段错误 - [PR #134381](https://github.com/kubernetes/kubernetes/pull/134381) - **影响：** 避免内存访问错误引起的服务中断
3. 修复 sidecar 容器启动探针工作线程终止问题 - [PR #133072](https://github.com/kubernetes/kubernetes/pull/133072) - **影响：** 解决容器启动卡在 Initializing 状态的问题
4. 修复 IPv6 分配器在 /64 CIDR 范围外分配地址的问题 - [PR #134193](https://github.com/kubernetes/kubernetes/pull/134193) - **影响：** 确保 IPv6 网络配置正确性
5. 修复 DRA 设备污点对 NoExecute 的容忍问题 - [PR #134479](https://github.com/kubernetes/kubernetes/pull/134479) - **影响：** 防止 Pod 被立即驱逐，确保资源分配稳定性
6. 修复 DRA 可消耗容量调度多个设备的问题 - [PR #133706](https://github.com/kubernetes/kubernetes/pull/133706) - **影响：** 提升设备资源调度效率

## 💥 破坏性变更
1. 🚨 废弃 cgroupV1 支持，使用 cgroupV1 的系统将无法启动 - [PR #134298](https://github.com/kubernetes/kubernetes/pull/134298) - **影响：** 需要迁移到 cgroupV2
2. 🚨 废弃 IPVS 模式，kube-proxy 将显示警告 - [PR #134539](https://github.com/kubernetes/kubernetes/pull/134539) - **影响：** 需要迁移到 nftables 模式
3. 🚨 锁定 ExecProbeTimeout 功能门为 true，无法禁用 - [PR #134635](https://github.com/kubernetes/kubernetes/pull/134635) - **影响：** 确保执行探针超时行为一致
4. 🚨 停止支持 policyv1beta1 PodDisruptionBudget - [PR #134685](https://github.com/kubernetes/kubernetes/pull/134685) - **影响：** 需要更新 PDB 资源到 policy/v1 API 版本 - [PR #134685](https://github.com/kubernetes/kubernetes/pull/134685) - **影响：** 需要迁移到稳定 API

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 废弃 cgroupV1 支持，设置 failCgroupV1 为 true - [PR #134298](https://github.com/kubernetes/kubernetes/pull/134298)
2. 标记 IPVS 模式为废弃，建议迁移到 nftables - [PR #134539](https://github.com/kubernetes/kubernetes/pull/134539)
3. 提升 HPA 可配置容忍度功能门到 Beta - [PR #133128](https://github.com/kubernetes/kubernetes/pull/133128)
4. 提升 StatefulSet 最大不可用功能门到 Beta - [PR #133153](https://github.com/kubernetes/kubernetes/pull/133153)
5. 删除 gogo protobuf 运行时依赖 - [PR #134256](https://github.com/kubernetes/kubernetes/pull/134256)
6. 锁定 ExecProbeTimeout 功能门为 true - [PR #134635](https://github.com/kubernetes/kubernetes/pull/134635)
7. 为 exec、attach 和 portforward 实现合成创建授权权限检查 - [PR #134577](https://github.com/kubernetes/kubernetes/pull/134577)

## 🚀 性能优化
1. 修复 APF 座位计数低估问题，正确计算无资源版本的 watch 调用 - [PR #134601](https://github.com/kubernetes/kubernetes/pull/134601) - **提升：** 保护 API Server 免受 CPU 过载，可能增加对 legacy watch 的限流 - [Issue #134580](https://github.com/kubernetes/kubernetes/issues/134580)
2. 修复 kubelet 忽略 idsPerPod 配置的问题 - [PR #133373](https://github.com/kubernetes/kubernetes/pull/133373) - **提升：** 确保用户命名空间配置正确生效
3. 升级到 Go 1.25.3 带来运行时性能优化 - [PR #134611](https://github.com/kubernetes/kubernetes/pull/134611) - **提升：** 整体性能和安全改进

## 🎯 风险评估
整体风险评估：中等风险。此版本包含多项 API 变更、废弃功能和关键 Bug 修复，可能影响生产环境稳定性。建议等待稳定版本发布后，在维护窗口期内进行升级。需要特别关注：cgroupV1 废弃影响、IPVS 迁移、RBAC 权限更新和 DRA 功能稳定性。

## 📋 升级建议
1. 在升级前验证集群是否使用 cgroupV1，如有使用需提前迁移到 cgroupV2
2. 检查 kube-proxy 配置，如果使用 IPVS 模式，开始规划迁移到 nftables
3. 更新 RBAC 策略，确保为 pods/exec、pods/attach 和 pods/portforward 授予 create 权限
4. 在测试环境中充分验证 CRD 和自定义资源，确保无 panic 风险
5. 监控升级后 APF 限流情况，特别是对 legacy watch 调用的影响
6. 备份 etcd 数据，并确保 etcd 版本升级到 v3.5.24 以获取安全修复
7. 关注 DRA 相关功能，确保设备分配和污点容忍正常工作

## 📋 Release 包含的变更

### PR #131411: Fix overlapping client CA and requestheader CA validation with proper certificate checking
- **链接：** https://github.com/kubernetes/kubernetes/pull/131411
- **状态：** closed
- **已合并：** 是
- **作者：** ballista01
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, sig/security, triage/accepted
- **变更说明：**
  修复客户端 CA 和 requestheader CA 重叠验证问题，通过正确的证书检查增强安全性，防止配置冲突。

### PR #132927: DRA API: implement ResourceClaim strategy for DRADeviceTaints
- **链接：** https://github.com/kubernetes/kubernetes/pull/132927
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, lgtm, release-note, size/XXL, approved, cncf-cla: yes, needs-priority, api-review, needs-triage, wg/device-management
- **变更说明：**
  修复DRA API：在ResourceClaim策略中正确移除无效的tolerations字段，基于KEP-5055。

### PR #133072: Fix startup probe worker termination for sidecar containers
- **链接：** https://github.com/kubernetes/kubernetes/pull/133072
- **状态：** closed
- **已合并：** 是
- **作者：** AadiDev005
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, ok-to-test, triage/accepted
- **变更说明：**
  修复 sidecar 容器启动探针 worker 终止问题，当 Pod restartPolicy=Never 时，确保 sidecar 容器（restartPolicy=Always）的探针 worker 继续运行，防止主容器卡在 Initializing 状态。

### PR #133128: Promote HPAConfigurableTolerance gate to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/133128
- **状态：** closed
- **已合并：** 是
- **作者：** jm-franc
- **标签：** lgtm, sig/api-machinery, release-note, sig/autoscaling, size/S, kind/api-change, kind/feature, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted
- **变更说明：**
  将HPAConfigurableTolerance特性门提升至beta并默认启用，允许配置HPA容忍度，基于KEP-4951。

### PR #133153: Update MaxUnavailableStatefulSet feature gate to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/133153
- **状态：** closed
- **已合并：** 是
- **作者：** helayoty
- **标签：** lgtm, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted
- **变更说明：**
  将MaxUnavailableStatefulSet特性门提升至beta并默认启用，优化StatefulSet滚动更新，基于KEP-961。

### PR #133373: [Carry 133278] kubelet: Don't ignore idsPerPod config #133278
- **链接：** https://github.com/kubernetes/kubernetes/pull/133373
- **状态：** closed
- **已合并：** 是
- **作者：** AkihiroSuda
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  修复kubelet中userns manager忽略idsPerPod配置的bug，问题源于初始化顺序错误，现通过参数传递确保配置正确应用。

### PR #133706: Fix DRAConsumableCapacity to schedule more than one devices
- **链接：** https://github.com/kubernetes/kubernetes/pull/133706
- **状态：** closed
- **已合并：** 是
- **作者：** sunya-ch
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DRA ConsumableCapacity 调度问题，使其能够正确调度多个设备，解决动态资源分配中的设备数量限制问题。

### PR #133721: fix panic for the crd with subresource but lose openAPIV3Schema
- **链接：** https://github.com/kubernetes/kubernetes/pull/133721
- **状态：** closed
- **已合并：** 是
- **作者：** fusida
- **标签：** kind/bug, area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, area/provider/gcp, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, sig/autoscaling, size/L, kind/api-change, area/release-eng, sig/auth, sig/apps, approved, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, sig/release, sig/architecture, area/conformance, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, area/e2e-test-framework, area/dependency, triage/accepted, area/stable-metrics, sig/etcd, wg/device-management
- **变更说明：**
  修复 CRD 带有子资源但缺少 openAPIV3Schema 时导致的 panic 问题，提升 API 服务器稳定性。

### PR #133778: Remove the --pod-infra-container-image flag from kubeadm and cluster/gce
- **链接：** https://github.com/kubernetes/kubernetes/pull/133778
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/cleanup, lgtm, area/provider/gcp, sig/cluster-lifecycle, release-note, size/L, approved, area/kubeadm, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  清理无用标志：移除kubeadm和cluster/gce中的--pod-infra-container-image参数。

### PR #134193: Fix IPv6 allocator for /64 CIDRs
- **链接：** https://github.com/kubernetes/kubernetes/pull/134193
- **状态：** closed
- **已合并：** 是
- **作者：** hoskeri
- **标签：** kind/bug, sig/network, lgtm, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复IPv6分配器bug：在/64 CIDR中防止地址分配超出子网范围。

### PR #134256: KEP-5589 - drop gogo runtime dependencies
- **链接：** https://github.com/kubernetes/kubernetes/pull/134256
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** sig/network, area/kubelet, kind/cleanup, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/architecture, area/code-generation, needs-priority, area/dependency, needs-triage, wg/device-management
- **变更说明：**
  移除对 gogo protobuf 的运行时依赖，清理生成的 protobuf 代码，提升与标准 protobuf 库的兼容性，完成 KEP-5589 第一阶段。

### PR #134298: [KEP-5573] Set failCgroupV1 to true
- **链接：** https://github.com/kubernetes/kubernetes/pull/134298
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/kubelet, lgtm, sig/node, size/M, kind/api-change, release-note-action-required, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, kind/deprecation, needs-triage
- **变更说明：**
  设置failCgroupV1为true，弃用cgroup v1，要求用户迁移至cgroup v2，基于KEP-5573。

### PR #134381: fix nested map segmentation fault
- **链接：** https://github.com/kubernetes/kubernetes/pull/134381
- **状态：** closed
- **已合并：** 是
- **作者：** kon-angelo
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/S, approved, sig/cli, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  修复嵌套 map 操作导致的段错误问题，提升 kubectl 和 API 服务器在处理复杂数据结构时的稳定性。

### PR #134388: KEP-4540: StrictCPUReservationOption moved to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134388
- **状态：** closed
- **已合并：** 是
- **作者：** psasnal
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  将CPU Manager静态策略选项`strict-cpu-reservation`升级到GA版本，标志着该功能正式稳定可用，无需额外配置即可启用。

### PR #134433: kubeadm: print errors during control-plane-wait retries
- **链接：** https://github.com/kubernetes/kubernetes/pull/134433
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/XS, kind/feature, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubeadm改进：在控制平面等待重试时打印错误信息，便于调试启动问题。

### PR #134479: DRA device taints: fix toleration of NoExecute
- **链接：** https://github.com/kubernetes/kubernetes/pull/134479
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, sig/node, release-note, size/L, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DRA 设备污点中 NoExecute 容忍问题，调度器现在正确传递容忍信息给驱逐控制器，避免已调度的 Pod 被立即驱逐。

### PR #134481: Update --chunk-size flag, dropping the beta information
- **链接：** https://github.com/kubernetes/kubernetes/pull/134481
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/documentation, kind/cleanup, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  将 kubectl describe、get、drain 和 events 命令的 --chunk-size 标志从 beta 状态提升为稳定状态，更新相关文档。

### PR #134510: build by running kube-cross directly
- **链接：** https://github.com/kubernetes/kubernetes/pull/134510
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** kind/cleanup, lgtm, release-note, size/L, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  构建系统改进，直接运行 kube-cross 进行构建，简化构建流程并提升效率。

### PR #134539: KEP: 5495 - Add deprecation warning for ipvs
- **链接：** https://github.com/kubernetes/kubernetes/pull/134539
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** sig/network, area/kube-proxy, lgtm, release-note, size/XS, approved, cncf-cla: yes, needs-priority, kind/deprecation, triage/accepted
- **变更说明：**
  添加kube-proxy ipvs模式弃用警告，提示用户迁移至nftables，依据KEP-5495。

### PR #134577: Implements synthetic create authz permission check for exec, attach, and portforward
- **链接：** https://github.com/kubernetes/kubernetes/pull/134577
- **状态：** closed
- **已合并：** 是
- **作者：** seans3
- **标签：** area/test, priority/important-soon, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  实现exec、attach和portforward子资源WebSocket升级请求的create权限检查，添加AuthorizePodWebsocketUpgradeCreatePermission特性门（beta，默认启用）。

### PR #134588: go 1.25.2/1.24.8 related fixes
- **链接：** https://github.com/kubernetes/kubernetes/pull/134588
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, sig/auth, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-triage
- **变更说明：**
  修复Go 1.25.2/1.24.8相关问题，包括IPv6比较和证书SAN生成，并添加集成测试。

### PR #134598: bump to go 1.25.3
- **链接：** https://github.com/kubernetes/kubernetes/pull/134598
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** kind/cleanup, lgtm, release-note, size/XS, area/release-eng, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  升级Go版本至1.25.3，提升构建安全性和兼容性。

### PR #134601: Properly account APF seats for legacy watches that compute init-events
- **链接：** https://github.com/kubernetes/kubernetes/pull/134601
- **状态：** closed
- **已合并：** 是
- **作者：** shyamjvs
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复 APF 中 legacy watch 调用（RV=0 或未设置）的 seat 计数问题，正确计算 init-events 成本，防止 API 服务器 CPU 过载，可能导致此类调用被更多节流。

### PR #134611: [go] Bump images, dependencies and versions to go 1.25.3 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/134611
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, lgtm, area/provider/gcp, sig/storage, release-note, size/M, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, sig/architecture, area/conformance, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  升级 Kubernetes 构建环境到 Go 1.25.3，同时更新 debian-base、setcap 和 distroless iptables 镜像。

### PR #134614: KEP-4622: promote topology manager `max-allowable-numa-nodes` to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/134614
- **状态：** closed
- **已合并：** 是
- **作者：** ffromani
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将 Topology Manager 策略选项 max-allowable-numa-nodes 提升为 GA，正式稳定该功能。

### PR #134625: Drop alphas no longer served in 1.35
- **链接：** https://github.com/kubernetes/kubernetes/pull/134625
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** area/test, kind/cleanup, lgtm, sig/storage, sig/api-machinery, release-note, size/M, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted, sig/etcd
- **变更说明：**
  在 Kubernetes 1.35 中停止提供 storage.k8s.io/v1alpha1 VolumeAttributesClass API，清理废弃的 alpha API。

### PR #134631: Promote ContainerRestartRules to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/134631
- **状态：** closed
- **已合并：** 是
- **作者：** yuanwang04
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将 ContainerRestartRules 功能提升为 beta，默认启用，并修复探针在容器终止后继续运行的 bug。

### PR #134635: Locked the (generally available) feature gate `ExecProbeTimeout` to true. 
- **链接：** https://github.com/kubernetes/kubernetes/pull/134635
- **状态：** closed
- **已合并：** 是
- **作者：** vivzbansal
- **标签：** area/test, lgtm, sig/node, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  将已普遍可用的功能门 ExecProbeTimeout 锁定为 true，不再可配置，确保一致性。

### PR #134654: Include relevant dimensions in pod controller indexing
- **链接：** https://github.com/kubernetes/kubernetes/pull/134654
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, sig/apps, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复pod控制器索引中仅包含uid的问题，现索引包括namespace、kind和name，避免在ownerReference uid不正确时控制器混淆。

### PR #134656: additional build simplification, drop rsync requirement
- **链接：** https://github.com/kubernetes/kubernetes/pull/134656
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** kind/cleanup, lgtm, release-note, size/L, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  构建简化：移除了对rsync的依赖，优化Kubernetes构建流程，减少外部工具要求。

### PR #134685: Drop support for policyv1beta1.PodDisruptionBudget in kubectl
- **链接：** https://github.com/kubernetes/kubernetes/pull/134685
- **状态：** closed
- **已合并：** 是
- **作者：** scaliby
- **标签：** kind/cleanup, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  移除kubectl对policyv1beta1 PodDisruptionBudget的支持，清理废弃API版本。

### PR #134692: etcd: Bump supported etcd version to v3.5.23 for release v1.31, v1.32, and v1.33
- **链接：** https://github.com/kubernetes/kubernetes/pull/134692
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** priority/important-soon, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/XS, approved, area/kubeadm, cncf-cla: yes, triage/accepted, sig/etcd
- **变更说明：**
  升级支持的etcd版本至v3.5.23，适用于Kubernetes v1.31、v1.32和v1.33版本。

### PR #134729: kep-4762: Promote HostnameOverride feature gate to beta stage
- **链接：** https://github.com/kubernetes/kubernetes/pull/134729
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** sig/network, lgtm, sig/node, release-note, size/XS, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将HostnameOverride特性门提升至beta阶段，允许覆盖节点主机名配置，基于KEP-4762。

### PR #134779: etcd: Bump supported etcd version to v3.5.24 for release v1.32, v1.33, and v1.34
- **链接：** https://github.com/kubernetes/kubernetes/pull/134779
- **状态：** closed
- **已合并：** 是
- **作者：** joshjms
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XS, area/release-eng, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将支持的etcd版本升级到v3.5.24，适用于Kubernetes v1.32、v1.33和v1.34版本，确保组件兼容性和安全性。

---
*本报告由 Containerd Release Tracker 自动生成*
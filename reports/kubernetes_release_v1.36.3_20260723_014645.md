# Kubernetes 版本发布分析报告
## v1.36.3 (v1.36.3)

### 📋 版本信息
- **版本标签：** v1.36.3
- **版本名称：** v1.36.3
- **发布时间：** 2026-07-23T00:35:52Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.36.3

### 🔍 分析统计
- **分析时间：** 2026-07-23 01:46:45
- **分析的 PR 数量：** 10
- **分析的 Issue 数量：** 0
- **重要项目数量：** 10

## 📊 版本概述
Kubernetes v1.36.3 是一个补丁版本，主要修复了 v1.36 系列中引入的几个关键回归问题，包括 kubelet 内存泄漏、服务器端应用（SSA）兼容性、DRA 资源分配器状态泄漏以及调度器 panic，强烈建议所有 v1.36 用户升级。

## 🔒 安全问题修复
1. ⚠️ 基础镜像和构建工具链更新至 Go 1.26.5 - [PR #140581](https://github.com/kubernetes/kubernetes/pull/140581) - **风险级别：** 低 - 此更新通常包含 Go 语言的安全修复，建议升级以获得最新的安全补丁。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kubeadm join 时获取 kubeadm-config ConfigMap 使用过短超时（350ms）的问题，现使用标准的 KubernetesAPICallTimeout（默认1分钟） - [PR #139808](https://github.com/kubernetes/kubernetes/pull/139808) - **影响：** 在 API 服务器响应较慢或网络延迟较高时，`kubeadm join` 可能因超时而失败。
2. 修复 kubeadm 在 etcd learner 成员提升逻辑中的问题，避免因客户端瞬时错误导致不必要的加入失败 - [PR #139910](https://github.com/kubernetes/kubernetes/pull/139910) - **影响：** 提升 etcd learner 节点时可能遇到非必要的失败，影响集群高可用扩展。
3. 优化 kubeadm 的 etcd MemberPromote 逻辑，当成员已是投票成员时跳过提升调用，避免不必要的重试和超时 - [PR #138493](https://github.com/kubernetes/kubernetes/pull/138493) - **影响：** 提升已投票成员时产生冗余 API 调用和延迟。
4. kubelet 停止为缺失的可选容器注解记录 V(4) 级别的“Label not found”日志 - [PR #140322](https://github.com/kubernetes/kubernetes/pull/140322) - **影响：** 减少不必要的日志噪音，提升日志可读性。

## 💥 破坏性变更
1. 🚨 此版本为补丁版本，未引入破坏性变更或 API 变更。所有修复旨在解决 v1.36 中的回归问题并恢复预期行为。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复 kubelet Pod 同步导致的内存泄漏回归 - [PR #140066](https://github.com/kubernetes/kubernetes/pull/140066)
2. 修复服务器端应用（SSA）对可空容器类型进行 patch 时的回归 - [PR #140296](https://github.com/kubernetes/kubernetes/pull/140296)
3. 修复 DRA 资源分配器在分配失败时未回滚预留状态，导致 Pod 无法调度的问题 - [PR #140663](https://github.com/kubernetes/kubernetes/pull/140663)
4. 修复启用 DRADeviceTaintRules 功能时，kube-scheduler 可能 panic 或忽略规则更新的问题 - [PR #139681](https://github.com/kubernetes/kubernetes/pull/139681)
5. 恢复 CRI API 中 KeyValue 字段的 JSON 编码方式，确保与旧版本 CRI 运行时的兼容性 - [PR #139965](https://github.com/kubernetes/kubernetes/pull/139965)

## 🚀 性能优化
1. kubeadm join 使用更合理的超时获取配置，减少因网络抖动导致的失败 - [PR #139808](https://github.com/kubernetes/kubernetes/pull/139808) - **提升：** 提高 `kubeadm join` 在非理想网络条件下的成功率。
2. kubeadm 优化 etcd 成员提升逻辑，避免冗余调用 - [PR #138493](https://github.com/kubernetes/kubernetes/pull/138493) - **提升：** 减少 etcd 集群管理操作的不必要延迟。

## 🎯 风险评估
整体风险评估：**低风险**。此版本专门针对 v1.36 中引入的回归问题进行修复，属于高优先级补丁。升级风险主要来自修复本身可能引入新问题的极低概率，但鉴于修复问题的严重性（内存泄漏、调度器 panic），升级收益远大于风险。建议在下一个维护窗口内进行升级。需要特别关注升级后 SSA 操作和 DRA 资源调度的行为是否符合预期。

## 📋 升级建议
1. **立即升级**：如果您正在运行 Kubernetes v1.36.x，尤其是受到上述内存泄漏、SSA 或 DRA 问题影响的集群，建议尽快安排升级到 v1.36.3。
2. **测试验证**：升级前，请在测试环境中验证服务器端应用（SSA）操作、使用 DRA 资源的 Pod 调度以及 kubelet 内存使用情况是否正常。
3. **关注 kubeadm**：如果您使用 kubeadm 管理集群，本次升级修复了多个 etcd 管理和节点加入的稳定性问题，升级后相关操作应更加可靠。
4. **无需等待**：由于此版本主要修复严重回归，风险较低，收益明确，无需等待后续版本。

## 📋 Release 包含的变更

### PR #138493: Automated cherry pick of #138390: kubeadm: skip promote call when etcd member is already a voting member
- **链接：** https://github.com/kubernetes/kubernetes/pull/138493
- **状态：** closed
- **已合并：** 是
- **作者：** wgkingk
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/S, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  优化 kubeadm 的 etcd 成员晋升逻辑。当成员已是投票成员时，跳过 promote API 调用，避免不必要的重试和超时。

### PR #139681: Automated cherry pick of #139651: Align DeviceTaintRule informer API version with handlers
- **链接：** https://github.com/kubernetes/kubernetes/pull/139681
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** kind/bug, area/test, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, priority/important-longterm, kind/failing-test, triage/accepted, wg/device-management
- **变更说明：**
  修复启用 DRADeviceTaintRules 特性时，因 DeviceTaintRule informer API 版本与处理器不匹配导致的 kube-scheduler panic 或忽略新规则的问题。

### PR #139808: Automated cherry pick of #139667: fix(kubeadm): use KubernetesAPICallTimeout for mandatory kubeadm-config fetch during join
- **链接：** https://github.com/kubernetes/kubernetes/pull/139808
- **状态：** closed
- **已合并：** 是
- **作者：** damdo
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm join 时获取 kubeadm-config ConfigMap 的超时问题。将短重试（350ms）改为使用 KubernetesAPICallTimeout（默认1分钟），并新增 shortConfigMapGet 参数供 kubeadm reset 等调用方继续使用短超时。

### PR #139910: Automated cherry pick of #139842: kubeadm: treat already promoted learner as successful
- **链接：** https://github.com/kubernetes/kubernetes/pull/139910
- **状态：** closed
- **已合并：** 是
- **作者：** jihyun-huh
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  提升 kubeadm etcd learner 成员晋升的健壮性。当晋升在 etcd 端成功但客户端返回瞬时错误时，kubeadm 现在能正确处理，避免不必要的 etcd-join 失败。

### PR #139965: [1.36] Automated cherry pick of #139964: Restore string JSON encoding of cri-api KeyValue
- **链接：** https://github.com/kubernetes/kubernetes/pull/139965
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复 cri-api 中 KeyValue 结构的 JSON 编码回归问题。将 value 字段的编码方式恢复为 1.34 版本之前的字符串编码。

### PR #140066: Automated cherry pick of #139850: kubelet startPodSync: reuse the previous context to fix memory leak regression
- **链接：** https://github.com/kubernetes/kubernetes/pull/140066
- **状态：** closed
- **已合并：** 是
- **作者：** compumike
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复 kubelet 在 1.36 版本中的内存泄漏回归问题。通过重用之前的 context，避免每次 Pod sync 操作泄露 context。

### PR #140296: Manual cherry-pick of # 140294: Revert SMD #306 to fix regression in SSA for nullable container types
- **链接：** https://github.com/kubernetes/kubernetes/pull/140296
- **状态：** closed
- **已合并：** 是
- **作者：** jpbetz
- **标签：** kind/bug, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, sig/auth, approved, sig/cli, cncf-cla: yes, sig/architecture, area/code-generation, sig/cloud-provider, needs-priority, area/dependency, kind/regression, needs-triage, wg/device-management
- **变更说明：**
  回退 structured-merge-diff (SMD) 的 #306 更改，以修复 Server-Side Apply (SSA) 在处理可空容器类型时出现的回归问题。

### PR #140322: Automated cherry pick of #140163: kubelet: stop logging missing optional container annotations
- **链接：** https://github.com/kubernetes/kubernetes/pull/140322
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  优化 kubelet 日志，停止为缺失的可选容器注解（如 io.kubernetes.cri-o.xxx）输出 V(4) 级别的“Label not found”日志，减少日志噪音。

### PR #140581: [release-1.36] Bump images and versions to golang 1.26.5 and update distroless-iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/140581
- **状态：** closed
- **已合并：** 是
- **作者：** palnabarun
- **标签：** area/test, lgtm, release-note, size/S, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将 Kubernetes 构建的 Go 语言版本升级至 1.26.5，并更新 distroless-iptables 基础镜像。

### PR #140663: Automated cherry pick of #140431: DRA: roll back reserved state in allocateDevice
- **链接：** https://github.com/kubernetes/kubernetes/pull/140663
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, lgtm, sig/node, release-note, size/XL, cherry-pick-approved, approved, cncf-cla: yes, needs-ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DRA（动态资源分配）在 allocateDevice 过程中预留状态回滚不全的问题。该问题会导致设备计数器泄漏，使调度器误判资源耗尽，影响 Pod 调度。

---
*本报告由 Containerd Release Tracker 自动生成*
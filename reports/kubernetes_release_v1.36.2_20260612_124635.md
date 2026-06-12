# Kubernetes 版本发布分析报告
## v1.36.2 (v1.36.2)

### 📋 版本信息
- **版本标签：** v1.36.2
- **版本名称：** v1.36.2
- **发布时间：** 2026-06-12T11:34:56Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.36.2

### 🔍 分析统计
- **分析时间：** 2026-06-12 12:46:35
- **分析的 PR 数量：** 11
- **分析的 Issue 数量：** 1
- **重要项目数量：** 12

## 📊 版本概述
Kubernetes v1.36.2 是一个关键的补丁版本，主要修复了多个可能导致集群组件panic、调度失败和数据丢失的重要bug，特别是针对DRA（动态资源分配）功能和1.34版本引入的回归问题。

## 🔒 安全问题修复
1. ⚠️ 升级构建工具Go版本至1.26.4，包含该版本的安全补丁 - [PR #138871](https://github.com/kubernetes/kubernetes/pull/138871), [PR #139585](https://github.com/kubernetes/kubernetes/pull/139585) - **风险级别：** 中 - 建议升级以应对Go底层依赖中潜在的CVE漏洞。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复kube-scheduler在处理使用`allocationMode: All`的DRA ResourceClaim时的panic - [PR #138988](https://github.com/kubernetes/kubernetes/pull/138988) - **影响：** 使用DRA的集群可能遭遇调度器崩溃，导致调度功能中断。
2. 修复DRA调度器bug，该bug可能导致互斥的设备分区被分配给多个Pod，引发设备冲突或数据丢失 - [PR #139211](https://github.com/kubernetes/kubernetes/pull/139211) - **影响：** 使用共享计数器（`SharedCounters`）和DRA可分配设备的场景下，可能导致严重的工作负载故障或数据一致性风险。
3. 修复端点控制器在处理`IPFamilies`字段为空（双栈前时代的遗留Service）的Service时发生的panic - [PR #139233](https://github.com/kubernetes/kubernetes/pull/139233) - **影响：** 此类Service的操作可能触发控制器崩溃，影响Service和Endpoint的管理。
4. 修复1.36引入的回归：被暂停但控制器尚未设置`JobSuspended`条件的Job，其调度指令修改会被错误拒绝 - [PR #139329](https://github.com/kubernetes/kubernetes/pull/139329) - **影响：** 影响批量Job的管理，无法在Job启动前调整其调度策略。
5. 修复CSI卷问题：当周期性`NodePublishVolume`调用失败时，kubelet误删挂载目录，导致后续成功重发布无法恢复数据 - [PR #139228](https://github.com/kubernetes/kubernetes/pull/139228) - **影响：** 使用`requiresRepublish=true`的CSI驱动可能面临数据损坏或丢失的风险。
6. 修复DRA计分bug：同时包含多节点声明和单节点声明的Pod可能陷入Pending状态 - [PR #139363](https://github.com/kubernetes/kubernetes/pull/139363) - **影响：** 使用混合DRA声明的Pod无法被成功调度。

## 💥 破坏性变更
1. 🚨 CRI API中环境变量值的字段类型从`string`更改为`bytes`，以恢复对非UTF-8二进制数据的支持 - [PR #139192](https://github.com/kubernetes/kubernetes/pull/139192) - **影响：** 这是为修复回归所做的API层修复性变更，不直接影响Kubernetes API，但可能影响直接与CRI交互的工具或自定义集成。此变更向下兼容同版本内已编码的数据。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复DRA（动态资源分配）相关的多个严重调度与分配bug，避免panic和错误的资源分配 - [PR #138988](https://github.com/kubernetes/kubernetes/pull/138988), [PR #139211](https://github.com/kubernetes/kubernetes/pull/139211), [PR #139363](https://github.com/kubernetes/kubernetes/pull/139363)
2. 修复1.34版本引入的Secret包含非UTF-8二进制数据时，Pod创建失败的严重回归 - [PR #139192](https://github.com/kubernetes/kubernetes/pull/139192) - 关联 [Issue #139132](https://github.com/kubernetes/kubernetes/issues/139132)
3. 修复端点控制器在处理旧式（pre-dual-stack）Service时的panic问题 - [PR #139233](https://github.com/kubernetes/kubernetes/pull/139233)
4. 修复对尚未启动的暂停Job修改调度指令（nodeSelector等）被拒绝的回归问题 - [PR #139329](https://github.com/kubernetes/kubernetes/pull/139329)
5. 提升SELinux指标发射的性能，减少节点上的开销 - [PR #139136](https://github.com/kubernetes/kubernetes/pull/139136)
6. 修复CSI卷在定期重发布失败时可能导致数据损坏的问题 - [PR #139228](https://github.com/kubernetes/kubernetes/pull/139228)
7. 修复kubeadm `init phase certs --dry-run`命令中CA文件拷贝路径的错误 - [PR #139445](https://github.com/kubernetes/kubernetes/pull/139445)

## 🚀 性能优化
1. 优化SELinux指标（`volume_manager_selinux_context_errors_total`）收集的比较逻辑，避免高成本操作 - [PR #139136](https://github.com/kubernetes/kubernetes/pull/139136) - **提升：** 显著减少节点上因频繁指标检查导致的CPU开销，尤其在高负载或大量Pod的节点上表现更明显。

## 🎯 风险评估
整体风险评估：中等偏低。此版本主要聚焦于修复严重的bug和回归问题，特别是针对DRA和几个关键的控制器panic。对于不使用DRA且未受影响的回归问题影响的集群，升级风险较小。升级能显著提高集群的稳定性和可靠性。建议在生产环境规划维护窗口进行升级，并重点关注上述修复点涉及的组件功能验证。

## 📋 升级建议
1. **强烈建议升级：** 如果您使用DRA功能，或者使用了包含非UTF-8二进制数据的Secret作为环境变量，应立即升级到v1.36.2以避免调度器panic、Pod创建失败或数据丢失风险。
2. **测试重点：** 升级前请在测试环境中重点验证：1) DRA设备的分配逻辑；2) 从Secret设置二进制环境变量的Pod；3) 对暂停Job的调度指令更新操作。
3. **kubeadm用户注意：** 如果使用`kubeadm init phase certs --dry-run`，升级可修复其路径错误。
4. **监控变更：** 升级后，密切关注调度器（kube-scheduler）和端点控制器（endpoint-controller）的日志，确保之前潜在的panic问题已解决。

## 📋 Release 包含的变更

### PR #138871: release-1.36: upgrade go to 1.26.4
- **链接：** https://github.com/kubernetes/kubernetes/pull/138871
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** lgtm, release-note, size/XS, kind/feature, cherry-pick-approved, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  将 Kubernetes 1.36 分支的 Go 版本升级至 1.26.4。

### PR #138988: Automated cherry pick of #138885: DRA: fix AllocationModeAll with consumed counters
- **链接：** https://github.com/kubernetes/kubernetes/pull/138988
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复当 DRA ResourceClaim 使用 `allocationMode: All` 并选择了消耗共享计数器的设备时，kube-scheduler 可能发生的 panic。

### PR #139136: Automated cherry pick of #138981: Improve performance characteristic of selinux metric emission
- **链接：** https://github.com/kubernetes/kubernetes/pull/139136
- **状态：** closed
- **已合并：** 是
- **作者：** gnufied
- **标签：** kind/bug, lgtm, sig/storage, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  优化 selinux 指标发射的性能特征，避免昂贵的比较操作，提升系统效率。

### PR #139192: [1.36] Restore ability to plumb binary data through envvar values
- **链接：** https://github.com/kubernetes/kubernetes/pull/139192
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 1.34 版本引入的回归问题，恢复将包含二进制非 UTF-8 数据的 Secret API 对象用作容器环境变量值的能力。

### PR #139211: Automated cherry pick of #139040: DRA: account for shared devices when rebuilding counters
- **链接：** https://github.com/kubernetes/kubernetes/pull/139211
- **状态：** closed
- **已合并：** 是
- **作者：** ashvindeodhar
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DRA 调度器在重建计数器时未考虑共享设备的问题，该 bug 可能导致相互排斥的设备分区被分配给多个 Pod，引发设备冲突或数据丢失。

### PR #139228: Automated cherry pick of #139045: fix(csi): preserve mount dir when NodePublish fails on a remount
- **链接：** https://github.com/kubernetes/kubernetes/pull/139228
- **状态：** closed
- **已合并：** 是
- **作者：** aramase
- **标签：** kind/bug, priority/important-soon, lgtm, sig/storage, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复当 CSI Driver 设置 `requiresRepublish=true` 时，kubelet 在周期性 NodePublishVolume 调用失败后会错误删除挂载目录的问题，确保后续成功的重新发布可以修复卷内容。

### PR #139233: Automated cherry pick of #138736: fix: avoid panic on services with empty IPFamilies
- **链接：** https://github.com/kubernetes/kubernetes/pull/139233
- **状态：** closed
- **已合并：** 是
- **作者：** rahulbabu95
- **标签：** kind/bug, sig/network, lgtm, release-note, size/M, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复 endpoint controller 在处理 IPFamilies 字段为空的 Service（即从未进行 spec 更新的 pre-dual-stack 服务）时可能发生的 panic。

### PR #139329: Automated cherry pick of #139287: batch/job: Fix scheduling directives mutation for not-yet-started suspended Jobs
- **链接：** https://github.com/kubernetes/kubernetes/pull/139329
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, sig/testing, kind/regression, triage/accepted
- **变更说明：**
  修复 1.36 版本中的回归问题：当 suspended Job 的 JobSuspended 条件尚未被 job controller 设置时，对其调度指令（nodeSelector、tolerations、node affinity）的修改会被拒绝。

### PR #139363: Automated cherry pick of #139017: Fix dra scoring bug with mixed allocated and unallocated claims
- **链接：** https://github.com/kubernetes/kubernetes/pull/139363
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DRA 评分 bug，解决同时使用多节点声明（multi-node claims）和每节点声明（per-node claims）的 Pod 可能卡在 Pending 状态的问题。

### PR #139445: Automated cherry pick of #139339: kubeadm: fix dry-run CA copy paths in init certs
- **链接：** https://github.com/kubernetes/kubernetes/pull/139445
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm init phase certs --dry-run 命令中复制现有 CA 文件路径的错误，这是一个回归问题。

### PR #139585: [release-1.36] [go]Bump images and versions to go 1.26.4 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/139585
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/critical-urgent, lgtm, release-note, size/S, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将 Kubernetes 构建基础升级至 Go 1.26.4 并更新 distroless iptables 镜像，属于常规依赖更新。

---
*本报告由 Containerd Release Tracker 自动生成*
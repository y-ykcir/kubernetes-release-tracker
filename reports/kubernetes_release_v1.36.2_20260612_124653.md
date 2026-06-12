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
- **分析时间：** 2026-06-12 12:46:53
- **分析的 PR 数量：** 11
- **分析的 Issue 数量：** 1
- **重要项目数量：** 12

## 📊 版本概述
Kubernetes v1.36.2 是一个重要的补丁版本，主要修复了多个可能导致组件崩溃（panic）、数据损坏的严重回归性Bug，并升级了Go版本以包含安全修复，建议受影响的集群尽快升级。

## 🔒 安全问题修复
1. ⚠️ 将构建Kubernetes的Go语言版本升级至1.26.4 - [PR #138871](https://github.com/kubernetes/kubernetes/pull/138871) / [PR #139585](https://github.com/kubernetes/kubernetes/pull/139585) - **风险级别：** 中 - **影响：** 通常Go小版本升级包含安全修复，建议升级以获取最新的运行时安全补丁。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复了DRA（动态资源分配）中，使用`allocationMode: All`并选择消耗共享计数器的设备时，kube-scheduler可能发生的panic - [PR #138988](https://github.com/kubernetes/kubernetes/pull/138988) - **影响：** 可能导致调度器崩溃，影响集群调度能力。
2. 修复了DRA调度器bug，该bug可能导致互斥的设备分区被分配给多个Pod，引发设备冲突、崩溃或数据丢失 - [PR #139211](https://github.com/kubernetes/kubernetes/pull/139211) - **影响：** 使用`SharedCounters`和`DRAConsumableCapacity`的DRA驱动可能面临严重的数据一致性和稳定性风险。
3. 修复了CSI卷在`requiresRepublish=true`时，如果重挂载（remount）调用失败，kubelet会错误删除挂载目录，导致Pod使用陈旧卷数据的问题 - [PR #139228](https://github.com/kubernetes/kubernetes/pull/139228) - **影响：** 使用该特性的CSI驱动可能无法成功修复挂载问题，导致Pod数据不一致。
4. 修复了DRA评分bug，该bug可能导致同时使用多节点声明和每节点声明的Pod卡在Pending状态 - [PR #139363](https://github.com/kubernetes/kubernetes/pull/139363) - **影响：** 使用复杂DRA资源声明的Pod可能无法被调度。
5. 修复了`kubeadm init phase certs --dry-run`命令中复制现有CA文件路径的错误 - [PR #139445](https://github.com/kubernetes/kubernetes/pull/139445) - **影响：** 影响使用`--dry-run`预检查证书流程的用户，命令行为不正确。

## 💥 破坏性变更
1. 🚨 此版本主要为Bug修复，未引入破坏性API变更。但请注意，PR #139192的修复涉及CRI API底层将`string`字段改为`bytes`，这对容器运行时是透明更改，不影响用户API，但确保了与gRPC严格UTF-8验证的兼容性。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复了从Secret中读取二进制（非UTF-8）数据作为环境变量时的回归问题，恢复了1.34之前的行为 - [PR #139192](https://github.com/kubernetes/kubernetes/pull/139192) - **影响：** 使用二进制Secret作为环境变量的Pod在1.34+版本会创建失败，此修复使其恢复正常。
2. 修复了处理`IPFamilies`字段为空的Service时，端点控制器（endpoint controller）可能发生的panic - [PR #139233](https://github.com/kubernetes/kubernetes/pull/139233) - **影响：** 影响从双栈支持前版本迁移过来且从未更新过spec的Service，可能导致控制器崩溃。
3. 修复了在Job的`suspended`条件尚未设置时，修改其调度指令（如nodeSelector）会被拒绝的回归问题 - [PR #139329](https://github.com/kubernetes/kubernetes/pull/139329) - **影响：** 影响1.36中暂停Job的管理流程，导致合法的更新操作失败。

## 🚀 性能优化
1. 优化了SELinux指标发射的性能，避免了昂贵的比较操作 - [PR #139136](https://github.com/kubernetes/kubernetes/pull/139136) - **提升：** 减少了节点上指标收集时的CPU开销，对大规模集群有益。

## 🎯 风险评估
**整体风险评估：中等。** 此版本修复了多个高优先级的稳定性和数据一致性Bug，升级收益显著高于风险。主要风险点在于DRA相关的修复较为集中，如果集群重度依赖DRA，需在测试环境中充分验证。Go版本升级风险较低。建议在测试集群验证无误后，尽快安排生产环境升级，特别是已受上述Bug影响的集群。

## 📋 升级建议
1. **立即升级建议：** 如果您的集群正在使用或计划使用DRA（动态资源分配）功能，或者有使用二进制数据Secret作为环境变量的工作负载，强烈建议尽快安排升级到v1.36.2，以修复可能导致调度器panic、数据损坏或Pod创建失败的严重问题。
2. **升级前检查：** 检查集群中是否存在`IPFamilies`字段为空的Service（通常是旧集群迁移遗留），升级将避免端点控制器因此panic。
3. **测试验证：** 升级后，重点测试DRA设备分配、CSI卷操作（特别是支持`requiresRepublish`的驱动）、以及从Secret设置环境变量的功能。
4. **kubeadm用户：** 如果依赖`--dry-run`进行初始化预检查，升级后可获得正确的行为。

## 📋 Release 包含的变更

### PR #138871: release-1.36: upgrade go to 1.26.4
- **链接：** https://github.com/kubernetes/kubernetes/pull/138871
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** lgtm, release-note, size/XS, kind/feature, cherry-pick-approved, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  将 Kubernetes 构建的 Go 语言版本升级至 1.26.4。这是一个针对 release-1.36 的基础设施更新。

### PR #138988: Automated cherry pick of #138885: DRA: fix AllocationModeAll with consumed counters
- **链接：** https://github.com/kubernetes/kubernetes/pull/138988
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复当 DRA ResourceClaim 使用 `allocationMode: All` 并选择了消耗共享计数器的设备时，可能引发的 kube-scheduler panic。

### PR #139136: Automated cherry pick of #138981: Improve performance characteristic of selinux metric emission
- **链接：** https://github.com/kubernetes/kubernetes/pull/139136
- **状态：** closed
- **已合并：** 是
- **作者：** gnufied
- **标签：** kind/bug, lgtm, sig/storage, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复 selinux 指标发射的性能问题，通过避免昂贵的比较操作来优化性能特性。这是一个针对 release-1.36 的 cherry-pick。

### PR #139192: [1.36] Restore ability to plumb binary data through envvar values
- **链接：** https://github.com/kubernetes/kubernetes/pull/139192
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 1.34 版本以来的回归问题：恢复使用包含二进制非 UTF-8 数据的 Secret API 对象作为容器环境变量值的能力。该修复将 cri-api 的 value 字段从 string 改为 bytes。

### PR #139211: Automated cherry pick of #139040: DRA: account for shared devices when rebuilding counters
- **链接：** https://github.com/kubernetes/kubernetes/pull/139211
- **状态：** closed
- **已合并：** 是
- **作者：** ashvindeodhar
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DRA 调度器 bug：当使用 SharedCounters (DRAPartitionableDevices) 和 multi-allocatable devices (DRAConsumableCapacity) 时，可能将互斥的设备分区分配给多个 Pod，导致设备冲突或数据丢失。

### PR #139228: Automated cherry pick of #139045: fix(csi): preserve mount dir when NodePublish fails on a remount
- **链接：** https://github.com/kubernetes/kubernetes/pull/139228
- **状态：** closed
- **已合并：** 是
- **作者：** aramase
- **标签：** kind/bug, priority/important-soon, lgtm, sig/storage, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 CSI 问题：当因 CSIDriver.spec.requiresRepublish=true 触发的周期性 NodePublishVolume 调用失败时，kubelet 会错误删除挂载目录，导致 Pod 卷内容过时且无法修复。

### PR #139233: Automated cherry pick of #138736: fix: avoid panic on services with empty IPFamilies
- **链接：** https://github.com/kubernetes/kubernetes/pull/139233
- **状态：** closed
- **已合并：** 是
- **作者：** rahulbabu95
- **标签：** kind/bug, sig/network, lgtm, release-note, size/M, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复 endpoint controller 在处理 IPFamilies 字段为空的 Service（即从未更新 spec 的 pre-dual-stack 服务）时可能发生的 panic。

### PR #139329: Automated cherry pick of #139287: batch/job: Fix scheduling directives mutation for not-yet-started suspended Jobs
- **链接：** https://github.com/kubernetes/kubernetes/pull/139329
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, sig/testing, kind/regression, triage/accepted
- **变更说明：**
  修复 1.36 版本中的回归问题：当 JobSuspended 条件尚未被 job controller 设置时，对 suspended Jobs 的调度指令（nodeSelector、tolerations、node affinity）的修改会被拒绝。

### PR #139363: Automated cherry pick of #139017: Fix dra scoring bug with mixed allocated and unallocated claims
- **链接：** https://github.com/kubernetes/kubernetes/pull/139363
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DRA 调度器评分 bug：当 Pod 同时使用多节点共享的 claim 和单节点 claim 时，可能导致 Pod 卡在 Pending 状态。

### PR #139445: Automated cherry pick of #139339: kubeadm: fix dry-run CA copy paths in init certs
- **链接：** https://github.com/kubernetes/kubernetes/pull/139445
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm init phase certs --dry-run 命令中复制现有 CA 文件路径的错误。这是一个针对 release-1.36 的 bug 修复。

### PR #139585: [release-1.36] [go]Bump images and versions to go 1.26.4 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/139585
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/critical-urgent, lgtm, release-note, size/S, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将 Kubernetes 构建工具链升级至 Go 1.26.4，并更新 distroless iptables 镜像版本。这是一个针对 release-1.36 的构建基础更新。

---
*本报告由 Containerd Release Tracker 自动生成*
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
- **分析时间：** 2026-06-12 12:46:55
- **分析的 PR 数量：** 11
- **分析的 Issue 数量：** 1
- **重要项目数量：** 12

## 📊 版本概述
Kubernetes v1.36.2 是一个关键的补丁版本，主要修复了 v1.36.0/1.36.1 中引入的多个严重 Bug 和回归问题，包括可能导致调度器 panic、数据损坏、Pod 创建失败和功能异常的缺陷，强烈建议受影响的集群升级。

## 🔒 安全问题修复
1. ⚠️ 基础镜像和构建工具链升级至 Go 1.26.4，通常包含重要的安全修复 - [PR #138871](https://github.com/kubernetes/kubernetes/pull/138871) & [PR #139585](https://github.com/kubernetes/kubernetes/pull/139585) - **风险级别：** 中 - 建议升级以获取最新的安全补丁。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复了 DRA `AllocationMode: All` 与消耗计数器一起使用时导致 kube-scheduler panic 的问题 - [PR #138988](https://github.com/kubernetes/kubernetes/pull/138988) - **影响：** 调度器组件崩溃，影响集群调度能力。
2. 修复了同时包含多节点声明和单节点声明的 Pod 可能卡在 Pending 状态的 DRA 计分 Bug - [PR #139363](https://github.com/kubernetes/kubernetes/pull/139363) - **影响：** 依赖 DRA 的 Pod 无法被调度。
3. 修复了 `kubeadm init phase certs --dry-run` 在复制现有 CA 文件时路径错误的问题 - [PR #139445](https://github.com/kubernetes/kubernetes/pull/139445) - **影响：** kubeadm dry-run 操作可能失败或产生误导性输出。

## 💥 破坏性变更
1. 🚨 此版本未引入新的破坏性变更。主要修复了之前版本（特别是 1.34 和 1.36.0/1.36.1）中引入的回归问题。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复了从 Secret 设置环境变量时，若包含二进制非 UTF-8 数据会导致 Pod 创建失败的回归问题 - [PR #139192](https://github.com/kubernetes/kubernetes/pull/139192) - **影响：** 自 1.34 版本起，使用二进制数据 Secret 作为环境变量的 Pod 将无法启动。
2. 修复了 Dynamic Resource Allocation (DRA) 调度器在设备使用 `SharedCounters` 时，可能将互斥的设备分区分配给多个 Pod 的严重 Bug - [PR #139211](https://github.com/kubernetes/kubernetes/pull/139211) - **影响：** 可能导致工作负载失败、设备冲突、崩溃或数据丢失。
3. 修复了当 CSI `requiresRepublish=true` 且 `NodePublishVolume` 调用失败时，kubelet 错误删除挂载目录的问题 - [PR #139228](https://github.com/kubernetes/kubernetes/pull/139228) - **影响：** Pod 内卷数据变为陈旧且无法修复，导致数据不一致。
4. 修复了 endpoint 控制器在处理 `IPFamilies` 字段为空的 Service（旧版单栈服务）时可能发生的 panic - [PR #139233](https://github.com/kubernetes/kubernetes/pull/139233) - **影响：** 控制器组件崩溃，影响服务发现功能。
5. 修复了 1.36 中修改处于 `suspended` 状态但 `JobSuspended` 条件尚未设置的 Job 的调度指令（如 nodeSelector）会被拒绝的回归问题 - [PR #139329](https://github.com/kubernetes/kubernetes/pull/139329) - **影响：** 无法动态更新挂起 Job 的调度约束。

## 🚀 性能优化
1. 优化了 SELinux 指标发射的性能，避免了昂贵的比较操作 - [PR #139136](https://github.com/kubernetes/kubernetes/pull/139136) - **提升：** 减少 kubelet 在生成 SELinux 相关指标时的 CPU 开销。

## 🎯 风险评估
整体风险评估：**中低风险**。此版本是修复导向的补丁发布，解决了多个可能导致服务中断和数据损坏的严重 Bug，因此升级的收益远大于风险。建议的升级时机是**尽快**，特别是对于已受上述 Bug 影响的集群。需要特别关注的方面是 DRA 设备驱动与 CSI 驱动在修复后的兼容性，以及升级过程中涉及状态重建的功能（如 CSI 卷重挂载）。

## 📋 升级建议
1. **立即升级建议：** 如果您正在使用 1.36.0 或 1.36.1，尤其是使用了 DRA 功能、CSI 存储卷（且 `requiresRepublish=true`）、或将包含二进制数据的 Secret 用作环境变量，请尽快安排升级到 v1.36.2。
2. **升级前检查：** 确认集群中是否存在 `IPFamilies` 字段为空的老式 Service，以及是否存在调度指令被意外拒绝的挂起 Job。
3. **测试策略：** 在非生产环境充分测试，重点验证 DRA 设备分配、CSI 卷操作、基于 Secret 的环境变量注入以及 Job 调度指令更新等功能。
4. **监控重点：** 升级后，密切关注 kube-scheduler 和 kube-controller-manager 的日志，检查是否有 panic 或错误；监控使用 DRA 和 CSI 的 Pod 状态。

## 📋 Release 包含的变更

### PR #138871: release-1.36: upgrade go to 1.26.4
- **链接：** https://github.com/kubernetes/kubernetes/pull/138871
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** lgtm, release-note, size/XS, kind/feature, cherry-pick-approved, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  在release-1.36中，将Go版本升级到1.26.4。

### PR #138988: Automated cherry pick of #138885: DRA: fix AllocationModeAll with consumed counters
- **链接：** https://github.com/kubernetes/kubernetes/pull/138988
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  cherry pick #138885到release-1.36，修复kube-scheduler panic：当DRA ResourceClaim使用allocationMode: All并选择消耗共享计数器的设备时。

### PR #139136: Automated cherry pick of #138981: Improve performance characteristic of selinux metric emission
- **链接：** https://github.com/kubernetes/kubernetes/pull/139136
- **状态：** closed
- **已合并：** 是
- **作者：** gnufied
- **标签：** kind/bug, lgtm, sig/storage, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  在release-1.36中cherry pick #138981，优化selinux metric emission的性能，避免高成本比较操作。

### PR #139192: [1.36] Restore ability to plumb binary data through envvar values
- **链接：** https://github.com/kubernetes/kubernetes/pull/139192
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  手动cherry pick #139168到release-1.36，修复1.34+回归：恢复处理包含二进制非UTF-8数据的Secret API对象作为容器环境变量的能力，避免CreateContainerError（涉及cri-api字段从string改为bytes）。

### PR #139211: Automated cherry pick of #139040: DRA: account for shared devices when rebuilding counters
- **链接：** https://github.com/kubernetes/kubernetes/pull/139211
- **状态：** closed
- **已合并：** 是
- **作者：** ashvindeodhar
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  cherry pick #139040到release-1.36，修复DRA调度器bug：在重建计数器时考虑共享设备（如SharedCounters和DRAConsumableCapacity），避免将互斥设备分区分配给多个Pods，防止设备冲突或数据丢失。

### PR #139228: Automated cherry pick of #139045: fix(csi): preserve mount dir when NodePublish fails on a remount
- **链接：** https://github.com/kubernetes/kubernetes/pull/139228
- **状态：** closed
- **已合并：** 是
- **作者：** aramase
- **标签：** kind/bug, priority/important-soon, lgtm, sig/storage, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  cherry pick #139045到release-1.36，修复CSI问题：当NodePublishVolume在remount（由CSIDriver.spec.requiresRepublish触发）失败时，kubelet不再删除mount目录，避免pod内容陈旧。

### PR #139233: Automated cherry pick of #138736: fix: avoid panic on services with empty IPFamilies
- **链接：** https://github.com/kubernetes/kubernetes/pull/139233
- **状态：** closed
- **已合并：** 是
- **作者：** rahulbabu95
- **标签：** kind/bug, sig/network, lgtm, release-note, size/M, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, kind/regression, needs-triage
- **变更说明：**
  cherry pick #138736到release-1.36，修复endpoint controller在处理IPFamilies字段为空的services（未更新的pre-dual-stack服务）时可能触发的panic。

### PR #139329: Automated cherry pick of #139287: batch/job: Fix scheduling directives mutation for not-yet-started suspended Jobs
- **链接：** https://github.com/kubernetes/kubernetes/pull/139329
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, sig/testing, kind/regression, triage/accepted
- **变更说明：**
  cherry pick #139287到release-1.36，修复1.36回归：允许修改未启动suspended Jobs的调度指令（nodeSelector、tolerations、node affinity），即使JobSuspended条件未设置。

### PR #139363: Automated cherry pick of #139017: Fix dra scoring bug with mixed allocated and unallocated claims
- **链接：** https://github.com/kubernetes/kubernetes/pull/139363
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  cherry pick #139017到release-1.36，修复DRA评分bug：当Pods共享multi-node claims并同时具有per-node claims时，避免Pod卡在Pending状态。

### PR #139445: Automated cherry pick of #139339: kubeadm: fix dry-run CA copy paths in init certs
- **链接：** https://github.com/kubernetes/kubernetes/pull/139445
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  cherry pick #139339到release-1.36，修复kubeadm init phase certs --dry-run中CA文件复制路径的错误，确保正确复制现有CA文件。

### PR #139585: [release-1.36] [go]Bump images and versions to go 1.26.4 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/139585
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/critical-urgent, lgtm, release-note, size/S, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  在release-1.36中，将Kubernetes构建工具升级到Go 1.26.4，并更新distroless iptables镜像。

---
*本报告由 Containerd Release Tracker 自动生成*
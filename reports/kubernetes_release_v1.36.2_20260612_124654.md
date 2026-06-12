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
- **分析时间：** 2026-06-12 12:46:54
- **分析的 PR 数量：** 11
- **分析的 Issue 数量：** 1
- **重要项目数量：** 12

## 📊 版本概述
Kubernetes v1.36.2 是一个关键的补丁版本，主要修复了从 v1.34 引入的多个严重回归问题、DRA（动态资源分配）相关的调度器panic/数据损坏风险，以及一个可能导致控制器panic的服务处理问题。

## 🔒 安全问题修复
1. ⚠️ 基础镜像和构建工具链升级至Go 1.26.4，通常包含安全修复 - [PR #138871](https://github.com/kubernetes/kubernetes/pull/138871), [PR #139585](https://github.com/kubernetes/kubernetes/pull/139585) - **风险级别：** 中 - 建议升级以获取最新的Go语言安全补丁。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复了Pods因混合使用多节点声明和单节点DRA声明而卡在Pending状态的问题 - [PR #139363](https://github.com/kubernetes/kubernetes/pull/139363) - **影响：** 使用复杂DRA资源声明的Pod可能无法被调度。
2. 修复了`kubeadm init phase certs --dry-run`命令在复制现有CA文件时路径错误的问题 - [PR #139445](https://github.com/kubernetes/kubernetes/pull/139445) - **影响：** 影响kubeadm的dry-run操作准确性，对实际集群部署无直接影响。

## 💥 破坏性变更
1. 🚨 此版本为补丁版本，主要修复回归和bug，未引入破坏性API变更。但修复了v1.34以来的行为回归（如Secret二进制数据），升级后行为将与v1.33及之前版本一致。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复了Secret中二进制数据作为环境变量的回归问题，恢复了v1.34之前的行为 - [PR #139192](https://github.com/kubernetes/kubernetes/pull/139192) - **影响：** 使用包含非UTF-8二进制数据（如加密密钥）的Secret作为环境变量的Pod在v1.34+会创建失败，此修复后恢复正常。
2. 修复了处理`IPFamilies`字段为空的Service时，端点控制器可能发生的panic - [PR #139233](https://github.com/kubernetes/kubernetes/pull/139233) - **影响：** 从旧版本（双栈支持前）迁移过来且从未更新过spec的Service可能导致控制器崩溃，影响服务发现。
3. 修复了CSI卷在`requiresRepublish=true`时，重发布失败会错误删除挂载目录的问题 - [PR #139228](https://github.com/kubernetes/kubernetes/pull/139228) - **影响：** Pod可能因挂载目录被删除而无法访问卷数据，导致数据不一致或应用故障。
4. 修复了DRA（动态资源分配）调度器在处理`allocationMode: All`和共享计数器设备时的panic - [PR #138988](https://github.com/kubernetes/kubernetes/pull/138988) - **影响：** 使用特定DRA配置时，kube-scheduler可能崩溃，导致调度中断。
5. 修复了DRA调度器在共享设备场景下可能将互斥设备分区分配给多个Pod的bug - [PR #139211](https://github.com/kubernetes/kubernetes/pull/139211) - **影响：** 可能导致设备冲突、工作负载失败、崩溃或数据丢失，风险较高。
6. 修复了挂起Job的调度指令（如nodeSelector）在特定条件下无法修改的回归问题 - [PR #139329](https://github.com/kubernetes/kubernetes/pull/139329) - **影响：** 在v1.36中，对尚未启动的挂起Job修改调度约束会被错误拒绝。

## 🚀 性能优化
1. 优化了SELinux指标发射的性能，避免了昂贵的比较操作 - [PR #139136](https://github.com/kubernetes/kubernetes/pull/139136) - **提升：** 减少了kubelet在收集SELinux上下文指标时的CPU开销，对大规模集群或高负载节点有益。

## 🎯 风险评估
**整体风险评估：低。** 此版本主要修复已知bug和回归问题，升级风险较低，且修复的问题（如控制器panic、数据损坏风险）本身对生产环境的威胁更大。**建议升级时机：** 对于已受上述bug影响的集群，应尽快安排升级。对于运行平稳的集群，可在下一个维护窗口进行升级。**需要特别关注的方面：** DRA功能的使用者、依赖二进制Secret的应用、以及使用老旧Service定义的集群。

## 📋 升级建议
1. **强烈建议升级：** 如果您在v1.34-v1.36.1版本中遇到以下问题，应立即计划升级：1) 使用二进制Secret作为环境变量的Pod创建失败；2) 端点控制器无故崩溃；3) 使用DRA功能时调度器panic或设备分配异常；4) CSI卷挂载出现数据不一致。
2. **升级前检查：** 确认集群中是否存在`IPFamilies`字段为空的Service（可通过`kubectl get svc -A -o jsonpath='{.items[?(@.spec.ipFamilies==null)].metadata.name}'`检查），此类服务是导致控制器panic的根源，建议在升级前或升级后更新其spec。
3. **测试验证：** 在测试环境中重点验证：1) 包含非UTF-8 Secret的Pod创建；2) DRA相关的工作负载调度与运行；3) CSI卷的挂载、重挂载和删除操作。

## 📋 Release 包含的变更

### PR #138871: release-1.36: upgrade go to 1.26.4
- **链接：** https://github.com/kubernetes/kubernetes/pull/138871
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** lgtm, release-note, size/XS, kind/feature, cherry-pick-approved, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  将 Go 语言版本升级至 1.26.4。

### PR #138988: Automated cherry pick of #138885: DRA: fix AllocationModeAll with consumed counters
- **链接：** https://github.com/kubernetes/kubernetes/pull/138988
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复当 DRA ResourceClaim 使用 `allocationMode: All` 并选择消耗共享计数器的设备时，可能引发的 kube-scheduler panic。

### PR #139136: Automated cherry pick of #138981: Improve performance characteristic of selinux metric emission
- **链接：** https://github.com/kubernetes/kubernetes/pull/139136
- **状态：** closed
- **已合并：** 是
- **作者：** gnufied
- **标签：** kind/bug, lgtm, sig/storage, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  改进 selinux metric emission 的性能特性，避免在指标发射过程中进行昂贵的比较操作。

### PR #139192: [1.36] Restore ability to plumb binary data through envvar values
- **链接：** https://github.com/kubernetes/kubernetes/pull/139192
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 1.34 版本引入的回归问题，恢复将包含二进制非 UTF-8 数据的 Secret API 对象用作容器环境变量的能力，解决由此引发的 CreateContainerError。

### PR #139211: Automated cherry pick of #139040: DRA: account for shared devices when rebuilding counters
- **链接：** https://github.com/kubernetes/kubernetes/pull/139211
- **状态：** closed
- **已合并：** 是
- **作者：** ashvindeodhar
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DRA 调度器 bug，该 bug 可能导致将互斥的设备分区分配给多个 Pod，影响使用 SharedCounters (DRAPartitionableDevices) 和 multi-allocatable devices (DRAConsumableCapacity) 的 DRA 驱动。

### PR #139228: Automated cherry pick of #139045: fix(csi): preserve mount dir when NodePublish fails on a remount
- **链接：** https://github.com/kubernetes/kubernetes/pull/139228
- **状态：** closed
- **已合并：** 是
- **作者：** aramase
- **标签：** kind/bug, priority/important-soon, lgtm, sig/storage, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 CSI 问题：当因 CSIDriver.spec.requiresRepublish=true 触发的周期性 NodePublishVolume 调用失败时，kubelet 不再错误删除挂载目录，防止 Pod 卷内容陈旧且无法修复。

### PR #139233: Automated cherry pick of #138736: fix: avoid panic on services with empty IPFamilies
- **链接：** https://github.com/kubernetes/kubernetes/pull/139233
- **状态：** closed
- **已合并：** 是
- **作者：** rahulbabu95
- **标签：** kind/bug, sig/network, lgtm, release-note, size/M, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复 endpoint controller 在处理 IPFamilies 字段为空的服务（即从未进行 spec 更新的 pre-dual-stack 服务）时可能发生的 panic。

### PR #139329: Automated cherry pick of #139287: batch/job: Fix scheduling directives mutation for not-yet-started suspended Jobs
- **链接：** https://github.com/kubernetes/kubernetes/pull/139329
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** kind/bug, area/test, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, sig/testing, kind/regression, triage/accepted
- **变更说明：**
  修复 1.36 版本中的回归问题：当 suspended Job 的 JobSuspended 条件尚未由 job controller 设置时，对其调度指令（nodeSelector、tolerations、node affinity）的修改会被错误拒绝。

### PR #139363: Automated cherry pick of #139017: Fix dra scoring bug with mixed allocated and unallocated claims
- **链接：** https://github.com/kubernetes/kubernetes/pull/139363
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 Dynamic Resource Allocation (DRA) 评分 bug，解决同时包含共享 multi-node claim 和 per-node claim 的 Pod 可能卡在 Pending 状态的问题。

### PR #139445: Automated cherry pick of #139339: kubeadm: fix dry-run CA copy paths in init certs
- **链接：** https://github.com/kubernetes/kubernetes/pull/139445
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm init phase certs --dry-run 命令中复制现有 CA 文件时的路径错误。

### PR #139585: [release-1.36] [go]Bump images and versions to go 1.26.4 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/139585
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/critical-urgent, lgtm, release-note, size/S, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将 Kubernetes 构建版本升级至 Go 1.26.4，并更新 distroless iptables 镜像。

---
*本报告由 Containerd Release Tracker 自动生成*
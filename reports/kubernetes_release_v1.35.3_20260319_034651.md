# Kubernetes 版本发布分析报告
## v1.35.3 (v1.35.3)

### 📋 版本信息
- **版本标签：** v1.35.3
- **版本名称：** v1.35.3
- **发布时间：** 2026-03-19T03:20:52Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.3

### 🔍 分析统计
- **分析时间：** 2026-03-19 03:46:51
- **分析的 PR 数量：** 3
- **分析的 Issue 数量：** 0
- **重要项目数量：** 2

## 📊 版本概述
Kubernetes v1.35.3 是一个补丁版本，主要修复了 kubeadm 在 etcd 成员管理和节点卸载过程中的两个关键 Bug，提升了集群操作的稳定性和可靠性。

## 🐛 重要问题修复
1. 修复 kubeadm 将 etcd learner 成员错误地添加到客户端端点列表的问题 - [PR #137257](https://github.com/kubernetes/kubernetes/pull/137257) - **影响：** 在 etcd 集群中使用 learner 成员时，kubeadm 生成的配置可能导致 API 服务器等组件连接到无效的 learner 端点，从而引发连接失败和控制平面不稳定。此修复确保了客户端仅连接到有投票权的成员。
2. 修复 kubeadm 在节点卸载阶段因遇到 EINVAL 错误而失败的问题 - [PR #137569](https://github.com/kubernetes/kubernetes/pull/137569) - **影响：** 在某些情况下（例如对已卸载的目录重复执行操作），`kubeadm reset` 或节点清理过程可能因系统调用返回 EINVAL 错误而意外中断，阻塞正常的集群维护或升级流程。此修复通过忽略该特定错误，使流程能够继续执行。
3. 修复 DRA（动态资源分配）设备污点驱逐控制器状态报告可能不准确的问题 - [PR #137047](https://github.com/kubernetes/kubernetes/pull/137047) - **影响：** 这是一个测试稳定性修复（Flake），主要影响单元测试的可靠性。在生产环境中，DRA 控制器在极短时间内可能报告一个稍显混乱的中间状态日志，但最终会达到正确状态。此修复通过延迟状态更新来避免混淆，提升了代码健壮性。

## 🎯 风险评估
整体风险评估：**极低**。此版本仅包含针对特定场景的 Bug 修复，不涉及 API 变更、功能废弃或架构调整。升级风险极小，是推荐的安全升级。建议在常规维护窗口内进行升级。需要特别关注升级后 `kubeadm reset` 等命令的行为是否符合预期。

## 📋 升级建议
1. **建议升级：** 对于所有使用 kubeadm 搭建或维护的 1.35 集群，特别是那些在 `kubeadm reset` 或涉及 etcd 操作时遇到问题的环境，建议安排升级到此版本。
2. **升级前检查：** 尽管是低风险补丁，升级前仍建议对集群状态（特别是 etcd 健康状态）和关键工作负载进行备份或检查。

## 📋 Release 包含的变更

### PR #137047: [release-1.35]Automated cherry pick of #135611: Fix flake TestDeviceTaintRule test
- **链接：** https://github.com/kubernetes/kubernetes/pull/137047
- **状态：** closed
- **已合并：** 是
- **作者：** vikasbolla
- **标签：** sig/scheduling, lgtm, release-note, size/L, kind/flake, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  此PR将#135611的修复cherry-pick到release-1.35分支，解决了DRA（动态资源分配）设备污点驱逐控制器中TestDeviceTaintRule测试的稳定性问题。修复通过延迟状态更新，避免了在Pod被驱逐后但informer缓存尚未更新前，控制器日志可能短暂显示混淆信息（如‘1 pod needs to be evicted’）的中间状态，确保状态报告始终准确。

### PR #137257: Automated cherry pick of #137251: kubeadm: do not add learner member to etcd client endpoints
- **链接：** https://github.com/kubernetes/kubernetes/pull/137257
- **状态：** closed
- **已合并：** 是
- **作者：** ahrtr
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  此PR将#137251的修复cherry-pick到release-1.35分支。修复了kubeadm在构建etcd客户端端点列表时，错误地将learner（学习者）成员包含在内的问题。这确保了客户端不会尝试连接到尚不具备完整服务能力的etcd成员，从而保证etcd客户端连接的稳定性与可靠性。

### PR #137569: [release-1.35] cmd/kubeadm: ignore EINVAL error during unmount
- **链接：** https://github.com/kubernetes/kubernetes/pull/137569
- **状态：** closed
- **已合并：** 是
- **作者：** fuweid
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  此PR针对release-1.35分支，修复了kubeadm在卸载操作中的一个问题。当目标文件系统未被挂载时，`unmount`系统调用会返回EINVAL错误。PR修改了相关代码以忽略此特定错误，避免了在此场景下因误报错误而导致的操作失败或误导性日志。

---
*本报告由 Containerd Release Tracker 自动生成*
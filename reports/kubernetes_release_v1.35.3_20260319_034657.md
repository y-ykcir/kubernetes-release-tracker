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
- **分析时间：** 2026-03-19 03:46:57
- **分析的 PR 数量：** 3
- **分析的 Issue 数量：** 0
- **重要项目数量：** 2

## 📊 版本概述
Kubernetes v1.35.3 是一个维护版本，主要修复了 kubeadm 中与 etcd learner 成员和文件系统卸载相关的两个关键 Bug，提升了集群部署与维护的稳定性。

## 🐛 重要问题修复
1. 修复 kubeadm 高可用 etcd 配置问题：当 etcd 集群中存在 learner（学习者）成员时，kubeadm 会错误地将其 IP 地址添加到 etcd 客户端的端点列表中，这可能导致控制平面组件（如 kube-apiserver）无法正确连接到 etcd 集群。 - [PR #137257](https://github.com/kubernetes/kubernetes/pull/137257) - **影响：** 使用 kubeadm 部署的、包含 learner 成员的高可用 etcd 集群可能面临控制平面连接不稳定或失败的风险。
2. 修复 kubeadm 卸载错误处理：在清理环境（如 `kubeadm reset`）时，如果尝试卸载一个不存在的挂载点，会返回 EINVAL 错误并导致整个操作失败。现在会忽略此特定错误，使清理流程更健壮。 - [PR #137569](https://github.com/kubernetes/kubernetes/pull/137569) - **影响：** 在特定场景下（如重复执行 reset 或部分清理后），集群重置或节点清理操作可能意外中断，阻碍运维流程。
3. 修复 DRA 设备污点驱逐控制器状态报告：修复了控制器在驱逐单个 Pod 时可能短暂报告误导性状态信息的问题，提升了监控和日志的可读性。 - [PR #137047](https://github.com/kubernetes/kubernetes/pull/137047) - **影响：** 此修复主要针对测试 flake 和日志清晰度，对生产环境功能无直接影响，但改善了运维人员通过日志诊断问题的体验。

## ✨ 主要变更
1. kubeadm：修复了在高可用 etcd 集群中，将 learner 成员错误地添加到客户端端点列表的问题 - [PR #137257](https://github.com/kubernetes/kubernetes/pull/137257)
2. kubeadm：修复了在执行 `kubeadm reset` 等操作时，因挂载点不存在（EINVAL 错误）而导致命令失败的问题 - [PR #137569](https://github.com/kubernetes/kubernetes/pull/137569)

## 🎯 风险评估
**整体风险评估：低**。此版本为纯 Bug 修复版本，未引入新功能、API 变更或破坏性更改，升级风险极小。
**建议升级时机：** 可以在常规维护窗口内进行升级。对于受上述两个 kubeadm Bug 影响的集群，建议尽快安排升级以消除潜在稳定性风险。
**需要特别关注的方面：** 无需特别关注，正常升级流程即可。升级后，可验证 `kubeadm` 相关操作（如重置、证书更新）是否正常。

## 📋 升级建议
1. **建议升级群体：** 强烈建议所有使用 `kubeadm` 工具管理集群，特别是部署了高可用 etcd 集群（且可能使用了 learner 角色）的用户升级到此版本。
2. **升级前检查：** 如果您在 etcd 集群中配置了 learner 成员，请在升级前确认控制平面与 etcd 的连接状态。升级此版本将自动修复客户端端点列表。
3. **运维影响：** 此版本修复了 `kubeadm reset` 的健壮性问题，对于经常需要重置节点或进行集群生命周期操作的环境，升级后操作体验会更顺畅。
4. **升级策略：** 这是一个补丁版本，仅包含错误修复，风险较低。可以按照标准的滚动更新流程，优先升级控制平面节点。

## 📋 Release 包含的变更

### PR #137047: [release-1.35]Automated cherry pick of #135611: Fix flake TestDeviceTaintRule test
- **链接：** https://github.com/kubernetes/kubernetes/pull/137047
- **状态：** closed
- **已合并：** 是
- **作者：** vikasbolla
- **标签：** sig/scheduling, lgtm, release-note, size/L, kind/flake, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  此 PR 将 #135611 的修复 cherry-pick 到 release-1.35 分支。解决了 DRA (Dynamic Resource Allocation) 设备污点驱逐控制器测试 TestDeviceTaintRule 的 flaky 问题。通过延迟状态更新，避免了因 informer 缓存延迟导致的中间状态报告不准确，使状态输出更清晰。

### PR #137257: Automated cherry pick of #137251: kubeadm: do not add learner member to etcd client endpoints
- **链接：** https://github.com/kubernetes/kubernetes/pull/137257
- **状态：** closed
- **已合并：** 是
- **作者：** ahrtr
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  此 PR 将 #137251 的修复 cherry-pick 到 release-1.35 分支。核心修复是 kubeadm 在生成 etcd 客户端配置时，不应将 learner 成员（只读、不参与共识）添加到客户端端点列表中，以避免客户端连接失败。

### PR #137569: [release-1.35] cmd/kubeadm: ignore EINVAL error during unmount
- **链接：** https://github.com/kubernetes/kubernetes/pull/137569
- **状态：** closed
- **已合并：** 是
- **作者：** fuweid
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/XS, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  此 PR 针对 release-1.35 分支，修复了 kubeadm 在卸载操作时遇到 EINVAL 错误的问题。当目标路径未挂载时，unmount 系统调用会返回 EINVAL，现在忽略此错误，使命令能正常完成，提升了健壮性。

---
*本报告由 Containerd Release Tracker 自动生成*
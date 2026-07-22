# Kubernetes 版本发布分析报告
## v1.35.7 (v1.35.7)

### 📋 版本信息
- **版本标签：** v1.35.7
- **版本名称：** v1.35.7
- **发布时间：** 2026-07-22T22:28:35Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.7

### 🔍 分析统计
- **分析时间：** 2026-07-22 23:46:45
- **分析的 PR 数量：** 6
- **分析的 Issue 数量：** 0
- **重要项目数量：** 6

## 📊 版本概述
Kubernetes v1.35.7 是一个维护版本，主要修复了 kubeadm 节点加入的稳定性问题、一个关键的 CRI API 回归问题，并减少了 kubelet 的冗余日志，同时更新了 Go 语言版本以包含安全补丁。

## 🔒 安全问题修复
1. ⚠️ 基础镜像更新至 Go 1.25.12：此更新包含了 Go 语言运行时的最新安全修复和漏洞补丁 - [PR #140585](https://github.com/kubernetes/kubernetes/pull/140585) - **风险级别：** 中（建议升级以应用最新的语言级安全修复）

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kubeadm etcd learner 提升的健壮性：当 etcd 端提升成功但客户端返回瞬时错误时，kubeadm 现在能正确处理，避免不必要的 etcd-join 失败 - [PR #139909](https://github.com/kubernetes/kubernetes/pull/139909) - **影响：** 提升使用 etcd learner 功能的集群在节点加入或恢复时的成功率
2. 修复 CRI API JSON 编码回归：此问题可能导致依赖特定 JSON 编码格式的容器运行时或监控工具出现解析错误 - [PR #139966](https://github.com/kubernetes/kubernetes/pull/139966) - **影响：** 修复了从 1.34 版本引入的一个潜在兼容性问题，建议所有用户升级以确保 CRI 交互稳定

## 💥 破坏性变更
1. 🚨 此版本无破坏性变更（Breaking Changes）。PR #139966 修复了一个回归问题，实际上是恢复到了之前版本（1.34 之前）的兼容行为。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复 kubeadm etcd 成员提升逻辑，避免对已是投票成员的节点进行不必要的 API 调用，从而减少超时和重试 - [PR #138492](https://github.com/kubernetes/kubernetes/pull/138492)
2. 修复 kubeadm join 时获取 kubeadm-config ConfigMap 的超时策略，使用更合理的 1 分钟超时替代 350ms 短超时，提升复杂网络环境下的成功率 - [PR #139809](https://github.com/kubernetes/kubernetes/pull/139809)
3. 修复 CRI API 中 KeyValue 字段的 JSON 编码回归，恢复为 1.34 版本之前的字符串编码，确保与容器运行时的兼容性 - [PR #139966](https://github.com/kubernetes/kubernetes/pull/139966)
4. kubelet 不再为缺失的可选容器注解记录 V(4) 级别的“Label not found”日志，减少日志噪音和系统负载 - [PR #140321](https://github.com/kubernetes/kubernetes/pull/140321)

## 🚀 性能优化
1. 优化 kubeadm etcd 成员提升逻辑，跳过不必要的 API 调用，减少节点加入或恢复时的延迟和资源消耗 - [PR #138492](https://github.com/kubernetes/kubernetes/pull/138492) - **提升：** 减少 etcd 操作超时和重试，加快节点加入过程
2. 减少 kubelet 冗余日志输出，降低日志系统的存储和索引压力，尤其有利于大规模集群 - [PR #140321](https://github.com/kubernetes/kubernetes/pull/140321) - **提升：** 减少无关日志条目，提升日志可读性和系统效率

## 🎯 风险评估
整体风险评估：**低风险**。此版本主要为错误修复和稳定性提升，未引入新功能或 API 变更。升级风险主要来自任何版本升级固有的通用风险。建议在常规维护窗口进行升级。需要特别关注的方面是验证节点加入流程（特别是使用 kubeadm 的集群）是否更加稳定，以及确保 CRI 接口的兼容性。

## 📋 升级建议
1. **建议升级**：对于运行 1.35 版本且频繁进行节点扩缩容或曾遇到 kubeadm join 超时问题的集群，建议安排升级以获取稳定性修复。
2. **升级前验证**：如果集群中使用了自定义的容器运行时或工具与 CRI API 深度交互，建议在测试环境中验证 PR #139966 的修复是否解决了任何潜在的 JSON 解析问题。
3. **升级策略**：这是一个补丁版本，风险较低，可以采用滚动升级方式。建议遵循标准的升级流程，先升级控制平面，再升级工作节点。
4. **日志监控**：升级后，可以观察 kubelet 日志中关于“Label not found”的冗余信息是否减少，以验证 PR #140321 的修复效果。

## 📋 Release 包含的变更

### PR #138492: Automated cherry pick of #138390: kubeadm: skip promote call when etcd member is already a voting member
- **链接：** https://github.com/kubernetes/kubernetes/pull/138492
- **状态：** closed
- **已合并：** 是
- **作者：** wgkingk
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/S, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  kubeadm 修复 MemberPromote 函数，当 etcd 成员已是投票成员时跳过 promote API 调用，避免不必要的重试和超时。

### PR #139809: Automated cherry pick of #139667: fix(kubeadm): use KubernetesAPICallTimeout for mandatory kubeadm-config fetch during join
- **链接：** https://github.com/kubernetes/kubernetes/pull/139809
- **状态：** closed
- **已合并：** 是
- **作者：** damdo
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm join 过程中获取 kubeadm-config ConfigMap 的超时问题，从 350ms 短重试改为使用 KubernetesAPICallTimeout（默认 1 分钟），并新增 shortConfigMapGet 参数以支持 kubeadm reset 等场景保持向后兼容。

### PR #139909: Automated cherry pick of #139842: kubeadm: treat already promoted learner as successful
- **链接：** https://github.com/kubernetes/kubernetes/pull/139909
- **状态：** closed
- **已合并：** 是
- **作者：** jihyun-huh
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  kubeadm 增强 etcd learner promotion 的韧性，正确处理 etcd 端成功但客户端返回瞬时错误的情况，避免不必要的 etcd-join 失败。

### PR #139966: [1.35] Automated cherry pick of #139964: Restore string JSON encoding of cri-api KeyValue
- **链接：** https://github.com/kubernetes/kubernetes/pull/139966
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  cri-api 恢复 KeyValue value 字段的 JSON 编码方式至 pre-1.34 的字符串编码，修复回归问题。

### PR #140321: Automated cherry pick of #140163: kubelet: stop logging missing optional container annotations
- **链接：** https://github.com/kubernetes/kubernetes/pull/140321
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubelet 不再记录 V(4) 级别关于缺失可选容器注解的 "Label not found" 日志，减少日志噪音。

### PR #140585: [release-1.35] Bump images and versions to golang 1.25.12 and update distroless-iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/140585
- **状态：** closed
- **已合并：** 是
- **作者：** palnabarun
- **标签：** area/test, lgtm, release-note, size/S, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  将 Kubernetes 构建的 Go 版本升级到 1.25.12，并更新 distroless-iptables 镜像，作为发布工程的一部分。

---
*本报告由 Containerd Release Tracker 自动生成*
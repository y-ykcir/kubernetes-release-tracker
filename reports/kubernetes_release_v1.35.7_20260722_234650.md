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
- **分析时间：** 2026-07-22 23:46:50
- **分析的 PR 数量：** 6
- **分析的 Issue 数量：** 0
- **重要项目数量：** 6

## 📊 版本概述
Kubernetes v1.35.7 是一个补丁版本，主要修复了 kubeadm 节点加入的稳定性问题、一个关键的 CRI-API 回归问题，并减少了 kubelet 的日志噪音，提升了集群运维的可靠性。

## 🐛 重要问题修复
1. 修复 kubeadm etcd 成员重复提升问题：当 etcd 成员已是投票成员时，跳过提升 API 调用，避免导致节点加入过程出现不必要的重试和超时失败 - [PR #138492](https://github.com/kubernetes/kubernetes/pull/138492) - **影响：** 使用 kubeadm 管理的高可用 etcd 集群在添加新控制平面节点时会更稳定，减少因重复调用导致的加入失败。
2. 修复 kubeadm join 配置获取超时：将获取必需的 kubeadm-config ConfigMap 的超时从 350ms 调整为标准的 KubernetesAPICallTimeout（默认1分钟） - [PR #139809](https://github.com/kubernetes/kubernetes/pull/139809) - **影响：** 在 API 服务器响应较慢或网络状况不佳时，`kubeadm join` 命令因获取配置超时而失败的概率显著降低。
3. 修复 CRI-API JSON 编码回归：恢复 KeyValue 结构中 `value` 字段的字符串 JSON 编码方式，修复了自 1.34 版本以来可能引入的与某些容器运行时的兼容性问题 - [PR #139966](https://github.com/kubernetes/kubernetes/pull/139966) - **影响：** 确保 kubelet 与容器运行时（CRI）的通信兼容性，避免潜在的容器创建或配置失败。此修复对使用自定义或特定版本 CRI 运行时的环境尤为重要。
4. 修复 kubeadm etcd learner 提升的客户端错误处理：当 etcd 服务端已成功提升 learner 但客户端收到瞬时错误时，kubeadm 现在会将其视为成功，而不是失败 - [PR #139909](https://github.com/kubernetes/kubernetes/pull/139909) - **影响：** 提高了向现有 etcd 集群添加 learner 成员（新控制平面节点）的成功率，增强了集群扩展的鲁棒性。

## ✨ 主要变更
1. 修复 kubeadm etcd 成员重复提升调用，避免不必要的重试和超时 - [PR #138492](https://github.com/kubernetes/kubernetes/pull/138492)
2. 修复 kubeadm join 时获取配置的超时逻辑，使用更合理的 1 分钟超时替代 350ms 短超时 - [PR #139809](https://github.com/kubernetes/kubernetes/pull/139809)
3. 提升 kubeadm etcd learner 成员提升的健壮性，正确处理客户端瞬时错误 - [PR #139909](https://github.com/kubernetes/kubernetes/pull/139909)
4. 修复 CRI-API 中 KeyValue 值的 JSON 编码回归，恢复至 1.34 版本前的字符串编码行为 - [PR #139966](https://github.com/kubernetes/kubernetes/pull/139966)
5. kubelet 不再为缺失的可选容器注解记录 V(4) 级别日志，减少日志噪音 - [PR #140321](https://github.com/kubernetes/kubernetes/pull/140321)
6. 更新构建基础镜像至 Go 1.25.12 并更新 distroless-iptables - [PR #140585](https://github.com/kubernetes/kubernetes/pull/140585)

## 🚀 性能优化
1. 减少 kubeadm etcd 成员管理的不必要 API 调用，优化节点加入流程 - [PR #138492](https://github.com/kubernetes/kubernetes/pull/138492) - **提升：** 减少 etcd 提升操作的重试和潜在超时等待，加快控制平面节点加入速度。
2. 消除 kubelet 对缺失可选容器注解的冗余日志记录，降低系统日志负载 - [PR #140321](https://github.com/kubernetes/kubernetes/pull/140321) - **提升：** 减少日志文件大小和日志收集系统的处理压力，特别是在大规模集群中。

## 🎯 风险评估
整体风险评估：**低风险**。此版本主要为向后兼容的 Bug 修复和稳定性增强，不包含 API 变更、功能废弃或已知的破坏性变更。核心修复针对 kubeadm 和 CRI-API 的特定问题，影响范围有限但重要。建议在常规维护窗口内进行升级。需要特别关注的方面是升级后新节点加入（`kubeadm join`）的行为以及容器运行时（如 containerd, CRI-O）与 kubelet 的交互是否正常。

## 📋 升级建议
1. **建议升级：** 对于运行 Kubernetes 1.35 版本且使用 kubeadm 部署的集群，特别是高可用（HA）架构，建议安排升级到此版本，以获取节点加入稳定性的重要修复。
2. **升级前测试：** 如果您的环境对容器运行时接口（CRI）有严格依赖或使用非标准运行时，请在测试环境中验证 PR #139966 的修复是否解决了任何潜在的兼容性问题。
3. **监控日志变化：** 升级后，观察 kubelet 日志中关于容器注解的 `V(4)` 级别错误信息是否减少，这属于预期行为。
4. **kubeadm 操作验证：** 在升级控制平面节点或添加新节点后，验证 `kubeadm` 相关操作（如 `join`, `init phase control-plane`）的日志，确认没有出现与 etcd 成员管理相关的新错误。

## 📋 Release 包含的变更

### PR #138492: Automated cherry pick of #138390: kubeadm: skip promote call when etcd member is already a voting member
- **链接：** https://github.com/kubernetes/kubernetes/pull/138492
- **状态：** closed
- **已合并：** 是
- **作者：** wgkingk
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/S, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  优化 kubeadm 的 etcd 成员提升逻辑。在 MemberPromote 中，如果目标成员已具有投票权，则跳过 etcd promote API 调用，避免不必要的重试和超时等待。

### PR #139809: Automated cherry pick of #139667: fix(kubeadm): use KubernetesAPICallTimeout for mandatory kubeadm-config fetch during join
- **链接：** https://github.com/kubernetes/kubernetes/pull/139809
- **状态：** closed
- **已合并：** 是
- **作者：** damdo
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm join 时获取 kubeadm-config ConfigMap 的超时问题。将重试超时从 350ms 改为使用 KubernetesAPICallTimeout（默认 1 分钟），以确保在 API 响应较慢时仍能成功获取必需的配置。为 kubeadm reset 等调用方新增 shortConfigMapGet 参数以保持短超时行为。

### PR #139909: Automated cherry pick of #139842: kubeadm: treat already promoted learner as successful
- **链接：** https://github.com/kubernetes/kubernetes/pull/139909
- **状态：** closed
- **已合并：** 是
- **作者：** jihyun-huh
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  增强 kubeadm 中 etcd learner 成员提升的健壮性。当 etcd 端提升成功但客户端返回临时错误时，kubeadm 现在会将其视为成功，从而避免不必要的 etcd-join 操作失败。

### PR #139966: [1.35] Automated cherry pick of #139964: Restore string JSON encoding of cri-api KeyValue
- **链接：** https://github.com/kubernetes/kubernetes/pull/139966
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复 cri-api 中 KeyValue 结构的 JSON 编码回归问题。将 value 字段的编码方式恢复为 1.34 版本之前的字符串编码，以确保向后兼容性。

### PR #140321: Automated cherry pick of #140163: kubelet: stop logging missing optional container annotations
- **链接：** https://github.com/kubernetes/kubernetes/pull/140321
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/S, cherry-pick-approved, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 Kubelet 日志噪音问题。Kubelet 不再为缺失的可选容器注解记录 V(4) 级别的 "Label not found" 日志，减少了非必要日志输出。

### PR #140585: [release-1.35] Bump images and versions to golang 1.25.12 and update distroless-iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/140585
- **状态：** closed
- **已合并：** 是
- **作者：** palnabarun
- **标签：** area/test, lgtm, release-note, size/S, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, needs-priority, needs-triage
- **变更说明：**
  更新 Kubernetes 构建的基础镜像和工具链版本。将 Go 语言版本升级至 1.25.12，并更新 distroless-iptables 镜像，属于常规的安全与稳定性更新。

---
*本报告由 Containerd Release Tracker 自动生成*
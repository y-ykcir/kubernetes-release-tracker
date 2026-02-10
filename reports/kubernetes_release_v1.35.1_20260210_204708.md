# Kubernetes 版本发布分析报告
## v1.35.1 (v1.35.1)

### 📋 版本信息
- **版本标签：** v1.35.1
- **版本名称：** v1.35.1
- **发布时间：** 2026-02-10T19:03:38Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.1

### 🔍 分析统计
- **分析时间：** 2026-02-10 20:47:08
- **分析的 PR 数量：** 16
- **分析的 Issue 数量：** 1
- **重要项目数量：** 17

## 📊 版本概述
Kubernetes v1.35.1 是一个紧急补丁版本，主要修复了 v1.35.0 中引入的调度器性能严重回退、kube-proxy 同步回归等关键问题，并包含了 Go 语言安全更新。

## 🔒 安全问题修复
1. ⚠️ 升级至 Go 1.25.6，修复 Go 标准库中的多个 CVE 漏洞 - [PR #136258](https://github.com/kubernetes/kubernetes/pull/136258) - **风险级别：** 中（取决于具体 CVE 利用条件）
2. ⚠️ 更新构建镜像和基础组件至包含安全修复的版本 - [PR #136466](https://github.com/kubernetes/kubernetes/pull/136466) - **风险级别：** 低

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kubelet 中错误使用 `V().Error()` 导致的日志泛滥问题 - [PR #136432](https://github.com/kubernetes/kubernetes/pull/136432) - **影响：** 错误日志无视 Verbosity 级别始终打印，干扰监控和排错
2. 修复 `kubectl exec` 中终端大小队列未初始化导致的 Panic - [PR #136280](https://github.com/kubernetes/kubernetes/pull/136280) - **影响：** 特定条件下 `kubectl exec` 命令会崩溃
3. 修复 kubeadm 升级时因 `kubeadm-flags.env` 文件内容为空导致的失败 - [PR #136131](https://github.com/kubernetes/kubernetes/pull/136131) - **影响：** 特定配置下 kubeadm 集群升级流程会中断
4. 修复 kubeadm 在 `kubeadm join` 时未等待 etcd learner 成员启动就尝试提升其状态的问题 - [PR #136348](https://github.com/kubernetes/kubernetes/pull/136348) - **影响：** 可能影响 etcd 集群的稳定性和数据一致性
5. 修复 SELinux 警告控制器对已完成 Pod 发出不必要事件的问题 - [PR #136098](https://github.com/kubernetes/kubernetes/pull/136098) - **影响：** 产生无关的警告事件，干扰事件流

## 💥 破坏性变更
1. 🚨 无新增的破坏性变更。此版本主要目的是修复 v1.35.0 中的回归问题。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 紧急禁用导致性能问题的 `SchedulerAsyncAPICalls` 特性门控 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904)
2. 修复 kube-proxy (ipvs/winkernel) 因同步逻辑变更导致的网络规则更新延迟回归 - [PR #136122](https://github.com/kubernetes/kubernetes/pull/136122)
3. 将核心组件构建版本升级至 Go 1.25.6，以修复相关 CVE 漏洞 - [PR #136258](https://github.com/kubernetes/kubernetes/pull/136258) 和 [PR #136466](https://github.com/kubernetes/kubernetes/pull/136466)
4. 修复 StatefulSet 中 `.status.availableReplicas` 计数延迟，加速滚动更新 - [PR #136097](https://github.com/kubernetes/kubernetes/pull/136097)
5. 修复 Windows kube-proxy (winkernel) 中双栈 Service 的负载均衡器共享问题 - [PR #136373](https://github.com/kubernetes/kubernetes/pull/136373)

## 🚀 性能优化
1. 禁用 `SchedulerAsyncAPICalls` 特性门控，解决因 API 客户端限流导致的调度性能严重下降 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904) - **提升：** 恢复 v1.35.0 之前的调度器性能基线
2. 修复 kubelet 错误日志级别，避免日志泛滥对系统 I/O 和日志收集系统造成不必要的压力 - [PR #136432](https://github.com/kubernetes/kubernetes/pull/136432) - **提升：** 减少无关日志输出，提升日志系统效率

## 🎯 风险评估
整体风险评估：**低风险，建议立即升级**。此版本是典型的补丁版本，旨在修复前一个版本（v1.35.0）中引入的严重回归问题，尤其是影响核心组件（调度器、kube-proxy）稳定性和性能的缺陷。升级风险较低，收益（稳定性、安全性修复）显著高于风险。建议的升级时机是尽快在测试环境中验证后，安排生产环境升级。需要特别关注升级后调度性能和网络服务的稳定性是否恢复正常。

## 📋 升级建议
1. **强烈建议所有正在运行或计划升级到 v1.35.0 的集群立即升级到 v1.35.1**，以解决调度器性能回退和 kube-proxy 网络同步问题。
2. 升级前，请确认集群中未显式启用 `SchedulerAsyncAPICalls` 特性门控（该门控在此版本中已被强制禁用）。
3. 对于 Windows 节点集群，此版本修复了双栈 Service 的关键问题，建议优先安排升级。
4. 升级后，观察调度器指标（如调度延迟）和 kube-proxy 日志，确认性能回归问题已解决。
5. 由于包含了 Go 语言安全更新，建议将此版本视为一次重要的安全维护升级。

## 📋 Release 包含的变更

### PR #135815: Automated cherry pick of #135367: Fix apiserver_watch_events_sizes metric.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135815
- **状态：** closed
- **已合并：** 是
- **作者：** mborsz
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复了 apiserver_watch_events_sizes 指标在 1.29 版本中的回归问题，使其能够再次正确报告总的传出 watch 流量。

### PR #135843: Automated cherry pick of #135748: Update vendored hnslib to v0.1.2
- **链接：** https://github.com/kubernetes/kubernetes/pull/135843
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, kind/cleanup, lgtm, release-note, size/M, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  更新了 Windows 网络依赖库 hnslib 至 v0.1.2：移除了已弃用的 github.com/pkg/errors 依赖，并支持最新的 HNS API，包括 ModifyLoadBalancerPolicy 以更新现有负载均衡策略。

### PR #135853: Automated cherry pick of #135400: kubeadm: do not sort extraArgs alpha-numerically
- **链接：** https://github.com/kubernetes/kubernetes/pull/135853
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 kubeadm 处理用户提供的 extraArgs 覆盖时的排序问题：现在仅对默认参数列表进行排序，而保持用户覆盖的参数列表顺序不变，以确保如 --service-account-issuer 等顺序敏感的标志正常工作。

### PR #135904: Automated cherry pick of #135903: Disable SchedulerAsyncAPICalls feature gate due to performance issues
- **链接：** https://github.com/kubernetes/kubernetes/pull/135904
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/XS, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, kind/regression, needs-triage
- **变更说明：**
  由于性能问题（由 API 客户端限流触发），禁用了 SchedulerAsyncAPICalls 特性门控，以修复 1.35.0 版本中的调度器性能回归。

### PR #136072: Automated cherry pick of #135776: kubeadm: always retry Patch() Node API calls
- **链接：** https://github.com/kubernetes/kubernetes/pull/136072
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, kind/feature, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm 在 Patch() Node API 调用时的错误处理逻辑：对于未知（非允许列表）的 API 错误，不再提前退出，而是在获取和修补 Node 对象的轮询持续时间内始终进行重试。

### PR #136097: Automated cherry pick of #135428: schedule pod availability checks at the correct time in StatefulSets
- **链接：** https://github.com/kubernetes/kubernetes/pull/136097
- **状态：** closed
- **已合并：** 是
- **作者：** atiratree
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 StatefulSet 中 Pod 可用性检查的调度时机，确保 .status.availableReplicas 能够被及时计数，从而加速 StatefulSet 的滚动更新进度。

### PR #136098: Automated cherry pick of #135629: selinux: Fix the controller to ignore finished pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/136098
- **状态：** closed
- **已合并：** 是
- **作者：** jsafrane
- **标签：** kind/bug, area/test, lgtm, sig/storage, release-note, size/XL, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复了 SELinux 告警控制器，使其忽略已完成的 Pod，避免为这些 Pod 发出不必要的事件。

### PR #136122: Automated cherry pick of #135631: Switch ipvs and winkernel back to more regular forced syncs
- **链接：** https://github.com/kubernetes/kubernetes/pull/136122
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, priority/important-soon, sig/network, area/kube-proxy, lgtm, release-note, size/XS, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, sig/testing, area/ipvs, triage/accepted
- **变更说明：**
  修复了 ipvs 和 winkernel kube-proxy 后端在 1.34+ 版本中的回归问题，将其强制同步行为恢复至 1.34 之前的模式，即定期重新检查所有规则，即使 Service 或 EndpointSlice 未发生变化。

### PR #136131: Automated cherry pick of #136127: kubeadm: fix a bug where kubeadm upgrade is failed if the content of the `kubeadm-flags.env` file is `KUBELET_KUBEADM_ARGS=""`
- **链接：** https://github.com/kubernetes/kubernetes/pull/136131
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/S, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复了 kubeadm upgrade 的一个 bug：当 /etc/default/kubeadm 或 /var/lib/kubelet/kubeadm-flags.env 文件内容为 KUBELET_KUBEADM_ARGS="" 时，升级过程会失败。

### PR #136258: update core binaries to go 1.25.6 for CVE fixes
- **链接：** https://github.com/kubernetes/kubernetes/pull/136258
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** lgtm, release-note, size/XS, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  将核心二进制文件更新至 Go 1.25.6 版本，以修复相关的 CVE 安全漏洞。

### PR #136280: Automated cherry pick of #135918: kubectl: Fix panic in exec terminal size queue
- **链接：** https://github.com/kubernetes/kubernetes/pull/136280
- **状态：** closed
- **已合并：** 是
- **作者：** seekskyworld
- **标签：** kind/bug, priority/backlog, area/kubectl, lgtm, release-note, size/XS, cherry-pick-approved, approved, sig/cli, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  修复了 kubectl exec 命令中终端大小队列委托未初始化时可能引发的 panic 问题。

### PR #136348: Automated cherry pick of #136014: kubeadm: waiting for etcd learner member to be started before promoting during 'kubeadm join'
- **链接：** https://github.com/kubernetes/kubernetes/pull/136348
- **状态：** closed
- **已合并：** 是
- **作者：** dlipovetsky
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复了 kubeadm join 过程中的一个 bug，现在会在提升 etcd learner 成员之前等待其完全启动，确保集群成员正确加入。

### PR #136373: Automated cherry pick of #136241: Fix for preferred dualstack and required dualstack in winkernel proxier.
- **链接：** https://github.com/kubernetes/kubernetes/pull/136373
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/L, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了 Windows kube-proxy (winkernel) 中 IPv4 和 IPv6 Service 负载均衡器可能被错误共享的问题。现在按 IP 家族独立跟踪负载均衡器，从而正确支持 PreferDualStack 和 RequireDualStack 类型的 Service。

### PR #136432: [release-1.35] fix(kubelet): convert V().Error() to V().Info() for verbosity-aware logging
- **链接：** https://github.com/kubernetes/kubernetes/pull/136432
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, triage/accepted, wg/device-management
- **变更说明：**
  PR #136432 是针对 release-1.35 的 cherry-pick，修复 kubelet 包中 logger.V(N).Error() 的错误用法。由于 go-logr 包设计问题，Error() 调用会绕过 verbosity 级别检查，导致日志总是打印。解决方案是将这些调用改为 V().Info()，以确保 verbosity-aware logging 正常工作。修改涉及 13 个文件的 21 个实例。

### PR #136466: [release-1.35] [go] Bump images and versions to go 1.25.6 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/136466
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/critical-urgent, lgtm, release-note, size/M, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将 Kubernetes 构建环境升级至 Go 1.25.6 并更新 distroless iptables 镜像，以获取安全修复和更新。

### PR #136634: Automated cherry pick of #136529: test: Read /proc/net/nf_conntrack instead of using conntrack binary
#136554: test: Fix KubeProxy CLOSE_WAIT test for IPv6 environments (and where /proc/net/nf_conntrack may be missing)
- **链接：** https://github.com/kubernetes/kubernetes/pull/136634
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** area/test, priority/critical-urgent, sig/network, kind/cleanup, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  改进了 KubeProxy 测试：将 conntrack 测试从依赖 conntrack 二进制工具改为直接读取 /proc/net/nf_conntrack 文件，并修复了在 IPv6 环境或缺少该文件时的测试问题。无用户可见变更。

---
*本报告由 Containerd Release Tracker 自动生成*
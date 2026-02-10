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
- **分析时间：** 2026-02-10 20:47:11
- **分析的 PR 数量：** 16
- **分析的 Issue 数量：** 1
- **重要项目数量：** 17

## 📊 版本概述
Kubernetes v1.35.1 是一个关键的补丁版本，主要修复了 v1.35.0 中引入的调度器性能回归、kube-proxy 网络同步问题，并包含了重要的 Go 语言安全更新。

## 🔒 安全问题修复
1. ⚠️ Go 语言 CVE 修复：升级至 Go 1.25.6 以修复该版本中包含的安全漏洞 - [PR #136258](https://github.com/kubernetes/kubernetes/pull/136258) - **风险级别：** 中（取决于具体 CVE 的利用条件和影响范围）

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kubeadm 升级失败：当 `kubeadm-flags.env` 文件内容为 `KUBELET_KUBEADM_ARGS=""` 时，`kubeadm upgrade` 会失败 - [PR #136131](https://github.com/kubernetes/kubernetes/pull/136131) - **影响：** 使用 kubeadm 且环境变量文件内容为空的集群将无法正常升级
2. 修复 StatefulSet 副本计数延迟：确保 `status.availableReplicas` 在正确时间点被统计，加快 StatefulSet 滚动更新速度 - [PR #136097](https://github.com/kubernetes/kubernetes/pull/136097) - **影响：** StatefulSet 的滚动更新进度可能比预期慢
3. 修复 kubectl exec panic：解决终端大小队列委托未初始化时导致的 panic - [PR #136280](https://github.com/kubernetes/kubernetes/pull/136280) - **影响：** 在某些条件下使用 `kubectl exec` 可能导致客户端崩溃
4. 修复 kubeadm etcd learner 成员提升：在 `kubeadm join` 过程中，等待 etcd learner 成员启动后再进行提升 - [PR #136348](https://github.com/kubernetes/kubernetes/pull/136348) - **影响：** 使用 etcd learner 功能的 kubeadm 集群在加入新节点时可能遇到问题
5. 修复 apiserver watch 事件大小指标：修复 v1.29 引入的回归问题，使 `apiserver_watch_events_sizes` 指标重新报告总传出 watch 流量 - [PR #135815](https://github.com/kubernetes/kubernetes/pull/135815) - **影响：** 监控该指标的告警或仪表板可能数据不准确

## 💥 破坏性变更
1. 🚨 禁用 SchedulerAsyncAPICalls 特性门控：该特性在 v1.35.0 默认启用，但因性能问题在 v1.35.1 被强制禁用。 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904) - **影响：** 依赖此特性进行异步调用的自定义调度器插件或配置需要调整。对于大多数用户，这是自动修复，无需操作。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复调度器性能回归：禁用 `SchedulerAsyncAPICalls` 特性门控以解决 API 客户端限流导致的性能问题 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904)
2. 修复 kube-proxy 同步回归：将 IPVS 和 Windows kernel 代理模式恢复为定期强制同步规则，解决服务发现潜在问题 - [PR #136122](https://github.com/kubernetes/kubernetes/pull/136122)
3. 安全基础更新：将核心组件构建的 Go 语言版本升级至 1.25.6，修复相关 CVE 漏洞 - [PR #136258](https://github.com/kubernetes/kubernetes/pull/136258) / [PR #136466](https://github.com/kubernetes/kubernetes/pull/136466)
4. 修复 Windows kube-proxy 双栈服务：解决 winkernel 代理中 IPv4/IPv6 负载均衡器错误共享的问题，正确支持 `PreferDualStack` 和 `RequireDualStack` 服务 - [PR #136373](https://github.com/kubernetes/kubernetes/pull/136373)

## 🚀 性能优化
1. 修复调度器性能回归：禁用有问题的特性门控，恢复调度器在 v1.35.0 之前的性能水平 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904) - **提升：** 解决因 API 限流导致的调度延迟增加和吞吐量下降问题
2. 修复 kubelet 错误日志 verbosity：将 `logger.V(N).Error()` 调用改为 `logger.V(N).Info()`，避免错误日志绕过 verbosity 检查导致日志泛滥 - [PR #136432](https://github.com/kubernetes/kubernetes/pull/136432) - **提升：** 减少不必要的磁盘 I/O 和日志存储压力，提升日志可读性

## 🎯 风险评估
整体风险评估：**低风险**。此版本主要为修复 v1.35.0 的回归性错误和安全补丁，不引入新的破坏性 API 变更。
建议的升级时机：**尽快安排**，特别是对于已运行 v1.35.0 且受到性能问题影响的集群。
需要特别关注的方面：1) 调度器性能是否恢复；2) Service 网络（特别是 IPVS/Windows 环境）的稳定性；3) kubeadm 升级流程（如果使用相关功能）。

## 📋 升级建议
1. **强烈建议升级**：如果您已升级到 v1.35.0，应尽快安排升级到 v1.35.1，以解决调度器性能下降和 kube-proxy 网络同步问题。
2. **升级前验证**：在测试环境中验证调度器性能（如 Pod 启动时间）和 Service 网络连通性是否恢复正常。
3. **关注 Windows 集群**：Windows 节点用户应特别关注此版本，它修复了 winkernel 代理的双栈服务关键问题。
4. **kubeadm 用户注意**：检查您的 `kubeadm-flags.env` 文件，如果内容为空，升级前请参考 PR #136131 的描述。
5. **监控调整**：升级后，验证 `apiserver_watch_events_sizes` 等监控指标是否恢复正常数据上报。

## 📋 Release 包含的变更

### PR #135815: Automated cherry pick of #135367: Fix apiserver_watch_events_sizes metric.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135815
- **状态：** closed
- **已合并：** 是
- **作者：** mborsz
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复了 apiserver_watch_events_sizes 指标在 1.29 版本中的回归问题，使其能够重新正确报告总的出站 watch 流量。

### PR #135843: Automated cherry pick of #135748: Update vendored hnslib to v0.1.2
- **链接：** https://github.com/kubernetes/kubernetes/pull/135843
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, kind/cleanup, lgtm, release-note, size/M, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  更新了 Windows 网络依赖库 hnslib 至 v0.1.2，移除了已弃用的 `github.com/pkg/errors` 库，并增加了对最新 HNS API（如 ModifyLoadBalancerPolicy）的支持。

### PR #135853: Automated cherry pick of #135400: kubeadm: do not sort extraArgs alpha-numerically
- **链接：** https://github.com/kubernetes/kubernetes/pull/135853
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 kubeadm 在处理用户提供的 `extraArgs` 参数时，会对其进行字母数字排序的问题。现在仅对默认参数排序，保持用户覆盖参数的原始顺序，确保如 `--service-account-issuer` 等顺序敏感的标记正常工作。

### PR #135904: Automated cherry pick of #135903: Disable SchedulerAsyncAPICalls feature gate due to performance issues
- **链接：** https://github.com/kubernetes/kubernetes/pull/135904
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/XS, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, kind/regression, needs-triage
- **变更说明：**
  由于性能问题（由 API 客户端限流触发），禁用了 `SchedulerAsyncAPICalls` 特性门控，以修复 1.35.0 版本中的调度器性能回归。

### PR #136072: Automated cherry pick of #135776: kubeadm: always retry Patch() Node API calls
- **链接：** https://github.com/kubernetes/kubernetes/pull/136072
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, kind/feature, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm 在 Patch Node 对象时，遇到未知（非允许列表）API 错误会提前退出的问题。现在会在整个轮询期间持续重试，提高了节点操作的健壮性。

### PR #136097: Automated cherry pick of #135428: schedule pod availability checks at the correct time in StatefulSets
- **链接：** https://github.com/kubernetes/kubernetes/pull/136097
- **状态：** closed
- **已合并：** 是
- **作者：** atiratree
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 StatefulSet 中 Pod 可用性检查的调度时机，确保 `.status.availableReplicas` 能够被及时更新，从而加快 StatefulSet 的滚动更新速度。

### PR #136098: Automated cherry pick of #135629: selinux: Fix the controller to ignore finished pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/136098
- **状态：** closed
- **已合并：** 是
- **作者：** jsafrane
- **标签：** kind/bug, area/test, lgtm, sig/storage, release-note, size/XL, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复了 SELinux 警告控制器，使其不再为已完成的 Pod 发出事件，减少了不必要的警告噪音。

### PR #136122: Automated cherry pick of #135631: Switch ipvs and winkernel back to more regular forced syncs
- **链接：** https://github.com/kubernetes/kubernetes/pull/136122
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, priority/important-soon, sig/network, area/kube-proxy, lgtm, release-note, size/XS, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, sig/testing, area/ipvs, triage/accepted
- **变更说明：**
  修复了 1.34+ 版本中 ipvs 和 winkernel kube-proxy 后端的回归问题，将其强制同步行为恢复为 1.34 之前的状态，即定期重新检查所有规则，即使 Service 或 EndpointSlice 未发生变化。

### PR #136131: Automated cherry pick of #136127: kubeadm: fix a bug where kubeadm upgrade is failed if the content of the `kubeadm-flags.env` file is `KUBELET_KUBEADM_ARGS=""`
- **链接：** https://github.com/kubernetes/kubernetes/pull/136131
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/S, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复了当 `kubeadm-flags.env` 文件内容为 `KUBELET_KUBEADM_ARGS=""`（空字符串）时，`kubeadm upgrade` 会失败的 bug。

### PR #136258: update core binaries to go 1.25.6 for CVE fixes
- **链接：** https://github.com/kubernetes/kubernetes/pull/136258
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** lgtm, release-note, size/XS, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  **PR #136258:** update core binaries to go 1.25.6 for CVE fixes
**标签:** lgtm, release-note, size/XS, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributor guidelines: https://git.k8s.io/c...

### PR #136280: Automated cherry pick of #135918: kubectl: Fix panic in exec terminal size queue
- **链接：** https://github.com/kubernetes/kubernetes/pull/136280
- **状态：** closed
- **已合并：** 是
- **作者：** seekskyworld
- **标签：** kind/bug, priority/backlog, area/kubectl, lgtm, release-note, size/XS, cherry-pick-approved, approved, sig/cli, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  修复了 `kubectl exec` 命令中，当终端大小队列委托未初始化时可能发生的 panic 问题。

### PR #136348: Automated cherry pick of #136014: kubeadm: waiting for etcd learner member to be started before promoting during 'kubeadm join'
- **链接：** https://github.com/kubernetes/kubernetes/pull/136348
- **状态：** closed
- **已合并：** 是
- **作者：** dlipovetsky
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复了在 `kubeadm join` 过程中，需要等待 etcd learner 成员启动完成后再将其提升为正式成员的问题，以确保数据一致性。

### PR #136373: Automated cherry pick of #136241: Fix for preferred dualstack and required dualstack in winkernel proxier.
- **链接：** https://github.com/kubernetes/kubernetes/pull/136373
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/L, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了 Windows kube-proxy (winkernel) 中 IPv4 和 IPv6 负载均衡器可能被错误共享的问题。现在按 IP 族独立跟踪负载均衡器，从而正确支持 Windows 节点上的 PreferDualStack 和 RequireDualStack Service。

### PR #136432: [release-1.35] fix(kubelet): convert V().Error() to V().Info() for verbosity-aware logging
- **链接：** https://github.com/kubernetes/kubernetes/pull/136432
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, triage/accepted, wg/device-management
- **变更说明：**
  PR #136432 是针对 release-1.35 分支的 cherry-pick，修复了 kubelet 包中错误使用 logger.V(N).Error() 的问题。由于 go-logr 包的设计缺陷，Error() 调用会完全绕过 verbosity 级别检查，导致日志始终被打印。解决方案是将这些调用统一转换为 V().Info()，以确保日志输出遵循 verbosity 设置。影响范围涉及 kubelet 的多个组件，包括 allocation_manager、devicemanager 等，共修改 13 个文件中的 21 处实例。

### PR #136466: [release-1.35] [go] Bump images and versions to go 1.25.6 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/136466
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/critical-urgent, lgtm, release-note, size/M, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将构建镜像和版本升级至 Go 1.25.6 和 distroless iptables。这是常规的依赖更新和安全修复。

### PR #136634: Automated cherry pick of #136529: test: Read /proc/net/nf_conntrack instead of using conntrack binary
#136554: test: Fix KubeProxy CLOSE_WAIT test for IPv6 environments (and where /proc/net/nf_conntrack may be missing)
- **链接：** https://github.com/kubernetes/kubernetes/pull/136634
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** area/test, priority/critical-urgent, sig/network, kind/cleanup, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  改进了 KubeProxy 测试，从依赖 `conntrack` 二进制文件改为直接读取 `/proc/net/nf_conntrack`，并修复了在 IPv6 环境或该文件缺失情况下的测试问题。

---
*本报告由 Containerd Release Tracker 自动生成*
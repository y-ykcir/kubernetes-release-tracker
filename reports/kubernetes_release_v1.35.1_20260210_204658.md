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
- **分析时间：** 2026-02-10 20:46:58
- **分析的 PR 数量：** 16
- **分析的 Issue 数量：** 1
- **重要项目数量：** 17

## 📊 版本概述
Kubernetes v1.35.1 是一个关键的补丁版本，主要修复了 v1.35.0 中引入的调度器性能严重回归、kube-proxy 网络问题以及多个 kubeadm 和日志相关的 Bug，建议所有 v1.35.0 用户尽快升级。

## 🔒 安全问题修复
1. ⚠️ 更新至 Go 1.25.6，修复多个 CVE - [PR #136258](https://github.com/kubernetes/kubernetes/pull/136258) - **风险级别：** 中 - 建议升级以获取最新的安全补丁。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复调度器性能回归：`SchedulerAsyncAPICalls` 特性门禁因导致 API 客户端限流而被禁用 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904) - **影响：** 在 v1.35.0 中启用此特性会导致调度延迟显著增加，影响 Pod 启动速度。
2. 修复 kube-proxy 网络回归：ipvs 和 winkernel 模式恢复定期强制同步规则的行为 - [PR #136122](https://github.com/kubernetes/kubernetes/pull/136122) - **影响：** v1.34+ 中，某些情况下 Service/EndpointSlice 变更可能无法及时生效，导致网络流量中断或路由错误。
3. 修复 StatefulSet 可用副本数检查延迟问题 - [PR #136097](https://github.com/kubernetes/kubernetes/pull/136097) - **影响：** StatefulSet 滚动更新或扩容时，`.status.availableReplicas` 更新延迟，影响 HPA 和就绪判断。
4. 修复 kubeadm 升级失败：当 `kubeadm-flags.env` 文件内容为 `KUBELET_KUBEADM_ARGS=""` 时 - [PR #136131](https://github.com/kubernetes/kubernetes/pull/136131) - **影响：** 特定配置下 `kubeadm upgrade` 命令会失败，阻碍集群升级流程。
5. 修复 kubectl exec 终端大小队列未初始化导致的 panic - [PR #136280](https://github.com/kubernetes/kubernetes/pull/136280) - **影响：** 执行 `kubectl exec` 时可能引发客户端崩溃。
6. 修复 SELinux 警告控制器对已完成 Pod 发出不必要事件的问题 - [PR #136098](https://github.com/kubernetes/kubernetes/pull/136098) - **影响：** 产生大量无关事件，干扰事件监控。

## 💥 破坏性变更
1. 🚨 `SchedulerAsyncAPICalls` 特性门禁被默认禁用 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904) - **影响：** 在 v1.35.0 中手动启用此特性以期望获得性能提升的用户，升级后该特性将失效。无需迁移动作，但需注意性能预期变化。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 紧急修复调度器性能回归，禁用 `SchedulerAsyncAPICalls` 特性门禁 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904)
2. 修复 kube-proxy (ipvs/winkernel) 因减少强制同步导致的网络规则更新延迟回归 - [PR #136122](https://github.com/kubernetes/kubernetes/pull/136122)
3. 修复 kubelet 错误使用 `V().Error()` 导致日志洪泛的问题 - [PR #136432](https://github.com/kubernetes/kubernetes/pull/136432) - [Issue #136027](https://github.com/kubernetes/kubernetes/issues/136027)
4. 修复 Windows kube-proxy (winkernel) 中双栈服务的负载均衡器共享问题 - [PR #136373](https://github.com/kubernetes/kubernetes/pull/136373)
5. 更新基础镜像至 Go 1.25.6，修复多个 CVE - [PR #136258](https://github.com/kubernetes/kubernetes/pull/136258) / [PR #136466](https://github.com/kubernetes/kubernetes/pull/136466)

## 🚀 性能优化
1. 修复调度器性能回归，避免因 `SchedulerAsyncAPICalls` 特性导致的 API 限流 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904) - **提升：** 恢复 v1.35.0 之前的调度性能，避免 Pod 调度延迟。
2. 修复 kube-proxy ipvs/winkernel 模式规则同步逻辑，确保网络变更及时生效 - [PR #136122](https://github.com/kubernetes/kubernetes/pull/136122) - **提升：** 避免因规则未同步导致的服务中断风险。

## 🎯 风险评估
整体风险评估：**低风险，高收益**。此版本主要为修复 v1.35.0 的严重回归问题，不包含引入新功能的重大变更。升级风险较低，但能显著提升集群的稳定性和性能。建议的升级时机：**尽快安排**，特别是受调度器性能问题影响的集群。需要特别关注的方面：升级后监控调度延迟和网络服务的连通性。

## 📋 升级建议
1. **强烈建议**所有正在运行 Kubernetes v1.35.0 的集群立即计划升级到 v1.35.1，以解决调度器性能严重回归和 kube-proxy 网络问题。
2. 如果使用 kubeadm，请确保在升级前检查所有节点上的 `kubeadm-flags.env` 文件，避免因空参数导致升级失败。
3. 对于 Windows 节点集群，此版本修复了双栈服务的关键问题，建议优先安排升级。
4. 升级后，观察调度器指标（如 `scheduler_pod_scheduling_duration_seconds`）和 kube-proxy 日志，确认性能回归和网络同步问题已解决。
5. 由于修复了 kubelet 日志级别错误，升级后相关组件的日志输出量可能会恢复正常，有助于故障排查。

## 📋 Release 包含的变更

### PR #135815: Automated cherry pick of #135367: Fix apiserver_watch_events_sizes metric.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135815
- **状态：** closed
- **已合并：** 是
- **作者：** mborsz
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复了 apiserver_watch_events_sizes 指标在 1.29 版本中的回归问题，使其能够再次正确报告总的出站 watch 流量。

### PR #135843: Automated cherry pick of #135748: Update vendored hnslib to v0.1.2
- **链接：** https://github.com/kubernetes/kubernetes/pull/135843
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, kind/cleanup, lgtm, release-note, size/M, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  更新了 Windows 网络依赖库 hnslib 至 v0.1.2，移除了已弃用的 `github.com/pkg/errors` 依赖，并增加了对 `ModifyLoadBalancerPolicy` HNS API 的支持，优化了负载均衡器策略更新流程。

### PR #135853: Automated cherry pick of #135400: kubeadm: do not sort extraArgs alpha-numerically
- **链接：** https://github.com/kubernetes/kubernetes/pull/135853
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 kubeadm 在合并用户提供的 `extraArgs` 覆盖参数时，对最终参数列表进行字母数字排序的问题。现在保持覆盖参数的原始顺序，确保了对参数顺序敏感的标志（如 `--service-account-issuer`）能够正常工作。

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
  修复了 kubeadm 在 patch Node 对象时，遇到非预期的 API 错误会过早退出的问题。现在会在整个轮询持续时间内始终重试，提高了操作的健壮性。

### PR #136097: Automated cherry pick of #135428: schedule pod availability checks at the correct time in StatefulSets
- **链接：** https://github.com/kubernetes/kubernetes/pull/136097
- **状态：** closed
- **已合并：** 是
- **作者：** atiratree
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 StatefulSet 控制器中 Pod 可用性检查的调度时机问题，确保 `.status.availableReplicas` 能被及时更新，从而加速 StatefulSet 的滚动更新进度。

### PR #136098: Automated cherry pick of #135629: selinux: Fix the controller to ignore finished pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/136098
- **状态：** closed
- **已合并：** 是
- **作者：** jsafrane
- **标签：** kind/bug, area/test, lgtm, sig/storage, release-note, size/XL, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复了 SELinux 告警控制器，使其不再为已完成的 Pod 发送事件，减少了不必要的告警噪音。

### PR #136122: Automated cherry pick of #135631: Switch ipvs and winkernel back to more regular forced syncs
- **链接：** https://github.com/kubernetes/kubernetes/pull/136122
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, priority/important-soon, sig/network, area/kube-proxy, lgtm, release-note, size/XS, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, sig/testing, area/ipvs, triage/accepted
- **变更说明：**
  修复了 1.34+ 版本中 ipvs 和 winkernel 模式 kube-proxy 的一个回归问题，将其强制同步规则的行为恢复至 1.34 之前的状态，即定期重新检查所有规则，即使 Service 或 EndpointSlice 未发生变化。

### PR #136131: Automated cherry pick of #136127: kubeadm: fix a bug where kubeadm upgrade is failed if the content of the `kubeadm-flags.env` file is `KUBELET_KUBEADM_ARGS=""`
- **链接：** https://github.com/kubernetes/kubernetes/pull/136131
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/S, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复了 kubeadm upgrade 的一个 bug：当 `/var/lib/kubelet/kubeadm-flags.env` 文件内容为 `KUBELET_KUBEADM_ARGS=""` 时，升级过程会失败。

### PR #136258: update core binaries to go 1.25.6 for CVE fixes
- **链接：** https://github.com/kubernetes/kubernetes/pull/136258
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** lgtm, release-note, size/XS, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  将核心二进制文件的构建版本更新至 Go 1.25.6，以修复相关的 CVE 安全漏洞。

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
  修复了 kubeadm join 过程中的一个 bug，确保在提升 etcd learner 成员之前，等待该成员完全启动，提高了集群加入过程的可靠性。

### PR #136373: Automated cherry pick of #136241: Fix for preferred dualstack and required dualstack in winkernel proxier.
- **链接：** https://github.com/kubernetes/kubernetes/pull/136373
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/L, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了 Windows kube-proxy (winkernel) 中 IPv4 和 IPv6 负载均衡器可能被错误共享的问题。现在按 IP 族跟踪负载均衡器，从而正确支持 Windows 节点上的 `PreferDualStack` 和 `RequireDualStack` 类型 Service。

### PR #136432: [release-1.35] fix(kubelet): convert V().Error() to V().Info() for verbosity-aware logging
- **链接：** https://github.com/kubernetes/kubernetes/pull/136432
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, triage/accepted, wg/device-management
- **变更说明：**
  修复kubelet包中日志verbosity问题：将`logger.V(N).Error()`改为`V().Info()`，避免go-logr包设计导致的verbosity级别检查绕过，确保日志按配置级别输出。针对release-1.35分支，手动cherry-pick自#136028，修改13个文件中的21处实例。

### PR #136466: [release-1.35] [go] Bump images and versions to go 1.25.6 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/136466
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/critical-urgent, lgtm, release-note, size/M, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将构建 Kubernetes 的 Go 版本升级至 1.25.6，并更新了相关的容器基础镜像，以获取安全修复和更新。

### PR #136634: Automated cherry pick of #136529: test: Read /proc/net/nf_conntrack instead of using conntrack binary
#136554: test: Fix KubeProxy CLOSE_WAIT test for IPv6 environments (and where /proc/net/nf_conntrack may be missing)
- **链接：** https://github.com/kubernetes/kubernetes/pull/136634
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** area/test, priority/critical-urgent, sig/network, kind/cleanup, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  合并了两个测试修复：将 KubeProxy 连接跟踪测试从依赖 `conntrack` 二进制改为读取 `/proc/net/nf_conntrack` 文件，并修复了该测试在 IPv6 环境或缺少该文件时的兼容性问题。

---
*本报告由 Containerd Release Tracker 自动生成*
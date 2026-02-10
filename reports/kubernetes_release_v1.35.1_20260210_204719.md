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
- **分析时间：** 2026-02-10 20:47:19
- **分析的 PR 数量：** 16
- **分析的 Issue 数量：** 1
- **重要项目数量：** 17

## 📊 版本概述
Kubernetes v1.35.1 是一个紧急补丁版本，主要修复了 v1.35.0 中引入的调度器性能回归、kube-proxy 网络同步问题、多个 kubeadm 缺陷以及关键的 Go 语言安全漏洞。

## 🔒 安全问题修复
1. ⚠️ 通过升级至 Go 1.25.6 修复多个 Go 语言运行时 CVE 漏洞 - [PR #136258](https://github.com/kubernetes/kubernetes/pull/136258) - **风险级别：** 中。具体 CVE 细节需参考 Go 1.25.6 发布说明，通常涉及 HTTP/2、TLS、archive/zip 等组件。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 apiserver 监控指标 `apiserver_watch_events_sizes` 在 1.29 版本后的回归，使其能正确报告 watch 流量 - [PR #135815](https://github.com/kubernetes/kubernetes/pull/135815) - **影响：** 监控仪表板中 watch 事件大小的数据可能在过去版本中缺失或不准。
2. 修复 StatefulSet 中 `.status.availableReplicas` 计数延迟的问题，加速滚动更新 - [PR #136097](https://github.com/kubernetes/kubernetes/pull/136097) - **影响：** 使用 StatefulSet 的应用，其滚动更新和就绪状态判断会更快、更准确。
3. 修复 kubeadm 升级时，当 `kubeadm-flags.env` 文件内容为空字符串导致的失败 - [PR #136131](https://github.com/kubernetes/kubernetes/pull/136131) - **影响：** 使用特定配置的 kubeadm 集群可能无法完成升级。
4. 修复 `kubectl exec` 中终端大小队列未初始化导致的 panic - [PR #136280](https://github.com/kubernetes/kubernetes/pull/136280) - **影响：** 在某些条件下执行 `kubectl exec` 可能导致客户端崩溃。
5. 修复 kubeadm 在 `join` 时，等待 etcd learner 成员启动的逻辑 - [PR #136348](https://github.com/kubernetes/kubernetes/pull/136348) - **影响：** 使用 etcd learner 的高可用 kubeadm 集群在添加节点时可能更稳定。
6. 修复 kubelet 中错误使用 `V().Error()` 导致的日志级别绕过问题 - [PR #136432](https://github.com/kubernetes/kubernetes/pull/136432) - **影响：** 高 verbosity 级别的错误日志会错误地打印出来，造成日志洪泛，干扰问题排查。

## 💥 破坏性变更
1. 🚨 `SchedulerAsyncAPICalls` 特性门控被强制禁用 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904) - **影响：** 任何显式启用此特性门控以测试异步 API 调用的配置将不再生效，回退到同步调用模式。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 紧急禁用 `SchedulerAsyncAPICalls` 特性门控以修复调度器性能回归 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904)
2. 修复 kube-proxy (ipvs/winkernel) 的规则同步回归，恢复至 1.34 之前的行为 - [PR #136122](https://github.com/kubernetes/kubernetes/pull/136122)
3. 修复 Windows kube-proxy 中双栈服务的负载均衡器共享问题 - [PR #136373](https://github.com/kubernetes/kubernetes/pull/136373)
4. 升级核心组件至 Go 1.25.6，修复多个 CVE 安全漏洞 - [PR #136258](https://github.com/kubernetes/kubernetes/pull/136258) / [PR #136466](https://github.com/kubernetes/kubernetes/pull/136466)

## 🚀 性能优化
1. 禁用 `SchedulerAsyncAPICalls` 特性门控，解决因 API 客户端限流导致的调度器性能下降 - [PR #135904](https://github.com/kubernetes/kubernetes/pull/135904) - **提升：** 恢复 v1.35.0 之前版本的调度性能，避免大规模集群调度延迟。
2. 修复 kubelet 错误日志级别问题，减少不必要的日志输出 - [PR #136432](https://github.com/kubernetes/kubernetes/pull/136432) - **提升：** 降低日志系统的 I/O 和存储压力，提升日志可读性。

## 🎯 风险评估
整体风险评估：**中等**。此版本主要为修复 v1.35.0 的严重回归问题，升级风险相对较低，收益显著。建议的升级时机：**尽快，尤其是在生产环境中已部署 v1.35.0 的集群**。需要特别关注的方面：1) 调度器性能是否恢复正常；2) 网络策略（特别是双栈和 Windows 环境）是否按预期工作；3) kubeadm 集群的升级流程。建议先在测试环境验证。

## 📋 升级建议
1. **强烈建议**所有运行 v1.35.0 的生产集群立即升级到 v1.35.1，以解决调度器性能回退和网络代理同步问题。
2. 如果使用 kubeadm，请确保在升级前检查 `kubeadm-flags.env` 文件内容，避免因空参数导致升级失败。
3. 对于 Windows 节点集群，此版本修复了重要的双栈服务支持问题，建议优先安排升级。
4. 升级后，监控调度延迟和 kube-proxy 的日志，确认性能回归和网络同步问题已解决。

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
  更新了 Windows 网络库 hnslib 至 v0.1.2，移除了已弃用的 `github.com/pkg/errors` 依赖，并增加了对最新 HNS API（如 `ModifyLoadBalancerPolicy`）的支持。

### PR #135853: Automated cherry pick of #135400: kubeadm: do not sort extraArgs alpha-numerically
- **链接：** https://github.com/kubernetes/kubernetes/pull/135853
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  kubeadm 在处理用户通过 `extraArgs` 提供的参数覆盖时，不再对最终参数列表进行字母数字排序，而是保持覆盖参数的原始顺序，以支持对顺序敏感的 flag（如 `--service-account-issuer`）。

### PR #135904: Automated cherry pick of #135903: Disable SchedulerAsyncAPICalls feature gate due to performance issues
- **链接：** https://github.com/kubernetes/kubernetes/pull/135904
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/XS, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, kind/regression, needs-triage
- **变更说明：**
  由于性能问题（由 API 客户端节流触发），禁用了 `SchedulerAsyncAPICalls` 特性门控，以修复 1.35.0 版本中的调度器性能回归。

### PR #136072: Automated cherry pick of #135776: kubeadm: always retry Patch() Node API calls
- **链接：** https://github.com/kubernetes/kubernetes/pull/136072
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, kind/feature, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubeadm 在修补 Node 对象时，不再因未知（非允许列表）API 错误而提前退出，而是在整个轮询期间始终进行重试，提高了操作的健壮性。

### PR #136097: Automated cherry pick of #135428: schedule pod availability checks at the correct time in StatefulSets
- **链接：** https://github.com/kubernetes/kubernetes/pull/136097
- **状态：** closed
- **已合并：** 是
- **作者：** atiratree
- **标签：** kind/bug, priority/important-soon, lgtm, release-note, size/L, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复了 StatefulSet 中 Pod 可用性检查的调度时机，确保 `.status.availableReplicas` 能够及时更新，从而加速 StatefulSet 的滚动更新过程。

### PR #136098: Automated cherry pick of #135629: selinux: Fix the controller to ignore finished pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/136098
- **状态：** closed
- **已合并：** 是
- **作者：** jsafrane
- **标签：** kind/bug, area/test, lgtm, sig/storage, release-note, size/XL, cherry-pick-approved, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复了 SELinux 警告控制器，使其不再为已完成的 Pod 发出事件，减少了不必要的通知。

### PR #136122: Automated cherry pick of #135631: Switch ipvs and winkernel back to more regular forced syncs
- **链接：** https://github.com/kubernetes/kubernetes/pull/136122
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** kind/bug, priority/important-soon, sig/network, area/kube-proxy, lgtm, release-note, size/XS, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, sig/testing, area/ipvs, triage/accepted
- **变更说明：**
  修复了 1.34+ 版本中 ipvs 和 winkernel kube-proxy 后端的回归问题，将其恢复为 1.34 之前的行为，即定期强制重新检查所有规则，即使 Service 或 EndpointSlice 未发生变化。

### PR #136131: Automated cherry pick of #136127: kubeadm: fix a bug where kubeadm upgrade is failed if the content of the `kubeadm-flags.env` file is `KUBELET_KUBEADM_ARGS=""`
- **链接：** https://github.com/kubernetes/kubernetes/pull/136131
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/S, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复了当 `kubeadm-flags.env` 文件内容为 `KUBELET_KUBEADM_ARGS=""`（空字符串）时，导致 `kubeadm upgrade` 失败的 bug。

### PR #136258: update core binaries to go 1.25.6 for CVE fixes
- **链接：** https://github.com/kubernetes/kubernetes/pull/136258
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** lgtm, release-note, size/XS, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/release, needs-priority, needs-triage
- **变更说明：**
  将核心二进制文件更新至 Go 1.25.6，以修复相关的 CVE 安全漏洞。

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
  在 `kubeadm join` 过程中，等待 etcd learner 成员启动完成后再将其提升为 voting member，以确保 etcd 集群的稳定性。

### PR #136373: Automated cherry pick of #136241: Fix for preferred dualstack and required dualstack in winkernel proxier.
- **链接：** https://github.com/kubernetes/kubernetes/pull/136373
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/L, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了 Windows kube-proxy (winkernel) 中 IPv4 和 IPv6 Service 负载均衡器可能被错误共享的问题，现在按 IP 系列跟踪负载均衡器，从而正确支持 `PreferDualStack` 和 `RequireDualStack` 类型的 Service。

### PR #136432: [release-1.35] fix(kubelet): convert V().Error() to V().Info() for verbosity-aware logging
- **链接：** https://github.com/kubernetes/kubernetes/pull/136432
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, triage/accepted, wg/device-management
- **变更说明：**
  此PR修复kubelet包中`logger.V(N).Error()`的错误使用。由于go-logr包设计，`Error()`调用会完全绕过verbosity级别检查，导致日志始终打印。解决方案是将这些调用转换为`V().Info()`，确保日志遵循配置的verbosity级别。这是针对release-1.35分支的cherry-pick，源自PR #136028，修改了13个文件中的21个实例。

### PR #136466: [release-1.35] [go] Bump images and versions to go 1.25.6 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/136466
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/critical-urgent, lgtm, release-note, size/M, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将构建镜像和版本升级至 Go 1.25.6 和 distroless iptables，属于常规的依赖项更新。

### PR #136634: Automated cherry pick of #136529: test: Read /proc/net/nf_conntrack instead of using conntrack binary
#136554: test: Fix KubeProxy CLOSE_WAIT test for IPv6 environments (and where /proc/net/nf_conntrack may be missing)
- **链接：** https://github.com/kubernetes/kubernetes/pull/136634
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** area/test, priority/critical-urgent, sig/network, kind/cleanup, lgtm, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  测试改进：将 KubeProxy 测试从依赖 `conntrack` 二进制改为读取 `/proc/net/nf_conntrack` 文件，并修复了在 IPv6 环境或该文件缺失情况下的测试问题。

---
*本报告由 Containerd Release Tracker 自动生成*
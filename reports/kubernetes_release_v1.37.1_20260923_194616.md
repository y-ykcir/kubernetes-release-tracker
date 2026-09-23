# Kubernetes 版本发布分析报告
## v1.37.1 (v1.37.1)

### 📋 版本信息
- **版本标签：** v1.37.1
- **版本名称：** v1.37.1
- **发布时间：** 2026-09-23T19:13:17Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.37.1

### 🔍 分析统计
- **分析时间：** 2026-09-23 19:46:16
- **分析的 PR 数量：** 6
- **分析的 Issue 数量：** 1
- **重要项目数量：** 7

## 📊 版本概述
Kubernetes v1.37.1 是一个补丁版本，主要修复了多个可能导致组件崩溃（panic）的关键Bug，并更新了基础组件版本以提升安全性，建议所有运行 v1.37 的用户升级以确保稳定性。

## 🔒 安全问题修复
1. ⚠️ 基础镜像和 Go 版本升级：此版本将构建环境升级至 Go 1.26.8，并使用了更新的 distroless iptables 镜像，通常包含上游的安全修复。 - [PR #142179](https://github.com/kubernetes/kubernetes/pull/142179) - **风险级别：** 低（预防性升级，未提及具体CVE）

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 Windows kube-proxy panic：当 Windows 主机网络服务（HNS）枚举到没有端口映射的负载均衡器时，kube-proxy 会 panic 并终止，导致节点网络功能中断。 - [PR #141681](https://github.com/kubernetes/kubernetes/pull/141681) - **影响：** 运行在 Windows 节点上的 kube-proxy 可能意外崩溃，影响 Service 的网络连通性。
2. 修复 DRA 整数溢出：在检查每个声明（claim）的设备限制时，对设备数量求和会发生整数溢出，可能导致调度器 panic 或分配错误数量的设备。 - [PR #141922](https://github.com/kubernetes/kubernetes/pull/141922) - **影响：** 使用 DRA 功能且申请大量设备（接近 int 最大值）的 Pod 可能触发此问题，导致 kube-scheduler 或 kubelet 不稳定。
3. 修复 DRA DeviceTaintSelector 逻辑：当 `DeviceTaintRule` 的 `spec.deviceSelector` 为 nil 时，错误地匹配了集群中的所有设备，导致所有 DRA 设备因污点而不可调度。 - [PR #141998](https://github.com/kubernetes/kubernetes/pull/141998) - **影响：** 使用 DRA 设备污点规则的集群，可能错误地隔离所有设备，导致 Pod 无法调度到预期设备上。
4. 修复 kubeadm 配置泄露：`kubeadm init` 时，节点特定的 systemd-resolved 解析器路径被错误地持久化到集群范围的 `kubelet-config` ConfigMap 中。 - [PR #141627](https://github.com/kubernetes/kubernetes/pull/141627) - **影响：** 使用不同解析器配置的节点可能从该 ConfigMap 获取到不正确的配置，影响 DNS 解析。

## 💥 破坏性变更
1. 🚨 无 API 变更、功能废弃或破坏性变更。此版本为纯 Bug 修复版本。
2. 🚨 DRA 行为修正：PR #141998 修复了 `DeviceTaintSelector` 的逻辑，从“匹配所有设备”改为“不匹配任何设备”。**影响：** 依赖 nil selector 来匹配所有设备的配置将失效，必须显式使用空选择器 `deviceSelector: {}`。需要检查并更新相关的 DRA DeviceClass 配置。 - [PR #141998](https://github.com/kubernetes/kubernetes/pull/141998)

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复 Windows kube-proxy 因 HNS 负载均衡器无端口映射而导致的 panic 崩溃 - [PR #141681](https://github.com/kubernetes/kubernetes/pull/141681)
2. 修复动态资源分配（DRA）中整数溢出导致的潜在 panic 和调度错误 - [PR #141922](https://github.com/kubernetes/kubernetes/pull/141922) / [Issue #141323](https://github.com/kubernetes/kubernetes/issues/141323)
3. 修复 DRA 中 DeviceTaintSelector 为 nil 时错误匹配所有设备的问题 - [PR #141998](https://github.com/kubernetes/kubernetes/pull/141998)
4. kubeadm 不再将节点特定的 systemd-resolved 路径泄露到集群范围的 ConfigMap 中 - [PR #141627](https://github.com/kubernetes/kubernetes/pull/141627)
5. 基础组件更新：构建版本升级至 Go 1.26.8 并使用 distroless iptables 镜像 - [PR #142179](https://github.com/kubernetes/kubernetes/pull/142179)

## 🚀 性能优化
1. Go 1.26.8 运行时：升级到 Go 1.26.8 可能包含语言运行时的性能改进和垃圾回收优化。 - [PR #142179](https://github.com/kubernetes/kubernetes/pull/142179) - **提升：** 间接提升，依赖于 Go 1.26.8 相对于之前小版本的改进。

## 🎯 风险评估
整体风险评估：**低风险**。这是一个专注于修复严重 Bug 和基础组件安全性的补丁版本，没有引入新的 API 或功能，升级中断风险较小。建议的升级时机：**尽快安排**，特别是受影响的 Windows 和 DRA 环境。需要特别关注的方面：检查 DRA 相关配置的兼容性，并确保 Windows 节点的网络功能在升级后正常。

## 📋 升级建议
1. **立即升级**：建议所有运行 Kubernetes v1.37.0 的生产环境尽快升级到 v1.37.1，特别是使用了 Windows 节点或 DRA 功能的集群，以修复可能导致核心组件崩溃的严重 Bug。
2. **DRA 配置检查**：如果使用了 DRA 的 DeviceTaintRule 且 `spec.deviceSelector` 为 nil，升级后此规则将失效。请将其修改为 `deviceSelector: {}` 以保持原“匹配所有设备”的意图。
3. **升级后验证**：升级后，重点验证 Windows 节点上 kube-proxy 的稳定性，以及使用 DRA 的 Pod 调度和设备分配是否正常。
4. **测试环境先行**：尽管是补丁版本，仍建议先在测试环境中进行升级验证。

## 📋 Release 包含的变更

### PR #141627: Automated cherry pick of #141337: Avoid leaking node-specific kubelet config into the ConfigMap
- **链接：** https://github.com/kubernetes/kubernetes/pull/141627
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, cherry-pick-approved, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  将主分支的 #141337 修复cherry-pick到release-1.37。修复了kubeadm的一个问题：在初始化期间，它会将节点特定的systemd-resolved解析配置文件（resolvConf）路径错误地持久化到集群范围的`kubelet-config` ConfigMap中。修复后，kubeadm不再将此类节点本地配置泄露到集群级配置中。

### PR #141681: Automated cherry pick of #141489: [kube-proxy/winkernel] Guard against load balancers without port mappings
- **链接：** https://github.com/kubernetes/kubernetes/pull/141681
- **状态：** closed
- **已合并：** 是
- **作者：** prince-melvin
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/M, cherry-pick-approved, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  将主分支的 #141489 修复cherry-pick到release-1.37。修复了Windows kube-proxy（winkernel）中的一个panic问题。当枚举到一个没有端口映射的HNS（Host Network Service）负载均衡器时，kube-proxy会崩溃。修复方法是为这种情况添加了防护检查，防止进程异常终止。

### PR #141780: Cherry pick of #141756: e2e auth: use unprivileged container port in projected podcertificate test
- **链接：** https://github.com/kubernetes/kubernetes/pull/141780
- **状态：** closed
- **已合并：** 是
- **作者：** yt2985
- **标签：** kind/bug, area/test, lgtm, release-note, size/S, cherry-pick-approved, sig/auth, approved, cncf-cla: yes, sig/testing, kind/failing-test, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  将主分支的 #141756 修复cherry-pick到release-1.37。调整了在1.37版本中添加的“Projected PodCertificate”端到端（e2e）一致性测试。将容器端口从特权端口（如443）更改为非特权端口，使该测试能够在非特权（例如，使用Rootless容器或特定安全策略）的环境中成功运行。

### PR #141922: Automated cherry pick of #141307: DRA: avoid integer overflow in per-claim device-limit checks
- **链接：** https://github.com/kubernetes/kubernetes/pull/141922
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将主分支的 #141307 修复cherry-pick到release-1.37。修复了DRA（设备资源分配）中每个声明（per-claim）设备数量检查的整数溢出漏洞。当两个`ExactCount`请求的设备数量之和（如`math.MaxInt/2 + 1`）导致原生`int`类型溢出为负数时，会绕过`> AllocationResultsMaxSize`检查，并导致后续分配结果切片大小错误。此漏洞影响所有分配器变体，且无需特性门控即可触发。

### PR #141998: Automated cherry pick of #141648: fix: make nil DeviceTaintSelector match no devices (tracker)
- **链接：** https://github.com/kubernetes/kubernetes/pull/141998
- **状态：** closed
- **已合并：** 是
- **作者：** marwan562
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将主分支的 #141648 修复cherry-pick到release-1.37。修复了DRA中`DeviceTaintRule`的一个bug：当`spec.deviceSelector`为`nil`时，规则会错误地匹配集群中的所有设备，导致所有DRA设备因`NoSchedule`或`NoExecute`污点而不可调度。修复后，`nil`选择器将正确匹配零个设备。如需匹配所有设备，需使用显式的空选择器（`deviceSelector: {}`）。

### PR #142179: [release-1.37] Bump images and versions to go 1.26.8 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/142179
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/critical-urgent, lgtm, release-note, size/S, kind/feature, area/release-eng, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将Kubernetes构建的Go版本升级至1.26.8，并更新了distroless iptables基础镜像版本。此PR属于常规的版本和安全更新，旨在将release-1.37分支的工具链和基础镜像同步到最新的稳定版本。

---
*本报告由 Containerd Release Tracker 自动生成*
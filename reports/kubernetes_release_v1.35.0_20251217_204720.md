# Kubernetes 版本发布分析报告
## Kubernetes v1.35.0 (v1.35.0)

### 📋 版本信息
- **版本标签：** v1.35.0
- **版本名称：** Kubernetes v1.35.0
- **发布时间：** 2025-12-17T20:01:55Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.0

### 🔍 分析统计
- **分析时间：** 2025-12-17 20:47:20
- **分析的 PR 数量：** 44
- **分析的 Issue 数量：** 12
- **重要项目数量：** 55

## 📊 版本概述
Kubernetes v1.35.0 是一个包含重要 API 提升、关键 Bug 修复和必要基础设施清理的版本，重点关注了 cgroup v2 强制迁移、废弃功能移除和多项功能进入 Beta 阶段。

## 🔒 安全问题修复
1. ⚠️ 修复客户端 CA 和请求头 CA 证书验证重叠的潜在权限提升漏洞 - [PR #131411](https://github.com/kubernetes/kubernetes/pull/131411) - **风险级别：** 中 - 仅在错误配置相同 CA 时存在风险，修复后验证逻辑更严格。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 HPA 副本数计算可能超过 int32 最大值导致错误扩缩的问题 - [PR #126979](https://github.com/kubernetes/kubernetes/pull/126979) - **影响：** 防止在指标值极大时，HPA 计算出错并错误地将副本数设为 1。
2. 修复客户端 CA 和请求头 CA 使用相同根证书时的验证重叠问题 - [PR #131411](https://github.com/kubernetes/kubernetes/pull/131411) - **影响：** 消除潜在的安全配置漏洞，确保两种认证方式的隔离性。
3. 修复当 Pod `restartPolicy=Never` 且 sidecar 容器 `restartPolicy=Always` 并配置 startupProbe 时，主容器可能无法启动的问题 - [PR #133072](https://github.com/kubernetes/kubernetes/pull/133072) - **影响：** 解决 sidecar 容器启动探针逻辑缺陷导致的工作负载启动阻塞。
4. 修复一个 Pod 中多个 volume 引用同一个 PVC 时可能出现的挂载问题 - [PR #122140](https://github.com/kubernetes/kubernetes/pull/122140) - **影响：** 确保存储卷挂载的正确性和一致性。
5. 改进镜像垃圾回收因磁盘压力失败时的错误信息，使其更具可操作性 - [PR #132578](https://github.com/kubernetes/kubernetes/pull/132578) - **影响：** 帮助运维人员更快速定位磁盘空间问题的根本原因。
6. 修复驱逐 Pod 时可能返回令人困惑的 `TooManyRequests` 错误信息的问题 - [PR #133097](https://github.com/kubernetes/kubernetes/pull/133097) - **影响：** 提供更准确的错误原因，便于排查 Pod 驱逐失败问题。

## 💥 破坏性变更
1. 🚨 ACTION REQUIRED: 移除 kubelet 的 `--pod-infra-container-image` 标志 - [PR #133779](https://github.com/kubernetes/kubernetes/pull/133779) - **影响：** 非 kubeadm 集群需从 kubelet 命令行或配置文件移除该标志；kubeadm 集群需从 kubelet 的 `extraArgs` 中移除。
2. 🚨 ACTION REQUIRED: 默认启用 `failCgroupV1`，不再支持 cgroup v1 - [PR #134298](https://github.com/kubernetes/kubernetes/pull/134298) - **影响：** 节点操作系统必须配置为使用 cgroup v2，否则 kubelet 将拒绝启动。
3. 🚨 kube-proxy IPVS 模式被标记为已废弃 - [PR #134539](https://github.com/kubernetes/kubernetes/pull/134539) - **影响：** 用户应开始规划从 IPVS 迁移到 nftables 或其他模式。
4. 🚨 验证 `--log-flush-frequency` 必须为正数，防止错误配置导致 panic - [PR #133540](https://github.com/kubernetes/kubernetes/pull/133540) - **影响：** 错误配置该标志将导致启动失败而非 panic，行为更可预测。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 移除已废弃的 `--pod-infra-container-image` kubelet 标志 - [PR #133779](https://github.com/kubernetes/kubernetes/pull/133779) - **影响：** 升级前必须从 kubelet 配置中手动移除该标志，否则 kubelet 将无法启动。
2. 将 `failCgroupV1` 设置为 true，正式移除对 cgroup v1 的支持 - [PR #134298](https://github.com/kubernetes/kubernetes/pull/134298) - **影响：** 所有节点必须运行在 cgroup v2 上，否则 kubelet 将无法启动。
3. 标记 kube-proxy 的 IPVS 模式为已废弃，建议迁移至 nftables - [PR #134539](https://github.com/kubernetes/kubernetes/pull/134539) - **影响：** 启动时将打印警告日志，需规划网络代理模式的迁移。
4. 更新 system-validators 依赖至 v1.12.1 - [PR #134744](https://github.com/kubernetes/kubernetes/pull/134744) - **影响：** 可能引入新的系统预检规则，影响 kubeadm 集群的安装或升级。
5. Deployment 的 `ReplicaSetTerminatingReplicas` 条件提升至 Beta - [PR #133087](https://github.com/kubernetes/kubernetes/pull/133087) - **影响：** 更精确地展示 Deployment 滚动更新期间 terminating 状态的 Pod 数量。
6. HPA 可配置容忍度 (`HPAConfigurableTolerance`) 功能门提升至 Beta 并默认启用 - [PR #133128](https://github.com/kubernetes/kubernetes/pull/133128) - **影响：** 允许用户通过 HPA 行为配置调整扩缩容的敏感度。
7. StatefulSet 的 `MaxUnavailable` 功能提升至 Beta 并默认启用 - [PR #133153](https://github.com/kubernetes/kubernetes/pull/133153) - **影响：** 允许 StatefulSet 在滚动更新时同时更新多个 Pod，加快更新速度。

## 🚀 性能优化
1. 为 DeltaFIFO 添加批量弹出项目处理，减少 Informer 缓存读写锁竞争 - [PR #132240](https://github.com/kubernetes/kubernetes/pull/132240) - **提升：** 在高负载集群中显著改善控制器事件处理吞吐量，减少缓存延迟。
2. 为 cloud-controller-manager 引入基于 Watch 的路由控制器协调机制（默认关闭） - [PR #131220](https://github.com/kubernetes/kubernetes/pull/131220) - **提升：** 减少对云提供商 API 的轮询调用，避免触发速率限制。
3. 从 `apiserver_request_sli_duration_seconds` 指标中排除 dryRun 请求 - [PR #131092](https://github.com/kubernetes/kubernetes/pull/131092) - **提升：** 使 API 延迟指标更准确地反映真实用户请求的性能。

## 🎯 风险评估
整体风险评估：**中等偏高**。此版本包含多个需要**手动干预**的破坏性变更（如移除标志、强制cgroup v2），若忽略将导致组件无法启动。此外，多项核心功能（HPA、StatefulSet）进入Beta且默认启用，可能改变现有工作负载的行为。建议的升级时机是在业务低峰期，并确保有完整的回滚方案。需要特别关注 kubelet 配置的兼容性和节点系统的 cgroup 版本。

## 📋 升级建议
1. **升级前强制检查：** 1) 确保所有节点已启用 cgroup v2。2) 检查并清理所有 kubelet 配置中的 `--pod-infra-container-image` 参数。
2. **测试策略：** 在测试环境中充分验证工作负载，特别是使用了 sidecar 容器、HPA、StatefulSet 和 Deployment 的应用。
3. **监控与观察：** 升级后密切关注 kube-proxy 日志中的 IPVS 废弃警告，并制定迁移计划。监控 HPA 和 StatefulSet 新功能的行为是否符合预期。
4. **配置清理：** 检查并移除任何可能引用已废弃标志（如 `--container-runtime`）的脚本或配置管理模板。

## 📋 Release 包含的变更

### PR #117160: Clean up service account print and describe
- **链接：** https://github.com/kubernetes/kubernetes/pull/117160
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** area/test, priority/backlog, kind/cleanup, area/kubectl, lgtm, release-note, size/M, approved, sig/cli, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  PR #117160 清理service account的kubectl输出，自1.24版本后secrets字段不再由核心组件填充，移除误导性的token和secret计数显示。

### PR #122140: kubelet: multiple volumes reference one PVC in one Pod
- **链接：** https://github.com/kubernetes/kubernetes/pull/122140
- **状态：** closed
- **已合并：** 是
- **作者：** huww98
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/storage, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, ok-to-test, triage/accepted
- **变更说明：**
  修复kubelet中一个Pod内多个卷引用同一PVC时产生的处理问题，属于存储相关bug修复。

### PR #123642: Add JWKS fetch metrics for jwt authenticator
- **链接：** https://github.com/kubernetes/kubernetes/pull/123642
- **状态：** closed
- **已合并：** 是
- **作者：** aramase
- **标签：** area/test, priority/important-soon, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  为JWT认证器添加JWKS获取指标：apiserver_authentication_jwt_authenticator_jwks_fetch_last_timestamp_seconds和apiserver_authentication_jwt_authenticator_jwks_fetch_last_key_set_info。需启用StructuredAuthenticationConfiguration特性。

### PR #125912: Migrate cpumanager to contextual logging
- **链接：** https://github.com/kubernetes/kubernetes/pull/125912
- **状态：** closed
- **已合并：** 是
- **作者：** ffromani
- **标签：** area/kubelet, kind/cleanup, lgtm, area/logging, sig/node, release-note, size/XL, approved, cncf-cla: yes, priority/important-longterm, triage/accepted, wg/structured-logging
- **变更说明：**
  PR #125912 将cpumanager迁移至上下文日志，提升日志可读性和调试效率。部分解决issue 123037和130069，属于结构化日志迁移工作。

### PR #126979: Fix replicaCount calculation exceeding max int32
- **链接：** https://github.com/kubernetes/kubernetes/pull/126979
- **状态：** closed
- **已合并：** 是
- **作者：** omerap12
- **标签：** kind/bug, lgtm, sig/autoscaling, size/S, release-note-none, sig/apps, approved, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  **PR #126979:** Fix replicaCount calculation exceeding max int32
**标签:** kind/bug, lgtm, sig/autoscaling, size/S, release-note-none, sig/apps, approved, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, ok-to-test, triage/accepted

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributor gui...

### PR #130548: Bump addon manager image to v9.1.8
- **链接：** https://github.com/kubernetes/kubernetes/pull/130548
- **状态：** closed
- **已合并：** 是
- **作者：** Jefftree
- **标签：** area/test, kind/cleanup, sig/scalability, lgtm, area/provider/gcp, release-note, size/XS, approved, cncf-cla: yes, sig/testing, lifecycle/rotten, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  PR #130548 将addon manager镜像版本升级至v9.1.8，属于常规维护性更新，确保组件保持最新状态。

### PR #130551: order sandbox by attempt or create time
- **链接：** https://github.com/kubernetes/kubernetes/pull/130551
- **状态：** closed
- **已合并：** 是
- **作者：** yylt
- **标签：** area/kubelet, lgtm, sig/node, size/S, kind/feature, release-note-none, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  PR #130551 为sandbox添加按尝试次数或创建时间排序功能，解决系统时钟回退导致的顺序问题，涉及kubelet容器管理。

### PR #130951: Adding metrics for Maxunavailable feature in StatefulSet
- **链接：** https://github.com/kubernetes/kubernetes/pull/130951
- **状态：** closed
- **已合并：** 是
- **作者：** Edwinhr716
- **标签：** lgtm, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, sig/instrumentation, priority/important-longterm, tide/merge-method-squash, triage/accepted, area/stable-metrics
- **变更说明：**
  为StatefulSet的MaxUnavailable特性添加监控指标，增强部署过程的可观测性。

### PR #131092: metrics: exclude dryRun requests from apiserver_request_sli_duration_seconds
- **链接：** https://github.com/kubernetes/kubernetes/pull/131092
- **状态：** closed
- **已合并：** 是
- **作者：** aldudko
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/instrumentation, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  **PR #131092:** metrics: exclude dryRun requests from apiserver_request_sli_duration_seconds
**标签:** area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/instrumentation, ok-to-test, needs-priority, triage/accepted

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read o...

### PR #131220: feat(ccm): watch-based route controller reconciliation
- **链接：** https://github.com/kubernetes/kubernetes/pull/131220
- **状态：** closed
- **已合并：** 是
- **作者：** lukasmetzner
- **标签：** lgtm, area/cloudprovider, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  **PR #131220:** feat(ccm): watch-based route controller reconciliation
**标签:** lgtm, area/cloudprovider, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, ok-to-test, needs-priority, triage/accepted

**PR内容:** #### What type of PR is this?
/kind feature

#### What this PR does / why we need it:
The route controller in the cloud-controller-ma...

### PR #131411: Fix overlapping client CA and requestheader CA validation with proper certificate checking
- **链接：** https://github.com/kubernetes/kubernetes/pull/131411
- **状态：** closed
- **已合并：** 是
- **作者：** ballista01
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, sig/security, triage/accepted
- **变更说明：**
  修复kube-apiserver中客户端CA与请求头CA验证重叠问题，通过严格证书检查增强安全性。

### PR #131755: Allow OpenAPI model package names to be declared by APIs
- **链接：** https://github.com/kubernetes/kubernetes/pull/131755
- **状态：** closed
- **已合并：** 是
- **作者：** jpbetz
- **标签：** area/test, sig/network, area/kubelet, kind/cleanup, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XL, kind/api-change, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, priority/important-longterm, sig/architecture, area/code-generation, lifecycle/stale, sig/cloud-provider, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  **PR #131755:** Allow OpenAPI model package names to be declared by APIs
**标签:** area/test, sig/network, area/kubelet, kind/cleanup, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/XL, kind/api-change, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/instrumentat...

### PR #132157: drop UserNamespacesPodSecurityStandards feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/132157
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** area/test, kind/cleanup, lgtm, sig/node, release-note, size/XXL, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  **PR #132157:** drop UserNamespacesPodSecurityStandards feature gate
**标签:** area/test, kind/cleanup, lgtm, sig/node, release-note, size/XXL, sig/auth, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted

**PR内容:** this feature gate was meant to be ephemeral, and only was used for guaranteeing a cluster admin didn't accidentally relax PSA policies before the kubelet would deny...

### PR #132240: Adding batch handling for popping items from RealFIFO
- **链接：** https://github.com/kubernetes/kubernetes/pull/132240
- **状态：** closed
- **已合并：** 是
- **作者：** yue9944882
- **标签：** sig/scheduling, lgtm, sig/storage, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  **PR #132240:** Adding batch handling for popping items from RealFIFO
**标签:** sig/scheduling, lgtm, sig/storage, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, priority/important-longterm, triage/accepted

**PR内容:** /kind feature
/sig api-machinery

### Summary

Ref: https://github.com/kubernetes/kubernetes/issues/130767

The above issue noted a problem ...

### PR #132288: chore: update CoreDNS to v1.12.3
- **链接：** https://github.com/kubernetes/kubernetes/pull/132288
- **状态：** closed
- **已合并：** 是
- **作者：** thevilledev
- **标签：** kind/cleanup, lgtm, area/provider/gcp, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/cloud-provider, ok-to-test, needs-priority, area/dependency, needs-triage
- **变更说明：**
  将CoreDNS依赖更新至v1.12.3版本，属于常规依赖项维护更新。

### PR #132441: [KEP-5440]: MutablePodResourcesForSuspendedJobs 
- **链接：** https://github.com/kubernetes/kubernetes/pull/132441
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/XL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, api-review, triage/accepted
- **变更说明：**
  实现KEP-5440：为暂停且未启动的Job启用可变Pod资源支持，通过特性门控控制仅允许容器资源更新。

### PR #132549: bug: Remove duplicate storage resources update validations
- **链接：** https://github.com/kubernetes/kubernetes/pull/132549
- **状态：** closed
- **已合并：** 是
- **作者：** gavinkflam
- **标签：** kind/bug, lgtm, sig/storage, release-note, size/XS, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  PR #132549 修复存储资源更新验证中的重复代码问题，移除冗余验证逻辑，涉及sig/storage相关组件。

### PR #132550: bug: Remove duplicate RBAC resources update validations
- **链接：** https://github.com/kubernetes/kubernetes/pull/132550
- **状态：** closed
- **已合并：** 是
- **作者：** gavinkflam
- **标签：** kind/bug, lgtm, release-note, size/S, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  PR #132550 修复RBAC资源更新验证中的重复代码，优化验证逻辑，涉及sig/auth管理的资源类型。

### PR #132578: Report actionable error when GC fails due to disk pressure
- **链接：** https://github.com/kubernetes/kubernetes/pull/132578
- **状态：** closed
- **已合并：** 是
- **作者：** drigz
- **标签：** kind/bug, priority/backlog, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  PR #132578 改进镜像垃圾回收失败时的错误信息，当因磁盘压力导致GC失败时提供更 actionable 的提示，修复issue 71869。

### PR #132579: KEP-2535: move objects to beta, add storage version migration to filesystem cache
- **链接：** https://github.com/kubernetes/kubernetes/pull/132579
- **状态：** closed
- **已合并：** 是
- **作者：** stlaz
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/L, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  PR #132579 基于KEP 2535将ImagePullIntent和ImagePulledRecord对象升级至v1beta1 API，并添加文件系统缓存版本迁移功能。

### PR #132606: add paths section to scheduler statusz endpoint
- **链接：** https://github.com/kubernetes/kubernetes/pull/132606
- **状态：** closed
- **已合并：** 是
- **作者：** Peac36
- **标签：** area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, lgtm, sig/node, sig/api-machinery, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  PR #132606 为kube-scheduler的statusz端点添加paths章节，列出/livez、/readyz等可用监控路径，修复issue 132539。

### PR #132644: kubelet: add metrics for EnsureImageExists
- **链接：** https://github.com/kubernetes/kubernetes/pull/132644
- **状态：** closed
- **已合并：** 是
- **作者：** stlaz
- **标签：** area/kubelet, lgtm, sig/node, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  **PR #132644:** kubelet: add metrics for EnsureImageExists
**标签:** area/kubelet, lgtm, sig/node, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, needs-priority, triage/accepted

**PR内容:** #### What type of PR is this?
/kind feature

#### What this PR does / why we need it:
This PR adds metrics for requests to kubelet image-manager `EnsureImageExists()` function.

##...

### PR #132663: applyconfiguration-gen: preserve struct and field comments in generated code
- **链接：** https://github.com/kubernetes/kubernetes/pull/132663
- **状态：** closed
- **已合并：** 是
- **作者：** mrIncompetent
- **标签：** lgtm, sig/api-machinery, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, area/code-generation, triage/needs-information, ok-to-test, needs-priority
- **变更说明：**
  **PR #132663:** applyconfiguration-gen: preserve struct and field comments in generated code
**标签:** lgtm, sig/api-machinery, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, area/code-generation, triage/needs-information, ok-to-test, needs-priority

**PR内容:** #### What type of PR is this?

/kind feature

#### What this PR does / why we need it:

Updates `applyconfiguration-...

### PR #132665: applyconfiguration-gen: add ExtractFrom with subresource support
- **链接：** https://github.com/kubernetes/kubernetes/pull/132665
- **状态：** closed
- **已合并：** 是
- **作者：** mrIncompetent
- **标签：** lgtm, sig/api-machinery, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, area/code-generation, triage/needs-information, ok-to-test, needs-priority
- **变更说明：**
  **PR #132665:** applyconfiguration-gen: add ExtractFrom with subresource support
**标签:** lgtm, sig/api-machinery, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, area/code-generation, triage/needs-information, ok-to-test, needs-priority

**PR内容:** #### What type of PR is this?

/kind feature

#### What this PR does / why we need it:

- Extends applyconfiguration-gen to gene...

### PR #132798: Show simple values in validation rule failures
- **链接：** https://github.com/kubernetes/kubernetes/pull/132798
- **状态：** closed
- **已合并：** 是
- **作者：** cbandy
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  改进kube-apiserver中CEL验证规则失败时的错误消息，现在包含失败的具体值（数字、布尔值、字符串）而非字段类型。修复issue #132528，提升用户调试体验。

### PR #132825: API: extending validations with WithOrigins for pkg/apis/core
- **链接：** https://github.com/kubernetes/kubernetes/pull/132825
- **状态：** closed
- **已合并：** 是
- **作者：** PatrickLaabs
- **标签：** kind/cleanup, lgtm, release-note, size/M, kind/api-change, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  在pkg/apis/core验证中添加WithOrigins字段支持，从PR #132577拆分出的清理工作，为后续验证功能扩展做准备。

### PR #132919: Pod level in place pod resize - alpha
- **链接：** https://github.com/kubernetes/kubernetes/pull/132919
- **状态：** closed
- **已合并：** 是
- **作者：** ndixita
- **标签：** area/test, area/kubelet, sig/scheduling, area/kubectl, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/auth, sig/apps, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, ok-to-test, needs-priority, api-review, area/e2e-test-framework, needs-triage, area/stable-metrics
- **变更说明：**
  实现Pod级别原地资源调整功能（Alpha阶段），允许运行时修改Pod资源规格，涉及API变更和多个SIG协作。

### PR #132927: DRA API: implement ResourceClaim strategy for DRADeviceTaints
- **链接：** https://github.com/kubernetes/kubernetes/pull/132927
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, lgtm, release-note, size/XXL, approved, cncf-cla: yes, needs-priority, api-review, needs-triage, wg/device-management
- **变更说明：**
  修复DRA API中DRADeviceTaints特性的ResourceClaim策略，正确丢弃无效的tolerations字段。基于KEP #5055。

### PR #132960: Configure JSON content type for generic webhook RESTClient.
- **链接：** https://github.com/kubernetes/kubernetes/pull/132960
- **状态：** closed
- **已合并：** 是
- **作者：** benluddy
- **标签：** kind/bug, area/kubelet, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复通用webhook RESTClient的Content-Type配置，确保正确设置为JSON格式。

### PR #133072: Fix startup probe worker termination for sidecar containers
- **链接：** https://github.com/kubernetes/kubernetes/pull/133072
- **状态：** closed
- **已合并：** 是
- **作者：** AadiDev005
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, ok-to-test, triage/accepted
- **变更说明：**
  PR #133072 修复sidecar容器启动探针worker终止bug。当pod为restartPolicy=Never且sidecar为Always时，确保主容器能正常启动，避免卡在Initializing状态。

### PR #133087: promote DeploymentReplicaSetTerminatingReplicas to Beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/133087
- **状态：** closed
- **已合并：** 是
- **作者：** atiratree
- **标签：** area/test, lgtm, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, priority/important-longterm, area/code-generation, api-review, triage/accepted
- **变更说明：**
  PR #133087 将DeploymentReplicaSetTerminatingReplicas特性升级至Beta阶段，涉及API变更，增强Deployment副本集终止副本的监控能力。

### PR #133097: Resolve confusing use of TooManyRequests error for eviction
- **链接：** https://github.com/kubernetes/kubernetes/pull/133097
- **状态：** closed
- **已合并：** 是
- **作者：** kei01234kei
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, sig/apps, approved, cncf-cla: yes, tide/merge-method-squash, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  PR #133097 修复驱逐过程中误用TooManyRequests错误代码的问题，避免错误信息混淆，涉及sig/node和sig/apps组件。

### PR #133128: Promote HPAConfigurableTolerance gate to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/133128
- **状态：** closed
- **已合并：** 是
- **作者：** jm-franc
- **标签：** lgtm, sig/api-machinery, release-note, sig/autoscaling, size/S, kind/api-change, kind/feature, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted
- **变更说明：**
  **PR #133128:** Promote HPAConfigurableTolerance gate to beta
**标签:** lgtm, sig/api-machinery, release-note, sig/autoscaling, size/S, kind/api-change, kind/feature, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted

**PR内容:** #### What type of PR is this?

/kind feature


#### What this PR does / why we need it:

#### Which issue(s) t...

### PR #133153: Update MaxUnavailableStatefulSet feature gate to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/133153
- **状态：** closed
- **已合并：** 是
- **作者：** helayoty
- **标签：** lgtm, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted
- **变更说明：**
  **PR #133153:** Update MaxUnavailableStatefulSet feature gate to beta
**标签:** lgtm, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted

**PR内容:** #### What type of PR is this?

/kind feature
/sig apps
/triage accepted
/milestone v1.35

#### What this PR d...

### PR #133327: Change KYAML gate to on-by-default
- **链接：** https://github.com/kubernetes/kubernetes/pull/133327
- **状态：** closed
- **已合并：** 是
- **作者：** thockin
- **标签：** area/kubectl, lgtm, release-note, size/XS, kind/api-change, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  默认启用kubectl get -o kyaml输出格式，用户可通过设置KUBECTL_KYAML=false禁用。基于KEP #5295，低风险API变更。

### PR #133338: defaultservicecidr controller no shutdown eventbroadcaster on start
- **链接：** https://github.com/kubernetes/kubernetes/pull/133338
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** kind/bug, sig/network, lgtm, release-note, size/XS, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复defaultservicecidr控制器事件广播器在启动时被错误关闭的问题，现仅在上下文完成时关闭。解决issue #133306，确保事件正常记录。

### PR #133389: Introduce node declared features framework
- **链接：** https://github.com/kubernetes/kubernetes/pull/133389
- **状态：** closed
- **已合并：** 是
- **作者：** pravk03
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, area/release-eng, sig/apps, approved, cncf-cla: yes, sig/testing, sig/release, area/code-generation, ok-to-test, needs-priority, api-review, area/dependency, triage/accepted
- **变更说明：**
  引入节点声明特性框架，涉及kubelet、apiserver等多组件的大型API变更和功能添加。

### PR #133540: validate that flush frequency must be positive
- **链接：** https://github.com/kubernetes/kubernetes/pull/133540
- **状态：** closed
- **已合并：** 是
- **作者：** BenTheElder
- **标签：** kind/bug, sig/network, area/kubelet, area/kube-proxy, lgtm, sig/node, release-note, size/S, kind/api-change, approved, cncf-cla: yes, sig/instrumentation, sig/architecture, needs-priority, triage/accepted
- **变更说明：**
  PR #133540 修复flush frequency参数验证问题，确保其必须为正数。涉及kubelet和kube-proxy组件，防止无效配置导致异常。

### PR #133648: [KEP:4020] Peer-aggregated discovery
- **链接：** https://github.com/kubernetes/kubernetes/pull/133648
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/test, sig/scheduling, area/apiserver, lgtm, area/cloudprovider, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, sig/cloud-provider, ok-to-test, needs-priority, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  **PR #133648:** [KEP:4020] Peer-aggregated discovery
**标签:** area/test, sig/scheduling, area/apiserver, lgtm, area/cloudprovider, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, sig/cloud-provider, ok-to-test, needs-priority, area/dependency, triage/accepted, wg/device-management

**PR内容:** <!--  Thanks for send...

### PR #133779: Remove deprecated pod-infra-container-image flag
- **链接：** https://github.com/kubernetes/kubernetes/pull/133779
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, size/XS, release-note-action-required, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  **PR #133779:** Remove deprecated pod-infra-container-image flag
**标签:** area/kubelet, kind/cleanup, lgtm, sig/node, size/XS, release-note-action-required, approved, cncf-cla: yes, needs-priority, needs-triage

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributor guidelines: https://git.k8s.io/community/con...

### PR #134298: [KEP-5573] Set failCgroupV1 to true
- **链接：** https://github.com/kubernetes/kubernetes/pull/134298
- **状态：** closed
- **已合并：** 是
- **作者：** kannon92
- **标签：** area/kubelet, lgtm, sig/node, size/M, kind/api-change, release-note-action-required, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, kind/deprecation, needs-triage
- **变更说明：**
  **PR #134298:** [KEP-5573] Set failCgroupV1 to true
**标签:** area/kubelet, lgtm, sig/node, size/M, kind/api-change, release-note-action-required, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, kind/deprecation, needs-triage

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributor gui...

### PR #134481: Update --chunk-size flag, dropping the beta information
- **链接：** https://github.com/kubernetes/kubernetes/pull/134481
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/documentation, kind/cleanup, area/kubectl, lgtm, release-note, size/XS, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  将kubectl的--chunk-size标志标记为稳定功能，移除beta标识。影响describe、get、drain和events命令。

### PR #134539: KEP: 5495 - Add deprecation warning for ipvs
- **链接：** https://github.com/kubernetes/kubernetes/pull/134539
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** sig/network, area/kube-proxy, lgtm, release-note, size/XS, approved, cncf-cla: yes, needs-priority, kind/deprecation, triage/accepted
- **变更说明：**
  PR #134539 为kube-proxy的ipvs模式添加启动警告，标记为已弃用。基于KEP 5495，ipvs模式将在未来Kubernetes版本中移除，建议用户迁移至nftables。

### PR #134744: vendor: update system-validators to v1.12.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/134744
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/important-soon, lgtm, sig/node, sig/cluster-lifecycle, size/M, kind/feature, release-note-action-required, approved, area/kubeadm, cncf-cla: yes, area/dependency, triage/accepted
- **变更说明：**
  **PR #134744:** vendor: update system-validators to v1.12.1
**标签:** priority/important-soon, lgtm, sig/node, sig/cluster-lifecycle, size/M, kind/feature, release-note-action-required, approved, area/kubeadm, cncf-cla: yes, area/dependency, triage/accepted

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributo...

---
*本报告由 Containerd Release Tracker 自动生成*
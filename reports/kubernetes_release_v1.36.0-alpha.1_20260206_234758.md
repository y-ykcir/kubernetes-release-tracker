# Kubernetes 版本发布分析报告
## v1.36.0-alpha.1 (v1.36.0-alpha.1)

### 📋 版本信息
- **版本标签：** v1.36.0-alpha.1
- **版本名称：** v1.36.0-alpha.1
- **发布时间：** 2026-02-06T22:38:32Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.36.0-alpha.1

### 🔍 分析统计
- **分析时间：** 2026-02-06 23:47:58
- **分析的 PR 数量：** 44
- **分析的 Issue 数量：** 18
- **重要项目数量：** 56

## 📊 版本概述
Kubernetes v1.36.0-alpha.1 是一个早期预览版本，核心价值在于调度性能优化、存储插件清理以及一系列重要的稳定性修复，为后续版本升级提供了重要的技术风向标。

## 🐛 重要问题修复
1. 修复 NodeResourcesFit 插件因 RequestedToCapacityRatio 配置缺失导致的空指针崩溃 - [PR #132120](https://github.com/kubernetes/kubernetes/pull/132120) - **影响：** 修复了调度器配置错误时可能引发的 panic，提升调度器稳定性。
2. 修复 kubelet 在通过 IP 地址连接时证书不重载的问题 - [PR #133654](https://github.com/kubernetes/kubernetes/pull/133654) - **影响：** 确保 kubelet 证书轮换后，API 服务器能正确重新连接，避免因证书过期导致节点失联。
3. 修复静态 Pod 状态在 Init 容器被 GC 后始终显示为 `Init:0/1` 的问题 - [PR #131317](https://github.com/kubernetes/kubernetes/pull/131317) - **影响：** 修复了 kubelet 重启后静态 Pod 状态显示错误，影响监控和自愈逻辑。
4. 修复插件管理器对注册失败的处理，增加指数退避重试 - [PR #133335](https://github.com/kubernetes/kubernetes/pull/133335) - **影响：** 防止有问题的插件导致 DoS，同时允许从瞬时故障中恢复，提升设备插件等场景的鲁棒性。
5. 修复 VolumeAttachment 在 CSI 驱动 `attachRequired` 从 true 变为 false 后无法清理的问题 - [PR #129664](https://github.com/kubernetes/kubernetes/pull/129664) - **影响：** 避免存储卷附件对象泄漏，确保存储资源正确回收。
6. 修复调度器 GatedPods 指标在 Pod 从非门控状态变为门控状态时不同步的问题 - [PR #135368](https://github.com/kubernetes/kubernetes/pull/135368) - **影响：** 修复监控指标不准确或出现负值的问题，确保调度队列监控数据可靠。
7. 修复大列表 CBOR 解码时因元素数量限制导致的客户端错误 - [PR #135340](https://github.com/kubernetes/kubernetes/pull/135340) - **影响：** 允许客户端处理更大的 CBOR 编码响应列表，提升兼容性。
8. 修复 `kubectl label` 同时添加和删除标签时输出信息不准确的问题 - [PR #134849](https://github.com/kubernetes/kubernetes/pull/134849) - **影响：** 命令行输出更准确，提升用户体验。

## 💥 破坏性变更
1. 🚨 移除内置 Portworx 卷插件 - [PR #135322](https://github.com/kubernetes/kubernetes/pull/135322) - **影响：** 使用 `kubernetes.io/portworx-volume` 存储类的 PVC 和 Pod 将失效。**迁移动作：** 必须在升级前将所有工作负载迁移至 Portworx CSI 驱动 (`pxd.portworx.com`)。
2. 🚨 kubeadm 移除已弃用的特性门控 `ControlPlaneKubeletLocalMode` - [PR #135773](https://github.com/kubernetes/kubernetes/pull/135773) - **影响：** 使用此特性门控的 kubeadm 配置文件将失效。**迁移动作：** 从配置中移除对该特性门控的引用。
3. 🚨 kubeadm 移除对 etcd (< 3.6.0) 两个已弃用标志的支持 - [PR #135701](https://github.com/kubernetes/kubernetes/pull/135701) - **影响：** 如果使用旧版 etcd 并自定义了相关配置，kubeadm 可能无法启动 etcd。**迁移动作：** 确保使用 etcd 3.6.0 或更高版本。
4. 🚨 client-go 中弃用的 `NewSimpleClientset` 在样例控制器中被替换 - [PR #131068](https://github.com/kubernetes/kubernetes/pull/131068) - **影响：** 依赖 `sample-controller` 代码模式的用户需要关注此变更。**迁移动作：** 参考样例，将测试代码中的 `NewSimpleClientset` 迁移至新的 `NewClientset`。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 调度器 PreBind 插件支持并行执行以降低绑定延迟 - [PR #135393](https://github.com/kubernetes/kubernetes/pull/135393) - **影响：** 自定义调度器插件的开发者需要更新 PreBindPreFlight 方法以返回 PreBindPreFlightResult 结构体并设置 `AllowParallel: true` 来启用并行，否则保持串行行为。
2. 移除内置 (intree) Portworx 卷插件 - [PR #135322](https://github.com/kubernetes/kubernetes/pull/135322) - **影响：** 仍在使用 Portworx 内置卷插件的集群将无法工作，必须迁移至 Portworx CSI 驱动。
3. VolumeAttributesClass 特性门锁定为默认启用 (true) - [PR #134556](https://github.com/kubernetes/kubernetes/pull/134556) - **影响：** 该功能趋于稳定，为后续存储属性管理功能铺平道路。
4. 为审计策略规则添加通配符 `*` 以过滤子资源噪音 - [PR #135262](https://github.com/kubernetes/kubernetes/pull/135262) - **影响：** 管理员可以配置如 `*/status` 的规则来减少对 status 子资源写操作的审计日志噪音。
5. 默认启用 WatchCacheInitializationPostStartHook - [PR #135777](https://github.com/kubernetes/kubernetes/pull/135777) - **影响：** 提升 API 服务器启动后 watch 缓存初始化的性能，有助于改善大规模集群的初始响应速度。

## 🚀 性能优化
1. 修复 `apiserver_watch_events_sizes` 指标低估问题，准确反映 watch 流量 - [PR #135367](https://github.com/kubernetes/kubernetes/pull/135367) - **提升：** 修复后该指标能真实反映被大量监听的资源（如 EndpointSlices）产生的流量，为容量规划提供准确数据。
2. 对来自 CRI 运行时的运行时处理器列表进行排序，避免不必要的节点对象更新 - [PR #135358](https://github.com/kubernetes/kubernetes/pull/135358) - **提升：** 减少因列表顺序变化导致的冗余 API 调用和节点状态更新，降低 etcd 和 API 服务器负载。
3. ImageLocality 插件现在在评分时考虑 ImageVolume 使用的镜像 - [PR #130231](https://github.com/kubernetes/kubernetes/pull/130231) - **提升：** 优化了使用 ImageVolume 的 Pod 的调度决策，提高镜像本地性，加速 Pod 启动。
4. ResourceClaim 控制器的并发同步数量变为可配置 - [PR #134701](https://github.com/kubernetes/kubernetes/pull/134701) - **提升：** 允许在大规模训练作业（如万级 Pod/节点）中调整并发度，优化资源分配性能。

## 🎯 风险评估
整体风险评估：**高（对于Alpha版本属正常）**。
- **升级风险级别：** 极高，不适用于生产。
- **建议的升级时机：** 仅限开发和测试集群，用于验证新功能和自定义组件兼容性。
- **需要特别关注的方面：** 1) **Portworx卷插件移除**是明确的、影响广泛的破坏性变更。2) **调度器插件接口变更**要求开发者主动适配。3) 多个**核心控制器（调度器、卷管理器、插件管理器）的稳定性修复**表明此版本在夯实基础，但也意味着在相关场景进行充分测试至关重要。

## 📋 升级建议
1. **对于所有用户：** 此版本为 alpha，绝对不要用于生产环境。可用于早期功能测试和升级影响评估。
2. **对于调度器插件开发者：** 立即检查并测试自定义的 PreBind 插件，根据 PR #135393 的要求更新代码以兼容并行执行，或确认返回 `nil` 保持串行行为。
3. **使用 Portworx 内置驱动的用户：** 这是最高优先级的迁移项。在考虑升级到未来包含此变更的稳定版（如 v1.36）之前，必须完成向 Portworx CSI 驱动的迁移。
4. **集群管理员：** 1) 关注 kubelet 证书轮换和 VolumeAttachment 清理的修复，这些提升了集群的长期运行稳定性。2) 利用审计日志通配符功能优化日志策略。3) 注意 kubeadm 配置的破坏性变更。
5. **准备升级计划：** 虽然距离稳定版尚早，但应基于这些变更开始规划，特别是处理 Portworx 移除和调度器插件更新。

## 📋 Release 包含的变更

### PR #129664: Fix VolumeAttachment cleanup when AttachRequired changes
- **链接：** https://github.com/kubernetes/kubernetes/pull/129664
- **状态：** closed
- **已合并：** 是
- **作者：** hkttty2009
- **标签：** kind/bug, area/test, lgtm, sig/storage, release-note, size/L, approved, cncf-cla: yes, sig/testing, lifecycle/rotten, ok-to-test, needs-priority, area/e2e-test-framework, needs-triage
- **变更说明：**
  修复当CSI驱动器的ATTACHREQUIRED从true变为false时，VolumeAttachment残留无法清理的问题。通过直接传递volumeName给MarkVolumeAsAttached函数，使其跳过plugin查找（该查找在AttachRequired变化时会失败），从而确保VolumeAttachment被正确清理。

### PR #130231: Update ImageLocality plugin to account ImageVolume images
- **链接：** https://github.com/kubernetes/kubernetes/pull/130231
- **状态：** closed
- **已合并：** 是
- **作者：** Barakmor1
- **标签：** sig/scheduling, lgtm, release-note, size/M, kind/feature, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  更新调度器的ImageLocality插件，使其在为Pod评分时，将ImageVolume类型的镜像也纳入考虑范围。这优化了节点选择，优先选择已缓存所需ImageVolume镜像的节点。

### PR #131068: Switch sample-controller to use NewClientset supporting applyconfiguration rather than deprecated NewSimpleClientset
- **链接：** https://github.com/kubernetes/kubernetes/pull/131068
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/XL, kind/api-change, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, triage/accepted
- **变更说明：**
  将 sample-controller 示例代码中使用的客户端从已弃用的 `NewSimpleClientset` 切换为支持 applyconfiguration 的新 `NewClientset`，这是对 client-go 代码生成新特性的跟进。

### PR #131317: Fix:Static pod status is always Init:0/1 if unable to get init container status
- **链接：** https://github.com/kubernetes/kubernetes/pull/131317
- **状态：** closed
- **已合并：** 是
- **作者：** bitoku
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  修复 kubelet 在处理 Static Pod 时的一个 bug：当无法获取 init container 状态时，Pod 状态会错误地始终显示为 `Init:0/1`。该修复确保了状态计算的准确性。

### PR #132120: fix the noderesourcefit plugin's nil pointer by validating RequestedToCapacityRatio config
- **链接：** https://github.com/kubernetes/kubernetes/pull/132120
- **状态：** closed
- **已合并：** 是
- **作者：** flpanbin
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/M, kind/api-change, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复 NodeResourceFit 插件的空指针崩溃问题，通过验证插件配置中的 `RequestedToCapacityRatio` 字段来避免因无效配置导致的 panic。

### PR #132402: Add node `arch` in the kubectl get node output
- **链接：** https://github.com/kubernetes/kubernetes/pull/132402
- **状态：** closed
- **已合并：** 是
- **作者：** astraw99
- **标签：** kind/documentation, lgtm, release-note, size/M, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, needs-triage
- **变更说明：**
  在 `kubectl get node -owide` 命令的输出中添加 `Arch` 列，用于显示节点的 CPU 架构（如 amd64、arm64），方便用户在多架构集群中进行识别和管理。

### PR #132807: [KEP-5365] Implement Image Volume with Digest
- **链接：** https://github.com/kubernetes/kubernetes/pull/132807
- **状态：** closed
- **已合并：** 是
- **作者：** iholder101
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  实现KEP-5365，为ImageVolume添加镜像摘要(Digest)支持。新增ImageVolumeWithDigest特性，将镜像卷的摘要信息记录到容器状态中，增强镜像的可追溯性和安全性。

### PR #133335: pluginmanager: fix handling registration failures
- **链接：** https://github.com/kubernetes/kubernetes/pull/133335
- **状态：** closed
- **已合并：** 是
- **作者：** bart0sh
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/storage, sig/node, release-note, size/M, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  改进kubelet pluginmanager对插件注册失败的处理。当插件注册或状态通知失败时，现将其从实际状态中移除并尝试注销，同时引入指数退避重试机制（初始500ms，最大约2分钟），以防止故障插件导致拒绝服务并允许从瞬时故障中恢复。

### PR #133654: Fix kubelet certificate reload when connecting by IP address
- **链接：** https://github.com/kubernetes/kubernetes/pull/133654
- **状态：** closed
- **已合并：** 是
- **作者：** kwohlfahrt
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/L, sig/auth, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  修复了当 kubelet 通过 IP 地址连接时，证书重载功能失效的问题。这是一个关键的 bug 修复，确保了证书轮换在特定网络配置下的可靠性。

### PR #133845: Clarify CPUCFSQuotaPeriod config vs CustomCPUCFSQuotaPeriod feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/133845
- **状态：** closed
- **已合并：** 是
- **作者：** rbiamru
- **标签：** area/kubelet, kind/documentation, kind/cleanup, lgtm, sig/node, release-note, size/XS, kind/api-change, area/release-eng, approved, cncf-cla: yes, priority/important-longterm, sig/release, area/code-generation, ok-to-test, triage/accepted
- **变更说明：**
  澄清kubelet配置字段`cpuCFSQuotaPeriod`与特性门`CustomCPUCFSQuotaPeriod`之间的关系。此PR属于文档清理，更新了代码注释、帮助文本和变更日志，明确指出非默认值需要启用对应的特性门，以消除混淆。

### PR #134422: ingressclass: show (default) marker for default IngressClass
- **链接：** https://github.com/kubernetes/kubernetes/pull/134422
- **状态：** closed
- **已合并：** 是
- **作者：** jaehanbyun
- **标签：** sig/network, lgtm, release-note, size/M, kind/feature, approved, sig/cli, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  在 `kubectl get ingressclass` 命令的输出中，为被标记为默认的 IngressClass 添加 `(default)` 标识，使其与 Kubernetes 中其他默认资源（如 StorageClass）的显示方式保持一致。

### PR #134556: lock the feature-gate VolumeAttributesClass to default (true)
- **链接：** https://github.com/kubernetes/kubernetes/pull/134556
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, api-review, needs-triage, sig/etcd, wg/device-management
- **变更说明：**
  将 `VolumeAttributesClass` 特性门锁（feature gate）的默认值设置为 true，这意味着该特性将在未来版本中默认启用并最终进入稳定状态，涉及存储和调度等多个SIG。

### PR #134701: Make ConcurrentResourceClaimSyncs configurable
- **链接：** https://github.com/kubernetes/kubernetes/pull/134701
- **状态：** closed
- **已合并：** 是
- **作者：** anson627
- **标签：** area/test, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, priority/important-longterm, area/code-generation, tide/merge-method-squash, ok-to-test, api-review, triage/accepted, wg/device-management
- **变更说明：**
  使 ResourceClaim 控制器的并发同步数量 (`ConcurrentResourceClaimSyncs`) 可配置。此功能增强了控制器在处理大规模工作负载（如万级 Pod）时的灵活性和性能。

### PR #134849: kubectl label: Add 'modified' output version
- **链接：** https://github.com/kubernetes/kubernetes/pull/134849
- **状态：** closed
- **已合并：** 是
- **作者：** tchap
- **标签：** kind/bug, priority/backlog, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复`kubectl label`命令的输出信息。当同时添加和删除标签时，原输出随机显示‘labeled’或‘unlabeled’，现统一改为输出‘modified’，以准确反映操作结果。

### PR #135126: scheduler: add metric for pods scheduled after flush
- **链接：** https://github.com/kubernetes/kubernetes/pull/135126
- **状态：** closed
- **已合并：** 是
- **作者：** mrvarmazyar
- **标签：** sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  为调度器新增一个名为 `scheduler_pod_scheduled_after_flush_total` 的 ALPHA 指标，用于追踪那些因超时从 `unschedulablePods` 队列刷新后成功被调度的 Pod 数量，有助于诊断队列提示优化问题。

### PR #135148: kubeadm: add --allow-deprecated-api to 'config validate'
- **链接：** https://github.com/kubernetes/kubernetes/pull/135148
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/M, kind/feature, approved, area/kubeadm, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 `kubeadm config validate` 命令新增 `--allow-deprecated-api` 标志，允许在验证配置时接受已弃用的 API 版本，提高了 kubeadm 配置验证的灵活性。

### PR #135227: Inverting DRAOperationsDuration metric by inverting 'is_error' label.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135227
- **状态：** closed
- **已合并：** 是
- **作者：** hime
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 DRAOperationsDuration 监控指标的标签逻辑错误，通过反转 `is_error` 标签的值来正确反映操作状态。

### PR #135262: added wildcard * for GroupResources to allow filtering of noisy subgr…
- **链接：** https://github.com/kubernetes/kubernetes/pull/135262
- **状态：** closed
- **已合并：** 是
- **作者：** cmuuss
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/auth, approved, cncf-cla: yes, sig/testing, area/code-generation, ok-to-test, needs-priority, api-review, triage/accepted
- **变更说明：**
  为审计策略 (`--audit-policy-file`) 中的 `GroupResources` 规则添加通配符 (`*`) 支持，允许用户配置规则来匹配所有 API 组，便于过滤如 `*/status` 子资源产生的审计噪音。

### PR #135281: Standardize `PodDescriber` behavior to return `NotFound` errors consistently
- **链接：** https://github.com/kubernetes/kubernetes/pull/135281
- **状态：** closed
- **已合并：** 是
- **作者：** scaliby
- **标签：** kind/cleanup, area/kubectl, lgtm, release-note, size/S, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  统一 `PodDescriber` 的错误处理行为，使其与其他资源描述器一致，在 Pod 不存在时始终返回标准的 `NotFound` 错误，移除了通过 `-f` 标志查询时的特殊处理逻辑。

### PR #135283: kubectl explain: Add -r shorthand flag for --recursive
- **链接：** https://github.com/kubernetes/kubernetes/pull/135283
- **状态：** closed
- **已合并：** 是
- **作者：** laervn
- **标签：** area/kubectl, lgtm, release-note, size/XS, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, ok-to-test, triage/accepted
- **变更说明：**
  为 `kubectl explain` 命令添加 `-r` 短标志，作为 `--recursive` 参数的快捷方式，改善了命令行用户体验。

### PR #135309: Enhance content negotiation for zpages
- **链接：** https://github.com/kubernetes/kubernetes/pull/135309
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/test, kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, approved, cncf-cla: yes, sig/instrumentation, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  增强zpages的内容协商能力。该PR属于清理(cleanup)类别，涉及apiserver和测试框架，旨在改进zpages端点的内容协商机制。

### PR #135322: [1.36] Remove intree volume plugin portworx
- **链接：** https://github.com/kubernetes/kubernetes/pull/135322
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, area/kubelet, kind/cleanup, sig/scalability, sig/scheduling, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, area/dependency, triage/accepted
- **变更说明：**
  在Kubernetes 1.36版本中，移除树内(intree)存储插件portworx。这是一项重大的清理工作，属于API变更，旨在推进CSI迁移并减少代码维护负担。

### PR #135325: Fix queue hint for inter-pod anti-affinity
- **链接：** https://github.com/kubernetes/kubernetes/pull/135325
- **状态：** closed
- **已合并：** 是
- **作者：** brejman
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, release-note, size/M, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复inter-pod anti-affinity的queue hint问题。当具有反亲和性的Pod被删除时，被其阻塞的pending Pod应被重新排队。原逻辑中queue hint可能不正确，导致调度延迟，此PR确保正确触发重新调度。

### PR #135331: Bump etcd 3.6.6 sdk
- **链接：** https://github.com/kubernetes/kubernetes/pull/135331
- **状态：** closed
- **已合并：** 是
- **作者：** yashsingh74
- **标签：** kind/cleanup, sig/scheduling, area/apiserver, lgtm, area/cloudprovider, sig/node, sig/api-machinery, release-note, size/M, sig/auth, approved, cncf-cla: yes, priority/important-longterm, sig/cloud-provider, area/dependency, triage/accepted, sig/etcd, wg/device-management
- **变更说明：**
  升级etcd客户端SDK至版本3.6.6。这是一项依赖项更新和清理工作，涉及apiserver等多个组件。

### PR #135340: cbor: bump limits as the defaults are not large enough
- **链接：** https://github.com/kubernetes/kubernetes/pull/135340
- **状态：** closed
- **已合并：** 是
- **作者：** ricardomaraschini
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  修复CBOR解码时因默认元素数量限制（1024）过小而导致客户端报错的问题。提高了CBOR数组和映射的默认大小限制，以支持处理更大的列表。

### PR #135358: Sort runtime handlers list coming from the CRI runtime
- **链接：** https://github.com/kubernetes/kubernetes/pull/135358
- **状态：** closed
- **已合并：** 是
- **作者：** harche
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复来自CRI运行时的runtime handlers列表顺序不一致的问题。现对列表进行排序，避免因顺序问题导致kubelet配置出现非必要的漂移。

### PR #135367: Fix apiserver_watch_events_sizes metric.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135367
- **状态：** closed
- **已合并：** 是
- **作者：** mborsz
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复因性能优化而损坏的`apiserver_watch_events_sizes`指标。该指标曾因计量位置变更而严重低估watch流量（如对endpointslices对象的监听）。此次修复确保指标准确，并优化了性能关键路径上的计量开销。

### PR #135368: Scheduler: Fix GatedPods metric desync in unschedulable queue
- **链接：** https://github.com/kubernetes/kubernetes/pull/135368
- **状态：** closed
- **已合并：** 是
- **作者：** vshkrabkov
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复调度器中`GatedPods`指标在unschedulable队列中不同步的问题。当Pod从‘Ungated’状态变为‘Gated’状态时，原逻辑因优化提前返回，导致指标未更新。现通过检测状态转换并重新入队来确保指标准确性。

### PR #135393: Run PreBind plugins in parallel
- **链接：** https://github.com/kubernetes/kubernetes/pull/135393
- **状态：** closed
- **已合并：** 是
- **作者：** tosi3k
- **标签：** area/test, sig/scheduling, lgtm, sig/storage, sig/node, size/XL, kind/feature, release-note-action-required, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  支持在调度器框架中并行运行PreBind插件以降低绑定延迟。插件可通过PreBindPreFlight方法返回`AllowParallel: true`来选择并行执行；返回nil则保持原有串行行为。此变更需要插件开发者采取行动进行适配。

### PR #135418: add Workload permissions to view, edit and admin clusterroles
- **链接：** https://github.com/kubernetes/kubernetes/pull/135418
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** lgtm, release-note, size/S, kind/feature, sig/auth, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  为 admin、edit 和 view 这三个内置的 clusterroles 添加了 Workload 资源的权限。这是对 PR #134722 的补充，后者仅为 scheduler 添加了权限。

### PR #135462: Add atomic replace in client-go
- **链接：** https://github.com/kubernetes/kubernetes/pull/135462
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** lgtm, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  在 client-go 库中新增了原子替换（atomic replace）操作的支持。这是一个重要的 API machinery 特性，为客户端提供了更强大的资源更新能力。

### PR #135485: Fix device plugin admission failure after container restart
- **链接：** https://github.com/kubernetes/kubernetes/pull/135485
- **状态：** closed
- **已合并：** 是
- **作者：** saschagrunert
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, sig/testing, priority/important-longterm, kind/failing-test, triage/accepted
- **变更说明：**
  修复了 kubelet 重启后设备插件（device plugin）测试失败的问题。包含三个关键修复：修正容器运行状态判断逻辑、从 podresources 中过滤终端状态 Pod、以及改进测试中的错误处理。

### PR #135522: Promote workqueue metrics from ALPHA to BETA
- **链接：** https://github.com/kubernetes/kubernetes/pull/135522
- **状态：** closed
- **已合并：** 是
- **作者：** petern48
- **标签：** area/test, lgtm, release-note, size/L, kind/api-change, approved, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, ok-to-test, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将 workqueue 相关的指标从 ALPHA 稳定性级别提升至 BETA 级别。这是一个 API 变更，表明这些指标已趋于稳定，涉及 sig/instrumentation 和 sig/api-machinery。

### PR #135611: Fix flake TestDeviceTaintRule test
- **链接：** https://github.com/kubernetes/kubernetes/pull/135611
- **状态：** closed
- **已合并：** 是
- **作者：** Karthik-K-N
- **标签：** sig/scheduling, lgtm, release-note, size/L, kind/flake, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修复了 `TestDeviceTaintRule` 测试中的偶发性失败（flake）。这是一个针对调度器设备污点规则测试的稳定性修复。

### PR #135694: Update cri-tools to v1.35.0
- **链接：** https://github.com/kubernetes/kubernetes/pull/135694
- **状态：** closed
- **已合并：** 是
- **作者：** saschagrunert
- **标签：** kind/cleanup, lgtm, area/provider/gcp, sig/node, release-note, size/S, approved, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  将 cri-tools 依赖更新至 v1.35.0 版本。这是一个常规的清理/更新 PR，旨在保持项目依赖为最新。

### PR #135701: kubeadm: remove the usage of 2 deprecated flags for etcd < 3.6.0
- **链接：** https://github.com/kubernetes/kubernetes/pull/135701
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/backlog, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/L, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  kubeadm 清理：移除对 etcd < 3.6.0 版本的两个已弃用标志的使用。此举简化了代码并消除了对旧版 etcd 的支持。

### PR #135742: Kubeadm: Graduate NodeLocalCRISocket feature gate to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/135742
- **状态：** closed
- **已合并：** 是
- **作者：** HirazawaUi
- **标签：** lgtm, sig/cluster-lifecycle, release-note, size/L, kind/feature, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将 kubeadm 的 `NodeLocalCRISocket` 特性门控从 Beta 升级为 GA（正式发布）。该特性允许为每个节点配置独立的 CRI socket 路径。

### PR #135744: Add appProtocol to the service describe output
- **链接：** https://github.com/kubernetes/kubernetes/pull/135744
- **状态：** closed
- **已合并：** 是
- **作者：** ali-a-a
- **标签：** priority/backlog, area/kubectl, lgtm, release-note, size/M, kind/feature, approved, sig/cli, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  在 `kubectl describe service` 命令的输出中添加 `appProtocol` 字段的显示，增强了 Service 资源的可观察性。

### PR #135773: kubeadm: remove the FG ControlPlaneKubeletLocalMode
- **链接：** https://github.com/kubernetes/kubernetes/pull/135773
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/important-soon, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/S, kind/feature, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  移除已弃用的 `ControlPlaneKubeletLocalMode` 特性门控 (Feature Gate)。这是一个清理操作，因为该功能已稳定且默认启用。

### PR #135776: kubeadm: always retry Patch() Node API calls
- **链接：** https://github.com/kubernetes/kubernetes/pull/135776
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** lgtm, sig/cluster-lifecycle, release-note, size/M, kind/feature, approved, area/kubeadm, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  修改 kubeadm，使其在执行 Node API 的 `Patch()` 调用时始终进行重试，提高了在临时性 API 服务器问题下的操作鲁棒性。

### PR #135777: Enable WatchCacheInitializationPostStartHook by default
- **链接：** https://github.com/kubernetes/kubernetes/pull/135777
- **状态：** closed
- **已合并：** 是
- **作者：** serathius
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/XS, kind/feature, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将 `WatchCacheInitializationPostStartHook` 特性默认启用。该 Hook 用于优化 API Server 启动时的 Watch Cache 初始化过程。

### PR #135782: Add identifier-based queue depth metrics for RealFIFO
- **链接：** https://github.com/kubernetes/kubernetes/pull/135782
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/instrumentation, sig/testing, sig/architecture, area/code-generation, needs-priority, triage/accepted
- **变更说明：**
  为 RealFIFO 队列添加基于标识符的队列深度指标，增强了 APIServer 内部队列的监控和可观测性能力。

### PR #135997: Add negative validation for imageMinimumGCAge
- **链接：** https://github.com/kubernetes/kubernetes/pull/135997
- **状态：** closed
- **已合并：** 是
- **作者：** ngopalak-redhat
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/S, kind/api-change, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, api-review, needs-triage
- **变更说明：**
  为 kubelet 配置参数 `imageMinimumGCAge` 添加了负值验证，防止用户设置无效的负值。这是一个 API 变更，涉及代码生成和 kubelet 配置验证逻辑。

### PR #136086: Graduate watch_list_duration_seconds to BETA
- **链接：** https://github.com/kubernetes/kubernetes/pull/136086
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/test, area/kubelet, area/apiserver, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/api-change, approved, cncf-cla: yes, sig/instrumentation, sig/testing, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将 `watch_list_duration_seconds` 指标从 ALPHA 稳定性级别提升至 BETA 级别。该指标用于监控 watch list 操作的耗时，涉及 apiserver 和 kubelet 等多个组件。

---
*本报告由 Containerd Release Tracker 自动生成*
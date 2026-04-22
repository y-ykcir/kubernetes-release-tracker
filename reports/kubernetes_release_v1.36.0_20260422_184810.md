# Kubernetes 版本发布分析报告
## v1.36.0 (v1.36.0)

### 📋 版本信息
- **版本标签：** v1.36.0
- **版本名称：** v1.36.0
- **发布时间：** 2026-04-22T17:57:14Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.36.0

### 🔍 分析统计
- **分析时间：** 2026-04-22 18:48:10
- **分析的 PR 数量：** 46
- **分析的 Issue 数量：** 16
- **重要项目数量：** 57

## 📊 版本概述
Kubernetes v1.36.0 是一个以性能优化、API 现代化和安全性增强为核心的版本，引入了调度器并行绑定、多项功能废弃和重要的 Bug 修复，升级前需重点关注监控指标变更和废弃 API 的迁移。

## 🔒 安全问题修复
1. ⚠️ 为动态资源分配（DRA）ResourceClaim 状态更新引入细粒度授权检查 - [PR #134947](https://github.com/kubernetes/kubernetes/pull/134947) - **风险级别：** 中 - **影响：** 默认启用，防止 DRA 插件越权更新其他驱动或节点的资源状态，符合最小权限原则。使用 DRA 的集群需审核并更新相关 ServiceAccount 的 RBAC 权限。
2. ⚠️ 修复 client-go CA 证书重载问题，提升 CA 轮换期间的连接安全性 - [PR #132922](https://github.com/kubernetes/kubernetes/pull/132922) - **风险级别：** 低 - **影响：** 非直接漏洞修复，但增强了证书自动轮换的可靠性，减少了因证书过期导致的服务中断窗口。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 NodeResourcesFit 插件在配置缺失 `RequestedToCapacityRatio` 字段时的空指针崩溃问题 - [PR #132120](https://github.com/kubernetes/kubernetes/pull/132120) - **影响：** 修复了可能导致调度器崩溃的配置错误，提升稳定性。
2. 修复静态 Pod 在 Init 容器被垃圾回收后状态卡在 `Init:0/1` 的问题 - [PR #131317](https://github.com/kubernetes/kubernetes/pull/131317) - **影响：** 确保静态 Pod（如控制平面组件）在异常重启后能正确报告运行状态。
3. 修复 client-go 在集群 CA 轮换后不重新加载信任根证书的问题 - [PR #132922](https://github.com/kubernetes/kubernetes/pull/132922) - **影响：** 使用 InClusterConfig 的客户端在 CA 轮换后无需重启即可自动恢复连接，对集群维护至关重要。
4. 修复 kubelet 在通过 IP 地址连接时证书不重载的问题 - [PR #133654](https://github.com/kubernetes/kubernetes/pull/133654) - **影响：** 确保 kubelet 证书轮换后，API Server 等组件能重新建立安全连接。
5. 修复 `kubectl attach` 命令不支持 `--detach-keys` 参数的问题 - [PR #134997](https://github.com/kubernetes/kubernetes/pull/134997) - **影响：** 用户现在可以自定义退出 attach 会话的按键组合，提升使用体验。
6. 修复 Pod 亲和性队列提示（Queue Hint）遗漏已存在 Pod 反亲和性场景的问题 - [PR #135325](https://github.com/kubernetes/kubernetes/pull/135325) - **影响：** 提升了调度器在 Pod 反亲和性场景下重新调度等待 Pod 的响应速度。
7. 修复 VolumeAttachment 在 CSI 驱动 `attachRequired` 从 true 变为 false 后无法清理的问题 - [PR #129664](https://github.com/kubernetes/kubernetes/pull/129664) - **影响：** 避免存储资源泄漏，确保 CSI 驱动配置变更后资源清理正常。

## 💥 破坏性变更
1. 🚨 ACTION REQUIRED: 将 kube-controller-manager 监控指标 `volume_operation_total_errors` 重命名为 `volume_operation_errors_total` - [PR #136399](https://github.com/kubernetes/kubernetes/pull/136399) - **影响：** 所有基于旧指标名称 `volume_operation_total_errors` 的自定义监控仪表板、告警规则或自动化脚本必须更新为使用新名称 `volume_operation_errors_total`，否则将无法获取数据。
2. 🚨 将 API Server admission 子系统中的 `sets.String` 类型替换为 `sets.Set[string]` - [PR #134044](https://github.com/kubernetes/kubernetes/pull/134044) - **影响：** 直接导入并使用 `k8s.io/apiserver/pkg/admission/plugin/namespace/lifecycle` 包中 `NewLifecycle` 函数等公共 API 的客户端代码需要更新类型。
3. 🚨 废弃并重命名 `kuberc` 凭证插件配置中的 `name` 字段为 `command` - [PR #137272](https://github.com/kubernetes/kubernetes/pull/137272) - **影响：** 使用该配置文件的工具需要更新配置文件格式。
4. 🚨 封装 `fieldsv1` 并废弃直接使用 `Raw` 字段 - [PR #137304](https://github.com/kubernetes/kubernetes/pull/137304) - **影响：** 直接操作 `ManagedFields` 底层 `Raw` 数据的客户端库或工具需要改用新增的访问器方法，以确保兼容性。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 调度器 PreBind 插件支持并行执行以降低绑定延迟 - [PR #135393](https://github.com/kubernetes/kubernetes/pull/135393) - **影响：** 自定义调度器插件需更新 `PreBindPreFlight` 方法以返回 `PreBindPreFlightResult` 并设置 `AllowParallel: true` 才能利用此优化。
2. 废弃 Service.spec.externalIPs 字段并添加警告 - [PR #137293](https://github.com/kubernetes/kubernetes/pull/137293) - **影响：** 使用此字段的服务将在日志中收到警告，需规划替代方案（如 LoadBalancer 或 Ingress）。
3. 锁定 gitRepo 卷驱动为禁用状态（正式废弃） - [PR #136400](https://github.com/kubernetes/kubernetes/pull/136400) - **影响：** 创建使用 `gitRepo` 卷的 Pod 将失败，需迁移至其他方案（如 InitContainer + git clone）。
4. 将凭证插件配置字段从 `name` 重命名为 `command` 以与 kubeconfig 保持一致 - [PR #137272](https://github.com/kubernetes/kubernetes/pull/137272) - **影响：** 使用 `kuberc` 配置文件的工具需要更新字段名。
5. 为动态资源分配（DRA）ResourceClaim 状态更新引入细粒度授权 - [PR #134947](https://github.com/kubernetes/kubernetes/pull/134947) - **影响：** DRA 驱动和控制器需要新的 RBAC 权限来更新 `status.allocation` 和 `status.devices` 子资源。
6. 新增 Kubelet gRPC API 用于查询节点本地 Pod 信息 - [PR #134627](https://github.com/kubernetes/kubernetes/pull/134627) - **影响：** 为监控、调试工具提供了更高效的 Pod 信息获取方式。
7. 引入 Pod 级别资源管理器（Alpha） - [PR #134768](https://github.com/kubernetes/kubernetes/pull/134768) - **影响：** 为未来更精细的资源管理（如 Pod 级别的 CPU、内存管理器）奠定基础，需启用特性门控。

## 🚀 性能优化
1. 调度器 PreBind 插件支持并行执行 - [PR #135393](https://github.com/kubernetes/kubernetes/pull/135393) - **提升：** 可显著降低 Pod 绑定阶段的延迟，尤其当使用多个串行 PreBind 插件时。
2. 新增 Kubelet gRPC API 用于高效查询节点本地 Pod 信息 - [PR #134627](https://github.com/kubernetes/kubernetes/pull/134627) - **提升：** 为节点级监控和调试工具提供了比 List-Watch 更轻量、更快速的数据获取通道。
3. DaemonSet 控制器新增陈旧性检测机制 - [PR #134937](https://github.com/kubernetes/kubernetes/pull/134937) - **提升：** 有助于更快地检测和处理因控制器状态不同步导致的 DaemonSet Pod 异常，提升系统自愈能力。
4. 线程安全存储（ThreadSafeStore）增加资源版本查询和书签支持 - [PR #134827](https://github.com/kubernetes/kubernetes/pull/134827) - **提升：** 为客户端缓存等场景提供更高效、准确的增量数据同步能力。

## 🎯 风险评估
整体风险评估：**中等**。

此版本包含一个必须处理的**紧急变更**（指标重命名）和多项API废弃及破坏性变更，但核心功能稳定，且包含大量重要的Bug修复和性能提升。

**建议升级时机：** 建议在完成对监控配置、自定义插件和废弃API使用情况的全面审计，并在预发布/测试环境中进行充分验证（至少1-2个迭代周期）后，安排生产环境升级。

**需要特别关注的方面：**
1.  **监控中断风险：** 忽略指标重命名变更将导致相关监控失效。
2.  **调度器兼容性：** 自定义调度器插件需适配并行PreBind接口。
3.  **废弃功能依赖：** 依赖 `gitRepo` 卷或 `Service.spec.externalIPs` 的工作负载将在未来版本中完全失效，需优先迁移。
4.  **权限模型变更：** DRA用户需提前更新RBAC配置，否则可能导致资源分配失败。

## 📋 升级建议
1. **立即行动：** 检查并更新所有监控系统中引用的 `volume_operation_total_errors` 指标，将其改为 `volume_operation_errors_total`。
2. **升级前测试：** 如果使用了自定义调度器插件，请在测试环境中验证插件在 PreBind 阶段并行执行下的兼容性与性能。
3. **审计与迁移：** 扫描集群中是否仍在使用 `Service.spec.externalIPs` 或 `gitRepo` 卷，并制定迁移计划。对于 `gitRepo`，立即寻找替代方案。
4. **权限审核：** 如果使用动态资源分配（DRA），审核并更新相关控制器和插件的 RBAC 权限，确保其拥有新的 `resourceclaims/binding` 和 `resourceclaims/devices` 子资源更新权限。
5. **客户端库更新：** 检查内部工具或控制器是否直接引用了 `sets.String` 或 `fieldsv1.Raw` 等已变更的 API，并计划升级客户端库代码。
6. **利用新特性：** 考虑评估新的 Kubelet gRPC API 和 Pod 级别资源管理器（Alpha），看是否能优化现有的监控或资源管理流程。

## 📋 Release 包含的变更

### PR #10: Move everything out of src and reorganize scripts.
- **链接：** https://github.com/kubernetes/kubernetes/pull/10
- **状态：** closed
- **已合并：** 是
- **作者：** jbeda
- **变更说明：**
  重构项目结构，将内容移出src目录并重组脚本。优化脚本健壮性，将e2e测试实例类型改为g1-small，更新文档以反映脚本新位置，并禁用未经充分测试且缺少cloudcfg工具的'curl | bash'集群启动方式。

### PR #5055: Start cluster management doc
- **链接：** https://github.com/kubernetes/kubernetes/pull/5055
- **状态：** closed
- **已合并：** 是
- **作者：** lavalamp
- **变更说明：**
  **PR #5055:** Start cluster management doc

### PR #129664: Fix VolumeAttachment cleanup when AttachRequired changes
- **链接：** https://github.com/kubernetes/kubernetes/pull/129664
- **状态：** closed
- **已合并：** 是
- **作者：** hkttty2009
- **标签：** kind/bug, area/test, lgtm, sig/storage, release-note, size/L, approved, cncf-cla: yes, sig/testing, lifecycle/rotten, ok-to-test, needs-priority, area/e2e-test-framework, needs-triage
- **变更说明：**
  修复存储子系统bug：解决当CSI驱动器的AttachRequired属性从true变为false时，已创建的VolumeAttachment对象无法被正确清理的遗留问题。通过绕过插件查找直接传递volumeName来修复。

### PR #130231: Update ImageLocality plugin to account ImageVolume images
- **链接：** https://github.com/kubernetes/kubernetes/pull/130231
- **状态：** closed
- **已合并：** 是
- **作者：** Barakmor1
- **标签：** sig/scheduling, lgtm, release-note, size/M, kind/feature, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  增强调度器`ImageLocality`插件，使其在计算节点镜像 locality 分数时，将Pod使用的`ImageVolume`镜像也纳入考量。

### PR #131068: Switch sample-controller to use NewClientset supporting applyconfiguration rather than deprecated NewSimpleClientset
- **链接：** https://github.com/kubernetes/kubernetes/pull/131068
- **状态：** closed
- **已合并：** 是
- **作者：** soltysh
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/XL, kind/api-change, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, triage/accepted
- **变更说明：**
  该PR将sample-controller从已弃用的`NewSimpleClientset`切换为支持applyconfiguration的新`NewClientset`。这是一个API变更/bug修复，遵循了代码生成客户端的更新建议，并修复了fake客户端与正确schema的兼容性问题。

### PR #131317: Fix:Static pod status is always Init:0/1 if unable to get init container status
- **链接：** https://github.com/kubernetes/kubernetes/pull/131317
- **状态：** closed
- **已合并：** 是
- **作者：** bitoku
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  修复kubelet bug：当无法获取init容器状态时，静态Pod（Static Pod）的状态不再错误地显示为'Init:0/1'，而是能正确反映Pod的实际阶段（如Pending、Running）。

### PR #131744: Add ResourceSlices field to kubectl describe node
- **链接：** https://github.com/kubernetes/kubernetes/pull/131744
- **状态：** closed
- **已合并：** 是
- **作者：** ArangoGutierrez
- **标签：** area/kubectl, lgtm, release-note, size/L, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  功能增强：在`kubectl describe node`命令的输出中添加`ResourceSlices`字段的显示。ResourceSlices是用于节点资源拓扑管理的新API资源，此变更增强了节点资源信息的可观察性。

### PR #131950: PodStartSLIDuration should exclude init container runtime, image pulling time, stateful pods, not immediately schedulable pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/131950
- **状态：** closed
- **已合并：** 是
- **作者：** alimaazamat
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/XL, approved, cncf-cla: yes, priority/important-longterm, tide/merge-method-squash, ok-to-test, area/dependency, triage/accepted
- **变更说明：**
  修复`PodStartSLIDuration`指标计算，使其排除init容器运行时间、镜像拉取时间、StatefulSet Pod以及非立即可调度Pod的耗时，以更准确反映Pod启动延迟。

### PR #132120: fix the noderesourcefit plugin's nil pointer by validating RequestedToCapacityRatio config
- **链接：** https://github.com/kubernetes/kubernetes/pull/132120
- **状态：** closed
- **已合并：** 是
- **作者：** flpanbin
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/M, kind/api-change, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复NodeResourceFit插件因`RequestedToCapacityRatio`配置为空而导致的nil指针崩溃问题，通过添加配置验证来防止。

### PR #132402: Add node `arch` in the kubectl get node output
- **链接：** https://github.com/kubernetes/kubernetes/pull/132402
- **状态：** closed
- **已合并：** 是
- **作者：** astraw99
- **标签：** kind/documentation, lgtm, release-note, size/M, kind/feature, approved, sig/cli, cncf-cla: yes, priority/important-longterm, needs-triage
- **变更说明：**
  在`kubectl get node -owide`命令的输出表格中新增`ARCH`列，用于显示节点的CPU架构信息（如amd64, arm64）。

### PR #132807: [KEP-5365] Implement Image Volume with Digest
- **链接：** https://github.com/kubernetes/kubernetes/pull/132807
- **状态：** closed
- **已合并：** 是
- **作者：** iholder101
- **标签：** area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  该PR实现了KEP-5365，为Image Volume添加了摘要（Digest）支持。这是一个API变更/功能，将镜像卷的摘要信息添加到容器状态中，增强了镜像内容的可追溯性。

### PR #132922: Fix the client-go issue of reloading trust root CAs.
- **链接：** https://github.com/kubernetes/kubernetes/pull/132922
- **状态：** closed
- **已合并：** 是
- **作者：** yt2985
- **标签：** kind/bug, area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/node, sig/api-machinery, release-note, size/XXL, area/release-eng, sig/auth, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/testing, sig/release, sig/architecture, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, area/dependency, triage/accepted, wg/device-management
- **变更说明：**
  该PR修复了client-go在重新加载信任根CA（trust root CAs）时的问题。这是一个影响广泛的bug修复，确保在证书更新后，客户端能正确刷新连接，涉及多个组件（kubelet、apiserver等）。

### PR #133335: pluginmanager: fix handling registration failures
- **链接：** https://github.com/kubernetes/kubernetes/pull/133335
- **状态：** closed
- **已合并：** 是
- **作者：** bart0sh
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/storage, sig/node, release-note, size/M, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复kubelet pluginmanager的bug：改进插件注册失败的处理，当注册或状态通知失败时，会从实际状态中移除插件并尝试取消注册。新增了指数退避重试机制（初始500ms，最大约2分钟），防止故障插件导致拒绝服务。

### PR #133654: Fix kubelet certificate reload when connecting by IP address
- **链接：** https://github.com/kubernetes/kubernetes/pull/133654
- **状态：** closed
- **已合并：** 是
- **作者：** kwohlfahrt
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, sig/api-machinery, release-note, size/L, sig/auth, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  修复kubelet bug：解决当通过IP地址连接时，kubelet证书重载功能失效的问题。确保在证书轮换后，使用IP地址的客户端连接也能使用新证书进行认证。

### PR #133845: Clarify CPUCFSQuotaPeriod config vs CustomCPUCFSQuotaPeriod feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/133845
- **状态：** closed
- **已合并：** 是
- **作者：** rbiamru
- **标签：** area/kubelet, kind/documentation, kind/cleanup, lgtm, sig/node, release-note, size/XS, kind/api-change, area/release-eng, approved, cncf-cla: yes, priority/important-longterm, sig/release, area/code-generation, ok-to-test, triage/accepted
- **变更说明：**
  澄清kubelet配置字段`cpuCFSQuotaPeriod`与特性门`CustomCPUCFSQuotaPeriod`的关系，更新代码注释、flag帮助文本和OpenAPI描述以消除混淆，不涉及字段重命名。

### PR #134044: Replace deprecated sets.String with sets.Set[string] in apiserver
- **链接：** https://github.com/kubernetes/kubernetes/pull/134044
- **状态：** closed
- **已合并：** 是
- **作者：** mcallzbl
- **标签：** kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, approved, cncf-cla: yes, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  在apiserver admission子系统中，将已弃用的`sets.String`类型替换为通用的`sets.Set[string]`，涉及7个文件，对`NewLifecycle`函数签名有破坏性变更。

### PR #134290: Do not get PV for externally deleting volume
- **链接：** https://github.com/kubernetes/kubernetes/pull/134290
- **状态：** closed
- **已合并：** 是
- **作者：** huww98
- **标签：** kind/cleanup, lgtm, sig/storage, release-note, size/M, sig/apps, approved, cncf-cla: yes, lifecycle/stale, needs-priority, needs-triage
- **变更说明：**
  优化存储控制器逻辑，当检测到卷被外部删除时，避免不必要的PersistentVolume (PV) API获取操作，减少冗余调用。

### PR #134394: kube-dns bump to v1.26.7
- **链接：** https://github.com/kubernetes/kubernetes/pull/134394
- **状态：** closed
- **已合并：** 是
- **作者：** toredash
- **标签：** kind/cleanup, lgtm, area/provider/gcp, size/S, release-note-none, approved, cncf-cla: yes, sig/cloud-provider, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  将kube-dns依赖项版本升级至v1.26.7，属于常规维护性更新。

### PR #134422: ingressclass: show (default) marker for default IngressClass
- **链接：** https://github.com/kubernetes/kubernetes/pull/134422
- **状态：** closed
- **已合并：** 是
- **作者：** jaehanbyun
- **标签：** sig/network, lgtm, release-note, size/M, kind/feature, approved, sig/cli, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  在`kubectl get ingressclass`命令的输出中，为默认的IngressClass添加`(default)`标记，与`kubectl get storageclass`行为保持一致。

### PR #134556: lock the feature-gate VolumeAttributesClass to default (true)
- **链接：** https://github.com/kubernetes/kubernetes/pull/134556
- **状态：** closed
- **已合并：** 是
- **作者：** carlory
- **标签：** area/test, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, api-review, needs-triage, sig/etcd, wg/device-management
- **变更说明：**
  将特性门`VolumeAttributesClass`的状态锁定为默认启用（true），标志着该特性进入稳定阶段。

### PR #134627: [KEP-4188] New Kubelet gRPC API returning node-local Pod info
- **链接：** https://github.com/kubernetes/kubernetes/pull/134627
- **状态：** closed
- **已合并：** 是
- **作者：** briansonnenberg
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, priority/important-longterm, ok-to-test, api-review, area/dependency, triage/accepted
- **变更说明：**
  根据KEP-4188，在Kubelet中实现新的gRPC API，用于向其他组件提供运行在该节点上的Pod信息。

### PR #134660: [KEP-3085] kubelet - extend RuntimeHelper interface with `OnPodSandboxReady` to update `PodReadyToStartContainers` condition correctly
- **链接：** https://github.com/kubernetes/kubernetes/pull/134660
- **状态：** closed
- **已合并：** 是
- **作者：** Priyankasaggu11929
- **标签：** kind/bug, area/test, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/XL, sig/apps, approved, cncf-cla: yes, sig/testing, triage/accepted
- **变更说明：**
  该PR扩展了kubelet的RuntimeHelper接口，添加了`OnPodSandboxReady`方法，以正确更新Pod的`PodReadyToStartContainers`条件。这是一个bug修复，解决了Pod沙箱就绪后状态条件更新不正确的问题。

### PR #134675: Enforce either optional or required tag on apiserverinternal API group
- **链接：** https://github.com/kubernetes/kubernetes/pull/134675
- **状态：** closed
- **已合并：** 是
- **作者：** JoelSpeed
- **标签：** lgtm, sig/storage, sig/node, sig/api-machinery, release-note, size/M, kind/api-change, sig/auth, sig/apps, approved, cncf-cla: yes, area/code-generation, needs-priority, api-review, triage/accepted
- **变更说明：**
  该PR强制执行API规范，要求apiserverinternal API组中的字段必须明确标记为`optional`或`required`标签。这是一个API变更，旨在提高API定义的一致性和清晰度。

### PR #134701: Make ConcurrentResourceClaimSyncs configurable
- **链接：** https://github.com/kubernetes/kubernetes/pull/134701
- **状态：** closed
- **已合并：** 是
- **作者：** anson627
- **标签：** area/test, lgtm, sig/node, sig/api-machinery, release-note, size/L, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, priority/important-longterm, area/code-generation, tide/merge-method-squash, ok-to-test, api-review, triage/accepted, wg/device-management
- **变更说明：**
  该PR使ResourceClaim控制器的并发同步数（ConcurrentResourceClaimSyncs）可配置。这是一个API变更/功能，旨在支持大规模训练作业（如10k Pods on 10k Nodes），增加了配置选项、验证逻辑和单元测试。

### PR #134768: [PodLevelResourceManagers] Pod Level Resource Managers - Alpha
- **链接：** https://github.com/kubernetes/kubernetes/pull/134768
- **状态：** closed
- **已合并：** 是
- **作者：** KevinTMtz
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/XXL, kind/feature, approved, cncf-cla: yes, sig/testing, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  该PR引入了Pod Level Resource Managers的Alpha实现。这是一个大型功能，为kubelet提供了新的资源管理架构，支持插件化的Pod级别资源管理器。

### PR #134827: Add Resource Version query and Bookmarks to thread safe store
- **链接：** https://github.com/kubernetes/kubernetes/pull/134827
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, lgtm, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  该PR为线程安全存储（thread safe store）添加了Resource Version查询和Bookmarks支持。这是一个功能增强，旨在改进API服务器的列表和监视能力。

### PR #134849: kubectl label: Add 'modified' output version
- **链接：** https://github.com/kubernetes/kubernetes/pull/134849
- **状态：** closed
- **已合并：** 是
- **作者：** tchap
- **标签：** kind/bug, priority/backlog, area/kubectl, lgtm, release-note, size/L, approved, sig/cli, cncf-cla: yes, triage/accepted
- **变更说明：**
  该PR修复了`kubectl label`命令的输出问题。当标签同时被添加和移除时，现在会正确输出‘modified’信息，而不是随机显示‘labeled’或‘unlabeled’。这是一个bug修复。

### PR #134937: Daemonset controller staleness detection
- **链接：** https://github.com/kubernetes/kubernetes/pull/134937
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XL, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, area/e2e-test-framework, triage/accepted, wg/device-management
- **变更说明：**
  该PR为DaemonSet控制器添加了陈旧性检测（staleness detection）功能。这是一个新功能，通过比较时间戳来识别并处理过时的Pod状态，提高控制器可靠性。

### PR #134947: Fine-grained Authorization for ResourceClaim Status Updates
- **链接：** https://github.com/kubernetes/kubernetes/pull/134947
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** area/test, area/kubelet, sig/scheduling, area/apiserver, lgtm, sig/node, sig/api-machinery, size/XXL, kind/api-change, kind/feature, release-note-action-required, sig/auth, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, area/code-generation, needs-priority, area/dependency, needs-triage, wg/device-management
- **变更说明：**
  该PR基于KEP-4817，为Dynamic Resource Allocation (DRA)的ResourceClaim状态更新实现了细粒度授权。这是一个API变更，引入了新的子资源（如`resourceclaims/binding`）权限控制，并通过`DRAResourceClaimGranularStatusAuthorization`特性门控（Beta，默认1.36启用）来增强安全性。

### PR #134981: kubelet: drop cpu load metrics from container metrics test
- **链接：** https://github.com/kubernetes/kubernetes/pull/134981
- **状态：** closed
- **已合并：** 是
- **作者：** haircommander
- **标签：** kind/bug, area/test, area/kubelet, lgtm, sig/node, release-note, size/XS, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  该PR从容器指标测试中移除了CPU负载（cpu load）指标。这是一个小型的bug修复/清理，因为这些指标不稳定且已弃用，旨在提高测试的稳定性。

### PR #134997: Add `--detach-keys` for `kubectl attach` command
- **链接：** https://github.com/kubernetes/kubernetes/pull/134997
- **状态：** closed
- **已合并：** 是
- **作者：** yangjunmyfm192085
- **标签：** kind/bug, priority/important-soon, area/kubectl, lgtm, sig/api-machinery, release-note, size/L, approved, sig/cli, cncf-cla: yes, needs-triage
- **变更说明：**
  该PR为`kubectl attach`命令添加了`--detach-keys`选项。这是一个bug修复/功能增强，允许用户自定义从容器会话分离的按键序列，与Docker CLI行为对齐。

### PR #135126: scheduler: add metric for pods scheduled after flush
- **链接：** https://github.com/kubernetes/kubernetes/pull/135126
- **状态：** closed
- **已合并：** 是
- **作者：** mrvarmazyar
- **标签：** sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  该PR为调度器添加了一个新的ALPHA稳定性度量指标`scheduler_pod_scheduled_after_flush_total`。这是一个功能，用于追踪因超时（默认5分钟）从`unschedulablePods`队列刷新后成功调度的Pod数量，帮助检测潜在的队列提示或事件处理问题。

### PR #135148: kubeadm: add --allow-deprecated-api to 'config validate'
- **链接：** https://github.com/kubernetes/kubernetes/pull/135148
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** kind/bug, lgtm, sig/cluster-lifecycle, release-note, size/M, kind/feature, approved, area/kubeadm, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  该PR为`kubeadm config validate`命令添加了`--allow-deprecated-api`选项。这是一个bug修复/功能增强，允许在验证配置时包含已弃用的API版本，提高了命令的灵活性。

### PR #135227: Inverting DRAOperationsDuration metric by inverting 'is_error' label.
- **链接：** https://github.com/kubernetes/kubernetes/pull/135227
- **状态：** closed
- **已合并：** 是
- **作者：** hime
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRAOperationsDuration监控指标：通过反转`is_error`标签的逻辑，确保该指标能正确反映Device Plugin API操作的成功与失败时长，便于监控和分析。

### PR #135281: Standardize `PodDescriber` behavior to return `NotFound` errors consistently
- **链接：** https://github.com/kubernetes/kubernetes/pull/135281
- **状态：** closed
- **已合并：** 是
- **作者：** scaliby
- **标签：** kind/cleanup, area/kubectl, lgtm, release-note, size/S, approved, sig/cli, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  清理：统一`PodDescriber`的错误处理行为，使其与其他资源描述器一致。移除通过`-f`标志查询已删除Pod时尝试获取事件的特殊逻辑，现在始终返回标准的'NotFound'错误，提高了一致性和代码简洁性。

### PR #135309: Enhance content negotiation for zpages
- **链接：** https://github.com/kubernetes/kubernetes/pull/135309
- **状态：** closed
- **已合并：** 是
- **作者：** richabanker
- **标签：** area/test, kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, approved, cncf-cla: yes, sig/instrumentation, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  清理/增强：改进apiserver中zpages（调试页面）的内容协商（Content Negotiation）能力，使其能更好地处理不同的Accept请求头，支持更灵活的格式输出。

### PR #135325: Fix queue hint for inter-pod anti-affinity
- **链接：** https://github.com/kubernetes/kubernetes/pull/135325
- **状态：** closed
- **已合并：** 是
- **作者：** brejman
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, release-note, size/M, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复调度器bug：当存在互斥Pod亲和性（inter-pod anti-affinity）时，修正因Pod删除而触发的队列提示（queue hint）逻辑，确保待调度Pod能被正确重新加入调度队列。

### PR #135393: Run PreBind plugins in parallel
- **链接：** https://github.com/kubernetes/kubernetes/pull/135393
- **状态：** closed
- **已合并：** 是
- **作者：** tosi3k
- **标签：** area/test, sig/scheduling, lgtm, sig/storage, sig/node, size/XL, kind/feature, release-note-action-required, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  功能增强：支持在kube-scheduler框架中并行运行PreBind插件以降低绑定延迟。需要插件通过PreBindPreFlight方法返回`AllowParallel: true`来启用此行为，否则保持串行执行。这是一个需要用户注意的变更（action required）。

### PR #135485: Fix device plugin admission failure after container restart
- **链接：** https://github.com/kubernetes/kubernetes/pull/135485
- **状态：** closed
- **已合并：** 是
- **作者：** saschagrunert
- **标签：** area/test, area/kubelet, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, sig/testing, priority/important-longterm, kind/failing-test, triage/accepted
- **变更说明：**
  修复kubelet设备插件相关bug：解决kubelet重启后设备插件测试失败的问题。具体包括：修正容器运行状态判断逻辑、在podresources接口中过滤已终止的Pod、以及改进测试中的错误处理以避免轮询提前退出。

### PR #136360: Add metric component and endpoint to metric reference docs
- **链接：** https://github.com/kubernetes/kubernetes/pull/136360
- **状态：** closed
- **已合并：** 是
- **作者：** skl
- **标签：** area/test, kind/documentation, lgtm, release-note, size/XXL, approved, cncf-cla: yes, sig/instrumentation, sig/testing, ok-to-test, needs-priority, triage/accepted
- **变更说明：**
  在自动生成的指标参考文档中，为每个指标添加其所属的组件（如kube-apiserver）和暴露端点信息，提升文档实用性。

### PR #136399: Rename metric `volume_operation_total_errors` to `volume_operation_errors_total`
- **链接：** https://github.com/kubernetes/kubernetes/pull/136399
- **状态：** closed
- **已合并：** 是
- **作者：** tico88612
- **标签：** area/test, lgtm, sig/storage, size/M, kind/feature, release-note-action-required, sig/apps, approved, cncf-cla: yes, sig/instrumentation, sig/testing, needs-priority, triage/accepted, area/stable-metrics
- **变更说明：**
  将指标`volume_operation_total_errors`重命名为符合命名规范的`volume_operation_errors_total`，并标记旧指标为弃用，用户需更新监控配置。

### PR #136400: KEP:5040 Lock gitRepo Volume Driver to disabled.
- **链接：** https://github.com/kubernetes/kubernetes/pull/136400
- **状态：** closed
- **已合并：** 是
- **作者：** vinayakankugoyal
- **标签：** lgtm, sig/storage, release-note, size/S, approved, cncf-cla: yes, needs-priority, kind/deprecation, needs-triage
- **变更说明：**
  根据KEP-5040，将`gitRepo`卷驱动锁定为禁用状态，以弃用此不安全的卷类型。

### PR #137272: Rename `name` to `command` in kuberc credentialPluginAllowlist entries
- **链接：** https://github.com/kubernetes/kubernetes/pull/137272
- **状态：** closed
- **已合并：** 是
- **作者：** pmengelbert
- **标签：** area/test, priority/important-soon, kind/cleanup, area/kubectl, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, sig/auth, approved, sig/cli, cncf-cla: yes, sig/testing, area/code-generation, kind/deprecation, triage/accepted
- **变更说明：**
  API变更：将kuberc配置文件中credentialPluginAllowlist条目的字段名从`name`重命名为`command`，以更准确地反映其用途。这是一个清理性质的变更，涉及kubectl和API machinery。

### PR #137293: KEP-5707: Deprecate Service.spec.externalIPs
- **链接：** https://github.com/kubernetes/kubernetes/pull/137293
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** sig/network, area/kube-proxy, lgtm, release-note, size/M, kind/api-change, sig/apps, approved, sig/windows, cncf-cla: yes, area/ipvs, needs-priority, kind/deprecation, needs-triage
- **变更说明：**
  根据KEP-5707第一阶段，弃用Service.spec.externalIPs字段。该字段存在安全风险（如中间人攻击），将在未来版本中移除。当前版本会添加警告和弃用声明。

### PR #137304: refactor: fieldsv1 encapsulation via accessors and deprecation of direct "Raw" field usage
- **链接：** https://github.com/kubernetes/kubernetes/pull/137304
- **状态：** closed
- **已合并：** 是
- **作者：** aaron-prindle
- **标签：** area/test, kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, kind/api-change, sig/apps, approved, cncf-cla: yes, sig/testing, needs-priority, kind/deprecation, triage/accepted
- **变更说明：**
  重构：通过访问器封装fieldsv1，并弃用直接使用`Raw`字段。这是一个API变更和清理，旨在改善代码封装性，为未来移除直接字段访问做准备，影响范围较大（size/XL）。

### PR #137909: Switch PLEGOnDemandRelist default to `false` for 1.36
- **链接：** https://github.com/kubernetes/kubernetes/pull/137909
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/S, kind/flake, approved, cncf-cla: yes, kind/failing-test, needs-priority, needs-triage
- **变更说明：**
  由于PR #137362导致测试"should never report container start when an init container fails"失败率急剧上升，加剧了containerd上游问题（PR #13049），因此将PLEGOnDemandRelist特性在1.36版本的默认值从true改回false。

---
*本报告由 Containerd Release Tracker 自动生成*
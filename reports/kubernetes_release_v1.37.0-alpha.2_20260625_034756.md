# Kubernetes 版本发布分析报告
## v1.37.0-alpha.2 (v1.37.0-alpha.2)

### 📋 版本信息
- **版本标签：** v1.37.0-alpha.2
- **版本名称：** v1.37.0-alpha.2
- **发布时间：** 2026-06-25T02:40:51Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.37.0-alpha.2

### 🔍 分析统计
- **分析时间：** 2026-06-25 03:47:56
- **分析的 PR 数量：** 32
- **分析的 Issue 数量：** 14
- **重要项目数量：** 44

## 📊 版本概述
Kubernetes v1.37.0-alpha.2 是一个早期开发版本，主要引入了工作负载感知调度（Workload-aware Scheduling）的重大API演进、关键的网络与节点稳定性修复，以及多项性能优化，为生产环境未来升级提供了重要的技术预览。

## 🔒 安全问题修复
1. ⚠️ client-go证书管理器硬编码ECDSA P-256密钥类型，无法配置为匹配集群CA的密钥类型 - [Issue #138987](https://github.com/kubernetes/kubernetes/issues/138987) - **风险级别：** 中 - 可能导致密钥类型不匹配，影响证书兼容性
2. ⚠️ API服务器在准入控制器Pod终止后仍保持TCP连接，可能向正在终止的Pod发送请求 - [Issue #127335](https://github.com/kubernetes/kubernetes/issues/127335) - **风险级别：** 中 - 可能破坏优雅关闭，导致请求失败或延迟

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复节点关闭管理器的dbus连接泄漏，该问题会导致线程耗尽和kubelet崩溃 - [PR #137141](https://github.com/kubernetes/kubernetes/pull/137141) - **影响：** 长时间运行后可能导致kubelet因线程耗尽而崩溃，影响节点稳定性
2. 修复Job控制器在Pod创建回退期间错误报告active=0，导致Pod卡在Terminating状态且Job状态更新失败 - [PR #139457](https://github.com/kubernetes/kubernetes/pull/139457) - **影响：** 使用指数退避的Job可能无法正确更新状态，导致Pod清理延迟
3. 修复kube-proxy无法清理无端点的UDP服务的陈旧conntrack条目，导致流量黑洞 - [PR #139629](https://github.com/kubernetes/kubernetes/pull/139629) - **影响：** 缩容到零端点的UDP服务（如statsd）流量可能被错误地DNAT到已删除的Pod IP，造成服务中断
4. 修复使用subPath挂载的Pod在FUSE/GlusterFS网络文件系统中断后陷入错误循环无法恢复 - [PR #139275](https://github.com/kubernetes/kubernetes/pull/139275) - **影响：** 使用特定网络文件系统的Pod在存储故障后可能无法自动恢复
5. 修复Windows kube-proxy在HNS重启后因重复创建负载均衡器而失败的问题 - [PR #139503](https://github.com/kubernetes/kubernetes/pull/139503) - **影响：** Windows节点在HNS服务重启期间可能丢失服务连接性
6. 修复kubeadm join过程中因API调用超时配置不当导致集群加入失败 - [PR #139667](https://github.com/kubernetes/kubernetes/pull/139667) - **影响：** 在API服务器响应慢时，新节点可能无法成功加入集群
7. 修复PodGroupState缓存中带删除时间戳的Pod未被正确移除的问题 - [PR #138445](https://github.com/kubernetes/kubernetes/pull/138445) - **影响：** 调度器缓存可能包含已删除的Pod，影响调度决策准确性
8. 修复DRA（动态资源分配）中ResourceClaim状态报告重复配置的问题 - [PR #139732](https://github.com/kubernetes/kubernetes/pull/139732) - **影响：** 资源分配状态信息可能不正确，影响设备管理

## 💥 破坏性变更
1. 🚨 PodGroupScheduled条件更名为PodGroupInitiallyScheduled，需要更新相关的监控和自动化脚本 - [PR #139743](https://github.com/kubernetes/kubernetes/pull/139743) - **影响：** 依赖此条件名称的客户端和监控工具需要更新
2. 🚨 服务代理子资源实现从Endpoints迁移到EndpointSlices，可能影响直接依赖内部API的自定义组件 - [PR #134860](https://github.com/kubernetes/kubernetes/pull/134860) - **影响：** 使用内部代理实现的工具需要适配新的EndpointSlice架构
3. 🚨 kubeadm现在显式将kube-proxy模式设置为'iptables'，覆盖可能的默认值 - [PR #139777](https://github.com/kubernetes/kubernetes/pull/139777) - **影响：** 依赖其他代理模式（如ipvs）的kubeadm集群需要显式配置

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 工作负载感知调度API演进：Workload和PodGroup API的minCount字段现在可变，允许动态调整Pod组的最小数量 - [PR #139279](https://github.com/kubernetes/kubernetes/pull/139279)
2. 功能门合并：GangScheduling和WorkloadAwarePreemption功能门合并为GenericWorkload，简化了配置 - [PR #139520](https://github.com/kubernetes/kubernetes/pull/139520)
3. PodGroup条件重命名：PodGroupScheduled条件更名为PodGroupInitiallyScheduled，以更准确地反映其含义 - [PR #139743](https://github.com/kubernetes/kubernetes/pull/139743) / [Issue #139740](https://github.com/kubernetes/kubernetes/issues/139740)
4. 服务代理子资源迁移：service/proxy子资源实现从Endpoints迁移到EndpointSlices，这是服务发现架构演进的一部分 - [PR #134860](https://github.com/kubernetes/kubernetes/pull/134860)
5. 节点监控并行化：引入MonitorNodes循环的并行化，提升大规模集群的节点监控效率 - [PR #137964](https://github.com/kubernetes/kubernetes/pull/137964)
6. HPA支持缩放到零：HPAScaleToZero功能门升级到Beta，允许HPA将副本数缩减到0 - [PR #139648](https://github.com/kubernetes/kubernetes/pull/139648)
7. 服务名称验证放宽：KEP-5311放宽服务DNS名称验证的功能升级到GA - [PR #139282](https://github.com/kubernetes/kubernetes/pull/139282)

## 🚀 性能优化
1. 优化调度器PVC引用计数聚合，通过增量计数减少计算开销 - [PR #139238](https://github.com/kubernetes/kubernetes/pull/139238) - **提升：** 显著改善大量使用PVC的集群的调度器性能
2. 引入WatchListCompression功能门，支持压缩watch列表传输数据 - [PR #139308](https://github.com/kubernetes/kubernetes/pull/139308) - **提升：** 减少API服务器和客户端之间的网络流量
3. 修复CEL对CRD metadata.name和metadata.generateName的成本估算，避免不必要的验证开销 - [PR #139573](https://github.com/kubernetes/kubernetes/pull/139573) - **提升：** 改善CRD验证性能
4. 优化节点监控循环的并行化，提升大规模集群的监控效率 - [PR #137964](https://github.com/kubernetes/kubernetes/pull/137964) - **提升：** 改善节点状态更新的响应时间

## 🎯 风险评估
整体风险评估：高（alpha版本）。此版本包含大量API变更、功能门合并和架构演进，虽然修复了多个重要bug，但作为早期开发版本，稳定性无法保证。建议的升级时机：仅用于开发和测试环境，生产环境应等待至少beta版本。需要特别关注的方面：1) 工作负载感知调度相关变更的兼容性；2) 网络栈变更对现有服务的影响；3) 调度器性能优化的实际效果验证；4) Windows相关修复的稳定性。

## 📋 升级建议
1. **生产环境暂缓升级**：这是alpha版本，包含实验性功能和不稳定变更，不建议用于生产环境
2. **测试环境重点验证**：在测试集群中重点验证工作负载感知调度相关功能，特别是PodGroup和Workload API的变更
3. **关注网络变更影响**：特别是kube-proxy UDP连接跟踪修复和Windows HNS处理改进，确保服务发现和负载均衡正常工作
4. **评估调度器性能**：如果集群大量使用PVC，验证PVC引用计数优化带来的调度性能提升
5. **更新监控配置**：注意PodGroup条件名称变更，相应更新Prometheus查询和告警规则
6. **为未来升级做准备**：审查服务代理子资源迁移的影响，确保自定义工具和脚本兼容EndpointSlice

## 📋 Release 包含的变更

### PR #134860: Port service/proxy subresource from Endpoints to EndpointSlice
- **链接：** https://github.com/kubernetes/kubernetes/pull/134860
- **状态：** closed
- **已合并：** 是
- **作者：** danwinship
- **标签：** priority/important-soon, sig/network, kind/cleanup, area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  将 apiserver 中 service/proxy 子资源的后端实现从 Endpoints 迁移到 EndpointSlice，作为 #129837 的后续清理工作。移除了一个长期未使用且标记为可删除的 Endpoints 特定代码块。由于 v1 和 internal API 版本差异，导致部分代理代码重复，但这是必要的迁移步骤。

### PR #135300: kubelet: add diagnostic message to PodReadyToStartContainers condition
- **链接：** https://github.com/kubernetes/kubernetes/pull/135300
- **状态：** closed
- **已合并：** 是
- **作者：** harche
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  修复 kubelet 问题，在 Pod 的 `PodReadyToStartContainers` 条件中添加诊断消息，帮助用户和调试工具识别容器启动延迟的具体原因。

### PR #137141: Fix dbus connection leak in node shutdown manager causing thread exhaustion
- **链接：** https://github.com/kubernetes/kubernetes/pull/137141
- **状态：** closed
- **已合并：** 是
- **作者：** harche
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, priority/important-longterm, lifecycle/rotten, triage/accepted
- **变更说明：**
  修复了 node shutdown manager 中因错误处理不当导致的 dbus 连接泄漏问题。通过改用私有连接并确保正确关闭，防止了线程耗尽和潜在的 kubelet 崩溃。

### PR #137652: kubelet: use DecimalSI format for ephemeral-storage capacity
- **链接：** https://github.com/kubernetes/kubernetes/pull/137652
- **状态：** closed
- **已合并：** 是
- **作者：** 0xMH
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/S, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复 kubelet 报告的 `ephemeral-storage` 容量显示格式不一致问题。将容量 `Quantity` 从 `BinarySI` 改为 `DecimalSI` 格式，使其与 `allocatable` 的格式保持一致。

### PR #137964: Introduce paralellization for MonitorNodes loop.
- **链接：** https://github.com/kubernetes/kubernetes/pull/137964
- **状态：** closed
- **已合并：** 是
- **作者：** niewysoki
- **标签：** lgtm, area/cloudprovider, sig/node, sig/api-machinery, release-note, size/XL, kind/api-change, kind/feature, sig/apps, approved, cncf-cla: yes, sig/instrumentation, area/code-generation, sig/cloud-provider, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  为节点控制器中的 `MonitorNodes` 循环引入并行处理机制。通过并发处理节点状态更新，提高了大规模集群中节点心跳处理和状态同步的可扩展性与性能。

### PR #138445: Fix pod updated with deletion timestamp not being removed from cached podGroupState
- **链接：** https://github.com/kubernetes/kubernetes/pull/138445
- **状态：** closed
- **已合并：** 是
- **作者：** iomarsayed
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  修复当已 assumed 的 pod 被标记删除时，未能从缓存的 podGroupState 中移除的问题。这导致 pod 滞留在 unschedulablePods 中。解决方案是确保在调用 Cache.ForgetPod() 的场景中（如处理带删除时间戳的 pod 更新），也调用 Cache.removePodGroupMember() 来正确清理 PodGroupState。

### PR #138999: client-go: add Config.GenerateKey in certificate_manager.go
- **链接：** https://github.com/kubernetes/kubernetes/pull/138999
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** lgtm, sig/api-machinery, release-note, size/L, kind/feature, sig/auth, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  这是一个特性PR，在client-go的certificate_manager.go中添加Config.GenerateKey功能。该新增配置选项用于生成密钥，增强证书管理能力。改动属于大尺寸（size/L），涉及sig/api-machinery和sig/auth，已获批准。

### PR #139237: webhook use resolved endpoint IP instead of cached
- **链接：** https://github.com/kubernetes/kubernetes/pull/139237
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** kind/bug, area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/XL, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  修复 kube-apiserver 在使用 `--enable-aggregator-routing=true` 时，admission webhook 请求负载不均衡的问题。此前 HTTP/1.1 连接池基于服务名缓存连接，导致并发请求可能复用同一后端连接。现改为使用动态解析的端点 IP 进行负载均衡，可通过 `WebhookRoundTripLoadBalancing` 特性门控控制。

### PR #139238: Optimize PVC ref count aggregation via delta counts
- **链接：** https://github.com/kubernetes/kubernetes/pull/139238
- **状态：** closed
- **已合并：** 是
- **作者：** yue9944882
- **标签：** area/test, sig/scheduling, lgtm, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  优化调度器中 PVC 引用计数的聚合性能。通过引入增量计数机制，替代每次全量重新计算所有 pod 的 PVC 使用情况，显著降低了在大型集群中更新 pod 缓存时的计算开销，提升了调度器可扩展性。

### PR #139275: Fix(kubelet):  pods with subPath mounts stuck in error loop after FUSE/GlusterFS network filesystem disruption 
- **链接：** https://github.com/kubernetes/kubernetes/pull/139275
- **状态：** closed
- **已合并：** 是
- **作者：** yuehaii
- **标签：** kind/bug, area/test, lgtm, sig/storage, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复了 kubelet 中当 FUSE 或 GlusterFS 等网络文件系统中断后，使用 subPath 挂载的 Pod 陷入永久错误循环的问题。措施是检测并 lazily-unmount 过时的 bind mount 以恢复 Pod。

### PR #139279: Make minCount mutable in Workload and PodGroup APIs
- **链接：** https://github.com/kubernetes/kubernetes/pull/139279
- **状态：** closed
- **已合并：** 是
- **作者：** antekjb
- **标签：** area/test, priority/important-soon, sig/scheduling, lgtm, sig/api-machinery, release-note, size/XL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, area/code-generation, ok-to-test, api-review, triage/accepted, area/api-validation, wg/workload-aware-scheduling
- **变更说明：**
  使 Workload 和 PodGroup API 中的 `minCount` 字段变为可变的（mutable）。这是一项 API 变更，允许运行时动态调整工作组所需的最少 Pod 数量，增强了调度灵活性。

### PR #139282: KEP-5311 Promote relaxed validation for Services names to GA
- **链接：** https://github.com/kubernetes/kubernetes/pull/139282
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** sig/network, lgtm, release-note, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  将 KEP-5311（放宽 Service 名称的 DNS 子域名验证规则）从 Beta 版本提升至 GA。此特性允许更长的 Service 名称，解决了之前的命名限制问题。

### PR #139308: Introduce WatchListCompression feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/139308
- **状态：** closed
- **已合并：** 是
- **作者：** p0lyn0mial
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  引入 `WatchListCompression` feature gate，用于控制 apiserver 在向客户端发送 watch 事件列表时是否启用压缩。这是一项优化 apiserver 性能和网络使用的新功能。

### PR #139407: feat: Create CompositePodGroup feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/139407
- **状态：** closed
- **已合并：** 是
- **作者：** jdzikowski
- **标签：** sig/scheduling, lgtm, release-note, size/S, kind/feature, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  创建了 `CompositePodGroup` 特性门 (feature gate)，用于为组合式工作负载的调度功能提供控制开关，标志着相关开发工作的开始。

### PR #139457: Fix job controller reporting active=0 during pod creation backoff
- **链接：** https://github.com/kubernetes/kubernetes/pull/139457
- **状态：** closed
- **已合并：** 是
- **作者：** akhilsingh-git
- **标签：** kind/bug, lgtm, release-note, size/M, sig/apps, approved, cncf-cla: yes, priority/important-longterm, ok-to-test, kind/regression, triage/accepted
- **变更说明：**
  修复 Job 控制器在 pod 创建回退期间错误报告 active=0 的回归问题。当 manageJob() 因 pod-failure backoff 延迟创建 pod 时，会返回硬编码的 active=0，导致 status.active=0 但 status.ready 仍反映运行中的 pod，触发 apiserver 422 错误（ready 不能大于 active）。此错误更新会阻塞控制器清理已终止的 pod 和更新 job 状态。修复后，两个 backoff 路径（全局和 per-index）均返回真实的 active 计数，并添加了回归测试。

### PR #139503: Handling syscall failures when hns is not running.
- **链接：** https://github.com/kubernetes/kubernetes/pull/139503
- **状态：** closed
- **已合并：** 是
- **作者：** princepereira
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/XL, approved, sig/windows, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  提升 Windows kube-proxy 在 HNS 暂时不可用（如重启恢复）期间的弹性。修复将 HNS API 调用（如 GetLoadBalancer）的临时系统调用失败错误地解释为负载均衡器不存在的问题，防止 kube-proxy 不必要地重置内部状态并尝试重复创建对象，从而避免后续的创建冲突错误。

### PR #139520: Merge GangScheduling and WorkloadAwarePreemption feature gates into GenericWorkload
- **链接：** https://github.com/kubernetes/kubernetes/pull/139520
- **状态：** closed
- **已合并：** 是
- **作者：** macsko
- **标签：** area/test, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, area/code-generation, needs-priority, needs-triage, wg/device-management, wg/workload-aware-scheduling
- **变更说明：**
  将 `GangScheduling` 和 `WorkloadAwarePreemption` 两个 feature gate 合并到统一的 `GenericWorkload` feature gate 中，是一项 API 变更 (kind/api-change)，旨在整合与调度工作负载相关的核心功能。

### PR #139573: Fix CEL cost estimates for CRD metadata.name and metadata.generateName
- **链接：** https://github.com/kubernetes/kubernetes/pull/139573
- **状态：** closed
- **已合并：** 是
- **作者：** jpbetz
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复了 CRD 对 `metadata.name` 和 `metadata.generateName` 字段的 CEL（Common Expression Language）表达式成本估算。现使其正确反映 Kubernetes 默认强制执行的 DNS 子域名长度限制（253字节）。

### PR #139629: kube-proxy: clear stale conntrack entries for UDP services with no endpoints
- **链接：** https://github.com/kubernetes/kubernetes/pull/139629
- **状态：** closed
- **已合并：** 是
- **作者：** Bafff
- **标签：** kind/bug, sig/network, area/kube-proxy, lgtm, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, kind/regression, needs-triage
- **变更说明：**
  修复 kube-proxy 在 UDP 服务缩容至零端点时，无法清理已建立连接的 conntrack 条目的回归问题。这会导致流量被持续黑洞至已删除的 Pod IP。修复确保即使服务 endpoints 数为零，conntrack reconciler 也会处理并清除相关的 UDP 连接跟踪条目。

### PR #139632: KEP-4222: Support CBOR encoding for non-resource endpoints.
- **链接：** https://github.com/kubernetes/kubernetes/pull/139632
- **状态：** closed
- **已合并：** 是
- **作者：** benluddy
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  根据 KEP-4222，为 apiserver 的非资源端点（如 `/healthz`, `/version`）添加 CBOR (Concise Binary Object Representation) 编码支持。客户端可通过 Accept 头部请求 CBOR 格式响应，以提高通信效率。

### PR #139648: KEP-2021: Promote HPAScaleToZero feature gate to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/139648
- **状态：** closed
- **已合并：** 是
- **作者：** johanneswuerbach
- **标签：** area/test, priority/backlog, lgtm, release-note, sig/autoscaling, size/L, kind/feature, sig/apps, approved, cncf-cla: yes, sig/testing, ok-to-test, triage/accepted
- **变更说明：**
  将 `HPAScaleToZero` feature gate 提升至 Beta 阶段。此特性使 HPA (HorizontalPodAutoscaler) 能够将副本数缩放到零，促进资源效率。

### PR #139651: Align DeviceTaintRule informer API version with handlers
- **链接：** https://github.com/kubernetes/kubernetes/pull/139651
- **状态：** closed
- **已合并：** 是
- **作者：** nojnhuh
- **标签：** kind/bug, area/test, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, sig/testing, kind/failing-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复了 `DeviceTaintRule` 监听器 (informer) 的 API 版本与处理程序 (handlers) 不匹配的问 题，解决了因此导致的测试失败问题。

### PR #139667: fix(kubeadm): use KubernetesAPICallTimeout for mandatory kubeadm-config fetch during join
- **链接：** https://github.com/kubernetes/kubernetes/pull/139667
- **状态：** closed
- **已合并：** 是
- **作者：** damdo
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/M, approved, area/kubeadm, cncf-cla: yes, triage/accepted
- **变更说明：**
  修复 kubeadm join 时，获取 `kubeadm-config` ConfigMap 的超时问题。原逻辑存在短时间重试预算消耗殆尽导致 join 失败的风险。现改为使用更长且可配置的 `KubernetesAPICallTimeout`（默认一分钟）并进行重试。

### PR #139731: DRA: Empty requests field in config status of resourceclaim when the config applies to all requests
- **链接：** https://github.com/kubernetes/kubernetes/pull/139731
- **状态：** closed
- **已合并：** 是
- **作者：** LionelJouin
- **标签：** kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  清理 Dynamic Resource Allocation (DRA) 中 resourceclaim 的状态表示。当资源配置适用于所有请求时，将其 status.configs 字段中的 requests 列表设为空数组，而不是包含所有请求的列表，使状态报告更清晰准确。

### PR #139732: DRA: Fix duplicated configs reported in resourceclaim status
- **链接：** https://github.com/kubernetes/kubernetes/pull/139732
- **状态：** closed
- **已合并：** 是
- **作者：** LionelJouin
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复 Dynamic Resource Allocation (DRA) 中 resourceclaim 状态可能重复报告相同配置的问题。确保在更新 status.configs 时进行去重，防止因重复条目导致状态信息不准确。

### PR #139735: bump coredns to v1.14.4
- **链接：** https://github.com/kubernetes/kubernetes/pull/139735
- **状态：** closed
- **已合并：** 是
- **作者：** yashsingh74
- **标签：** lgtm, area/provider/gcp, sig/cluster-lifecycle, release-note, size/S, kind/feature, approved, area/kubeadm, cncf-cla: yes, sig/cloud-provider, needs-priority, area/dependency, needs-triage
- **变更说明：**
  将 CoreDNS 依赖版本升级至 v1.14.4。这是一个常规的依赖项更新，以获取新功能、bug 修复和安全补丁。

### PR #139743: Rename PodGroupScheduled condition to PodGroupInitiallyScheduled
- **链接：** https://github.com/kubernetes/kubernetes/pull/139743
- **状态：** closed
- **已合并：** 是
- **作者：** antekjb
- **标签：** area/test, kind/cleanup, sig/scheduling, lgtm, sig/api-machinery, release-note, size/L, kind/api-change, approved, cncf-cla: yes, sig/testing, area/code-generation, ok-to-test, needs-priority, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  将 PodGroup 状态条件 `PodGroupScheduled` 重命名为 `PodGroupInitiallyScheduled`，以更准确地反映其含义（表示 PodGroup 的初始调度周期已完成）。这是一个 API 变更和清理工作。

### PR #139755: Expose a way to wait for a controller listener to be fully shutdown
- **链接：** https://github.com/kubernetes/kubernetes/pull/139755
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  为控制器监听器暴露一个等待其完全关闭的方法 (`WaitForStop`)。修复了在优雅关闭期间，监听器可能尚未完全停止就继续执行后续逻辑，导致事件丢失或竞争条件的问题。

### PR #139760: update the error message, to make it to be more explict for windows
- **链接：** https://github.com/kubernetes/kubernetes/pull/139760
- **状态：** closed
- **已合并：** 是
- **作者：** zylxjtu
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/XS, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  这是一个清理PR，更新kubelet中的错误消息，使其在Windows环境下更明确。改进旨在提升错误提示的清晰度，帮助Windows用户更好地诊断问题。标签显示已批准，属于小改动（size/XS）。

### PR #139777: kubeadm: explicitly set the kube-proxy mode to 'iptables'
- **链接：** https://github.com/kubernetes/kubernetes/pull/139777
- **状态：** closed
- **已合并：** 是
- **作者：** neolit123
- **标签：** priority/important-soon, kind/cleanup, lgtm, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, kind/deprecation, triage/accepted
- **变更说明：**
  在 kubeadm 中显式将 kube-proxy 模式设置为 'iptables'。此清理和弃用变更旨在明确配置，因 ipvs 虽为默认，但部分环境不支持。

### PR #139842: kubeadm: treat already promoted learner as successful
- **链接：** https://github.com/kubernetes/kubernetes/pull/139842
- **状态：** closed
- **已合并：** 是
- **作者：** jihyun-huh
- **标签：** kind/bug, priority/backlog, lgtm, sig/cluster-lifecycle, release-note, size/L, approved, area/kubeadm, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  修复 kubeadm 在提升 etcd learner 成员时的处理逻辑。当尝试提升一个已经是 voting member 的节点时，操作会失败。此 PR 确保将已经成功晋升的 learner 节点视为成功状态，而不是错误，提高了 etcd 成员管理操作的健壮性。

### PR #139968: Register APIServer informers for metrics and naming
- **链接：** https://github.com/kubernetes/kubernetes/pull/139968
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** area/test, area/apiserver, lgtm, sig/api-machinery, release-note, size/S, kind/feature, approved, cncf-cla: yes, sig/testing, needs-priority, triage/accepted
- **变更说明：**
  为 APIServer 中的 informer 进行注册，以开启相关的指标（metrics）收集和命名（naming），便于对 APIServer 内部的 informer 行为进行监控和调试。

---
*本报告由 Containerd Release Tracker 自动生成*
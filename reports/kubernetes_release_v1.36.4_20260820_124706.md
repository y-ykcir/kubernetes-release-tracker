# Kubernetes 版本发布分析报告
## v1.36.4 (v1.36.4)

### 📋 版本信息
- **版本标签：** v1.36.4
- **版本名称：** v1.36.4
- **发布时间：** 2026-08-20T11:48:16Z
- **发布者：** k8s-release-robot
- **预发布版本：** 否
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.36.4

### 🔍 分析统计
- **分析时间：** 2026-08-20 12:47:06
- **分析的 PR 数量：** 5
- **分析的 Issue 数量：** 0
- **重要项目数量：** 5

## 📊 版本概述
Kubernetes v1.36.4 是一个补丁版本，主要修复了设备资源分配（DRA）、Pod调度抢占、client-go测试工具中的关键bug，并更新了golang依赖以修复安全漏洞。

## 🔒 安全问题修复
1. ⚠️ 安全问题描述：更新golang.org/x/text至v0.39.0+以修复漏洞GO-2026-5970；更新golang.org/x/net至v0.55.0+以修复漏洞GO-2026-5026 - [PR #141226](https://github.com/kubernetes/kubernetes/pull/141226) - **风险级别：** 中。这些是底层库的安全更新，可能涉及文本处理或网络通信中的潜在漏洞。建议升级以保持安全基线。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复描述：DRA结构化分配器计数器缓存未按PoolID（驱动+池名）区分，导致不同驱动下同名资源池的设备计数被错误共享，可能接受或拒绝错误的设备分配 - [PR #140504](https://github.com/kubernetes/kubernetes/pull/140504) - **影响：** 影响使用多个设备驱动程序且存在同名资源池的生产环境，可能导致设备分配错误。DRA在1.36为Beta且默认启用，建议使用DRA的集群升级。
2. 修复描述：调度器抢占逻辑中存在竞态条件，可能导致执行抢占的Pod（preemptor）自身被错误标记并卡在不可调度队列中，无法被重新调度 - [PR #140685](https://github.com/kubernetes/kubernetes/pull/140685) - **影响：** 影响依赖抢占机制来调度高优先级Pod的集群，可能导致关键Pod无法启动，影响服务可用性。
3. 修复描述：kubelet在DRA的PrepareResources调用部分失败后重试时，未正确重置设备列表，导致重复的CDI设备ID被传递给容器运行时，引发容器启动失败 - [PR #140955](https://github.com/kubernetes/kubernetes/pull/140955) - **影响：** 影响使用DRA进行设备管理的生产环境，在设备准备发生瞬时故障时，可能导致容器持续启动失败。
4. 修复描述：client-go的FakeCustomStore未实现cache.Store接口在v0.36版本新增的Bookmark和LastStoreSyncResourceVersion方法，导致依赖该接口的单元测试失败 - [PR #141001](https://github.com/kubernetes/kubernetes/pull/141001) - **影响：** 主要影响开发和测试环节，使用FakeCustomStore进行单元测试的代码需要更新client-go版本以通过测试，对运行中的生产集群无直接影响。

## 💥 破坏性变更
1. 🚨 本版本为补丁版本，未引入破坏性变更（Breaking Changes）、API变更或功能废弃。所有修复均为向后兼容的bug修复和安全更新。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复DRA结构化分配器计数器缓存键问题，防止不同驱动间同名资源池的设备分配冲突 - [PR #140504](https://github.com/kubernetes/kubernetes/pull/140504)
2. 修复抢占逻辑中的竞态条件，防止抢占者Pod卡在不可调度队列中 - [PR #140685](https://github.com/kubernetes/kubernetes/pull/140685)
3. 修复kubelet/DRA在重试资源准备时传递重复CDI设备ID导致容器启动失败的问题 - [PR #140955](https://github.com/kubernetes/kubernetes/pull/140955)
4. 修复client-go中FakeCustomStore以重新符合cache.Store接口 - [PR #141001](https://github.com/kubernetes/kubernetes/pull/141001)
5. 更新golang.org/x/text和golang.org/x/net依赖以包含安全更新 - [PR #141226](https://github.com/kubernetes/kubernetes/pull/141226)

## 🚀 性能优化
1. 性能改进描述：修复DRA计数器缓存键问题，避免了因缓存键冲突导致的无效设备分配尝试和拒绝，可能间接提升设备分配决策效率 - [PR #140504](https://github.com/kubernetes/kubernetes/pull/140504) - **提升：** 修复逻辑正确性，在特定多驱动同名池场景下避免性能浪费。

## 🎯 风险评估
整体风险评估：**低风险**。此版本主要包含针对特定场景的bug修复和一个安全依赖项更新，不涉及核心API或架构变更。对于受影响的集群（使用DRA、高抢占压力），修复的问题可能直接影响稳定性，因此升级收益明显。建议的升级时机为下一个维护窗口。需要特别关注的方面是升级后观察DRA设备分配和Pod调度行为是否恢复正常。

## 📋 升级建议
1. **升级建议：** 对于正在运行Kubernetes 1.36.x版本的生产集群，特别是那些使用了DRA（设备资源分配）功能或频繁发生Pod抢占的集群，建议安排升级到v1.36.4以获取关键修复。
2. **注意事项：** 1. 升级前，请在测试环境中验证与您使用的设备驱动程序（Device Plugin）的兼容性。2. 如果您的服务依赖client-go库并使用了FakeCustomStore进行测试，升级后您的测试套件应能正常运行。3. 作为常规操作，升级前请备份关键配置和状态。

## 📋 Release 包含的变更

### PR #140504: Automated cherry pick of #140435: DRA: key the structured allocator counter caches by PoolID
- **链接：** https://github.com/kubernetes/kubernetes/pull/140504
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复DRA调度中结构化分配器计数器缓存键问题，从pool name改为PoolID（driver+pool name），避免不同驱动器间计数器定义冲突，影响release-1.36的beta功能。

### PR #140685: Automated cherry pick of #139162: Fix case where preemptor may be stuck in unschedulable queue
#139330: Unset WasFlushedFromUnschedulable for gated pods
#139331: Make sure gated pods are flushed with the same frequency as non-gated
- **链接：** https://github.com/kubernetes/kubernetes/pull/140685
- **状态：** closed
- **已合并：** 是
- **作者：** iomarsayed
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  修复调度器中抢占者pod可能卡在不可调度队列的竞争条件，并调整gated pods的刷新逻辑，确保与非gated pods频率一致。

### PR #140955: Automated cherry pick of #140274: kubelet/dra: reset devices before processing gRPC response
- **链接：** https://github.com/kubernetes/kubernetes/pull/140955
- **状态：** closed
- **已合并：** 是
- **作者：** bart0sh
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  修复kubelet/DRA中重试部分失败的PrepareResources时产生重复CDI设备ID的bug，通过在处理gRPC响应前重置设备，防止容器启动失败。

### PR #141001: Automated cherry pick of #140966: client-go: restore FakeCustomStore conformance to cache.Store
- **链接：** https://github.com/kubernetes/kubernetes/pull/141001
- **状态：** closed
- **已合并：** 是
- **作者：** alancaldelas
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  修复client-go中FakeCustomStore不满足cache.Store接口的问题，通过实现v0.36新增的Bookmark和LastStoreSyncResourceVersion方法，恢复兼容性。

### PR #141226: Update golang.org/x deps
- **链接：** https://github.com/kubernetes/kubernetes/pull/141226
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, sig/auth, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/architecture, area/code-generation, sig/cloud-provider, area/dependency, sig/security, triage/accepted, wg/device-management
- **变更说明：**
  更新golang.org/x/text至v0.39.0+和golang.org/x/net至v0.55.0+依赖，修复安全漏洞GO-2026-5970和GO-2026-5026。

---
*本报告由 Containerd Release Tracker 自动生成*
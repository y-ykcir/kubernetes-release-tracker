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
- **分析时间：** 2026-08-20 19:46:39
- **分析的 PR 数量：** 5
- **分析的 Issue 数量：** 0
- **重要项目数量：** 5

## 📊 版本概述
Kubernetes v1.36.4 是一个重要的补丁版本，主要修复了设备分配（DRA）、调度抢占和 client-go 测试工具中的关键 Bug，并包含了重要的 Golang 安全依赖更新。

## 🔒 安全问题修复
1. ⚠️ 更新 golang.org/x/text 依赖以修复漏洞 GO-2026-5970 - [PR #141226](https://github.com/kubernetes/kubernetes/pull/141226) - **风险级别：** 中（依赖项安全更新）
2. ⚠️ 更新 golang.org/x/net 依赖以修复漏洞 GO-2026-5026 - [PR #141226](https://github.com/kubernetes/kubernetes/pull/141226) - **风险级别：** 中（依赖项安全更新）

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 DRA 计数器缓存键问题：当两个设备驱动在同一节点上发布同名池时，会导致设备被错误地接受或拒绝。**影响：** 使用 DRA（Device Resource Access）功能且部署了多个设备驱动的集群，设备分配可能不可靠。 - [PR #140504](https://github.com/kubernetes/kubernetes/pull/140504)
2. 修复调度器抢占竞态条件：可能导致高优先级 Pod（抢占者）在抢占成功后仍被错误地留在不可调度队列中，无法被调度。**影响：** 依赖抢占机制来保证关键工作负载调度的集群，可能出现 Pod 调度延迟或失败。 - [PR #140685](https://github.com/kubernetes/kubernetes/pull/140685)
3. 修复 DRA 设备 ID 重复问题：在部分失败的 PrepareResources 调用重试时，kubelet 可能向 CRI 运行时传递重复的 CDI 设备 ID。**影响：** 使用 DRA 且设备准备可能部分失败的场景，容器启动会失败。 - [PR #140955](https://github.com/kubernetes/kubernetes/pull/140955)
4. 修复 client-go 的 FakeCustomStore 测试工具：使其重新符合 cache.Store 接口规范。**影响：** 主要影响使用 FakeCustomStore 进行单元测试的开发者，测试可能因接口方法缺失而失败。 - [PR #141001](https://github.com/kubernetes/kubernetes/pull/141001)

## 💥 破坏性变更
1. 🚨 此版本为补丁版本，未引入破坏性变更或 API 变更。所有修复均为向后兼容的 Bug 修复和安全更新。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. 修复 DRA 结构化分配器计数器缓存键问题，避免不同驱动间池名冲突导致的设备分配错误 - [PR #140504](https://github.com/kubernetes/kubernetes/pull/140504)
2. 修复调度器抢占逻辑中的竞态条件，防止抢占者 Pod 卡在不可调度队列中 - [PR #140685](https://github.com/kubernetes/kubernetes/pull/140685)
3. 修复 kubelet/DRA 在重试 PrepareResources 时可能传递重复 CDI 设备 ID 导致容器启动失败的问题 - [PR #140955](https://github.com/kubernetes/kubernetes/pull/140955)
4. 更新 golang.org/x/text 和 golang.org/x/net 依赖以包含安全修复 - [PR #141226](https://github.com/kubernetes/kubernetes/pull/141226)

## 🎯 风险评估
整体风险评估：**低风险**。这是一个专注于修复已知 Bug 和安全更新的补丁版本，升级引入新问题的可能性较低。建议的升级时机：下一个维护窗口。需要特别关注的方面：升级后观察 DRA 设备分配和 Pod 调度行为是否正常，尤其是涉及抢占的场景。

## 📋 升级建议
1. **强烈建议**所有运行 Kubernetes 1.36.x 版本的集群升级到 v1.36.4，特别是那些使用了 DRA 设备管理功能或对调度抢占可靠性有要求的集群。
2. 升级前，请在测试环境中验证 DRA 设备驱动和调度器行为是否正常。
3. 对于开发者，如果单元测试因 `FakeCustomStore` 相关问题失败，升级到此版本后应能解决。
4. 虽然此版本包含安全依赖更新，但仍建议结合自身安全策略评估是否需要更紧急的升级。

## 📋 Release 包含的变更

### PR #140504: Automated cherry pick of #140435: DRA: key the structured allocator counter caches by PoolID
- **链接：** https://github.com/kubernetes/kubernetes/pull/140504
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将 #140435 的修复cherry-pick到release-1.36分支。修复了DRA结构化分配器的一个bug：将availableCounters/consumedCounters缓存的键从池名改为PoolID，防止不同驱动下同名池共享计数器定义，导致设备分配错误。

### PR #140685: Automated cherry pick of #139162: Fix case where preemptor may be stuck in unschedulable queue
#139330: Unset WasFlushedFromUnschedulable for gated pods
#139331: Make sure gated pods are flushed with the same frequency as non-gated
- **链接：** https://github.com/kubernetes/kubernetes/pull/140685
- **状态：** closed
- **已合并：** 是
- **作者：** iomarsayed
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  将三个调度器修复cherry-pick到release-1.36分支。主要解决了预抢占器Pod可能卡在不可调度队列中的竞态条件问题，并确保gated pods与普通pod以相同频率被刷新，同时重置其WasFlushedFromUnschedulable标志。

### PR #140955: Automated cherry pick of #140274: kubelet/dra: reset devices before processing gRPC response
- **链接：** https://github.com/kubernetes/kubernetes/pull/140955
- **状态：** closed
- **已合并：** 是
- **作者：** bart0sh
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将 #140274 的修复cherry-pick到release-1.36分支。修复了kubelet/DRA中的一个bug：在重试部分失败的PrepareResources调用时，会向CRI运行时传递重复的CDI设备ID，导致容器启动失败。修复方法是在处理gRPC响应前重置设备状态。

### PR #141001: Automated cherry pick of #140966: client-go: restore FakeCustomStore conformance to cache.Store
- **链接：** https://github.com/kubernetes/kubernetes/pull/141001
- **状态：** closed
- **已合并：** 是
- **作者：** alancaldelas
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  将 #140966 的修复cherry-pick到release-1.36分支。修复了client-go中的FakeCustomStore，使其实现了cache.Store接口在v0.36版本新增的Bookmark和LastStoreSyncResourceVersion方法，从而恢复了接口兼容性。

### PR #141226: Update golang.org/x deps
- **链接：** https://github.com/kubernetes/kubernetes/pull/141226
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, sig/auth, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/architecture, area/code-generation, sig/cloud-provider, area/dependency, sig/security, triage/accepted, wg/device-management
- **变更说明：**
  更新golang.org/x/text至v0.39.0+和golang.org/x/net至v0.55.0+，以修复安全漏洞GO-2026-5970和GO-2026-5026。这是一个涉及多个SIG和组件的安全依赖项更新。

---
*本报告由 Containerd Release Tracker 自动生成*
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
- **分析时间：** 2026-08-20 19:46:48
- **分析的 PR 数量：** 5
- **分析的 Issue 数量：** 0
- **重要项目数量：** 5

## 📊 版本概述
Kubernetes v1.36.4 是一个补丁版本，主要修复了 DRA（设备资源分配）中的关键 bug、调度器竞态条件以及更新了安全依赖，旨在提升集群的稳定性和安全性。

## 🔒 安全问题修复
1. ⚠️ 更新 golang.org/x/text 依赖以修复漏洞 GO-2026-5970。 - [PR #141226](https://github.com/kubernetes/kubernetes/pull/141226) - **风险级别：** 中
2. ⚠️ 更新 golang.org/x/net 依赖以修复漏洞 GO-2026-5026。 - [PR #141226](https://github.com/kubernetes/kubernetes/pull/141226) - **风险级别：** 中

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 DRA 计数器缓存键问题：当多个设备驱动在同一节点上使用相同的池名时，会导致设备分配逻辑错误，可能错误地接受或拒绝设备请求。 - [PR #140504](https://github.com/kubernetes/kubernetes/pull/140504) - **影响：** 使用 DRA 功能且部署了多个设备驱动的生产环境，可能导致设备分配失败或错误分配。
2. 修复调度器抢占竞态条件：一个抢占者 Pod 可能被错误地标记并卡在不可调度队列中，无法被正常调度。 - [PR #140685](https://github.com/kubernetes/kubernetes/pull/140685) - **影响：** 依赖抢占机制的高优先级工作负载（如关键批处理任务）可能无法及时启动，影响服务等级目标（SLO）。
3. 修复 DRA 设备 ID 重复问题：在部分失败的 PrepareResources 调用重试时，kubelet 可能向容器运行时传递重复的 CDI 设备 ID。 - [PR #140955](https://github.com/kubernetes/kubernetes/pull/140955) - **影响：** 使用 DRA 管理 GPU、FPGA 等设备的 Pod 可能在启动时失败，导致服务中断。
4. 修复 client-go 测试工具兼容性：FakeCustomStore 现在正确实现了 cache.Store 接口新增的方法。 - [PR #141001](https://github.com/kubernetes/kubernetes/pull/141001) - **影响：** 主要影响使用 FakeCustomStore 进行单元测试的组件（如自定义控制器），修复后可确保测试代码的兼容性和正确性。

## ✨ 主要变更
1. 修复 DRA 结构化分配器计数器缓存键问题，防止不同驱动间池名冲突导致设备分配错误 - [PR #140504](https://github.com/kubernetes/kubernetes/pull/140504)
2. 修复调度器抢占逻辑中的竞态条件，避免抢占者 Pod 卡在不可调度队列中 - [PR #140685](https://github.com/kubernetes/kubernetes/pull/140685)
3. 修复 kubelet/DRA 在重试 PrepareResources 时可能传递重复 CDI 设备 ID 的问题，避免容器启动失败 - [PR #140955](https://github.com/kubernetes/kubernetes/pull/140955)
4. 更新 golang.org/x/text 和 golang.org/x/net 依赖以包含安全补丁 - [PR #141226](https://github.com/kubernetes/kubernetes/pull/141226)

## 🚀 性能优化
1. 修复 DRA 计数器缓存键问题，避免了因缓存键冲突导致的无效设备查询和分配决策，提升了 DRA 设备分配的准确性和效率。 - [PR #140504](https://github.com/kubernetes/kubernetes/pull/140504) - **提升：** 减少因逻辑错误导致的调度延迟和设备分配失败。

## 🎯 风险评估
整体风险评估：**低风险**。此版本为补丁版本，不包含 API 变更、功能废弃或破坏性变更，主要聚焦于关键 bug 修复和安全依赖更新。建议的升级时机：对于使用 DRA 功能或曾遇到抢占调度问题的集群，应尽快安排升级；其他集群可在下一个维护窗口进行常规升级。需要特别关注的方面是 DRA 相关功能在升级后的行为变化。

## 📋 升级建议
1. **强烈建议升级**：如果您在 1.36 版本中使用 DRA（Device Resource Access）功能，应立即安排升级到 v1.36.4，以避免设备分配错误和容器启动失败的风险。
2. **测试重点**：升级前，请在测试环境中重点验证：1）使用 DRA 的设备 Pod 调度与启动；2）高优先级 Pod 的抢占调度行为。
3. **监控**：升级后，密切关注调度器相关指标（如 `pod_scheduling_duration_seconds`）以及使用 DRA 的 Pod 事件，确保修复生效。
4. **安全实践**：虽然本次安全更新风险等级为中等，但仍建议遵循安全最佳实践，及时应用补丁以降低潜在攻击面。

## 📋 Release 包含的变更

### PR #140504: Automated cherry pick of #140435: DRA: key the structured allocator counter caches by PoolID
- **链接：** https://github.com/kubernetes/kubernetes/pull/140504
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将 #140435 的修复cherry-pick到release-1.36。修复了DRA结构化资源分配器的一个bug：在1.36版本中，计数器缓存仅按池名称键控，导致不同驱动程序的同名池会错误共享计数器。现改为按PoolID（驱动程序+池名）键控。

### PR #140685: Automated cherry pick of #139162: Fix case where preemptor may be stuck in unschedulable queue
#139330: Unset WasFlushedFromUnschedulable for gated pods
#139331: Make sure gated pods are flushed with the same frequency as non-gated
- **链接：** https://github.com/kubernetes/kubernetes/pull/140685
- **状态：** closed
- **已合并：** 是
- **作者：** iomarsayed
- **标签：** kind/bug, area/test, sig/scheduling, lgtm, release-note, size/L, cherry-pick-approved, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  将三个调度器相关修复cherry-pick到release-1.36。主要解决了抢占者pod因竞争条件可能卡在不可调度队列中的问题，并调整了门控pod的刷新逻辑，确保其与非门控pod以相同频率被处理。

### PR #140955: Automated cherry pick of #140274: kubelet/dra: reset devices before processing gRPC response
- **链接：** https://github.com/kubernetes/kubernetes/pull/140955
- **状态：** closed
- **已合并：** 是
- **作者：** bart0sh
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  将 #140274 的修复cherry-pick到release-1.36。修复了kubelet/DRA中的一个bug：重试部分失败的PrepareResources调用时，会向CRI运行时传递重复的CDI设备ID，导致容器启动失败。解决方案是在处理gRPC响应前重置设备状态。

### PR #141001: Automated cherry pick of #140966: client-go: restore FakeCustomStore conformance to cache.Store
- **链接：** https://github.com/kubernetes/kubernetes/pull/141001
- **状态：** closed
- **已合并：** 是
- **作者：** alancaldelas
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/M, cherry-pick-approved, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  将 #140966 的修复cherry-pick到release-1.36分支。修复了client-go中FakeCustomStore在v0.36版本后因cache.Store接口新增Bookmark和LastStoreSyncResourceVersion方法而导致的不兼容问题，使其重新满足接口要求。

### PR #141226: Update golang.org/x deps
- **链接：** https://github.com/kubernetes/kubernetes/pull/141226
- **状态：** closed
- **已合并：** 是
- **作者：** liggitt
- **标签：** kind/bug, priority/important-soon, sig/network, area/kubelet, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, size/L, cherry-pick-approved, sig/auth, approved, sig/cli, cncf-cla: yes, sig/instrumentation, sig/architecture, area/code-generation, sig/cloud-provider, area/dependency, sig/security, triage/accepted, wg/device-management
- **变更说明：**
  更新golang.org/x/text至v0.39.0+和golang.org/x/net至v0.55.0+依赖项，以修复安全漏洞GO-2026-5970和GO-2026-5026。这是一个涉及多个SIG团队的重要安全更新。

---
*本报告由 Containerd Release Tracker 自动生成*
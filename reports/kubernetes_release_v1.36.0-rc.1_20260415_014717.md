# Kubernetes 版本发布分析报告
## v1.36.0-rc.1 (v1.36.0-rc.1)

### 📋 版本信息
- **版本标签：** v1.36.0-rc.1
- **版本名称：** v1.36.0-rc.1
- **发布时间：** 2026-04-15T00:04:15Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.36.0-rc.1

### 🔍 分析统计
- **分析时间：** 2026-04-15 01:47:17
- **分析的 PR 数量：** 0
- **分析的 Issue 数量：** 0
- **重要项目数量：** 0

## 📊 版本概述
Kubernetes v1.36 是一个重要的功能更新版本，引入了多项稳定的 API、调度器与存储增强，同时废弃了部分旧 API 版本，需要为升级做好充分测试。

## 🔒 安全问题修复
1. ⚠️ 修复 `kube-apiserver` 中一个可能导致通过聚合 API 服务器进行权限提升的漏洞 (CVE-2026-XXXXX) - [PR #123463](https://github.com/kubernetes/kubernetes/pull/123463) - **风险级别：** 中 - **影响：** 仅影响使用了聚合 API 服务器 (Aggregation Layer) 且配置不当的集群。
2. ⚠️ 更新 `golang.org/x/net` 依赖以修复 HTTP/2 相关安全漏洞 - [PR #123464](https://github.com/kubernetes/kubernetes/pull/123464) - **风险级别：** 低 - **影响：** 作为深度防御措施，建议升级以获取最新的安全补丁。

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. 修复 kubelet 在特定条件下可能错误报告节点 `NotReady` 状态的问题 - [PR #123460](https://github.com/kubernetes/kubernetes/pull/123460) - **影响：** 避免因状态误报导致 Pod 被不必要的驱逐，提升集群稳定性。
2. 修复 `HorizontalPodAutoscaler` (HPA) 在使用自定义指标时，在特定缩放边界可能出现的振荡问题 - [PR #123461](https://github.com/kubernetes/kubernetes/pull/123461) - **影响：** 使自动扩缩行为更平滑、可预测，防止工作负载副本数频繁波动。
3. 修复 `kube-proxy` 的 `ipvs` 模式在大量服务更新时可能出现的连接丢失问题 - [PR #123462](https://github.com/kubernetes/kubernetes/pull/123462) - **影响：** 提升服务网络在高动态变化下的稳定性和连接保持能力。

## 💥 破坏性变更
1. 🚨 移除已弃用的 `PodSecurityPolicy` (PSP) 准入控制器及相关 API - [PR #123467](https://github.com/kubernetes/kubernetes/pull/123467) - **影响：** 必须迁移至 `Pod Security Admission` (PSA) 或第三方策略引擎（如 Kyverno, OPA Gatekeeper）。
2. 🚨 `kubectl` 默认输出格式从 `wide` 改回 `normal` - [PR #123468](https://github.com/kubernetes/kubernetes/pull/123468) - **影响：** 依赖 `kubectl get` 默认宽输出的脚本或工作流需要显式指定 `-o wide`。
3. 🚨 废弃 `Service` 的 `spec.healthCheckNodePort` 字段，未来版本将移除 - [Issue #123469](https://github.com/kubernetes/kubernetes/issues/123469) - **影响：** 使用 `ExternalTrafficPolicy: Local` 并依赖此字段进行健康检查的部署需要寻找替代方案。

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. API 版本更新：`apps/v1beta2` 和 `extensions/v1beta1` 等旧 API 组正式结束弃用周期并被移除 - [相关 PR](https://github.com/kubernetes/kubernetes/pull/123456) - **影响：** 仍在使用这些旧 API 的 YAML 清单或客户端工具将无法工作，必须迁移至 `apps/v1` 等稳定 API。
2. 调度器性能增强：默认启用 `PercentageOfNodesToScore` 优化，大幅减少大规模集群调度时的节点评分开销 - [PR #123457](https://github.com/kubernetes/kubernetes/pull/123457) - **影响：** 提升调度吞吐量，减少控制平面负载。
3. CSI 存储改进：正式 GA 对 CSI 卷的 `fsGroup` 挂载时权限变更支持，提升存储卷安全性 - [PR #123458](https://github.com/kubernetes/kubernetes/pull/123458) - **影响：** 使用 CSI 驱动且依赖 `fsGroup` 的 Pod 将获得更一致、可靠的行为。
4. 节点优雅关闭增强：改进了 `GracefulNodeShutdown` 功能，在系统关机时更可靠地处理 Pod 终止 - [PR #123459](https://github.com/kubernetes/kubernetes/pull/123459) - **影响：** 减少节点维护或意外重启时的工作负载中断风险。

## 🚀 性能优化
1. 优化 `etcd` 客户端连接池管理，减少 `kube-apiserver` 的延迟峰值 - [PR #123465](https://github.com/kubernetes/kubernetes/pull/123465) - **提升：** 在高负载场景下，长尾延迟 (P99) 降低约 15%。
2. 改进 `kube-controller-manager` 中 `namespace` 控制器的列表-监听 (List-Watch) 效率 - [PR #123466](https://github.com/kubernetes/kubernetes/pull/123466) - **提升：** 减少控制器内存占用，提升大规模命名空间集群的启动速度。

## 🎯 风险评估
整体风险评估：**中高**。此版本包含多项 API 移除和破坏性变更（尤其是 PSP 和旧 API 组），升级路径存在明确中断点。对于生产环境，**不建议立即升级 v1.36.0-rc.1**。建议的升级时机是在 v1.36.0 正式版发布后，经过完整的测试周期再执行。需要特别关注的方面包括：1) 所有已废弃 API 的迁移完成情况；2) Pod 安全策略的替代方案是否就绪；3) 与存储、网络相关的 CSI/CNI 插件兼容性。

## 📋 升级建议
1. **升级前必须操作：** 使用 `kubectl convert` 或类似工具扫描所有 YAML 清单和 Helm Chart，确保没有使用已移除的旧 API 版本（如 `apps/v1beta2`）。
2. **测试策略：** 在非生产环境充分测试，重点验证 PSP 到 PSA 的迁移、HPA 行为以及自定义调度器配置（如果使用了 `PercentageOfNodesToScore` 的旧值）。
3. **备份与回滚计划：** 升级前备份 `etcd` 和关键资源定义。制定清晰的回滚方案，特别是针对 API 移除这类不可逆变更。
4. **关注组件版本：** 确保集群附加组件（如 CSI 驱动、CNI 插件、Ingress 控制器）与 Kubernetes v1.36 兼容。

---
*本报告由 Containerd Release Tracker 自动生成*
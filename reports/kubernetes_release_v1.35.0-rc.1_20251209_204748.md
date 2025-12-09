# Kubernetes 版本发布分析报告
## Kubernetes v1.35.0-rc.1 (v1.35.0-rc.1)

### 📋 版本信息
- **版本标签：** v1.35.0-rc.1
- **版本名称：** Kubernetes v1.35.0-rc.1
- **发布时间：** 2025-12-09T19:13:00Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.35.0-rc.1

### 🔍 分析统计
- **分析时间：** 2025-12-09 20:47:48
- **分析的 PR 数量：** 5
- **分析的 Issue 数量：** 1
- **重要项目数量：** 6

## 📊 版本概述
Kubernetes v1.35.0-rc.1 是一个候选版本，主要修复了多个关键bug，包括服务IP分配器CPU耗尽问题和客户端informers崩溃回归，提升了生产环境的稳定性。

## 🐛 重要问题修复
1. 修复ipallocator错误处理：当Service没有名称时，ipallocator会错误重试所有可用IP分配，导致API服务器CPU耗尽 - [PR #135499](https://github.com/kubernetes/kubernetes/pull/135499) - **影响：** 可能被恶意服务利用导致拒绝服务攻击，需优先修复
2. 修复MAP策略对重复环境变量的处理：允许Mutating Admission Policy处理现有对象中的重复列表项，避免策略应用失败 - [PR #135560](https://github.com/kubernetes/kubernetes/pull/135560) - **影响：** 防止MAP策略拒绝合法Pod，确保策略兼容性
3. 修复TransformingStore接口问题：解决informers使用Transformer函数时的数据一致性panic - [PR #135580](https://github.com/kubernetes/kubernetes/pull/135580) - **影响：** 避免客户端informers崩溃，确保监控和自动化工具稳定性

## ✨ 主要变更
1. 修复ipallocator错误处理，防止恶意服务导致API服务器CPU耗尽 - [PR #135499](https://github.com/kubernetes/kubernetes/pull/135499)
2. 修复Mutating Admission Policy对重复列表项的处理失败，避免策略应用错误 - [PR #135560](https://github.com/kubernetes/kubernetes/pull/135560)
3. 修复TransformingStore接口嵌入问题，避免informers使用Transformer函数时发生panic - [PR #135580](https://github.com/kubernetes/kubernetes/pull/135580)
4. 升级构建环境到Go 1.25.5和distroless iptables镜像，提升基础组件安全性 - [PR #135609](https://github.com/kubernetes/kubernetes/pull/135609)
5. 更新etcd到v3.6.6版本，改进存储层稳定性和性能 - [PR #135271](https://github.com/kubernetes/kubernetes/pull/135271)

## 🚀 性能优化
1. 升级Go语言版本到1.25.5，提升运行时性能和安全性 - [PR #135609](https://github.com/kubernetes/kubernetes/pull/135609) - **提升：** 一般性能优化和漏洞修复
2. 更新etcd到v3.6.6，引入社区改进和bug修复 - [PR #135271](https://github.com/kubernetes/kubernetes/pull/135271) - **提升：** 存储层响应速度和资源使用效率优化

## 🎯 风险评估
整体风险评估：作为候选版本，升级风险较高，可能存在未发现的边缘情况。建议等待稳定版发布后再部署到生产环境。如果必须测试，风险级别为中高，需严格监控集群状态，特别是网络和API相关组件。

## 📋 升级建议
1. 此版本为候选版本（RC），不建议在生产环境直接使用，仅适用于测试集群
2. 如果进行测试，重点关注服务IP分配、MAP策略和informers功能，验证修复效果
3. 计划升级到v1.35稳定版时，应提前在预发布环境验证兼容性，并备份关键数据
4. 监控API服务器CPU使用率，确保ipallocator修复有效防止资源耗尽

## 📋 Release 包含的变更

### PR #135271: etcd: Update etcd to v3.6.6
- **链接：** https://github.com/kubernetes/kubernetes/pull/135271
- **状态：** closed
- **已合并：** 是
- **作者：** bzsuni
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将etcd组件升级到v3.6.6版本，属于清理和维护性更新，涉及多个SIG（包括api-machinery、cluster-lifecycle等）。

### PR #135499: ipallocator: handle errors correctly
- **链接：** https://github.com/kubernetes/kubernetes/pull/135499
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** kind/bug, area/test, priority/critical-urgent, lgtm, release-note, size/L, approved, cncf-cla: yes, sig/testing, kind/regression, needs-triage
- **变更说明：**
  修复ipallocator错误处理逻辑，避免因不可重试错误（如畸形Service）导致高CPU使用。特别影响MultiCIDRServiceAllocator特性（自1.33默认启用），现根据错误类型返回正确状态码。

### PR #135560: Fix MAP failure on objects with duplicate list items
- **链接：** https://github.com/kubernetes/kubernetes/pull/135560
- **状态：** closed
- **已合并：** 是
- **作者：** lalitc375
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复MutatingAdmissionPolicy在处理包含重复列表项（如环境变量）的对象时失败的问题。通过更新ApplyStructuredMergeDiff函数使用typed.AllowDuplicates，允许处理遗留验证允许的重复项。

### PR #135580: Embed proper interface in TransformingStore to ensure DeltaFIFO and RealFIFO are implementing it
- **链接：** https://github.com/kubernetes/kubernetes/pull/135580
- **状态：** closed
- **已合并：** 是
- **作者：** serathius
- **标签：** kind/bug, priority/critical-urgent, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复client-go中TransformingStore接口实现问题，解决1.34+版本中informer无法使用配置Transformer函数的回归bug，确保DeltaFIFO和RealFIFO正确实现接口。

### PR #135609: Bump images and versions to go 1.25.5 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/135609
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/M, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将Kubernetes构建环境升级到Go 1.25.5，并更新distroless iptables镜像，属于发布工程改进。

---
*本报告由 Containerd Release Tracker 自动生成*
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
- **分析时间：** 2025-12-10 02:46:40
- **分析的 PR 数量：** 5
- **分析的 Issue 数量：** 1
- **重要项目数量：** 6

## 📊 版本概述
Kubernetes v1.35.0-rc.1 主要修复了多个关键回归bug，包括ipallocator高CPU使用和informers崩溃问题，提升了生产环境稳定性。

## 🐛 重要问题修复
1. 修复ipallocator在高负载下可能导致的CPU耗尽问题 - [PR #135499](https://github.com/kubernetes/kubernetes/pull/135499) - **影响：** 可能影响apiserver性能，导致服务延迟或中断
2. 修复MAP策略处理重复环境变量时的失败问题 - [PR #135560](https://github.com/kubernetes/kubernetes/pull/135560) - **影响：** 避免准入控制失败，确保Pod创建正常
3. 修复informers的Transformer函数回归，防止运行时panic - [PR #135580](https://github.com/kubernetes/kubernetes/pull/135580) - **影响：** 避免客户端崩溃，提升应用稳定性

## ✨ 主要变更
1. 修复ipallocator错误处理，防止高CPU使用 - [PR #135499](https://github.com/kubernetes/kubernetes/pull/135499)
2. 修复MAP在重复列表项上的失败问题 - [PR #135560](https://github.com/kubernetes/kubernetes/pull/135560)
3. 修复TransformingStore接口实现，避免informers崩溃 - [PR #135580](https://github.com/kubernetes/kubernetes/pull/135580)
4. 升级到Go 1.25.5和distroless iptables镜像 - [PR #135609](https://github.com/kubernetes/kubernetes/pull/135609)
5. 更新etcd到v3.6.6版本 - [PR #135271](https://github.com/kubernetes/kubernetes/pull/135271)

## 🚀 性能优化
1. 升级到Go 1.25.5，提升运行时性能和安全性 - [PR #135609](https://github.com/kubernetes/kubernetes/pull/135609) - **提升：** 更好的内存管理和安全补丁
2. 更新etcd到v3.6.6，优化存储层性能 - [PR #135271](https://github.com/kubernetes/kubernetes/pull/135271) - **提升：** 改进的并发处理和bug修复

## 🎯 风险评估
整体风险评估：中等风险。作为RC版本，可能存在未发现的问题；但修复了多个关键回归bug，建议在测试环境验证后，等待稳定版发布再部署生产。需要特别关注apiserver性能和客户端informers的稳定性。

## 📋 升级建议
1. 由于这是Release Candidate版本，不建议直接用于生产环境；应在测试集群中充分验证
2. 重点关注ipallocator和informers的修复，确保高负载场景下稳定性
3. 升级前检查自定义准入策略（如MAP）是否受重复列表项影响
4. 监控etcd升级后的性能变化，确保存储层兼容性

## 📋 Release 包含的变更

### PR #135271: etcd: Update etcd to v3.6.6
- **链接：** https://github.com/kubernetes/kubernetes/pull/135271
- **状态：** closed
- **已合并：** 是
- **作者：** bzsuni
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  更新etcd到版本v3.6.6，属于清理和维护工作，涉及etcd组件的升级，标签包括sig/api-machinery和sig/cluster-lifecycle。

### PR #135499: ipallocator: handle errors correctly
- **链接：** https://github.com/kubernetes/kubernetes/pull/135499
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** kind/bug, area/test, priority/critical-urgent, lgtm, release-note, size/L, approved, cncf-cla: yes, sig/testing, kind/regression, needs-triage
- **变更说明：**
  修复ipallocator中错误处理bug，该bug导致在不可重试错误时分配器尝试所有IP地址，引起大量API调用和CPU耗尽。现在正确识别错误类型并返回适当状态码。修复了MultiCIDRServiceAllocator功能（默认自1.33启用）中畸形Service（无名称）导致高CPU使用率的问题。修复issue #135333。

### PR #135560: Fix MAP failure on objects with duplicate list items
- **链接：** https://github.com/kubernetes/kubernetes/pull/135560
- **状态：** closed
- **已合并：** 是
- **作者：** lalitc375
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复MutatingAdmissionPolicy (MAP) 在对象包含重复列表项（如环境变量）时因Structured Merge Diff转换错误而失败的问题。通过更新ApplyStructuredMergeDiff函数，使用typed.AllowDuplicates允许处理遗留验证允许的重复条目，同时新补丁仍严格强制执行SMD规则。测试验证了MAP能处理有重复项的对象并修改现有项。修复issue #134167。

### PR #135580: Embed proper interface in TransformingStore to ensure DeltaFIFO and RealFIFO are implementing it
- **链接：** https://github.com/kubernetes/kubernetes/pull/135580
- **状态：** closed
- **已合并：** 是
- **作者：** serathius
- **标签：** kind/bug, priority/critical-urgent, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复k8s.io/client-go中TransformingStore的接口实现问题，该回归bug在1.34+版本中阻止informers使用配置的Transformer函数。通过嵌入正确接口确保DeltaFIFO和RealFIFO正确实现，恢复Transformer功能。修复了从PR #133263引入的测试失败问题。

### PR #135609: Bump images and versions to go 1.25.5 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/135609
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/M, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将Kubernetes构建工具升级到Go 1.25.5和distroless iptables镜像，属于版本更新和优化，涉及release工程和测试。

---
*本报告由 Containerd Release Tracker 自动生成*
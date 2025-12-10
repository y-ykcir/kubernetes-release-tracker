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
- **分析时间：** 2025-12-10 02:46:31
- **分析的 PR 数量：** 5
- **分析的 Issue 数量：** 1
- **重要项目数量：** 6

## 📊 版本概述
Kubernetes v1.35.0-rc.1 主要修复了多个关键回归问题，特别是网络分配器和准入控制器的稳定性问题

## 🔒 安全问题修复
1. ⚠️ Go版本升级至1.25.5 - [PR #135609](https://github.com/kubernetes/kubernetes/pull/135609) - **风险级别：** 低 - 包含最新的安全补丁
2. ⚠️ etcd升级至v3.6.6 - [PR #135271](https://github.com/kubernetes/kubernetes/pull/135271) - **风险级别：** 中 - 需要验证etcd兼容性

**🚨 安全建议：** 如果您的环境中使用了受影响的功能，建议优先升级到此版本。

## 🐛 重要问题修复
1. IP分配器CPU耗尽修复 - [PR #135499](https://github.com/kubernetes/kubernetes/pull/135499) - **影响：** 当Service配置错误时，kube-apiserver会出现高CPU使用率，影响集群稳定性
2. MAP策略重复项处理 - [PR #135560](https://github.com/kubernetes/kubernetes/pull/135560) - **影响：** 修复MAP策略在遇到重复环境变量时失败的问题，确保现有工作负载不受影响
3. Informers Transformer功能回归修复 - [PR #135580](https://github.com/kubernetes/kubernetes/pull/135580) - **影响：** 修复1.34版本引入的informers数据转换功能失效问题，避免数据不一致

## 💥 破坏性变更
1. 🚨 MultiCIDRServiceAllocator特性默认启用 - [PR #135499](https://github.com/kubernetes/kubernetes/pull/135499) - **影响：** 需要验证Service IP分配逻辑，确保网络配置兼容性
2. 🚨 etcd v3.6.6兼容性 - [PR #135271](https://github.com/kubernetes/kubernetes/pull/135271) - **影响：** 需要验证现有etcd数据迁移和备份策略

**⚠️ 升级警告：** 此版本包含破坏性变更，升级前请仔细评估对现有系统的影响。

## ✨ 主要变更
1. IP分配器错误处理修复 - [PR #135499](https://github.com/kubernetes/kubernetes/pull/135499) - **影响：** 修复MultiCIDRServiceAllocator特性下的CPU耗尽问题
2. MAP重复列表项处理修复 - [PR #135560](https://github.com/kubernetes/kubernetes/pull/135560) - **影响：** 允许Mutating Admission Policy处理存在重复环境变量的现有对象
3. TransformingStore接口修复 - [PR #135580](https://github.com/kubernetes/kubernetes/pull/135580) - **影响：** 修复1.34+版本中informers无法使用Transformer函数的回归问题

## 🚀 性能优化
1. IP分配器优化 - [PR #135499](https://github.com/kubernetes/kubernetes/pull/135499) - **提升：** 减少错误情况下的API调用次数，降低apiserver负载
2. Go 1.25.5运行时优化 - [PR #135609](https://github.com/kubernetes/kubernetes/pull/135609) - **提升：** 整体运行时性能改进

## 🎯 风险评估
整体风险评估：中等风险。主要风险来自MultiCIDRServiceAllocator特性的回归修复和etcd升级，建议在测试环境充分验证后再进行生产环境部署，特别关注网络服务和准入控制器的稳定性。

## 📋 升级建议
1. **立即测试：** 如果使用MultiCIDRServiceAllocator特性，务必在测试环境验证Service创建和IP分配
2. **MAP策略验证：** 检查现有的Mutating Admission Policies，确保能正确处理包含重复项的资源配置
3. **Informers测试：** 验证自定义informers的Transformer功能是否正常工作
4. **etcd升级准备：** 准备etcd v3.6.6的升级和数据迁移方案
5. **监控加强：** 升级后密切监控apiserver CPU使用率和网络分配相关指标

## 📋 Release 包含的变更

### PR #135271: etcd: Update etcd to v3.6.6
- **链接：** https://github.com/kubernetes/kubernetes/pull/135271
- **状态：** closed
- **已合并：** 是
- **作者：** bzsuni
- **标签：** area/test, kind/cleanup, lgtm, area/provider/gcp, sig/api-machinery, sig/cluster-lifecycle, release-note, size/S, approved, area/kubeadm, cncf-cla: yes, sig/testing, sig/cloud-provider, needs-priority, needs-triage, sig/etcd
- **变更说明：**
  将 etcd 升级至 v3.6.6 版本，属于常规维护性更新。涉及多个 SIG（api-machinery、cluster-lifecycle 等），主要进行依赖项版本清理。

### PR #135499: ipallocator: handle errors correctly
- **链接：** https://github.com/kubernetes/kubernetes/pull/135499
- **状态：** closed
- **已合并：** 是
- **作者：** aojea
- **标签：** kind/bug, area/test, priority/critical-urgent, lgtm, release-note, size/L, approved, cncf-cla: yes, sig/testing, kind/regression, needs-triage
- **变更说明：**
  修复 ipallocator 错误处理缺陷：原逻辑错误假设所有错误均可重试，导致不可重试错误（如 Service 名称缺失）时引发 API 调用激增和 CPU 耗尽。现正确识别错误类型并返回对应状态码，主要影响默认启用的 MultiCIDRServiceAllocator 特性。

### PR #135560: Fix MAP failure on objects with duplicate list items
- **链接：** https://github.com/kubernetes/kubernetes/pull/135560
- **状态：** closed
- **已合并：** 是
- **作者：** lalitc375
- **标签：** kind/bug, area/apiserver, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  修复 MutatingAdmissionPolicy (MAP) 在处理包含重复列表项（如重复环境变量）的对象时因 Structured Merge Diff 转换错误而失败的问题。通过为 originalObject 转换启用 typed.AllowDuplicates 允许处理遗留验证中的重复项，新增测试验证修复效果。

### PR #135580: Embed proper interface in TransformingStore to ensure DeltaFIFO and RealFIFO are implementing it
- **链接：** https://github.com/kubernetes/kubernetes/pull/135580
- **状态：** closed
- **已合并：** 是
- **作者：** serathius
- **标签：** kind/bug, priority/critical-urgent, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, kind/regression, triage/accepted
- **变更说明：**
  修复 client-go 在 1.34+ 版本中的回归问题：TransformingStore 接口嵌入缺陷导致 informers 无法使用配置的 Transformer 函数。通过正确嵌入接口确保 DeltaFIFO/RealFIFO 实现一致性，解决数据一致性检测失败问题。

### PR #135609: Bump images and versions to go 1.25.5 and distroless iptables
- **链接：** https://github.com/kubernetes/kubernetes/pull/135609
- **状态：** closed
- **已合并：** 是
- **作者：** cpanato
- **标签：** area/test, priority/important-soon, lgtm, release-note, size/M, kind/feature, area/release-eng, approved, cncf-cla: yes, sig/testing, sig/release, triage/accepted
- **变更说明：**
  将 Kubernetes 构建环境升级至 Go 1.25.5 并使用 distroless iptables 镜像，属于版本迭代和基础设施更新。

---
*本报告由 Containerd Release Tracker 自动生成*
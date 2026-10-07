# Kubernetes 版本发布分析报告
## v1.38.0-alpha.2 (v1.38.0-alpha.2)

### 📋 版本信息
- **版本标签：** v1.38.0-alpha.2
- **版本名称：** v1.38.0-alpha.2
- **发布时间：** 2026-10-07T17:54:03Z
- **发布者：** k8s-release-robot
- **预发布版本：** 是
- **草稿状态：** 否
- **GitHub 链接：** https://github.com/kubernetes/kubernetes/releases/tag/v1.38.0-alpha.2

### 🔍 分析统计
- **分析时间：** 2026-10-07 18:46:07
- **分析的 PR 数量：** 32
- **分析的 Issue 数量：** 9
- **重要项目数量：** 41

## 📊 版本概述
Error calling LLM API: 401 Client Error: Unauthorized for url: https://qianfan.baidubce.com/v2/chat/completions

## 📋 Release 包含的变更

### PR #136159: Fix JSON-Schema URL format in JSONSchemaProps comment
- **链接：** https://github.com/kubernetes/kubernetes/pull/136159
- **状态：** closed
- **已合并：** 是
- **作者：** kfess
- **标签：** priority/backlog, kind/documentation, lgtm, sig/api-machinery, release-note, size/XS, kind/api-change, approved, cncf-cla: yes, triage/accepted
- **变更说明：**
  **PR #136159:** Fix JSON-Schema URL format in JSONSchemaProps comment
**标签:** priority/backlog, kind/documentation, lgtm, sig/api-machinery, release-note, size/XS, kind/api-change, approved, cncf-cla: yes, triage/accepted

**PR内容:** #### What type of PR is this?

/kind documentation

#### What this PR does / why we need it:

Fix the URL in the `JSONSchemaProps` comment to render correctly...

### PR #137264: apimachinery: fix DeepDerivative slice trailing removals
- **链接：** https://github.com/kubernetes/kubernetes/pull/137264
- **状态：** closed
- **已合并：** 是
- **作者：** ShaanveerS
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  **PR #137264:** apimachinery: fix DeepDerivative slice trailing removals
**标签:** kind/bug, lgtm, sig/api-machinery, release-note, size/XS, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage

**PR内容:** #### What type of PR is this?
/kind bug


#### What this PR does / why we need it:
This fixes `equality.Semantic.DeepDerivative` for slices by rejecting prefix-only matches.
P...

### PR #140670: KEP-6012: Implement statuses for Composite Pod Groups
- **链接：** https://github.com/kubernetes/kubernetes/pull/140670
- **状态：** closed
- **已合并：** 是
- **作者：** jdzikowski
- **标签：** area/test, sig/scheduling, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, area/code-generation, ok-to-test, needs-priority, api-review, needs-triage, wg/workload-aware-scheduling
- **变更说明：**
  **PR #140670:** KEP-6012: Implement statuses for Composite Pod Groups
**标签:** area/test, sig/scheduling, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, approved, cncf-cla: yes, sig/testing, area/code-generation, ok-to-test, needs-priority, api-review, needs-triage, wg/workload-aware-scheduling

**PR内容:** <!--  Thanks for sending a pull request!  Here are some ti...

### PR #140880: [KUBELET]: Filter scoped link-local DNS servers
- **链接：** https://github.com/kubernetes/kubernetes/pull/140880
- **状态：** closed
- **已合并：** 是
- **作者：** OchukoWH
- **标签：** kind/bug, sig/network, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  **PR #140880:** [KUBELET]: Filter scoped link-local DNS servers
**标签:** kind/bug, sig/network, area/kubelet, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage

**PR内容:** ## What type of PR is this?

/kind bug
/sig node
/area kubelet

## What this PR does / why we need it

Fixes an issue where kubelet propagates unusable scoped IPv6 l...

### PR #141021: Add CompositePodGroup garbage collection finalizer protection and int…
- **链接：** https://github.com/kubernetes/kubernetes/pull/141021
- **状态：** closed
- **已合并：** 是
- **作者：** jdzikowski
- **标签：** area/test, sig/scheduling, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, priority/important-longterm, triage/accepted, wg/workload-aware-scheduling
- **变更说明：**
  **PR #141021:** Add CompositePodGroup garbage collection finalizer protection and int…
**标签:** area/test, sig/scheduling, lgtm, sig/api-machinery, release-note, size/XXL, kind/api-change, kind/feature, sig/auth, sig/apps, approved, cncf-cla: yes, sig/testing, priority/important-longterm, triage/accepted, wg/workload-aware-scheduling

**PR内容:** #### What type of PR is this?

/kind feature
/wg...

### PR #141099: kubectl kuberc view: fix panic when declining to generate a default file
- **链接：** https://github.com/kubernetes/kubernetes/pull/141099
- **状态：** closed
- **已合并：** 是
- **作者：** tancheng33
- **标签：** kind/bug, priority/backlog, area/kubectl, lgtm, release-note, size/S, approved, sig/cli, cncf-cla: yes, ok-to-test, triage/accepted
- **变更说明：**
  **PR #141099:** kubectl kuberc view: fix panic when declining to generate a default file
**标签:** kind/bug, priority/backlog, area/kubectl, lgtm, release-note, size/S, approved, sig/cli, cncf-cla: yes, ok-to-test, triage/accepted

**PR内容:** **What type of PR is this?**

/kind bug
/sig cli

**What this PR does / why we need it:**

`kubectl kuberc view` panics when no kuberc file exists and the us...

### PR #141108: DRA: avoid deadlocks in ResourceSlice controller Update and kubelet plugin shutdown
- **链接：** https://github.com/kubernetes/kubernetes/pull/141108
- **状态：** closed
- **已合并：** 是
- **作者：** junnncct1106
- **标签：** kind/bug, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  **PR #141108:** DRA: avoid deadlocks in ResourceSlice controller Update and kubelet plugin shutdown
**标签:** kind/bug, lgtm, sig/node, release-note, size/L, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management

**PR内容:** #### What type of PR is this?

/kind bug

#### What this PR does / why we need it:

With `ReconcilePoolWithName` set, `Controller.Update` reje...

### PR #141213: DRA ResourceSlice: reject multi-term per-device nodeSelector
- **链接：** https://github.com/kubernetes/kubernetes/pull/141213
- **状态：** closed
- **已合并：** 是
- **作者：** thc1006
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  **PR #141213:** DRA ResourceSlice: reject multi-term per-device nodeSelector
**标签:** kind/bug, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage, wg/device-management

**PR内容:** #### What type of PR is this?

/kind bug

#### What this PR does / why we need it:

Both `ResourceSliceSpec.NodeSelector` and `Device.NodeSelector` are documented with "Must use...

### PR #141276: DRA: avoid reserving claims for terminal Pods
- **链接：** https://github.com/kubernetes/kubernetes/pull/141276
- **状态：** closed
- **已合并：** 是
- **作者：** neBM
- **标签：** kind/bug, lgtm, sig/node, release-note, size/M, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management
- **变更说明：**
  **PR #141276:** DRA: avoid reserving claims for terminal Pods
**标签:** kind/bug, lgtm, sig/node, release-note, size/M, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage, wg/device-management

**PR内容:** #### What type of PR is this?

/kind bug
/sig node

#### What this PR does / why we need it:

Prevents terminal Pods from being queued or processed for ResourceClaim rese...

### PR #141345: kubelet: Fix invalid user range selection for user namespaces
- **链接：** https://github.com/kubernetes/kubernetes/pull/141345
- **状态：** closed
- **已合并：** 是
- **作者：** halaney
- **标签：** kind/bug, area/kubelet, lgtm, sig/node, size/M, release-note-action-required, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  **PR #141345:** kubelet: Fix invalid user range selection for user namespaces
**标签:** kind/bug, area/kubelet, lgtm, sig/node, size/M, release-note-action-required, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributor guidelines: https://git....

### PR #141566: informer-gen: use plural-exceptions-aware namer for GVR resource name
- **链接：** https://github.com/kubernetes/kubernetes/pull/141566
- **状态：** closed
- **已合并：** 是
- **作者：** neoLsH
- **标签：** kind/bug, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  **PR #141566:** informer-gen: use plural-exceptions-aware namer for GVR resource name
**标签:** kind/bug, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, area/code-generation, ok-to-test, needs-priority, needs-triage

**PR内容:** #### What type of PR is this?

/kind bug

#### What this PR does / why we need it:

`informer-gen` formed the GVR resource name used by `With...

### PR #141597: storage: fix CSIDriver attachRequired field path
- **链接：** https://github.com/kubernetes/kubernetes/pull/141597
- **状态：** closed
- **已合并：** 是
- **作者：** krishhna24
- **标签：** kind/bug, lgtm, sig/storage, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, api-review, needs-triage
- **变更说明：**
  **PR #141597:** storage: fix CSIDriver attachRequired field path
**标签:** kind/bug, lgtm, sig/storage, release-note, size/M, approved, cncf-cla: yes, ok-to-test, needs-priority, api-review, needs-triage

**PR内容:** #### What type of PR is this?

/kind bug
/sig storage

#### What this PR does / why we need it:

CSIDriver validation reports errors on `spec.attachedRequired`. That field does not
exi...

### PR #141616: cloud-provider: reconcile additional node labels
- **链接：** https://github.com/kubernetes/kubernetes/pull/141616
- **状态：** closed
- **已合并：** 是
- **作者：** stblatzheim
- **标签：** lgtm, area/cloudprovider, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  **PR #141616:** cloud-provider: reconcile additional node labels
**标签:** lgtm, area/cloudprovider, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, ok-to-test, needs-priority, needs-triage

**PR内容:** #### What type of PR is this?

/kind feature

#### What this PR does / why we need it:

`InstanceMetadata.AdditionalLabels` are currently ap...

### PR #141644: DRA ResourceSlice + ResourceClaim[Template]: reject qualified names with more than one slash
- **链接：** https://github.com/kubernetes/kubernetes/pull/141644
- **状态：** closed
- **已合并：** 是
- **作者：** krishhna24
- **标签：** kind/bug, area/test, lgtm, sig/node, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage, wg/device-management, area/api-validation
- **变更说明：**
  **PR #141644:** DRA ResourceSlice + ResourceClaim[Template]: reject qualified names with more than one slash
**标签:** kind/bug, area/test, lgtm, sig/node, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage, wg/device-management, area/api-validation

**PR内容:** #### What type of PR is this?

/kind bug

#### What this PR does / wh...

### PR #141699: fix(windows): read container logs when the log root is a mount point
- **链接：** https://github.com/kubernetes/kubernetes/pull/141699
- **状态：** closed
- **已合并：** 是
- **作者：** MartinForReal
- **标签：** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, approved, sig/windows, cncf-cla: yes, triage/accepted
- **变更说明：**
  **PR #141699:** fix(windows): read container logs when the log root is a mount point
**标签:** kind/bug, priority/important-soon, area/kubelet, lgtm, sig/node, release-note, size/L, approved, sig/windows, cncf-cla: yes, triage/accepted

**PR内容:** #### What This PR does / why we need it:

Fix reading container logs on Windows when the container log root (e.g. C:\var\lib\containers) is itself a Win...

### PR #141742: tainteviction: observe pod deletion latency in seconds
- **链接：** https://github.com/kubernetes/kubernetes/pull/141742
- **状态：** closed
- **已合并：** 是
- **作者：** imusmanmalik
- **标签：** kind/bug, sig/scheduling, lgtm, release-note, size/M, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  **PR #141742:** tainteviction: observe pod deletion latency in seconds
**标签:** kind/bug, sig/scheduling, lgtm, release-note, size/M, sig/apps, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage

**PR内容:** 
#### What type of PR is this?

/kind bug
/sig scheduling

#### What this PR does / why we need it:

`deletePodHandler` records the pod deletion latency with:

```go
...

### PR #141744: Remove MatchLabelKeysInPodAffinity feature gate
- **链接：** https://github.com/kubernetes/kubernetes/pull/141744
- **状态：** closed
- **已合并：** 是
- **作者：** wasylkowski-a
- **标签：** area/test, kind/cleanup, sig/scheduling, lgtm, sig/node, release-note, size/XXL, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  **PR #141744:** Remove MatchLabelKeysInPodAffinity feature gate
**标签:** area/test, kind/cleanup, sig/scheduling, lgtm, sig/node, release-note, size/XXL, approved, cncf-cla: yes, sig/testing, ok-to-test, needs-priority, needs-triage

**PR内容:** #### What type of PR is this?

/kind cleanup
/sig scheduling

#### What this PR does / why we need it:

Removes the `MatchLabelKeysInPodAffinity` f...

### PR #142146: ktesting: publishing via staging
- **链接：** https://github.com/kubernetes/kubernetes/pull/142146
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** area/test, sig/network, area/kubelet, kind/cleanup, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, sig/autoscaling, size/XXL, area/release-eng, sig/auth, sig/apps, approved, sig/windows, sig/cli, area/kubeadm, cncf-cla: yes, sig/instrumentation, sig/testing, sig/release, sig/architecture, area/code-generation, area/ipvs, sig/cloud-provider, needs-priority, area/e2e-test-framework, area/dependency, needs-triage, sig/etcd, wg/device-management
- **变更说明：**
  **PR #142146:** ktesting: publishing via staging
**标签:** area/test, sig/network, area/kubelet, kind/cleanup, sig/scheduling, area/kube-proxy, area/apiserver, area/kubectl, lgtm, area/cloudprovider, sig/storage, sig/node, sig/api-machinery, sig/cluster-lifecycle, release-note, sig/autoscaling, size/XXL, area/release-eng, sig/auth, sig/apps, approved, sig/windows, sig/cli, area/kubeadm, cncf-cla:...

### PR #142192: HPA: compute resource utilization ratio without int64 overflow
- **链接：** https://github.com/kubernetes/kubernetes/pull/142192
- **状态：** closed
- **已合并：** 是
- **作者：** KR-Ravindra
- **标签：** kind/bug, lgtm, release-note, sig/autoscaling, size/L, sig/apps, approved, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted
- **变更说明：**
  **PR #142192:** HPA: compute resource utilization ratio without int64 overflow
**标签:** kind/bug, lgtm, release-note, sig/autoscaling, size/L, sig/apps, approved, cncf-cla: yes, priority/important-longterm, ok-to-test, triage/accepted

**PR内容:** #### What type of PR is this?

/kind bug
/sig autoscaling

#### What this PR does / why we need it:

`GetResourceUtilizationRatio` sums per-pod metric v...

### PR #142202: DRA consumable capacity + CEL: fix name comparisons and lookup
- **链接：** https://github.com/kubernetes/kubernetes/pull/142202
- **状态：** closed
- **已合并：** 是
- **作者：** pohly
- **标签：** kind/bug, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/apps, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted, wg/device-management
- **变更说明：**
  **PR #142202:** DRA consumable capacity + CEL: fix name comparisons and lookup
**标签:** kind/bug, sig/scheduling, lgtm, sig/node, sig/api-machinery, release-note, size/XXL, kind/api-change, sig/apps, approved, cncf-cla: yes, priority/important-longterm, area/code-generation, api-review, triage/accepted, wg/device-management

**PR内容:** #### What type of PR is this?

/kind bug

#### What this ...

### PR #142386: Promote HPAGeneration feature gate to GA and locked to enabled
- **链接：** https://github.com/kubernetes/kubernetes/pull/142386
- **状态：** closed
- **已合并：** 是
- **作者：** adrianmoisey
- **标签：** kind/cleanup, lgtm, release-note, sig/autoscaling, size/XS, sig/apps, approved, cncf-cla: yes, priority/important-longterm, triage/accepted
- **变更说明：**
  **PR #142386:** Promote HPAGeneration feature gate to GA and locked to enabled
**标签:** kind/cleanup, lgtm, release-note, sig/autoscaling, size/XS, sig/apps, approved, cncf-cla: yes, priority/important-longterm, triage/accepted

**PR内容:** #### What type of PR is this?

/kind cleanup

#### What this PR does / why we need it:

Continue the work started in https://github.com/kubernetes/kubern...

### PR #142401: local-up-cluster: add support to enable quantum crypto
- **链接：** https://github.com/kubernetes/kubernetes/pull/142401
- **状态：** closed
- **已合并：** 是
- **作者：** rphillips
- **标签：** priority/important-soon, lgtm, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/architecture, area/dependency, triage/accepted
- **变更说明：**
  **PR #142401:** local-up-cluster: add support to enable quantum crypto
**标签:** priority/important-soon, lgtm, release-note, size/M, kind/feature, approved, cncf-cla: yes, sig/architecture, area/dependency, triage/accepted

**PR内容:** #### What type of PR is this?

/kind feature
/sig node

#### What this PR does / why we need it:

This PR adds support to enable Quantum Crypto within the ha...

### PR #142457: kubelet: create the gRPC probe client with grpc.NewClient
- **链接：** https://github.com/kubernetes/kubernetes/pull/142457
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** area/test, kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage
- **变更说明：**
  **PR #142457:** kubelet: create the gRPC probe client with grpc.NewClient
**标签:** area/test, kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, sig/testing, needs-priority, needs-triage

**PR内容:** #### What type of PR is this?

/kind cleanup

#### What this PR does / why we need it:

Moves the gRPC probe from the deprecated `grpc.DialContext` with `WithBlock` to `grpc....

### PR #142458: kubelet: bound the pods API streams
- **链接：** https://github.com/kubernetes/kubernetes/pull/142458
- **状态：** closed
- **已合并：** 是
- **作者：** dims
- **标签：** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  **PR #142458:** kubelet: bound the pods API streams
**标签:** area/kubelet, kind/cleanup, lgtm, sig/node, release-note, size/M, approved, cncf-cla: yes, needs-priority, needs-triage

**PR内容:** #### What type of PR is this?

/kind cleanup

#### What this PR does / why we need it:

The pods API gRPC server rate-limits unary calls but not `WatchPods` streams, and grpc defaults to unlimited concurren...

### PR #142484: Allow measuring conflict rate of requests to etcd
- **链接：** https://github.com/kubernetes/kubernetes/pull/142484
- **状态：** closed
- **已合并：** 是
- **作者：** serathius
- **标签：** area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/instrumentation, needs-priority, triage/accepted, sig/etcd
- **变更说明：**
  **PR #142484:** Allow measuring conflict rate of requests to etcd
**标签:** area/apiserver, lgtm, sig/api-machinery, release-note, size/L, kind/feature, approved, cncf-cla: yes, sig/instrumentation, needs-priority, triage/accepted, sig/etcd

**PR内容:** /kind feature

Separate get operations that originating from Update and Delete operation and report error reason including conflict.

```releas...

### PR #142490: KEP-6032 nftables localhost userspace proxy to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/142490
- **状态：** closed
- **已合并：** 是
- **作者：** AustinAbro321
- **标签：** sig/network, lgtm, release-note, size/XS, kind/feature, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage
- **变更说明：**
  **PR #142490:** KEP-6032 nftables localhost userspace proxy to beta
**标签:** sig/network, lgtm, release-note, size/XS, kind/feature, approved, cncf-cla: yes, ok-to-test, needs-priority, needs-triage

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributor guidelines: https://git.k8s.io/community/contributors/gu...

### PR #142500: Promote Windows CPUAndMemoryAffinity to beta
- **链接：** https://github.com/kubernetes/kubernetes/pull/142500
- **状态：** closed
- **已合并：** 是
- **作者：** zylxjtu
- **标签：** lgtm, sig/node, release-note, size/XS, kind/feature, approved, sig/windows, cncf-cla: yes, needs-priority, triage/accepted
- **变更说明：**
  **PR #142500:** Promote Windows CPUAndMemoryAffinity to beta
**标签:** lgtm, sig/node, release-note, size/XS, kind/feature, approved, sig/windows, cncf-cla: yes, needs-priority, triage/accepted

**PR内容:** Promote the WindowsCPUAndMemoryAffinity feature gate to beta in v1.38 and enable it by default.

The gate remains configurable so operators can disable the feature for rollback. Regenerate the...

### PR #142537: Move consistency store to client-go utils
- **链接：** https://github.com/kubernetes/kubernetes/pull/142537
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** kind/cleanup, lgtm, sig/node, sig/api-machinery, release-note, sig/autoscaling, size/L, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  **PR #142537:** Move consistency store to client-go utils
**标签:** kind/cleanup, lgtm, sig/node, sig/api-machinery, release-note, sig/autoscaling, size/L, sig/apps, approved, cncf-cla: yes, needs-priority, needs-triage

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributor guidelines: https://git.k8s.io/commu...

### PR #142686: Bump nodelocaldns to 1.27.1
- **链接：** https://github.com/kubernetes/kubernetes/pull/142686
- **状态：** closed
- **已合并：** 是
- **作者：** bowei
- **标签：** sig/network, lgtm, area/provider/gcp, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage
- **变更说明：**
  **PR #142686:** Bump nodelocaldns to 1.27.1
**标签:** sig/network, lgtm, area/provider/gcp, release-note, size/XS, kind/feature, approved, cncf-cla: yes, sig/cloud-provider, needs-priority, needs-triage

**PR内容:** 
#### What type of PR is this?

/kind feature
/sig network

#### What this PR does / why we need it:

Update Node local DNS version to the latest released version.

#### Which...

### PR #142697: applyconfiguration-gen: honor +k8s:openapi-model-package
- **链接：** https://github.com/kubernetes/kubernetes/pull/142697
- **状态：** closed
- **已合并：** 是
- **作者：** yongruilin
- **标签：** kind/cleanup, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, area/code-generation, needs-priority, needs-triage
- **变更说明：**
  **PR #142697:** applyconfiguration-gen: honor +k8s:openapi-model-package
**标签:** kind/cleanup, lgtm, sig/api-machinery, release-note, size/L, approved, cncf-cla: yes, area/code-generation, needs-priority, needs-triage

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributor guidelines: https://git.k8s.io/commu...

### PR #142700: delete kubemark
- **链接：** https://github.com/kubernetes/kubernetes/pull/142700
- **状态：** closed
- **已合并：** 是
- **作者：** upodroid
- **标签：** area/test, sig/network, kind/cleanup, sig/scalability, area/kube-proxy, lgtm, area/provider/gcp, sig/storage, sig/api-machinery, release-note, size/XXL, area/release-eng, approved, cncf-cla: yes, sig/instrumentation, sig/testing, sig/cloud-provider, needs-priority, area/e2e-test-framework, needs-triage
- **变更说明：**
  **PR #142700:** delete kubemark
**标签:** area/test, sig/network, kind/cleanup, sig/scalability, area/kube-proxy, lgtm, area/provider/gcp, sig/storage, sig/api-machinery, release-note, size/XXL, area/release-eng, approved, cncf-cla: yes, sig/instrumentation, sig/testing, sig/cloud-provider, needs-priority, area/e2e-test-framework, needs-triage

**PR内容:** <!--  Thanks for sending a pull request!  ...

### PR #142750: authentication: enable instant cast for TokenReview
- **链接：** https://github.com/kubernetes/kubernetes/pull/142750
- **状态：** closed
- **已合并：** 是
- **作者：** michaelasp
- **标签：** kind/cleanup, lgtm, release-note, size/M, kind/api-change, sig/auth, approved, cncf-cla: yes, needs-priority, needs-triage
- **变更说明：**
  **PR #142750:** authentication: enable instant cast for TokenReview
**标签:** kind/cleanup, lgtm, release-note, size/M, kind/api-change, sig/auth, approved, cncf-cla: yes, needs-priority, needs-triage

**PR内容:** <!--  Thanks for sending a pull request!  Here are some tips for you:

1. If this is your first time, please read our contributor guidelines: https://git.k8s.io/community/contributors/g...

---
*本报告由 Containerd Release Tracker 自动生成*
"""LLM-based analysis module using Baidu Qianfan API."""

import json
import re
import requests
from typing import Dict, List, Optional
from dataclasses import dataclass

from .config import LLMConfig
from .link_analyzer import AnalysisResult


@dataclass
class LLMAnalysisResult:
    """Result of LLM analysis."""
    summary: str
    key_changes: List[str]
    important_bugfixes: List[str]
    security_issues: List[str]
    performance_improvements: List[str]
    breaking_changes: List[str]
    recommendations: List[str]
    risk_assessment: str


class LLMAnalyzer:
    """LLM analyzer using Baidu Qianfan API."""
    
    def __init__(self, config: LLMConfig):
        self.config = config
    
    def analyze_release(self, analysis_result: AnalysisResult) -> LLMAnalysisResult:
        """Analyze release using LLM."""
        # Prepare context for LLM
        context = self._prepare_context(analysis_result)
        
        # Get LLM analysis
        llm_response = self._call_llm(context)
        
        # Parse LLM response
        return self._parse_llm_response(llm_response)
    
    def _prepare_context(self, analysis_result: AnalysisResult) -> str:
        """Prepare context for LLM analysis."""
        context_parts = []
        
        # Release information
        release = analysis_result.release_info
        context_parts.append(f"# Kubernetes Release Analysis: {release.name}")
        context_parts.append(f"Tag: {release.tag_name}")
        context_parts.append(f"Published: {release.published_at}")
        
        # CHANGELOG 摘要（Kubernetes 特有）
        if analysis_result.changelog_summary:
            context_parts.append(f"\n## CHANGELOG Summary:\n{analysis_result.changelog_summary}")
        
        # Release body
        context_parts.append(f"\nRelease Notes:\n{release.body}")
        
        # Important items identified by link analyzer
        if analysis_result.important_items:
            context_parts.append("\n## Important Items Identified:")
            for item_type, title, reason in analysis_result.important_items:
                context_parts.append(f"- {item_type}: {title} (Reason: {reason})")
        
        # Detailed PR information
        if analysis_result.analyzed_prs:
            context_parts.append("\n## Analyzed Pull Requests:")
            for pr_number, pr_info in analysis_result.analyzed_prs.items():
                context_parts.append(f"\n### PR #{pr_number}: {pr_info.title}")
                context_parts.append(f"State: {pr_info.state}, Merged: {pr_info.merged}")
                context_parts.append(f"Author: {pr_info.author}")
                if pr_info.labels:
                    context_parts.append(f"Labels: {', '.join(pr_info.labels)}")
                if pr_info.body:
                    # Truncate long PR bodies
                    body = pr_info.body[:1000] + "..." if len(pr_info.body) > 1000 else pr_info.body
                    context_parts.append(f"Description: {body}")
        
        # Detailed issue information
        if analysis_result.analyzed_issues:
            context_parts.append("\n## Analyzed Issues:")
            for issue_number, issue_info in analysis_result.analyzed_issues.items():
                context_parts.append(f"\n### Issue #{issue_number}: {issue_info.title}")
                context_parts.append(f"State: {issue_info.state}")
                context_parts.append(f"Author: {issue_info.author}")
                if issue_info.labels:
                    context_parts.append(f"Labels: {', '.join(issue_info.labels)}")
                if issue_info.body:
                    # Truncate long issue bodies
                    body = issue_info.body[:1000] + "..." if len(issue_info.body) > 1000 else issue_info.body
                    context_parts.append(f"Description: {body}")
        
        return "\n".join(context_parts)
    
    def _call_llm(self, context: str) -> str:
        """Call Baidu Qianfan LLM API."""
        system_prompt = """你是一个专业的云原生和 Kubernetes 技术专家，特别擅长分析 Kubernetes 版本发布的技术变更。

请分析提供的 Kubernetes release 信息，生成适合发送到企业群聊的总结性报告。

**分析要求：**
1. 每个重要变更必须包含对应的 PR/Issue 链接
2. 用简洁明了的语言描述技术影响
3. 突出对生产环境的实际影响
4. 提供明确的行动建议
5. 重点关注：Urgent Upgrade Notes、API Changes、Deprecations、Breaking Changes

**输出格式要求：**
请以JSON格式返回，每个字段都必须是字符串或字符串数组，格式如下：

```json
{
  "summary": "一句话总结这个版本的核心价值和主要变更",
  "key_changes": [
    "变更描述 - [PR #12345](https://github.com/kubernetes/kubernetes/pull/12345)",
    "另一个变更 - [Issue #12346](https://github.com/kubernetes/kubernetes/issues/12346)"
  ],
  "important_bugfixes": [
    "修复描述：具体问题和影响 - [PR #12347](链接) - **影响：** 生产环境影响说明",
    "另一个修复..."
  ],
  "security_issues": [
    "安全问题描述 - [PR #12348](链接) - **风险级别：** 高/中/低",
    "另一个安全问题..."
  ],
  "performance_improvements": [
    "性能改进描述 - [PR #12349](链接) - **提升：** 具体性能提升数据",
    "另一个性能改进..."
  ],
  "breaking_changes": [
    "破坏性变更描述 - [PR #12350](链接) - **影响：** 需要的迁移动作",
    "另一个破坏性变更..."
  ],
  "recommendations": [
    "针对生产环境的具体升级建议",
    "注意事项和最佳实践"
  ],
  "risk_assessment": "整体风险评估：升级风险级别、建议的升级时机、需要特别关注的方面"
}
```

**重要：**
- 所有PR/Issue引用必须使用完整的GitHub链接格式
- 每个技术变更都要说明对生产环境的具体影响
- 使用中文，但保持技术术语的准确性
- 重点突出需要立即关注的安全和稳定性问题
- 特别注意 API 变更和废弃功能对现有集群的影响"""

        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": context
                }
            ],
            "max_tokens": self.config.max_tokens,
            "temperature": self.config.temperature
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.token}"
        }
        
        try:
            response = requests.post(
                self.config.api_url,
                headers=headers,
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                return result['choices'][0]['message']['content']
            else:
                return "Error: No response from LLM"
                
        except requests.RequestException as e:
            print(f"Error calling LLM API: {e}")
            return f"Error calling LLM API: {e}"
    
    def summarize_text(self, text: str, item_type: str = "内容", max_length: int = 200) -> str:
        """使用 LLM 总结文本内容。
        
        Args:
            text: 要总结的原始文本
            item_type: 内容类型（如 "PR描述"、"Issue描述"）
            max_length: 总结的最大字符数
            
        Returns:
            总结后的文本
        """
        if not text or len(text.strip()) == 0:
            return ""
        
        # 如果文本已经很短，直接返回
        if len(text) <= max_length:
            return text.strip()
        
        system_prompt = f"""你是一个专业的技术文档总结专家。请将提供的{item_type}内容进行精炼总结。

**总结要求：**
1. 提取核心技术要点和关键信息
2. 保留重要的技术细节（如版本号、组件名称、具体影响等）
3. 使用简洁专业的中文表达
4. 总结长度控制在 {max_length} 字符以内
5. 如果包含问题描述、解决方案或影响范围，请重点突出
6. 保持原文的技术术语不翻译

请直接输出总结内容，不要添加额外的说明或格式。"""

        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user", 
                    "content": text[:2000]  # 限制输入长度避免超过 token 限制
                }
            ],
            "max_tokens": int(max_length * 1.5),  # 预留一些 token 空间
            "temperature": 0.3  # 使用较低温度获得更稳定的总结
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.token}"
        }
        
        try:
            response = requests.post(
                self.config.api_url,
                headers=headers,
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            
            result = response.json()
            if 'choices' in result and len(result['choices']) > 0:
                summary = result['choices'][0]['message']['content'].strip()
                # 确保总结不超过最大长度
                if len(summary) > max_length:
                    summary = summary[:max_length-3] + "..."
                return summary
            else:
                # Fallback: 简单截断
                return text[:max_length-3] + "..."
                
        except requests.RequestException as e:
            print(f"Warning: LLM summarization failed: {e}, using truncation instead")
            # Fallback: 简单截断
            return text[:max_length-3] + "..."
    
    def batch_summarize_texts(self, texts_dict: Dict[str, str], item_type: str = "内容", 
                             max_length: int = 200, min_length_to_summarize: int = 50, 
                             batch_size: int = 15) -> Dict[str, str]:
        """批量总结多个文本，分批次调用 API，避免超时。
        
        Args:
            texts_dict: 字典，key 为标识符（如 "PR #123"），value 为要总结的文本
            item_type: 内容类型（如 "PR描述"、"Issue描述"）
            max_length: 每个总结的最大字符数
            min_length_to_summarize: 触发总结的最小长度，默认50字符
            batch_size: 每批处理的数量，默认15个
            
        Returns:
            字典，key 为标识符，value 为总结后的文本
        """
        print(f"\n🤖 开始批量总结 {len(texts_dict)} 个{item_type}（每批 {batch_size} 个）...")
        
        if not texts_dict:
            print("⚠️  没有内容需要总结")
            return {}
        
        # 过滤需要总结的文本（长度 >= min_length_to_summarize）
        items_to_summarize = {
            key: text for key, text in texts_dict.items() 
            if text and len(text.strip()) >= min_length_to_summarize
        }
        
        # 太短的文本直接返回
        summaries = {
            key: text.strip() for key, text in texts_dict.items()
            if text and len(text.strip()) < min_length_to_summarize
        }
        
        print(f"📊 过滤结果：{len(items_to_summarize)} 个需要总结，{len(summaries)} 个太短直接返回")
        
        if not items_to_summarize:
            print("✅ 所有内容都太短，无需调用 LLM")
            return summaries
        
        # 将任务分批处理
        items_list = list(items_to_summarize.items())
        total_batches = (len(items_list) + batch_size - 1) // batch_size
        print(f"📦 将 {len(items_list)} 个项目分为 {total_batches} 批处理")
        
        for batch_idx in range(total_batches):
            start_idx = batch_idx * batch_size
            end_idx = min(start_idx + batch_size, len(items_list))
            batch_items = dict(items_list[start_idx:end_idx])
            
            print(f"\n🔄 处理第 {batch_idx + 1}/{total_batches} 批（{len(batch_items)} 个项目）...")
            
            # 调用单批次总结方法
            batch_summaries = self._batch_summarize_single_batch(
                batch_items, item_type, max_length
            )
            
            # 合并结果
            summaries.update(batch_summaries)
        
        print(f"\n✅ 批量总结完成，共 {len(summaries)} 个结果")
        return summaries
    
    def _batch_summarize_single_batch(self, items_to_summarize: Dict[str, str], 
                                     item_type: str, max_length: int) -> Dict[str, str]:
        """处理单个批次的总结。
        
        Args:
            items_to_summarize: 当前批次要总结的文本字典
            item_type: 内容类型
            max_length: 每个总结的最大字符数
            
        Returns:
            当前批次的总结结果
        """
        summaries = {}
        
        # 构造批量总结的 prompt
        system_prompt = f"""你是一个专业的技术文档总结专家。我会提供多个{item_type}，请对每个内容进行精炼总结。

**总结要求：**
1. 提取核心技术要点和关键信息
2. 保留重要的技术细节（如版本号、组件名称、具体影响等）
3. 使用简洁专业的中文表达
4. 每个总结长度控制在 {max_length} 字符以内
5. 如果包含问题描述、解决方案或影响范围，请重点突出
6. 保持原文的技术术语不翻译

请按照 JSON 格式输出，格式如下：
```json
{{
  "ID1": "总结内容1",
  "ID2": "总结内容2"
}}
```"""

        # 构造批量输入
        batch_input = []
        for key, text in items_to_summarize.items():
            # 限制每个文本长度
            truncated_text = text[:1500] if len(text) > 1500 else text
            batch_input.append(f"【{key}】\n{truncated_text}\n")
        
        user_content = "\n".join(batch_input)
        
        print(f"📝 构造的输入内容长度: {len(user_content)} 字符")
        print(f"📝 预期的 max_tokens: {len(items_to_summarize) * int(max_length * 1.5)}")
        
        payload = {
            "model": self.config.model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_content
                }
            ],
            "max_tokens": len(items_to_summarize) * int(max_length * 1.5),
            "temperature": 0.3
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.token[:20]}..." if self.config.token else "None"
        }
        
        print(f"🌐 调用 LLM API: {self.config.api_url}")
        print(f"📋 模型: {self.config.model}")
        
        try:
            response = requests.post(
                self.config.api_url,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.config.token}"
                },
                json=payload,
                timeout=300  # 5分钟超时（批量总结需要更长时间）
            )
            
            print(f"📡 API 响应状态码: {response.status_code}")
            
            response.raise_for_status()
            
            result = response.json()
            print(f"📦 API 返回数据键: {list(result.keys())}")
            
            if 'choices' in result and len(result['choices']) > 0:
                response_text = result['choices'][0]['message']['content']
                print(f"✅ LLM 返回内容长度: {len(response_text)} 字符")
                print(f"📄 LLM 返回内容预览 (前200字符):\n{response_text[:200]}")
                
                # 尝试解析 JSON 响应
                try:
                    json_start = response_text.find('{')
                    json_end = response_text.rfind('}') + 1
                    
                    print(f"🔍 JSON 位置: start={json_start}, end={json_end}")
                    
                    if json_start >= 0 and json_end > json_start:
                        json_str = response_text[json_start:json_end]
                        print(f"📋 提取的 JSON 长度: {len(json_str)} 字符")
                        print(f"📋 提取的 JSON 预览 (前300字符):\n{json_str[:300]}")
                        
                        # 清理格式：修复 LLM 返回的不规范 JSON
                        # 1. 将 "\n\n  " 模式替换为 ", " (键值对之间缺少逗号的情况)
                        json_str_cleaned = re.sub(r'"\s*\n\s+\n\s+"', '",\n  "', json_str)
                        # 2. 将多余的空行压缩
                        json_str_cleaned = re.sub(r'\n\s*\n', '\n', json_str_cleaned)
                        
                        if json_str_cleaned != json_str:
                            print(f"🔧 JSON 格式已清理")
                        
                        batch_summaries = json.loads(json_str_cleaned)
                        print(f"✅ JSON 解析成功，得到 {len(batch_summaries)} 个总结")
                        print(f"📋 总结的键: {list(batch_summaries.keys())}")
                        
                        # 合并结果，确保长度限制
                        for key, summary in batch_summaries.items():
                            if key in items_to_summarize:
                                if len(summary) > max_length:
                                    summaries[key] = summary[:max_length-3] + "..."
                                    print(f"✂️  {key}: 总结被截断 ({len(summary)} -> {max_length})")
                                else:
                                    summaries[key] = summary
                                    print(f"✅ {key}: 总结成功 (长度: {len(summary)})")
                            else:
                                print(f"⚠️  {key}: 不在待总结列表中，跳过")
                    else:
                        print(f"❌ 未找到有效的 JSON 结构 (start={json_start}, end={json_end})")
                        print(f"📄 完整返回内容:\n{response_text}")
                        
                except json.JSONDecodeError as e:
                    print(f"❌ JSON 解析失败: {e}")
                    print(f"📄 尝试解析的内容:\n{json_str if 'json_str' in locals() else response_text}")
                    # Fallback: 对失败的项使用简单截断
                    for key, text in items_to_summarize.items():
                        if key not in summaries:
                            summaries[key] = text[:max_length-3] + "..."
                            print(f"⚠️  {key}: 使用 fallback 截断")
            else:
                print(f"❌ API 返回格式异常: {result}")
            
            # 对任何未成功总结的项使用简单截断
            for key in items_to_summarize:
                if key not in summaries:
                    summaries[key] = items_to_summarize[key][:max_length-3] + "..."
                    print(f"⚠️  {key}: 未找到总结结果，使用 fallback 截断")
                    
        except requests.RequestException as e:
            print(f"❌ API 请求失败: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"❌ 响应状态码: {e.response.status_code}")
                print(f"❌ 响应内容: {e.response.text[:500]}")
            # Fallback: 对所有项使用简单截断
            for key, text in items_to_summarize.items():
                summaries[key] = text[:max_length-3] + "..."
                print(f"⚠️  {key}: API 失败，使用 fallback 截断")
        
        print(f"\n✅ 批量总结完成，共 {len(summaries)} 个结果")
        return summaries
    
    def _parse_llm_response(self, response: str) -> LLMAnalysisResult:
        """Parse LLM response into structured result."""
        def ensure_string(value, default=""):
            """Ensure value is a string."""
            if isinstance(value, str):
                return value
            elif isinstance(value, (dict, list)):
                return str(value)
            else:
                return default

        def ensure_list(value, default=None):
            """Ensure value is a list of strings."""
            if default is None:
                default = []
            if isinstance(value, list):
                return [ensure_string(item) for item in value]
            elif isinstance(value, str):
                return [value]
            else:
                return default

        try:
            # Try to extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1

            if json_start >= 0 and json_end > json_start:
                json_str = response[json_start:json_end]
                data = json.loads(json_str)

                return LLMAnalysisResult(
                    summary=ensure_string(data.get('summary', '')),
                    key_changes=ensure_list(data.get('key_changes', [])),
                    important_bugfixes=ensure_list(data.get('important_bugfixes', [])),
                    security_issues=ensure_list(data.get('security_issues', [])),
                    performance_improvements=ensure_list(data.get('performance_improvements', [])),
                    breaking_changes=ensure_list(data.get('breaking_changes', [])),
                    recommendations=ensure_list(data.get('recommendations', [])),
                    risk_assessment=ensure_string(data.get('risk_assessment', ''))
                )
            else:
                # Fallback: treat entire response as summary
                return LLMAnalysisResult(
                    summary=response,
                    key_changes=[],
                    important_bugfixes=[],
                    security_issues=[],
                    performance_improvements=[],
                    breaking_changes=[],
                    recommendations=[],
                    risk_assessment=""
                )

        except json.JSONDecodeError:
            # Fallback: treat entire response as summary
            return LLMAnalysisResult(
                summary=response,
                key_changes=[],
                important_bugfixes=[],
                security_issues=[],
                performance_improvements=[],
                breaking_changes=[],
                recommendations=[],
                risk_assessment=""
            )

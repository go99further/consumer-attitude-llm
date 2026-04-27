"""
变量提取模块
功能：通过大模型API提取消费者信念、评价、强度和行为意向，计算态度指数(ATT)
输入：cleaned_reviews.csv
输出：final_analysis_data.csv（包含：review_id, ATT, BI, rating）
"""

import json
import time
import pandas as pd
import os
import sys
from typing import List, Dict, Optional
import re

# Windows 终端常见为 GBK，遇到 ✓/✗ 等字符会报 UnicodeEncodeError；
# 这里尽量强制 stdout/stderr 使用 UTF-8，避免全量跑到一半因为打印崩掉。
try:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

# ====================== 调试日志工具（Debug Mode） ======================
# 所有调试日志统一写入：e:\bi_ye_she_ji\.cursor\debug.log （NDJSON）
DEBUG_LOG_PATH = r"e:\bi_ye_she_ji\.cursor\debug.log"
DEBUG_SESSION_ID = "debug-session"


def _agent_debug_log(run_id: str, hypothesis_id: str, location: str, message: str, data: Dict):
    """
    向 Debug 日志文件追加一行 NDJSON（调试模式专用，避免影响正常逻辑）
    """
    payload = {
        "sessionId": DEBUG_SESSION_ID,
        "runId": run_id,
        "hypothesisId": hypothesis_id,
        "location": location,
        "message": message,
        "data": data or {},
        "timestamp": int(time.time() * 1000),
    }
    # region agent log
    try:
        # 确保日志目录存在
        log_dir = os.path.dirname(DEBUG_LOG_PATH)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)
        with open(DEBUG_LOG_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    except Exception:
        # 调试日志失败不能影响主流程
        pass
    # endregion


# 导入商品元数据加载模块
try:
    from load_product_metadata import load_product_metadata, format_metadata_for_prompt
except ImportError:
    # 如果模块不存在，定义空函数
    def load_product_metadata(*args, **kwargs):
        return {}
    def format_metadata_for_prompt(*args, **kwargs):
        return ""

# 导入配置
try:
    from config import (
        BASE_URL,
        API_KEY,
        MODEL,
        API_PROVIDER,
        API_TIMEOUT,
        API_MAX_RETRIES,
        API_DELAY,
    )
except ImportError:
    # 兼容旧配置
    try:
        from config import (
            OPENAI_API_KEY,
            OPENAI_BASE_URL,
            OPENAI_MODEL,
            DEEPSEEK_API_KEY,
            DEEPSEEK_BASE_URL,
            DEEPSEEK_MODEL,
            API_PROVIDER,
            API_TIMEOUT,
            API_MAX_RETRIES,
            API_DELAY,
        )
        # 使用旧配置
        if API_PROVIDER.lower() == "openai":
            BASE_URL = OPENAI_BASE_URL if OPENAI_BASE_URL != "https://api.openai.com/v1" else None
            API_KEY = OPENAI_API_KEY
            MODEL = OPENAI_MODEL
        elif API_PROVIDER.lower() == "deepseek":
            BASE_URL = DEEPSEEK_BASE_URL
            API_KEY = DEEPSEEK_API_KEY
            MODEL = DEEPSEEK_MODEL
        else:
            raise ValueError(f"不支持的API提供商: {API_PROVIDER}")
    except:
        print("错误：无法导入config.py，请确保配置文件存在且配置正确。")
        sys.exit(1)

# 初始化OpenAI客户端（支持便携AI聚合API）
try:
    from openai import OpenAI
    # 便携AI聚合API使用OpenAI兼容接口
    if API_PROVIDER.lower() == "bianxie":
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    elif API_PROVIDER.lower() == "openai":
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL if BASE_URL else None)
    elif API_PROVIDER.lower() == "deepseek":
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
    else:
        print(f"错误：不支持的API提供商: {API_PROVIDER}")
        sys.exit(1)
except ImportError:
    print("错误：请安装openai库：pip install openai")
    sys.exit(1)


def call_api(prompt: str, max_retries: int = API_MAX_RETRIES) -> str:
    """
    调用大模型API的通用函数
    
    参数:
        prompt: 提示词
        max_retries: 最大重试次数
    
    返回:
        API返回的文本内容
    """
    run_id = "pre-fix"
    for attempt in range(max_retries):
        try:
            _agent_debug_log(
                run_id=run_id,
                hypothesis_id="H1",
                location="variable_extraction.call_api",
                message="before_api_call",
                data={
                    "attempt": attempt + 1,
                    "max_retries": max_retries,
                    "prompt_len": len(prompt),
                },
            )
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": "你是一位专业的消费者心理分析专家，擅长从文本中提取结构化信息。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # 降低随机性，提高一致性
                timeout=API_TIMEOUT
            )
            _agent_debug_log(
                run_id=run_id,
                hypothesis_id="H1",
                location="variable_extraction.call_api",
                message="after_api_call_success",
                data={"attempt": attempt + 1},
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            _agent_debug_log(
                run_id=run_id,
                hypothesis_id="H1",
                location="variable_extraction.call_api",
                message="api_call_exception",
                data={"attempt": attempt + 1, "error": str(e)},
            )
            if attempt < max_retries - 1:
                wait_time = (attempt + 1) * 2  # 指数退避
                print(f"API调用失败（尝试 {attempt + 1}/{max_retries}），{wait_time}秒后重试...")
                time.sleep(wait_time)
            else:
                print(f"API调用最终失败: {e}")
                raise
    return ""


def extract_beliefs_and_evaluation(full_text: str, product_metadata: str = "") -> List[Dict[str, any]]:
    """
    从评论文本中提取产品属性信念及其情感评价
    
    参数:
        full_text: 完整的评论文本
        product_metadata: 商品元数据文本（用于增强上下文，因为信念与产品属性相关）
    
    返回:
        信念列表，格式：[{"text": "信念文本", "e_i": 1/-1/0}, ...]
    """
    # English prompt for better extraction performance
    # Calculate review length for adaptive extraction
    review_length = len(full_text)
    
    theory_context = """
Theoretical Foundation: Based on Aspect-Based Sentiment Analysis (ABSA) theory and Fishbein's 
multi-attribute attitude theory, this extraction follows a flexible strategy:
- Priority: Extract specific attribute beliefs (e.g., "very moisturizing", "beautiful packaging")
- Fallback: When no clear attributes are expressed, extract overall evaluation beliefs and mark as "general_belief"
- This approach aligns with ABSA theory which acknowledges the value of overall evaluation in understanding user attitudes

Belief Extraction Criteria (Aridor et al., 2022; Su et al., 2023; ABSA theory):
- Primary: Extract beliefs about specific product attributes (e.g., texture, efficacy, packaging, price, brand)
- Secondary: If no clear attributes are expressed, extract overall evaluation beliefs (e.g., "product is good", "worth buying") and mark with "type": "general_belief"
- Beliefs should be specific and identifiable when possible
- Focus on key attributes that influence consumer decisions

Belief Evaluation (e_i) Scoring Criteria (Su et al., 2023 sentiment analysis framework):
- +1: Clearly positive evaluation (e.g., "very moisturizing", "excellent effect", "high quality")
- 0: Neutral or mixed evaluation (e.g., "okay", "average", "nothing special")
- -1: Clearly negative evaluation (e.g., "not moisturizing enough", "poor effect", "average quality")

Extraction Quantity Guidelines (based on text information theory and cognitive load theory):
- Short reviews (<50 characters): Extract 1 main belief
- Medium reviews (50-500 characters): Extract 1-3 key beliefs
- Long reviews (>500 characters): Extract 3-5 key beliefs

Note: According to Su et al. (2023), emotional tendencies in consumer reviews significantly influence 
decision-making, so accurate identification of emotional polarity for each belief is crucial.
"""
    
    metadata_section = f"""
Product Information (for understanding review context - beliefs are related to product attributes):
{product_metadata}
""" if product_metadata else ""
    
    # Determine extraction quantity based on review length
    if review_length < 50:
        num_beliefs = "1"
    elif review_length < 500:
        num_beliefs = "1-3"
    else:
        num_beliefs = "3-5"
    
    prompt = f"""You are a consumer psychology expert specializing in multi-attribute attitude theory.

{theory_context}

{metadata_section}

IMPORTANT CONSTRAINT: ONLY extract beliefs that are EXPLICITLY stated or clearly implied in the review text below. Do NOT infer, fabricate, or add beliefs that are not present in the original text. If the review is very short or vague, extract only what is clearly expressed.

Task: Extract user beliefs from the following review and score the emotional polarity (e_i) for each belief.

Extraction Strategy:
1. PRIORITY: Extract beliefs about specific product attributes (e.g., texture, efficacy, packaging, price, brand)
2. FALLBACK: If no clear attributes are expressed, extract overall evaluation beliefs and mark with "type": "general_belief"
3. Quantity: Extract approximately {num_beliefs} key belief(s) based on review length ({review_length} characters)
4. Score the emotional polarity for each belief:
   - +1: Clearly positive (e.g., "very moisturizing", "excellent effect", "high quality")
   - 0: Neutral or mixed (e.g., "okay", "average", "nothing special")
   - -1: Clearly negative (e.g., "not moisturizing enough", "poor effect", "average quality")

Output Format: Strictly follow this JSON format (do not add any other text):
{{"beliefs": [{{"text": "belief1", "e_i": 1, "type": "attribute"}}, {{"text": "belief2", "e_i": -1, "type": "general_belief"}}]}}
Note: Use "type": "attribute" for specific attribute beliefs, "type": "general_belief" for overall evaluation beliefs.

Review:
{full_text}

Output JSON only, no other text."""

    try:
        response = call_api(prompt)
        
        # 尝试提取JSON（可能包含markdown代码块）
        json_match = re.search(r'\{[^{}]*"beliefs"[^{}]*\[.*?\]\s*\}', response, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response
        
        # 解析JSON
        result = json.loads(json_str)
        beliefs = result.get("beliefs", [])
        
        # 验证格式（支持新的type字段）
        valid_beliefs = []
        for belief in beliefs:
            if isinstance(belief, dict) and "text" in belief and "e_i" in belief:
                e_i = belief["e_i"]
                # 确保e_i是-1, 0, 或1
                if e_i in [-1, 0, 1]:
                    belief_dict = {
                        "text": str(belief["text"]).strip(),
                        "e_i": int(e_i)
                    }
                    # 如果包含type字段，也保存
                    if "type" in belief:
                        belief_dict["type"] = belief["type"]
                    valid_beliefs.append(belief_dict)
        
        return valid_beliefs if valid_beliefs else []
    
    except json.JSONDecodeError as e:
        print(f"JSON解析失败: {response[:200]}...")
        return []
    except Exception as e:
        print(f"提取信念时出错: {e}")
        return []


def assess_belief_strength(belief_text: str, review_context: str = "", review_length: int = 0) -> Optional[float]:
    """
    评估信念陈述的确定性程度（信念强度 b_i）
    
    理论基础：基于Turney & Littman (2002)语义取向理论、Garcia et al. (2011)信息量研究、
    Simpson & Gurevych (2018)论证说服力研究和Araque et al. (2019)道德基础预测研究
    
    参数:
        belief_text: 信念文本
        review_context: 评论全文（用于上下文分析）
        review_length: 评论长度（用于考虑详细程度）
    
    返回:
        b_i: 0.4-1.0之间的浮点数
    """
    prompt = f"""Theoretical Foundation: According to Turney & Littman (2002) semantic orientation theory
and Garcia et al. (2011) information content research, belief strength assessment should consider:
1. Certainty words (e.g., "absolutely", "definitely") reflect speaker's degree of certainty
2. Emotional intensity words (e.g., "very", "extremely") directly affect belief expression strength
3. Contextual factors (emphasis, contrast, rhetorical devices) influence strength expression (Simpson & Gurevych, 2018)
4. Review length and detail level reflect cognitive effort, with detailed reviews providing richer strength information (Araque et al., 2019)

Assessment Criteria (comprehensive framework):
- 1.0: Absolutely certain
  Indicators: Certainty words ("absolutely", "definitely", "certainly", "undoubtedly") +
              Strong emotional intensity words ("extremely", "incredibly") +
              Emphasis or contrast in context
- 0.9: Very certain
  Indicators: Very strong emotional intensity words ("very", "extremely", "highly", "exceptionally") +
              Certainty words ("surely", "undoubtedly")
- 0.8: Quite certain
  Indicators: Moderate intensity words ("quite", "rather", "pretty", "fairly") +
              Positive certainty indicators
- 0.7: Possible/general
  Indicators: Uncertainty words ("possibly", "seems", "should", "probably", "likely") +
              Moderate expression
- 0.5: Uncertain
  Indicators: Uncertainty words ("maybe", "perhaps", "might", "could")
- 0.4: Heard/feel
  Indicators: Indirect expression ("heard", "feel", "seems like", "reportedly", "appears")

Calibration Examples (few-shot):
- "absolutely love it" → 1.0 (absolute certainty + strong positive intensity)
- "works really well for my skin" → 0.9 (strong certainty, specific claim)
- "pretty good moisturizer" → 0.8 (moderate intensity, fairly certain)
- "it's okay I guess" → 0.6 (uncertain, hedged)
- "seems decent" → 0.5 (uncertain, indirect)
- "I've heard it's good" → 0.4 (indirect, second-hand)

Contextual Factors to Consider (Simpson & Gurevych, 2018):
- Emphasis markers (e.g., "!", capitalization, repetition)
- Contrast markers (e.g., "but", "however", "compared to")
- Position in text (beginning/end may indicate stronger emphasis)
- Review detail level: Detailed reviews (>500 chars) may indicate higher cognitive effort and stronger beliefs

Task: Assess the certainty degree of the following belief statement, considering:
1. Certainty and emotional intensity words
2. Contextual factors (emphasis, contrast, position)
3. Review detail level (review length: {review_length} characters)

Belief Statement: {belief_text}
{f'Review Context: {review_context[:200]}...' if review_context else ''}

Return a number between 0.4 and 1.0 (one decimal place).
Important: If the belief statement does not contain sufficient information to assess strength,
or if the assessment is truly ambiguous, return "NA" or "missing" instead of a number.
Return only the number or "NA"/"missing", no other text."""

    try:
        response = call_api(prompt)
        response_lower = response.strip().lower()
        
        # 检查是否返回了"NA"或"missing"
        if response_lower in ["na", "missing", "n/a", "none", "null"]:
            print(f"    LLM判断无法评估信念强度: {response.strip()}")
            return None
        
        # 提取数字
        numbers = re.findall(r'\d+\.?\d*', response)
        if numbers:
            b_i = float(numbers[0])
            # 限制在0.4-1.0范围内
            b_i = max(0.4, min(1.0, b_i))
            return round(b_i, 1)
        else:
            # 无法提取数字且不是明确的"NA"标记，视为提取失败
            print(f"    警告：无法从LLM响应中提取信念强度数字: {response[:100]}...")
            return None
    except Exception as e:
        print(f"    评估信念强度时出错: {e}")
        return None  # 提取失败，返回缺失值


def extract_perceived_value(full_text: str) -> Optional[int]:
    """
    Extract Perceived Value (PV) from the review: 0–3 (overall value level).
    """

    prompt = f"""You are an expert in perceived value research in digital and e-commerce contexts.

Theoretical background:
- Perceived value (PV) is defined as the consumer's overall assessment of the utility of a product or service
  based on a trade-off between perceived benefits and perceived costs (Zeithaml, 1988).
- Recent work in entertainment platforms, live-streaming commerce, and virtual influencer marketing
  (e.g., Yum & Kim, 2024; Wu & Huang, 2023; Cao et al., 2025) conceptualizes PV as multidimensional,
  including utilitarian/functional value (performance, quality, usefulness, value for money),
  hedonic value (enjoyment, fun, excitement), and social value (status, social approval, image).
- For practical annotation and regression modeling with language models, we compress perceived value
  into a four-category overall scale from 0 to 3, representing no/low, weak, moderate, and strong perceived value.

Your task:
Read the following review and judge the reviewer’s overall perceived value (benefits relative to costs),
using the following 0–3 scale:

PV scale (0–3):
- 3: High perceived value.
  - Benefits clearly outweigh costs.
  - The review explicitly or implicitly indicates that the product is a very good deal or excellent value for money.
- 2: Moderate/acceptable perceived value.
  - Benefits and costs appear roughly balanced; value is acceptable or fair.
- 1: Low–moderate or ambiguous perceived value.
  - The reviewer is neutral or only slightly positive about value for money,
    or mentions both pros and cons without clearly endorsing value.
- 0: Low perceived value.
  - The review clearly indicates that the product is not worth the price or that costs outweigh benefits.

Consider comments about price, quality, performance, usefulness, enjoyment, and any explicit mention of value for money.

Review:
{full_text}

Output:
Return ONLY one integer: 0, 1, 2, or 3. 
Important: If the review does not contain sufficient information about perceived value 
(e.g., no mention of price, value for money, or cost-benefit trade-off), return "NA" or "missing".
Do not include any explanation."""

    try:
        response = call_api(prompt)
        response_lower = response.strip().lower()
        
        # 检查是否返回了"NA"或"missing"
        if response_lower in ["na", "missing", "n/a", "none", "null"]:
            print(f"    LLM判断评论中无感知价值相关信息")
            return None
        
        # 提取数字
        numbers = re.findall(r'\d+', response)
        if numbers:
            pv = int(numbers[0])
            pv = max(0, min(3, pv))
            return pv
        else:
            # 无法提取数字且不是明确的"NA"标记，视为提取失败
            print(f"    警告：无法从LLM响应中提取感知价值数字: {response[:100]}...")
            return None
    except Exception as e:
        print(f"    提取感知价值时出错: {e}")
        return None  # 提取失败，返回缺失值


def extract_behavioral_intention(full_text: str) -> Optional[int]:
    """
    提取用户的行为意向（Behavioral Intention, BI）
    
    理论基础：根据Morwitz (2012)的行为意向测量原则和Ajzen (1991)的计划行为理论，
    行为意向是预测实际行为的最直接前因变量。
    
    参数:
        full_text: 完整的评论文本
    
    返回:
        BI: 0-3之间的整数
        3 = 强烈意向（会回购/强烈推荐）
        2 = 中度意向（可能再买/考虑推荐）
        1 = 弱意向（仅说产品好，无明确行为指向）
        0 = 无意向（未提及或表达负面意向）
    """
    prompt = f"""Theoretical Foundation: Based on recent research (He et al., 2024; Aridor et al., 2022), 
Behavioral Intention refers to the consumer's tendency and plan to perform specific behaviors, 
and is a key mediating variable in how online reviews influence purchase decisions.

Measurement Criteria (He et al., 2024; Aridor et al., 2022; Su et al., 2023):
- 3: Strong intention (explicitly expresses future behavior)
  Example phrases: "will repurchase", "definitely buy again", "strongly recommend", "must recommend", 
  "will definitely buy", "will continue using"
  Characteristic: Contains explicit future behavior commitment
- 2: Moderate intention (may perform behavior)
  Example phrases: "might buy again", "will consider recommending", "should buy", "might try", 
  "will recommend to friends"
  Characteristic: Expresses possibility but not certain
- 1: Weak intention (only positive evaluation, no explicit behavior direction)
  Example phrases: "works well", "good", "satisfied", "like", but no mention of future behavior
  Characteristic: Only positive evaluation, no behavior commitment
- 0: No intention (not mentioned or expresses negative intention)
  Example phrases: "won't buy", "not recommend", "won't buy again", "won't repurchase", 
  or completely no behavior expression
  Characteristic: Explicit rejection or completely no behavior expression

Note: According to He et al. (2024), customer reviews significantly influence consumers' perceived 
value, which in turn affects purchase decisions. Behavioral intention is a key variable in this 
influence path.

Task: Determine the user's future behavioral intention expressed in the review. Return an integer (0, 1, 2, or 3).
Important: If the review does not contain any explicit or implicit expression of future behavioral intention 
(e.g., repurchase, recommendation, continued use), return "NA" or "missing" instead of a number.
Note: "0" should only be used when the review explicitly expresses negative intention (e.g., "won't buy again").

Review:
{full_text}

Return only the number (0, 1, 2, 3) or "NA"/"missing", no other text."""

    try:
        response = call_api(prompt)
        response_lower = response.strip().lower()
        
        # 检查是否返回了"NA"或"missing"
        if response_lower in ["na", "missing", "n/a", "none", "null"]:
            print(f"    LLM判断评论中无行为意向相关信息")
            return None
        
        # 提取数字
        numbers = re.findall(r'\d+', response)
        if numbers:
            bi = int(numbers[0])
            # 限制在0-3范围内
            bi = max(0, min(3, bi))
            return bi
        else:
            # 无法提取数字且不是明确的"NA"标记，视为提取失败
            print(f"    警告：无法从LLM响应中提取行为意向数字: {response[:100]}...")
            return None
    except Exception as e:
        print(f"    提取行为意向时出错: {e}")
        return None  # 提取失败，返回缺失值


def load_progress(temp_file: str) -> Dict:
    """加载临时进度文件"""
    if os.path.exists(temp_file):
        try:
            with open(temp_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}
    return {}


def save_progress(temp_file: str, progress: Dict):
    """保存临时进度文件"""
    with open(temp_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)


def main_extraction_pipeline(
    input_csv_path: str,
    output_csv_path: str,
    delay: float = API_DELAY,
    batch_size: int = 10,
    start_from: int = 0,
    metadata_file: str = None,
    product_id: str = "B004EDYQX6"
):
    """
    主流程函数：批量处理所有评论，计算ATT和BI
    
    参数:
        input_csv_path: 输入的CSV文件路径
        output_csv_path: 输出的CSV文件路径
        delay: API调用之间的延迟（秒）
        batch_size: 每处理多少条保存一次临时结果
        start_from: 从第几条开始处理（用于断点续传）
        metadata_file: 商品元数据文件路径（可选）
        product_id: 商品ID（用于加载元数据）
    """
    run_id = "pre-fix"
    _agent_debug_log(
        run_id=run_id,
        hypothesis_id="H2",
        location="variable_extraction.main_extraction_pipeline",
        message="pipeline_start",
        data={
            "input_csv_path": input_csv_path,
            "output_csv_path": output_csv_path,
            "delay": delay,
            "batch_size": batch_size,
            "start_from": start_from,
            "metadata_file": metadata_file,
            "product_id": product_id,
        },
    )
    print("="*60)
    print("开始变量提取流程")
    print("="*60)
    
    # 检查API密钥
    if API_KEY == "your-openai-api-key-here" or API_KEY == "your-deepseek-api-key-here" or API_KEY == "sk-your-api-key-here":
        print("错误：请在 config.py 中配置你的API密钥！")
        return
    
    # 加载商品元数据（如果提供）
    product_metadata_text = ""
    if metadata_file and os.path.exists(metadata_file):
        print(f"\n加载商品元数据: {metadata_file}")
        metadata = load_product_metadata(metadata_file, product_id)
        if metadata:
            product_metadata_text = format_metadata_for_prompt(metadata)
            print("✓ 商品元数据加载成功")
        else:
            print("⚠ 未找到商品元数据，将不使用元数据增强提示词")
    else:
        print("\n⚠ 未提供商品元数据文件，将不使用元数据增强提示词")
    
    # 读取数据
    print(f"\n读取数据文件: {input_csv_path}")
    if not os.path.exists(input_csv_path):
        print(f"错误：找不到输入文件: {input_csv_path}")
        return
    
    df = pd.read_csv(input_csv_path, encoding='utf-8-sig')
    total_rows = len(df)
    print(f"共 {total_rows} 条评论需要处理")
    _agent_debug_log(
        run_id=run_id,
        hypothesis_id="H2",
        location="variable_extraction.main_extraction_pipeline",
        message="data_loaded",
        data={"total_rows": total_rows},
    )
    
    # 检查断点续传
    temp_file = output_csv_path.replace('.csv', '_temp.json')
    progress = load_progress(temp_file)
    processed_ids = set(progress.get('processed_ids', []))
    
    if processed_ids:
        print(f"\n检测到未完成的进度，已处理 {len(processed_ids)} 条评论")
        # 非交互式默认继续，避免在自动化/后台跑时卡住
        resume_env = os.environ.get("AUTO_RESUME", "y").strip().lower()
        if resume_env not in ("y", "yes", "1", "true"):
            print("AUTO_RESUME != y，已选择从头开始（清空历史进度）")
            processed_ids = set()
            progress = {}
        else:
            print("AUTO_RESUME=y，继续上次进度")
    
    # 准备结果列表
    results = progress.get('results', [])
    
    # 处理每条评论
    print(f"\n开始处理（从第 {start_from + 1} 条开始）...")
    print(f"API延迟设置: {delay} 秒/次")
    print(f"每 {batch_size} 条保存一次临时结果\n")
    
    for idx, row in df.iterrows():
        if idx < start_from:
            continue
        
        review_id = row['review_id']
        full_text = row['full_text']
        rating = row['rating']
        
        # 跳过已处理的
        if review_id in processed_ids:
            continue
        
        print(f"[{idx + 1}/{total_rows}] 处理 {review_id}...")
        _agent_debug_log(
            run_id=run_id,
            hypothesis_id="H3",
            location="variable_extraction.main_extraction_pipeline",
            message="before_review_process",
            data={
                "idx": idx,
                "review_id": str(review_id),
                "total_rows": total_rows,
            },
        )
        
        try:
            # 1. 提取信念与评价（传入商品元数据）
            print("  → 提取信念与评价...")
            beliefs = extract_beliefs_and_evaluation(full_text, product_metadata_text)
            time.sleep(delay)
            _agent_debug_log(
                run_id=run_id,
                hypothesis_id="H3",
                location="variable_extraction.main_extraction_pipeline",
                message="after_belief_extraction",
                data={
                    "idx": idx,
                    "review_id": str(review_id),
                    "belief_count": len(beliefs) if isinstance(beliefs, list) else -1,
                },
            )
            
            if not beliefs:
                print(f"  警告：未提取到信念，ATT标记为缺失")
                # 如果没有提取到信念，ATT应该为缺失值（NaN），而不是0.0
                # 因为"没有态度表达"和"态度中性"是不同的概念
                # 仍然提取BI和PV（它们可能有值）
                bi = extract_behavioral_intention(full_text)
                time.sleep(delay)
                pv = extract_perceived_value(full_text)
                time.sleep(delay)
                results.append({
                    'review_id': review_id,
                    'ATT': None,  # 缺失值
                    'BI': bi,  # 可能是None
                    'PV': pv,  # 可能是None
                    'rating': rating,
                    'beliefs': json.dumps([], ensure_ascii=False)
                })
                processed_ids.add(review_id)
                continue
            print(f"  提取到 {len(beliefs)} 条信念")
            
            # 2. 计算ATT = Σ(b_i × e_i)，同时保存信念详细信息
            total_att = 0.0
            beliefs_detail = []  # 保存每个信念的详细信息
            
            for belief in beliefs:
                belief_text = belief['text']
                e_i = belief['e_i']
                
                # 评估信念强度（传入评论上下文和长度）
                print(f"    → 评估信念强度: {belief_text[:50]}...")
                b_i = assess_belief_strength(belief_text, full_text, len(full_text))
                time.sleep(delay)
                
                # 如果b_i为缺失值，跳过该信念（无法计算态度分量）
                if b_i is None:
                    print(f"      警告：信念强度无法评估，跳过该信念")
                    # 仍然保存信念信息，但标记b_i和att_component为None
                    beliefs_detail.append({
                        'belief_text': belief_text,
                        'b_i': None,
                        'e_i': e_i,
                        'att_component': None,
                        'type': belief.get('type', 'unknown')
                    })
                    continue
                
                # 计算态度分量
                att_comp = b_i * e_i
                total_att += att_comp
                print(f"      b_i={b_i}, e_i={e_i}, att_comp={att_comp:.2f}")
                
                # 保存信念详细信息
                beliefs_detail.append({
                    'belief_text': belief_text,
                    'b_i': b_i,
                    'e_i': e_i,
                    'att_component': att_comp,
                    'type': belief.get('type', 'unknown')  # 如果存在type字段
                })
                
                _agent_debug_log(
                    run_id=run_id,
                    hypothesis_id="H4",
                    location="variable_extraction.main_extraction_pipeline",
                    message="belief_strength_evaluated",
                    data={
                        "idx": idx,
                        "review_id": str(review_id),
                        "belief_text": belief_text,  # 保存信念文本内容
                        "b_i": b_i,
                        "e_i": e_i,
                        "att_comp": att_comp,
                    },
                )
            
            # 3. 计算ATT的最终值（先计算，后续才能用于debug_log）
            # 检查是否有有效信念（至少有一个b_i不是None）
            valid_beliefs_count = sum(1 for bd in beliefs_detail if bd.get('b_i') is not None)
            # 如果所有信念的b_i都是None，ATT应该标记为缺失
            att_final = round(total_att, 2) if valid_beliefs_count > 0 else None
            att_debug_value = att_final  # 用于debug_log
            
            # 4. 提取感知价值与行为意向
            print("  → 提取感知价值（PV）...")
            pv = extract_perceived_value(full_text)
            time.sleep(delay)

            print("  → 提取行为意向（BI）...")
            bi = extract_behavioral_intention(full_text)
            time.sleep(delay)

            _agent_debug_log(
                run_id=run_id,
                hypothesis_id="H5",
                location="variable_extraction.main_extraction_pipeline",
                message="after_behavior_intention",
                data={
                    "idx": idx,
                    "review_id": str(review_id),
                    "ATT": att_debug_value,
                    "BI": bi,
                    "PV": pv,
                },
            )
            
            # 保存结果（包含信念详细信息，保存为JSON字符串）
            results.append({
                'review_id': review_id,
                'ATT': att_final,  # 如果所有信念都无法评估，ATT为None
                'BI': bi,
                'PV': pv,
                'rating': rating,
                'beliefs': json.dumps(beliefs_detail, ensure_ascii=False)  # 保存信念详细信息为JSON
            })
            
            # 格式化输出（处理缺失值）
            att_str = f"{total_att:.2f}" if att_final is not None else "NaN"
            bi_str = str(bi) if bi is not None else "NaN"
            pv_str = str(pv) if pv is not None else "NaN"
            print(f"  ✓ 完成: ATT={att_str}, BI={bi_str}, PV={pv_str}")
            
            processed_ids.add(review_id)
            
            # 每batch_size条保存一次临时结果
            if (idx + 1) % batch_size == 0:
                progress = {
                    'processed_ids': list(processed_ids),
                    'results': results,
                    'last_index': idx
                }
                save_progress(temp_file, progress)
                print(f"\n  [进度保存] 已处理 {len(processed_ids)}/{total_rows} 条评论\n")
        
        except Exception as e:
            print(f"  ✗ 处理失败: {e}")
            print(f"  跳过该评论，继续处理下一条...\n")
            continue
    
    # 保存最终结果
    print("\n" + "="*60)
    print("处理完成，保存最终结果...")
    print("="*60)
    
    if not results:
        print("错误：没有处理任何评论！")
        return
    
    # 转换为DataFrame并保存
    result_df = pd.DataFrame(results)
    # 确保包含所有列：review_id, ATT, BI, PV, rating, beliefs
    required_columns = ['review_id', 'ATT', 'BI', 'PV', 'rating', 'beliefs']
    # 只选择存在的列
    available_columns = [col for col in required_columns if col in result_df.columns]
    result_df = result_df[available_columns]
    
    output_dir = os.path.dirname(output_csv_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 保存CSV（pandas会自动将None转换为空值或"nan"字符串）
    result_df.to_csv(output_csv_path, index=False, encoding='utf-8-sig', na_rep='')
    print(f"\n结果已保存到: {output_csv_path}")
    print(f"共处理 {len(results)} 条评论")
    
    # 统计缺失值
    print(f"\n缺失值统计:")
    numeric_cols = ['ATT', 'BI', 'PV', 'rating']
    for col in numeric_cols:
        if col in result_df.columns:
            missing_count = result_df[col].isna().sum()
            total_count = len(result_df)
            print(f"  {col}: {missing_count}/{total_count} ({missing_count/total_count*100:.1f}%)")
    
    print(f"\n数据预览（前10条）:")
    print(result_df.head(10).to_string())
    
    print(f"\n描述性统计（仅完整数据）:")
    # 只显示数值列的描述性统计（自动排除缺失值）
    numeric_df = result_df[numeric_cols] if all(col in result_df.columns for col in numeric_cols) else result_df.select_dtypes(include=[float, int])
    print(numeric_df.describe())
    
    # 删除临时文件
    if os.path.exists(temp_file):
        os.remove(temp_file)
        print(f"\n临时文件已删除: {temp_file}")


def main():
    """主函数 - 提取所有评论（已验证购买和未验证购买）"""
    # 文件路径配置
    # 处理所有评论（包括已验证购买和未验证购买）
    input_file = "../data/cleaned_reviews.csv"
    output_file = "../data/final_analysis_data_complete.csv"
    metadata_file = "../meta_Beauty_and_Personal_Care.jsonl"
    product_id = "B004EDYQX6"  # 伯特小蜜蜂护手霜套装
    
    # 如果文件不在上级目录，尝试当前目录
    if not os.path.exists(input_file):
        input_file = "data/cleaned_reviews.csv"
        output_file = "data/final_analysis_data_complete.csv"
        metadata_file = "meta_Beauty_and_Personal_Care.jsonl"
    
    if not os.path.exists(input_file):
        print(f"错误：找不到输入文件: {input_file}")
        print("请确保 data/cleaned_reviews.csv 文件存在")
        return
    
    # 检查文件中的评论数量
    try:
        df_check = pd.read_csv(input_file, encoding='utf-8-sig')
        total_reviews = len(df_check)
        print(f"\n输入文件包含 {total_reviews} 条评论")
        
        # 检查是否有verified_purchase列
        if 'verified_purchase' in df_check.columns:
            verified_count = df_check['verified_purchase'].sum() if df_check['verified_purchase'].dtype == bool else df_check['verified_purchase'].value_counts().get(True, 0)
            unverified_count = total_reviews - verified_count
            print(f"  - 已验证购买: {verified_count} 条")
            print(f"  - 未验证购买: {unverified_count} 条")
    except Exception as e:
        print(f"警告：无法读取输入文件统计信息: {e}")
    
    print("\n" + "="*60)
    print("开始提取所有评论的潜变量（ATT、BI、PV、信念数据）")
    print("="*60)
    print("注意：这将提取所有评论，包括已验证购买和未验证购买")
    print("="*60)
    
    # 运行主流程
    main_extraction_pipeline(
        input_csv_path=input_file,
        output_csv_path=output_file,
        delay=API_DELAY,
        batch_size=10,
        start_from=0,
        metadata_file=metadata_file,
        product_id=product_id
    )
    
    print("\n" + "="*60)
    print("所有评论的变量提取完成！")
    print("="*60)
    print(f"结果已保存到: {output_file}")
    print("\n提取的变量包括：")
    print("  - ATT（态度指数）：从信念计算得出")
    print("  - BI（行为意向）：0-3整数")
    print("  - PV（感知价值）：0-3整数")
    print("  - beliefs（信念详细信息）：JSON格式")
    print("  - rating（评分）：原始评分")


if __name__ == "__main__":
    main()


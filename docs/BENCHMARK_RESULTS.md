# FinVault AI: Empirical Benchmark Report

**Dataset:** FinanceBench SEC Regulatory Filings (84 Documents, 32 Companies, 150 Questions)  
**Splits:** 75 Dev Questions, 75 Held-Out Test Questions (Seed 42)  
**Frozen Configuration Hash:** `357e5de5955c06edec0c892289a2acdb3fefdebaa916ef8e302af52e82d03ebb`  
**Embedding Engine:** `BAAI/bge-small-en-v1.5` (FastEmbed ONNX Runtime, 384 dimensions)  
**Primary Generator & Judge:** DeepSeek `deepseek-flash` (`"thinking": {"type": "disabled"}`, temp=0.0)  

---

## 1. Executive Summary

This report aggregates all empirical benchmarks collected across the FinVault AI system:
1. **Embedding Engine Ablation:** FastEmbed ONNX Runtime vs. PyTorch SentenceTransformers.
2. **Retrieval Ablation (Dev & Held-Out Test):** Vanilla Vector Search (Config A), Company-Filtered (Config B), Inferred Metadata with Missing-Year Fallback (Config C), and Oracle.
3. **Prompt Iteration Ablation (Dev Split):** Frozen Prompt `v0` vs. Numerical Ordering Candidate `v1`.
4. **Answer-Level Evaluation (Held-Out Test Split):** Accuracy, Hallucination/Error Rate, Faithful Abstention, and Page Hit conditional breakdown with 95% Wilson score confidence intervals.

---

## 2. Embedding Engine Performance Ablation

Tested on Apple Silicon hardware running Python 3.11 with identical model weights (`BAAI/bge-small-en-v1.5`, 384 dimensions):

| Metric | SentenceTransformers (PyTorch 2.x) | FastEmbed (ONNX Runtime) | Measured Improvement |
| :--- | :--- | :--- | :--- |
| **Virtualenv Disk Footprint** | 1,200 MB | 239 MB | **-80.1%** |
| **Peak Resident Set Size (RSS)** | 540.73 MB | 216.70 MB | **-59.9%** |
| **Cold-Start 1st Query Latency** | 3,630 ms | 60 ms | **-98.3%** |
| **100-Query Inference Latency** | 0.5513s (5.51 ms/query) | 0.3155s (3.16 ms/query) | **-42.8%** |
| **Cosine Similarity to Reference Embeddings (N=100)** | 1.000000 | Min: 0.999998, Mean: 0.999999 | **99.9999% identical** |

---

## 3. Retrieval Ablation: Held-Out Test Split (n = 75)

Evaluated against ground truth SEC filing pages and token recall excerpts from FinanceBench:

| Retrieval Configuration | Page Hit@10 | Page Hit Rate (%) | 95% Wilson Score CI | Token Hit@10 ($\ge 0.8$) | Token Hit Rate (%) | 95% Wilson Score CI |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Config A (Vanilla Baseline)** | 28 / 75 | 37.3% | [27.3%, 48.6%] | 17 / 75 | 22.7% | [14.7%, 33.3%] |
| **Config C (Inferred Metadata Pipeline)** | **42 / 75** | **56.0%** | **[44.7%, 66.8%]** | **24 / 75** | **32.0%** | **[22.5%, 43.2%]** |
| **Oracle (Ground-Truth Company + Year)** | 43 / 75 | 57.3% | [46.0%, 68.0%] | 25 / 75 | 33.3% | [23.7%, 44.6%] |

### Key Findings
- **Metadata Power:** Applying inferred company and year filtering lifts Page Hit@10 from 37.3% to 56.0% (+18.7 percentage points).
- **Oracle Parity:** Config C captures 42 out of 43 Oracle hits (97.7% Oracle recovery), proving the alias and comparative filing fallback engine introduces negligible drop-off compared to perfect knowledge.

---

## 4. Dev Split Prompt Iteration: `v0` vs. `v1`

During prompt development on the 75-question dev split, an extra instruction was tested in `v1`:
> *"When comparing numerical quantities, verify the exact numbers and their relative magnitudes before stating which is greater or smaller."*

| Metric | Dev `v0` (Frozen) | Dev `v1` (Candidate) | Empirical Impact |
| :--- | :--- | :--- | :--- |
| **Overall Correct** | 30 / 75 (40.0%) [29.7%, 51.3%] | 30 / 75 (40.0%) [29.7%, 51.3%] | Unchanged |
| **Overall Wrong (Errors)** | **6 / 75 (8.0%)** [3.7%, 16.4%] | 11 / 75 (14.7%) [8.4%, 24.4%] | **+5 false answers** |
| **Overall Abstained** | **39 / 75 (52.0%)** [40.9%, 62.9%] | 34 / 75 (45.3%) [34.6%, 56.6%] | -5 abstentions |
| **Accuracy Among Attempted** | **30 / 36 (83.3%)** [68.1%, 92.1%] | 30 / 41 (73.2%) [58.1%, 84.3%] | **-10.1% accuracy** |
| **Page Miss Faithful Abstention** | **26 / 30 (86.7%)** [70.3%, 94.7%] | 24 / 30 (80.0%) [62.7%, 90.5%] | -6.7% discipline |

**Conclusion:** `v1` induced prompt drift by encouraging the model to attempt questions where context was incomplete. `v0` was frozen for superior precision (83.3% accuracy among attempted).

---

## 5. Held-Out Test Split: Full Answer-Level Evaluation (n = 75)

Evaluated under frozen configuration `357e5de5955c` on commit `67bac6f`.

### Comprehensive Metrics Table

| Evaluation Segment | Metric | k / n | Rate (%) | 95% Wilson Score Confidence Interval |
| :--- | :--- | :--- | :--- | :--- |
| **Overall Pipeline** | Correct Answers | 30 / 75 | **40.0%** | [29.7%, 51.3%] |
| | Wrong Answers (Errors) | 9 / 75 | **12.0%** | [6.4%, 21.3%] |
| | Explicit Abstentions | 36 / 75 | **48.0%** | [37.1%, 59.1%] |
| | **Accuracy Among Attempted** | **30 / 39** | **76.9%** | **[61.7%, 87.4%]** |
| **Retrieval Diagnostics** | Page Hit@10 | 41 / 75 | 54.7% | [43.4%, 65.4%] |
| | Token Recall Hit@10 ($\ge 0.8$) | 24 / 75 | 32.0% | [22.5%, 43.2%] |
| **Conditional on Page Hit** ($n = 41$) | Correct Answers | 26 / 41 | **63.4%** | [48.1%, 76.4%] |
| | Wrong Answers | 6 / 41 | 14.6% | [6.9%, 28.4%] |
| | Abstained | 9 / 41 | 22.0% | [12.0%, 36.7%] |
| **Conditional on Page Miss** ($n = 34$) | Faithful Abstention Rate | 27 / 34 | **79.4%** | **[63.2%, 89.7%]** |
| | False Answers (Hallucination) | 3 / 34 | **8.8%** | [3.0%, 23.0%] |
| | Serendipitous Correct | 4 / 34 | 11.8% | [4.7%, 26.6%] |
| **By Evaluation Mechanism** | Pure Numeric Tolerance Match | 9 / 9 | **100.0%** | [70.1%, 100.0%] |
| | LLM Judge Rubric Match | 21 / 30 | **70.0%** | [52.1%, 83.3%] |

### Operational Performance
- **API Errors / Dropped Queries:** 0 (100% completion rate)
- **Total Tokens Consumed:** 188,401 tokens
- **Average Generation Latency:** 1,477 ms / query

---

## 6. Mathematical Formulas

### Wilson Score Interval Formula
For observed successes $k$ in sample size $n$, with point estimate $p = k/n$ and standard normal quantile $z = 1.95996$:

$$Center = \frac{p + \frac{z^2}{2n}}{1 + \frac{z^2}{n}}$$

$$Margin = \frac{z \sqrt{\frac{p(1-p)}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}}$$

$$CI_{95} = [ \max(0, Center - Margin), \min(1, Center + Margin) ]$$

### Relative Tolerance Match Formula
For gold value $V_{gold}$ and predicted candidate $V_{pred}$:

$$\Delta_{rel} = \frac{|V_{pred} - V_{gold}|}{\max(|V_{gold}|, 10^{-6})} \le 0.015 \quad (1.5\%)$$

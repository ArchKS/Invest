---
CreateTime: 2026-08-30 14:45:20
LastUpdate: 2026-08-30 14:45:20
---

# PD-1/VEGF 双特异性抗体药理机制与临床数据分析
## ——以依沃西单抗（Ivonescimab, AK112/SMT112）为核心

**报告日期：2026-08-29**

---

## 摘要（结论先行）

PD-1/VEGF 双特异性抗体代表了免疫检查点抑制剂的"二代范式"：将 PD-1 免疫激活与 VEGF 抗血管生成整合进单一分子。以康方生物/Summit 的依沃西单抗（AK112）为例，其核心差异化机制是 **VEGF 存在时 PD-1 结合亲和力提升约 18 倍的"协同结合"效应**，配合 Fc 沉默与较短半衰期设计，理论上实现肿瘤微环境（TME）富集和更优治疗窗。

临床验证已走到全球 III 期阶段：

- **首个 III 期头对头击败帕博利珠单抗（K药）**：HARMONi-2 中 PFS HR 0.51（[Lancet 2025](https://pubmed.ncbi.nlm.nih.gov/40057343/)）
- **已确证 OS 统计学显著获益的 III 期**：HARMONi-A（OS HR 0.74, p=0.019）、HARMONi-6（OS HR 0.66, p=0.0017）、HARMONi-GI1 胆道癌（topline 阳性）
- **全球 III 期 HARMONi**：PFS 显著（HR 0.52）但 OS 多次更新均未达统计学显著（HR 0.76–0.79），FDA 明确该适应症需 OS 显著；BLA 已受理，**PDUFA 日期 2026-11-14**（[Summit 公告](https://www.fiercepharma.com/pharma/summit-therapeutics-updates-ivonescimab-survival-data-ahead-fda-decision-date)）
- **NMPA 已批 3 项适应症**（2024-05、2025-04、2026-08），中国累计用药患者超 70,000 例
- **安全性**：VEGF 相关 ≥3 级不良事件率低（高血压约 5%、蛋白尿 3%、出血 1–2%），鳞癌出血风险可控，整体不劣于贝伐珠单抗历史数据

核心未决问题：① OS 获益幅度能否在 PD-L1 阳性单药人群（HARMONi-2 最终 OS）和西方人群中坐实统计学显著；② "TME 锚定富集"仍缺乏体内直接证据。

---

## 一、分子设计与药理机制

### 1.1 分子结构：对称四价 IgG-scFv（2+2）双抗

依沃西单抗为人源化对称型双特异性抗体，基于康方生物自有 **Tetrabody 四价双抗平台**构建：

- **主体结构**：以抗 VEGF-A 的全长 IgG1 抗体为主体（两个 Fab 结合 VEGF-A），在其**重链 C 端通过柔性 (Gly₄Ser) 连接肽融合抗 PD-1 的 scFv**
- **价态**：2 个抗 VEGF 结合位点 + 2 个抗 PD-1 结合位点，即"2+2"四价；分子量约 201 kDa
- **Fc 段工程化**：引入 L234A/L235A（LALA）突变沉默 Fc 功能——检测不到与 FcγR 及 C1q 的结合，体外无 ADCC、ADCP、CDC 及细胞因子释放

来源：Zhong T et al., *iScience* 2025（[PMC 全文](https://pmc.ncbi.nlm.nih.gov/articles/PMC11872405/)）；JITC SITC 2023 摘要 1194（[JITC](https://jitc.bmj.com/content/11/Suppl_1/A1316)）

**设计逻辑**：

| 设计要素 | 目的 |
|---|---|
| 四价对称结构 | VEGF 天然以二聚体存在，四价结构可桥接 VEGF 二聚体与 PD-1 形成稳定"簇状复合物"，产生亲合力（avidity）效应——这是协同结合的结构基础 |
| Fc 沉默（LALA） | ① 疗效：避免 ADCC/ADCP 清除表达 PD-1 的活化 T 细胞；② 安全：Fc 效应与 irAE、细胞因子释放相关 |
| 较短半衰期（首剂 5–7 天，稳态约 10 天，vs 贝伐珠单抗约 20 天） | 每个给药周期后段血清游离 VEGF 部分回升，压缩持续 VEGF 抑制的毒性暴露窗口 |

来源：*iScience* 2025（同上）；Wang F et al., *Cancer Medicine* 2025（[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11925807/)）

### 1.2 双靶点各自通路

- **PD-1 阻断臂**：竞争性阻断 PD-1/PD-L1 相互作用，解除 T 细胞免疫抑制。报告基因体系中阻断 PD-1/PD-L1 信号 IC50 为 3.29 nM（VEGF 存在时）vs 17.16 nM（无 VEGF）；与 PD-1 的 ELISA 结合 EC50 约 0.06 nM
- **VEGF 中和臂**：结合 VEGF-A（EC50 约 0.036 nM），阻断 VEGF-A/VEGFR2 下游信号，诱导**肿瘤血管正常化**、增加瘤内灌注、促进 CTL 浸润

来源：*iScience* 2025（[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11872405/)）

### 1.3 协同的生物学基础：VEGF 是免疫抑制因子

VEGF 除促血管生成外，还是 TME 中关键免疫抑制因子：抑制树突状细胞成熟、促进 Treg 与 MDSC、**上调肿瘤浸润 CD8⁺ T 细胞的 PD-1 表达**、维持异常血管结构阻碍效应 T 细胞浸润。VEGF 与 PD-1 在 TME 中共表达且表达强相关——这是"单分子双阻断 + 局部富集"策略的核心依据。

来源：Frentzas et al., *JITC* 2024（[JITC](https://jitc.bmj.com/content/12/4/e008037)）

### 1.4 核心差异化机制：协同结合（Cooperative Binding）

这是依沃西单抗区别于"PD-1 单抗 + 贝伐珠单抗"简单联用的 emergent 性质：

- SEC-HPLC 证实依沃西与 VEGF 二聚体形成**可溶性多聚复合物**（多个抗体分子经 VEGF 二聚体桥接）
- **VEGF → PD-1 方向**：VEGF 存在时，依沃西对 PD-1 的结合亲和力**提升 18 倍**（相对派安普利单抗），主要源于解离速率减慢；伴随 PD-1 内化增强、阻断效价提升（IC50 17.16 → 3.29 nM）、T 细胞活化增强
- **PD-1 → VEGF 方向**：PD-1 结合使依沃西对 VEGF 的亲和力**提升 >4 倍**，游离 VEGF 清除增强
- 体内验证：人源化小鼠 HCC827（EGFR 突变肺腺癌）与 U87MG 模型中呈剂量依赖性抗肿瘤，优于贝伐珠单抗

来源：*iScience* 2025（[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11872405/)）；康方生物 SITC 2023 新闻稿（[Akeso](https://www.akesobio.com/en/media/akeso-news/231103/)）

### 1.5 肿瘤微环境锚定/富集假说

逻辑链：TME 中 VEGF 与 PD-1 双高共表达 → 协同结合使"四结合位点全占据"的簇状复合物最稳定 → 双抗被滞留于肿瘤组织而非正常组织。**注意：该假说目前主要由体外协同结合数据 + 机制推断支持，iScience 原文承认缺乏体内直接证据**（需三敲入小鼠模型验证）。

来源：JITC 2024（[JITC](https://jitc.bmj.com/content/12/4/e008037)）；Summit 投资者材料（[PDF](https://www.smmttx.com/wp-content/uploads/2024/03/2024_PR_0305_Barclays-Teaser_FINAL.pdf)）

### 1.6 双抗一体化 vs 两药联用的理论优势

| 维度 | 双抗一体化优势 | 依据 |
|---|---|---|
| 药代同步 | 单分子 PK，两靶点抑制同步发生 | Summit 投资者材料 |
| 局部浓度 | VEGF 锚定 + 协同结合 → TME 富集 | iScience 2025 |
| 亲和力 | VEGF 存在下 PD-1 亲和力 +18 倍，联用两单抗无法获得 | iScience 2025 |
| 安全性 | Fc 沉默 + 短半衰期；真实世界研究显示 PD-(L)1+贝伐联用是多种毒性的独立危险因素 | iScience 2025；JITC 2024 |

---

## 二、早期临床数据（I 期）

### 2.1 AK112-101（首次人体试验，澳大利亚，NCT04047290）

| 项目 | 数据 |
|---|---|
| 设计 | 3+3+3 剂量爬坡 0.3–30 mg/kg Q2W，晚期实体瘤，n=51 |
| MTD | 20 mg/kg Q2W（30 mg/kg 出现 2 例 DLT：肌钙蛋白升高、3 级高血压） |
| PK | 暴露量剂量比例性增长；表观 t1/2 约 4.5–6.6 天 |
| PD | **≥3 mg/kg 剂量组 PD-1 受体占有率多剂后持续 >80%**；血清游离 VEGF 首剂后 24 小时内下降 80%–95% |
| 疗效 | 确认 ORR 25.5%（12/47），DCR 63.8%；铂耐药卵巢癌 26.3% PR |
| 安全性 | ≥3 级 TRAE 27.5%（高血压 13.7%）；**无 ≥2 级出血、无胃肠穿孔** |

来源：Frentzas et al., *JITC* 2024（[PubMed](https://pubmed.ncbi.nlm.nih.gov/38642937/)）

### 2.2 AK112-102（中国 I 期，NCT04597541）

- 剂量 3–30 mg/kg Q2W / 10–20 mg/kg Q3W，n=59；**MTD 未达到**（仅 1 例 DLT）
- PK：线性 PK，t1/2 4.98–7.30 天，约 5 次给药达稳态；**中西方人群 PK 无差异**
- PD：首剂后 1 天 PD-1 占有率即达约 90%，全程维持 >80%；血清 VEGF 首剂后 1 天内下降 63.3%–96.4%，第 8 天起部分回升（与"短半衰期 → 周期后段 VEGF 部分恢复 → 减轻毒性"的机制解释一致）
- 安全性：≥3 级 TRAE 23.7%，**无治疗相关死亡**；VEGF 靶点相关 ≥3 级：高血压 5.1%、蛋白尿 3.4%、**无 ≥3 级出血**——低于 IMbrave150（阿替利珠+贝伐联用）≥3 级 TRAE 45.3%

来源：Wang F et al., *Cancer Medicine* 2025（[PubMed](https://pubmed.ncbi.nlm.nih.gov/40114411/)，[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11925807/)）

### 2.3 AK112-201（II 期，依沃西+化疗，NSCLC 三队列）

| 队列 | n | 关键数据 |
|---|---|---|
| 1L 无驱动基因 NSCLC | 43 | ORR 53.5%；扩展后鳞癌 n=63：ORR 67%、mPFS 11.1 个月、24 个月 OS 率 64.8% |
| EGFR-TKI 进展 | 19 | ORR 68.4%、mPFS 8.5 个月、mOS 22.5 个月 |
| 铂类+PD-(L)1 失败 | 20 | ORR 40.0%、mPFS 7.5 个月 |

安全性：≥3 级 TRAE 26.5%，停药率低。来源：*Signal Transduct Target Ther* 2023（[PubMed](https://pubmed.ncbi.nlm.nih.gov/37593227/)）；ELCC 2024 更新（[Business Wire](https://www.businesswire.com/news/home/20241030447809/en/)）

---

## 三、关键注册性 III 期数据

### 3.1 HARMONi-A（AK112-301）——EGFR-TKI 耐药 nsq-NSCLC（中国 III 期）

- **设计**：随机双盲，n=322，依沃西 20 mg/kg Q3W + 培美曲塞/卡铂 vs 安慰剂+化疗；主要终点 IRRC-PFS
- **PFS**：mPFS 7.06 vs 4.80 个月，**HR 0.46（95%CI 0.34–0.62），p<0.001**；ORR 50.6% vs 35.4%
- **OS 最终分析（mFU 32.5 个月，SITC 2025 公布）**：mOS 16.8 vs 14.1 个月，**HR 0.74（95%CI 0.58–0.95），p=0.019，统计学显著**——全球首个依沃西方案 OS 显著阳性的 III 期；脑转移亚组 HR 0.61
- **安全性**：≥3 级 TRAE 61.5% vs 49.1%（多为化疗血液学毒性）；≥3 级 VEGF 相关 AE 仅 3.1% vs 2.5%；≥3 级 irAE 6.2% vs 2.5%

来源：*JAMA* 2024（[PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11337070/)）；SITC 2025 最终 OS（[SEC 文件](https://www.sec.gov/Archives/edgar/data/1599298/000159929825000166/a2025_prx1107sitcharmoni.htm)）

### 3.2 HARMONi-2（AK112-303）——1L PD-L1 阳性 NSCLC 单药头对头 K 药（中国 III 期）

这是全球首个在 III 期头对头击败帕博利珠单抗的研究：

- **设计**：n=398，依沃西单药 vs 帕博利珠单抗单药；PD-L1 TPS≥1%、EGFR/ALK 阴性；不允许交叉
- **PFS**：mPFS 11.14 vs 5.82 个月，**HR 0.51（95%CI 0.38–0.69），p<0.0001**；ORR 50.0% vs 38.5%。亚组一致性极佳：TPS≥50% HR 0.46–0.48、TPS 1–49% HR 0.54、鳞癌 HR 0.48–0.50
- **OS 中期分析（39% 成熟度，2025-04-25 公布）**：HR 0.777（未达统计学显著）；**截至 2026-08-29 最终 OS 尚未公布**
- **安全性**：≥3 级 TRAE 29% vs 16%（VEGF 相关毒性贡献增量）；≥3 级 irAE 7% vs 8%（相当）；**VEGF 相关 3 级 AE：出血 1%、蛋白尿 3%、高血压 5%，无 4–5 级**

来源：*Lancet* 2025（[PubMed](https://pubmed.ncbi.nlm.nih.gov/40057343/)）；Summit 新闻稿（[PDF](https://www.smmttx.com/wp-content/uploads/2024/09/2024_PR_0908_WCLC-HARMONi-2-Data-_-FINAL-7.pdf)）；OS 中期分析（[SEC](https://www.sec.gov/Archives/edgar/data/1599298/000159929825000066/a2025_prx0425xivonescima.htm)）

### 3.3 HARMONi-6（AK112-306）——1L 鳞状 NSCLC 头对头替雷利珠+化疗（中国 III 期）

- **设计**：n=532，依沃西+化疗 vs 替雷利珠单抗+化疗；约 63% 为中央型鳞癌
- **PFS**：mPFS 11.14 vs 6.90 个月，**HR 0.60（95%CI 0.46–0.78），p<0.0001**（ESMO 2025 主席研讨会）
- **OS 中期分析（mFU 21.4 个月，ASCO 2026 全体大会 LBA4 + Lancet 同步发表）**：mOS 27.9 vs 23.7 个月，**HR 0.66（95%CI 0.50–0.87），p=0.0017，达预设界值，统计学显著**；24 个月 OS 率 64.7% vs 48.6%；PD-L1 阴性亚组 HR 0.64。**全球首个对比 PD-1+化疗最优 SOC 取得 OS+PFS 双阳性的 III 期**
- 争议点：≥65 岁亚组未校正 HR≈0.93；康方称校正基线不平衡后死亡风险降幅约 31%
- **安全性**：≥3 级 TRAE 64% vs 54%；**≥3 级治疗相关出血仅 2% vs 1%**——在含 63% 中央型鳞癌人群中突破了贝伐珠单抗禁用于鳞癌的历史限制

来源：Summit 公告（[2026-05-31](https://smmttx.com/news/press-releases/news-details/2026/Ivonescimab-with-Chemotherapy-Demonstrated-a-Statistically-Significant-Overall-Survival-Benefit-Compared-to-Tislelizumab-Plus-Chemotherapy-in-1L-Treatment-of-Patients-with-Squamous-NSCLC-in-the-HARMONi-6-Study-Conducted-by-Akeso-in-China/default.aspx)）；Fierce Pharma（[2026-05-31](https://www.fiercepharma.com/pharma/asco-akeso-ivonescimab-bests-pd-1-inhibitor-squamous-nsclc-overall-survival)）

### 3.4 HARMONi（全球 III 期，NCT06396065）——2L+ EGFRm nsq-NSCLC

- **设计**：多区域双盲，n=438（约 38% 西方患者），依沃西+化疗 vs 安慰剂+化疗；双主要终点 PFS+OS
- **主要分析（2025-05-30 topline）**：PFS HR 0.52（p<0.00001）；mPFS 6.8 vs 4.4 个月；**OS HR 0.79，p=0.057，未达统计学显著**
- **OS 更新（DCO 2026-06，2026-07-22 公布）**：ITT HR 0.76、西方亚组 HR 0.76（西方 mOS 从 HR 0.98 → 0.84 → 0.76 持续改善），仍非统计学显著；主要分析已发表于 *Lancet Oncology* 2026
- **监管影响**：FDA 明确该适应症获批需 OS 统计学显著；Summit 仍于 2025 Q4 提交 BLA，2026-01 获受理，**PDUFA 目标日期 2026-11-14**——2026 年最大催化事件

来源：Summit topline（[PDF](https://www.smmttx.com/wp-content/uploads/2025/05/2025_PR_0530-_-HARMONi-Data-_-FINAL.docx.pdf)）；2026 OS 更新（[Summit](https://smmttx.com/news/press-releases/news-details/2026/Ivonescimab-Plus-Chemotherapy-Shows-Consistent-Favorable-Overall-Survival-Results-in-Western-and-Asian-Patients-in-Updated-Analysis-from-Global-Phase-III-HARMONi-Study/default.aspx)）

### 3.5 其他 III 期布局

| 研究 | 瘤种/人群 | 状态（截至 2026-08-29） |
|---|---|---|
| HARMONi-3 | 1L NSCLC（鳞+非鳞）vs K药+化疗 | 入组中，非鳞队列最终 PFS 预计 2027 上半年 |
| HARMONi-7 | 1L PD-L1 高表达单药 vs K药 | 入组中 |
| HARMONi-GI1（AK112-309） | 1L 胆道癌 vs 度伐利尤+化疗 | **2026-08-26 公布中期分析达 OS 主要终点**（具体数字待会议发表），首个消化道肿瘤 III 期阳性 |
| HARMONi-GI3 | 1L 结直肠癌 vs 贝伐+化疗 | 2025 Q4 启动入组 |
| 其他 | TNBC、头颈鳞、胰腺癌、尿路上皮癌、IO 耐药 NSCLC、LS-SCLC 等 | 共 16 项注册性 III 期（6 项国际多中心、7 项头对头 PD-1/L1） |

来源：康方新闻稿（[2026-08-26](https://www.akesobio.com/cn/media/akeso-news/20260826/)、[2026-06-15](https://www.akesobio.com/cn/media/akeso-news/20260615/)）

---

## 四、安全性综合分析

| 研究 | 方案 | ≥3 级 TRAE | ≥3 级 VEGF 相关 AE |
|---|---|---|---|
| AK112-101（Ia） | 单药 | 27.5% | 高血压 13.7% |
| AK112-102（I） | 单药 | 23.7% | 蛋白尿为主（多低级别），无 ≥3 级出血 |
| HARMONi-2（III） | 单药 vs K药 | 29% vs 16% | 出血 1%、蛋白尿 3%、高血压 5%，无 4–5 级 |
| HARMONi-A（III） | +化疗 vs 化疗 | 61.5% vs 49.1% | 3.1% vs 2.5% |
| HARMONi-6（III，鳞癌） | +化疗 vs 替雷利珠+化疗 | 64% vs 54% | 出血 2% vs 1% |
| 贝伐珠单抗历史对照（E4599/SAiL，非头对头） | 贝伐+化疗 | — | ≥3 级高血压 6–8%、出血 4–5.2%（含致死性肺出血）；**鳞癌禁忌** |

**解读**：依沃西单药的 VEGF 相关 ≥3 级 AE 率（高血压 5%、蛋白尿 3%、出血 1–2%）整体不劣于、甚至低于贝伐珠单抗历史水平；HARMONi-6 证明在鳞癌（含中央型）中出血风险可控，构成相对贝伐珠单抗的差异化安全性优势。但需注意：**机制上"降低 VEGF 毒性"的证据强于"消除毒性"**——HARMONi-2 中依沃西组 ≥3 级 TRAE 仍高于 K药（29% vs 16%），VEGF 相关毒性贡献了明确增量。

来源：各研究原始数据见上文引用；贝伐数据见 DailyMed 说明书（[链接](https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid=70ab1de6-fb68-aee4-a6cb-f9a0f146687f&audience=consumer)）

---

## 五、机制—临床闭环分析

**机制预测 → 临床验证的对应关系：**

1. **"双靶协同优于单靶阻断"** → HARMONi-2 单药头对头 K药 PFS HR 0.51：这是协同结合假说最强的人体证据。若依沃西只是"PD-1+VEGF 两效叠加"，单药对单药在 PD-L1 阳性人群中取得接近翻倍的 mPFS（11.1 vs 5.8 个月）较难解释。
2. **"VEGF 臂贡献真实疗效"** → HARMONi-6 在鳞癌中 PFS/OS 双阳性（OS HR 0.66）：鳞癌 PD-1 单药/联合方案历史上 OS 改善幅度有限，且贝伐因出血被排除在鳞癌之外，依沃西同时解锁了"鳞癌抗 VEGF"这一空白。
3. **"安全性设计（Fc 沉默+短半衰期）"** → 各研究中 ≥3 级 VEGF AE 率（1–5%）低于贝伐历史数据，无致死性肺出血信号；鳞癌出血 2%。
4. **尚存缺口的环节**：OS 获益的幅度与稳健性。HARMONi-2 中期 OS HR 0.777、全球 HARMONi OS HR 0.76–0.79 均未达统计学显著——提示 PFS 获益向 OS 转化的幅度可能中等（HR 约 0.75–0.80），需要更长随访和更大样本确认。全球 HARMONi 西方亚组 HR 从 0.98 改善至 0.76，显示后线治疗交叉/随访时长对 OS 的影响，但也构成 FDA 审批的核心不确定性（PDUFA 2026-11-14）。

**机制层面未决问题**：
- TME 锚定富集缺乏体内直接证据（iScience 原文承认）
- "短半衰期是刻意设计还是靶点介导清除（TMDD）"未明确区分
- 协同结合的 18 倍数据为与派安普利单抗比较的体外数值，人体内的实际增益无法直接测量

---

## 六、竞争格局（同类 PD-(L)1/VEGF 双抗）

| 药物 | 公司 | 分子设计 | 协同结合数据 | 临床进展 |
|---|---|---|---|---|
| **依沃西 AK112** | 康方/Summit | 抗 VEGF IgG1 + C端抗 PD-1 scFv，2+2 四价，Fc-LALA | PD-1 亲和力 +18 倍，VEGF +4 倍 | **3 项 NMPA 适应症；FDA BLA 受理（PDUFA 2026-11-14）；16 项 III 期** |
| **BNT327/PM8002** | BioNTech/BMS（111 亿美元合作） | 抗 VEGF-A IgG1 + C端 2 个抗 PD-L1 VHH | 未公开定量协同数据 | ES-SCLC II 期 ORR 76.3%；ROSETTA Lung-02 NSCLC cORR 57–68%；多瘤种 III 期推进 |
| **SSGJ-707** | 三生制药/辉瑞（首付 12.5 亿美元，创中国出海纪录） | 对称 2+2 四价 IgG4 | 辉瑞宣称 PD-1 亲和力 +100 倍（未经同行评议验证） | II 期 1L PD-L1+ NSCLC：cORR 67.6%、mPFS 12.4 个月（ASCO 2026）；头对头 K药 III 期进行中 |

来源：BNT327：Fierce Biotech（[2025-09-08](https://www.fiercebiotech.com/biotech/biontech-bms-tout-first-global-data-pd-l1xvegf-bispecific-set-phase-3-dose-small-cell-lung)）；SSGJ-707：三生制药（[2026-05-27](https://www.3sbio.com/mobile/news/details.aspx?id=344)）、辉瑞投资者材料（[PDF](https://s206.q4cdn.com/795948973/files/doc_events/2025/Jul/25/PfizerPflash_3SBio_FINAL.pdf)）

**格局判断**：依沃西在进度上领先 2–3 年，但 BNT327 与 SSGJ-707 背后分别为 BioNTech/BMS 与辉瑞的全球开发资源，2027–2028 年赛道竞争将显著加剧。

---

## 七、监管状态时间线

| 时间 | 事件 |
|---|---|
| 2024-05-24 | NMPA 首次批准：依沃西+化疗用于 EGFR-TKI 耐药 nsq-NSCLC |
| 2025-01-01 | 纳入中国国家医保目录 |
| 2025-04-25 | NMPA 第 2 项适应症：1L PD-L1 阳性 NSCLC 单药 |
| 2026-01 | FDA 受理 BLA（2L+ EGFRm nsq-NSCLC），PDUFA 2026-11-14 |
| 2026-01 | NMPA 说明书更新，纳入 HARMONi-A 最终 PFS+OS 双阳性数据 |
| 2026-08-12 | NMPA 第 3 项适应症：1L 鳞状 NSCLC +化疗 |

来源：Akeso 公告（[2024-05-31](https://www.akesobio.com/en/media/akeso-news/240531)）；CancerNetwork（[2026-08-28](https://www.cancernetwork.com/view/ivonescimab-chemotherapy-maintains-os-benefit-in-egfr-mutant-nsclc)）；Morningstar/PRNewswire（[2026-08-12](https://www.morningstar.com/news/pr-newswire/20260812cn24853/)）

---

## 八、总体评价

**优势（已有数据支撑）**：
1. 协同结合机制独特且有完整体外证据链；HARMONi-2 头对头击败 K药是机制→临床闭环的标志性证据
2. 三项 OS 显著阳性的 III 期（HARMONi-A、HARMONi-6、GI1），覆盖化疗联合场景
3. VEGF 相关重度毒性率低于贝伐单抗历史数据，鳞癌安全性突破有差异化价值
4. 中国商业化已验证（超 70,000 例患者），医保放量

**风险与不确定性**：
1. **OS 转化的稳健性**：PD-L1 阳性单药人群（HARMONi-2）与全球研究（HARMONi）的 OS 均未达统计学显著，FDA 审批（2026-11-14）存在被拒风险
2. 全球 HARMONi 数据源自中国研究外推，西方人群亚组样本有限
3. 机制叙事中"TME 锚定"缺体内证据；竞品的差异化宣称（如 SSGJ-707 "100 倍亲和力"）缺乏同行评议验证
4. HARMONi-6 ≥65 岁亚组 OS 获益不明确（HR≈0.93）

---

*本报告基于 2026-08-29 前公开资料整理，关键数字均回溯至期刊论文、公司公告或 SEC 文件。胆道癌 HARMONi-GI1 具体数字、HARMONi-2 最终 OS 尚未披露，报告将随数据更新而需修订。*

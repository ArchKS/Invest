---
CreateTime: 2026-08-05 09:54:46
LastUpdate: 2026-08-05 10:45:59
---

# 统计BCL-2靶点在三期临床失败的案例，以及失败的原因

截至 2026-07-07，按公开可核实资料，我建议这样统计：

**结论**
BCL-2 靶点/通路药物三期失败可分两类：

- **明确未达三期主要终点：5 项**
- **主要终点达到但获益风险失败：1 项，BELLINI**
- **若把“监管失败/开发失败”也算入：再加 1 项，oblimersen 在 CLL**

**主表**

| 药物                          | 试验/适应症                                            | 三期结果                                                     | 失败类型     | 主要失败原因                                                 |
| ----------------------------- | ------------------------------------------------------ | ------------------------------------------------------------ | ------------ | ------------------------------------------------------------ |
| oblimersen，BCL-2反义寡核苷酸 | 晚期黑色素瘤，+达卡巴嗪，771例                         | OS 9.0 vs 7.8月，p=0.077；PFS/ORR改善                        | 主要OS未达   | BCL-2抑制不足以逆转黑色素瘤化疗耐药；无强生物标志物筛选；疗效幅度太小 |
| oblimersen                    | AGENDA，低/正常LDH黑色素瘤，314例                      | OS和PFS均无显著改善                                          | 确证性失败   | 回顾性LDH亚组未能前瞻验证；LDH更像预后因子，不是可靠预测因子 |
| oblimersen                    | CALGB 10201，老年初治AML，506例                        | 1年OS 43% vs 40%，p=0.13；DFS/EFS无改善                      | 疗效失败     | 反义药物组织递送/靶点敲低有限；AML凋亡依赖异质，常受MCL-1/BCL-xL等旁路保护 |
| venetoclax                    | VIALE-C，初治不适合强化化疗AML，+低剂量阿糖胞苷，211例 | 初次分析OS未达统计显著；后续6个月随访OS 8.4 vs 4.1月，p=0.040 | 边缘统计失败 | 初次分析随访不成熟；LDAC骨架弱；AML人群异质性大              |
| venetoclax                    | BELLINI，复发/难治MM，+硼替佐米/地塞米松，291例        | PFS显著改善，但死亡/感染风险升高；终版提示应避免用于一般RRMM人群 | 获益风险失败 | 未筛选MM人群并非普遍BCL-2依赖；非t(11;14)/低BCL2患者获益差；中性粒细胞减少、肺炎、致死感染增加 |
| venetoclax                    | CANOVA，t(11;14)复发/难治MM，VenDex vs PomDex，263例   | PFS 9.9 vs 5.8月，但HR 0.823，p=0.24；未达主要终点           | 疗效统计失败 | t(11;14)仍不是充分预测标志物；MM内部BCL-2依赖程度不一；对照组活性较强；感染/死亡信号压低获益风险 |

**一个不计入“主要终点失败”、但应关注的案例**
oblimersen + 氟达拉滨/环磷酰胺在复发/难治CLL中，CR/nPR主要终点达到，17% vs 7%，p=0.025；但5年ITT OS无显著差异，HR 0.87，p=0.34，FDA认为总体获益不足，最终没有获批。这个更像**监管/开发失败**，不是典型三期主要终点失败。

**共性原因**
BCL-2靶点失败的核心不是“靶点无效”，而是**依赖性筛选很难**。CLL、部分AML、t(11;14) MM更容易BCL-2依赖；但黑色素瘤、未筛选MM、异质性AML里，肿瘤常转向MCL-1、BCL-xL等抗凋亡旁路。

第二个原因是**治疗窗问题**。venetoclax本身是选择性BCL-2抑制剂，但和化疗/蛋白酶体抑制剂合用时，感染、粒缺、肺炎会把PFS收益吃掉。BELLINI就是典型：PFS赢了，但获益风险输了。

第三个原因是**早期oblimersen这个技术平台本身不够强**：反义药物需要连续静脉输注，肿瘤组织递送和BCL-2蛋白下调不如后来的BH3 mimetic直接、稳定，所以多项三期只能看到小幅信号，难转化为OS获益。

来源：BELLINI [2020](https://pubmed.ncbi.nlm.nih.gov/33129376/) / [2025 OS终报](https://pubmed.ncbi.nlm.nih.gov/40587991/)，CANOVA [JCO 2026](https://pubmed.ncbi.nlm.nih.gov/41370738/)，VIALE-C [Blood Cancer Journal 2021](https://pubmed.ncbi.nlm.nih.gov/34599139/)，oblimersen黑色素瘤 [JCO 2006](https://pubmed.ncbi.nlm.nih.gov/16966688/)，AGENDA [Melanoma Research 2014](https://pubmed.ncbi.nlm.nih.gov/24667300/)，CALGB 10201 [Blood Advances 2021](https://pubmed.ncbi.nlm.nih.gov/34251414/)，CLL [JCO 2007](https://pubmed.ncbi.nlm.nih.gov/17296974/) / [5年随访](https://pubmed.ncbi.nlm.nih.gov/19738118/)。





# 考虑中国的临床数据，亚盛的2575会有这类问题吗

会有“同类风险”，但不能一概而论。我的判断是：

**在CLL/SLL里，2575重演BELLINI/CANOVA式失败的概率较低；在AML、MM和实体瘤里，风险明显更高。**

2575，也就是lisaftoclax/APG-2575，是选择性BCL-2抑制剂。公开资料显示，它2025年7月10日在中国首次获批，用于既往至少一线系统治疗、且包括BTK抑制剂治疗后的成人CLL/SLL；给药采用5天爬坡，第6天达到目标剂量。[Drugs 2025](https://pubmed.ncbi.nlm.nih.gov/41060518/)

为什么CLL/SLL风险相对低？因为CLL本来就是BCL-2依赖最清楚的疾病之一，venetoclax已经在这个病种证明过BCL-2路线可行。2575如果主要打BTKi经治CLL/SLL，失败风险更多来自“疗效幅度和安全性是否足够好”，而不是靶点逻辑错误。

但中国数据不能完全消除三类问题：

1. **BELLINI式安全性问题仍要看联合方案**
   2575选择性BCL-2，不像navitoclax强打BCL-xL，所以理论上血小板毒性更少。但BCL-2抑制剂和BTKi、HMA、化疗联用时，仍可能出现中性粒细胞减少、感染、肺炎、治疗相关死亡。BELLINI不是因为PFS没赢，而是PFS赢了但感染/死亡信号毁掉获益风险。
2. **CANOVA式“标志物不够强”问题在MM最值得担心**
   t(11;14) MM已经是BCL-2依赖较强的亚群，但venetoclax CANOVA仍未达PFS主要终点。2575如果在MM里推进，必须证明比venetoclax更好的安全性或更精准的筛选。单靠“BCL-2抑制剂”或“t(11;14)”不够。
3. **AML里是可行路线，但比较残酷**
   2575+阿扎胞苷已有AML三期登记，主要终点是OS，计划入组486例。[NCT06389292](https://clinicaltrials.gov/study/NCT06389292) 这里逻辑类似venetoclax+HMA，但问题是：venetoclax已经很强，2575要么证明安全性/便利性更好，要么在疗效上接近或超过。AML里感染、粒缺、早期死亡是最核心风险。

**看正在进行的三期设计**

- 复发/难治CLL/SLL：2575+BTK抑制剂 vs BTK抑制剂，PFS主要终点，预计400例。[NCT06104566](https://clinicaltrials.gov/study/NCT06104566)
- 初治CLL/SLL：2575+acalabrutinib vs 免疫化疗，PFS主要终点，预计344例。[NCT06319456](https://clinicaltrials.gov/study/NCT06319456)
- AML：2575+阿扎胞苷 vs 安慰剂+阿扎胞苷，OS主要终点，预计486例。[NCT06389292](https://clinicaltrials.gov/study/NCT06389292)

我的底线判断：

**CLL/SLL：成药逻辑较强，最大风险是商业/对照组/安全性，而不是靶点失败。**
**AML：有机会，但必须控制感染和早死，并面对venetoclax标准治疗的阴影。**
**MM：最容易重演BELLINI/CANOVA，需要极强患者筛选和安全性优势。**
**实体瘤：风险最高，BCL-2依赖性通常不够清楚。**

所以，考虑中国临床数据，2575在已获批的CLL/SLL场景里不像“历史BCL-2失败药”；但如果亚盛把它往MM、AML、实体瘤大规模扩展，刚才那些失败模式仍然会回来敲门。
# ai coding: 汇总三款多发性骨髓瘤药物临床研究并生成带来源链接的Excel 2026/09/09: 14:12
from pathlib import Path

from openpyxl import Workbook, load_workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.worksheet.table import Table, TableStyleInfo
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter


OUT = Path("/Users/zendu/Documents/Invest/医药/Carvykti_Tecvayli_Talvey_临床汇总_截至2026-09-09.xlsx")
DATA_CUTOFF = "2026-09-09"


def ctgov(nct):
    return f"https://clinicaltrials.gov/study/{nct}"


def pubmed(term):
    return "https://pubmed.ncbi.nlm.nih.gov/?term=" + term.replace(" ", "+")


def google(term):
    return "https://www.google.com/search?q=" + term.replace(" ", "+")


def link(label, url):
    return (label, url)


trial_headers = [
    "药物", "商品名", "研究名称", "NCT", "分期", "适应症/人群", "方案与对照",
    "样本量", "主要终点", "已读出疗效", "PFS/OS/DOR/MRD", "关键安全性",
    "状态/数据截止", "证据等级", "来源链接", "备注",
]


early_rows = [
    ["cilta-cel", "Carvykti", "LEGEND-2", "NCT03090659", "I（早期）", "R/R多发性骨髓瘤；BCMA CAR-T；中国先导", "LCAR-B38M/cilta-cel单臂；单次回输；无对照", "n=74（关键论文）；原始西安队列n=57", "安全性、ORR、CR/sCR、PFS/OS", "ORR 87.8%；CR 73.0%", "4年随访mPFS约18–19.9个月；长期OS数据按队列报告", "CRS常见；神经毒性和感染需结合队列解读", "已读出；公开随访口径不同", "A/B", link("ClinicalTrials.gov", ctgov("NCT03090659")), "研究产品命名及队列存在LCAR-B38M/cilta-cel差异。"],
    ["cilta-cel", "Carvykti", "CARTITUDE-1", "NCT03548207", "Ib/II（早期/关键注册）", "多线经治R/R MM；既往≥3线，含PI/IMiD/抗CD38暴露", "cilta-cel单臂；淋巴清除后单次输注；无对照", "n=97", "ORR、sCR、DOR、PFS、OS及安全性", "ORR约97%；早期sCR约80%", "mFU约33.4个月mPFS 34.9个月；约61.3个月随访mOS 60.7个月；约1/3患者5年无进展", "CRS、ICANS、感染、长期血细胞减少；早期研究无随机对照", "已读出；2025–2026长期更新", "A", link("ClinicalTrials.gov", ctgov("NCT03548207")), "长期数据是关键商业化和治疗持续性依据。"],
    ["teclistamab", "Tecvayli", "MajesTEC-1", "NCT03145181", "I/II（早期）", "R/R MM；既往多线，三药暴露/难治人群", "teclistamab单药；皮下给药；无对照", "关键队列n=165", "ORR、CR或更好、DOR、PFS、OS及安全性", "ORR 63.0%；CR或更好约39.4%", "mPFS 11.3个月；mOS约18.3个月；mDOR约24个月", "CRS 72.1%，≥3级约0.6%；ICANS约3%；中性粒细胞减少约65.5%", "已读出；长期随访/不同队列口径需区分", "A", link("ClinicalTrials.gov", ctgov("NCT03145181")), "MajesTEC-1是Tecvayli单药在三药暴露R/R MM中的核心早期证据。"],
    ["teclistamab", "Tecvayli", "MajesTEC-2（公开多队列）", "NCT04722146", "Ib（早期）", "R/R MM；不同联合方案队列", "teclistamab联合daratumumab、lenalidomide/pomalidomide等；多队列、无统一对照", "公开分析集/队列不同；部分资料n约65", "安全性、ORR、CR/sCR、MRD及联合方案可行性", "早期公开联合队列ORR约88.5%；具体队列/分析集数据，不能外推为所有队列", "部分队列报告CR/MRD及PFS，但正式长期总结果未统一成熟", "CRS、感染、血液学毒性；联合免疫调节剂可能增加骨髓抑制", "部分读出；以具体队列资料为准", "B", link("ClinicalTrials.gov", ctgov("NCT04722146")), "保留为早期联合探索，不与MajesTEC-3随机三期结果混用。"],
    ["talquetamab", "Talvey", "MonumenTAL-1", "NCT03399799 / NCT04634552", "I/II（早期）", "R/R MM；既往多线/三药暴露，含TCE暴露人群", "talquetamab单药；0.4 mg/kg QW或0.8 mg/kg Q2W；无对照", "关键pivotal队列约n=288；0.4 mg/kg QW n=143", "RP2D、安全性、ORR、DOR、PFS", "0.4 mg/kg QW ORR 74.1%；0.8 mg/kg Q2W ORR约71.7%", "0.4 mg/kg QW mPFS 7.5个月；0.8 mg/kg Q2W mPFS约11.9个月", "CRS、感染、味觉障碍、皮肤/指甲毒性、体重下降", "已读出；不同剂量/队列分别解读", "A/B", link("ClinicalTrials.gov", ctgov("NCT03399799")), "NCT04634552为后续II期注册/扩展，主表另列。"],
    ["talquetamab", "Talvey", "TRIMM-2", "NCT04108195", "Ib（早期）", "R/R MM；talquetamab联合daratumumab", "talquetamab+daratumumab；多剂量/给药频次队列；无统一对照", "多队列；公开资料分析集不同", "联合方案安全性、RP2D、ORR、DOR", "早期公开队列ORR约71–84%；RP2D 0.8 mg/kg Q2W+ dara 1800 mg Q2W队列ORR约82.4%", "长期PFS/OS未形成统一成熟总结果", "CRS、感染、味觉障碍和皮肤毒性；联合方案需关注感染负担", "部分读出；队列数据", "B", link("ClinicalTrials.gov", ctgov("NCT04108195")), "ORR为具体队列数据，不能替代随机对照证据。"],
    ["talquetamab", "Talvey", "MonumenTAL-2", "NCT05050097", "Ib（早期）", "R/R MM；既往≥2线治疗", "talquetamab+pomalidomide；多队列；无对照", "多队列；公开分析集不同", "安全性、RP2D、ORR、DOR、PFS", "约2年随访更新ORR 85.7%", "长期PFS/OS需按Cohort E及后续发表数据核对", "CRS、感染、味觉障碍、皮肤/指甲毒性、血细胞减少", "已读出；约2年随访更新", "B", link("ClinicalTrials.gov", ctgov("NCT05050097")), "联合方案结果受队列选择和既往治疗影响。"],
    ["talquetamab", "Talvey", "RedirecTT-1", "NCT04586426", "Ib/II（早期）", "R/R MM；既往多线；talquetamab+teclistamab双靶向", "talquetamab+teclistamab；剂量探索及扩展；无对照", "多队列；Phase I full-dose cohort按公开分析集", "安全性、RP2D、ORR、DOR、PFS", "混合R/R MM早期ORR约79%", "Phase I full-dose cohort mPFS约38.6个月（数据截止2025年7月）", "CRS、感染、味觉/皮肤毒性及长期免疫球蛋白下降风险", "部分读出；不同队列不可合并外推", "B", link("ClinicalTrials.gov", ctgov("NCT04586426")), "该研究同时涉及Tecvayli和Talvey，按Talvey组合项目归类。"],
]


phase2_rows = [
    ["cilta-cel", "Carvykti", "CARTIFAN-1", "NCT03758417", "II", "中国R/R MM；既往多线治疗", "cilta-cel单臂；单次输注；无对照", "可评估n=48", "ORR、CR/sCR、DOR、PFS、OS及安全性", "ORR 89.6%", "mPFS、mOS尚未达到（公开早期更新）", "3级CRS约0；感染、血细胞减少和神经毒性需随访", "已读出；中国队列", "A/B", link("ClinicalTrials.gov", ctgov("NCT03758417")), "公开资料可能按ITT、疗效可评估集或不同随访报告。"],
    ["cilta-cel", "Carvykti", "CARTITUDE-2（Cohorts A/B/D）", "NCT04133636", "II", "不同线次/治疗背景的MM；含早期复发及既往治疗暴露人群", "多队列单臂；cilta-cel单次输注；无对照", "Cohort A n=20；B/D为公开队列", "各队列ORR、sCR、MRD、PFS和安全性", "Cohort A ORR 95%（19/20）；Cohort D ORR约94.1%、sCR约88.2%", "Cohort A 24个月PFS 75%；Cohort B 24个月PFS约73%", "CRS、ICANS、感染、长期血细胞减少；不同队列背景差异大", "已读出；多队列更新", "A/B", link("ClinicalTrials.gov", ctgov("NCT04133636")), "A/B/D结果应按具体队列和治疗线次解读。"],
    ["teclistamab", "Tecvayli", "MajesTEC-1（II期注册/扩展）", "NCT04557098", "II", "R/R MM；三药暴露/难治人群", "teclistamab单药；皮下给药；无对照", "与核心MajesTEC-1公开分析集重叠；关键队列n=165", "ORR、CR或更好、DOR、PFS、OS及安全性", "核心关键队列ORR 63.0%；CR或更好约39.4%", "mPFS 11.3个月；mOS约18.3个月；mDOR约24个月", "CRS 72.1%；≥3级CRS约0.6%；ICANS约3%；中性粒细胞减少约65.5%", "已读出；与NCT03145181数据需避免重复计数", "A", link("ClinicalTrials.gov", ctgov("NCT04557098")), "该行用于体现II期注册；核心疗效数据来自MajesTEC-1程序。"],
    ["teclistamab", "Tecvayli", "MajesTEC-5 / GMMG-HD10/DSMM-XX", "NCT05695508", "II", "初治、移植适合NDMM；诱导阶段", "teclistamab+daratumumab+lenalidomide，±bortezomib；多队列；无随机对照", "n=49（3个诱导队列）", "ORR、MRD阴性、移植可行性及安全性", "ORR 100%（49/49）", "MRD：48/49有可用样本，所有可评估样本NGF阴性；公开报道整体约98.0%（不同MRD口径）", "以感染、CRS、血液学毒性及移植相关安全性为主；长期PFS/OS未成熟", "已读出；2026年更新；研究仍在进行", "B", link("ClinicalTrials.gov", ctgov("NCT05695508")), "小样本、多队列诱导数据，不能替代随机三期。"],
    ["talquetamab", "Talvey", "MonumenTAL-1（pivotal II期队列）", "NCT04634552", "II", "R/R MM；既往多线/三药暴露，含TCE暴露人群", "talquetamab单药；0.4 mg/kg QW或0.8 mg/kg Q2W；无对照", "关键pivotal队列约n=288；0.4 mg/kg QW n=143", "ORR、DOR、PFS、安全性", "0.4 mg/kg QW ORR 74.1%；0.8 mg/kg Q2W ORR约71.7%", "0.4 mg/kg QW mPFS 7.5个月；0.8 mg/kg Q2W mPFS约11.9个月", "CRS、感染、味觉障碍、皮肤/指甲毒性、体重下降", "已读出；剂量队列分别报告", "A/B", link("ClinicalTrials.gov", ctgov("NCT04634552")), "与NCT03399799同属MonumenTAL-1开发项目。"],
]


phase3_rows = [
    ["cilta-cel", "Carvykti", "CARTITUDE-4", "NCT04181827", "III", "lenalidomide-refractory R/R MM；既往1–3线", "cilta-cel单次输注 vs DPd或PVd", "n=419", "主要终点PFS；关键次要终点ORR、OS、MRD、安全性", "初始mFU约16个月：ORR 84.6% vs 67.3%", "PFS HR 0.26；12个月PFS 75.9% vs 48.7%；更新mFU约33.6个月30个月PFS约80.5% vs 59.9%", "CRS、ICANS、感染、血细胞减少和继发恶性肿瘤监测", "已读出；随机三期阳性；长期OS持续更新", "A", link("ClinicalTrials.gov", ctgov("NCT04181827")), "对照为DPd/PVd；不同分析的随访时间必须注明。"],
    ["cilta-cel", "Carvykti", "CARTITUDE-3", "NCT04566419", "III", "NDMM；初始治疗后、移植相关策略人群", "研究方案含cilta-cel策略与标准治疗比较；以注册库为准", "注册库实时更新", "PFS、OS、MRD、缓解深度及安全性", "正式随机疗效读出未在本次资料中确认", "尚未形成可引用的成熟PFS/OS数据", "CAR-T治疗相关CRS、ICANS、感染、血细胞减少", "进行中/未确认正式读出；截至2026-09-09", "C", link("ClinicalTrials.gov", ctgov("NCT04566419")), "仅列注册设计，不把预设终点当作已读出数据。"],
    ["cilta-cel", "Carvykti", "CARTITUDE-5", "NCT04923893", "III", "NDMM；VRd诱导后，前线cilta-cel策略", "VRd诱导后cilta-cel vs VRd/移植相关标准策略（以注册库为准）", "注册库实时更新", "PFS为核心终点，另含OS、MRD和安全性", "正式随机疗效读出未在本次资料中确认", "尚无成熟随机PFS/OS公开结果纳入本表", "CAR-T和诱导/移植策略相关血液学毒性、感染、CRS/ICANS", "进行中/未确认正式读出；截至2026-09-09", "C", link("ClinicalTrials.gov", ctgov("NCT04923893")), "设计信息以ClinicalTrials.gov最新版本为准。"],
    ["cilta-cel", "Carvykti", "CARTITUDE-6", "NCT05257083", "III", "NDMM；移植适合人群", "DVRd诱导后cilta-cel策略 vs DVRd后ASCT/维持路径（以注册库为准）", "注册库实时更新", "PFS、OS、MRD、缓解和安全性", "正式随机疗效读出未在本次资料中确认", "尚无成熟随机PFS/OS公开结果纳入本表", "诱导、CAR-T、移植相关感染/血液学毒性；CRS/ICANS", "进行中/未确认正式读出；截至2026-09-09", "C", link("ClinicalTrials.gov", ctgov("NCT05257083")), "仅列注册设计和开发位置。"],
    ["teclistamab", "Tecvayli", "MajesTEC-3", "NCT05083169", "III", "R/R MM；既往1–3线，含免疫调节剂/蛋白酶体抑制剂治疗后", "Tec-Dara vs DPd/DVd", "n=587（291 vs 296）", "PFS；OS、ORR、MRD及安全性", "mFU 34.5个月：ORR约89% vs 75.3%；MRD阴性CR 58.4% vs 17.1%", "mPFS未达到 vs 18.1个月；PFS HR 0.17；36个月PFS 83.4% vs 29.7%", "严重不良反应和感染较常见；CRS、ICANS、低丙种球蛋白血症需管理", "已读出；2026年长期更新", "A/B", link("ClinicalTrials.gov", ctgov("NCT05083169")), "本项目正确注册号为NCT05083169。"],
    ["teclistamab", "Tecvayli", "MajesTEC-4 / EMN30", "NCT05243797", "III", "NDMM；诱导及ASCT后维持", "Tec-Len、Tec单药 vs Len单药；随机开放标签", "注册库实时更新；安全性run-in为小样本", "PFS、MRD、OS及安全性", "安全性run-in：ASCT后CR或更好比例接近100%（小样本/早期分析）", "截至2025-09-17：57%仍在治疗，22%完成固定疗程；正式随机PFS/OS未成熟", "安全性run-in显示可管理；CRS、感染、血液学毒性需长期观察", "部分读出；正式随机疗效未成熟", "B", link("ClinicalTrials.gov", ctgov("NCT05243797")), "将SRI结果与正式随机比较结果分开标注。"],
    ["teclistamab + talquetamab", "Tecvayli + Talvey", "MajesTEC-7", "NCT05552222", "III", "NDMM；ASCT不适合/不计划移植", "Tec-DR和Tal-DR vs DRd；随机开放标签", "注册库实时更新", "PFS、MRD、OS、安全性；含安全性run-in", "安全性run-in：CRS约61.5%，均为1级；ICANS约1例1级；3/4级中性粒细胞减少约50%", "正式随机疗效尚未成熟/未确认", "CRS、感染、血液学毒性；Tec/Tal组合的长期免疫抑制需观察", "部分读出；正式随机疗效未成熟", "B/C", link("ClinicalTrials.gov", ctgov("NCT05552222")), "该研究同时覆盖Tecvayli和Talvey。"],
    ["teclistamab", "Tecvayli", "MajesTEC-9", "NCT05572515", "III", "R/R MM；既往1–3线；较早线次复发人群", "teclistamab单药 vs 研究者选择PVd或Kd", "注册库实时更新；公开分析含随机比较人群", "PFS为主要终点；OS、ORR、DOR及安全性", "ORR 84.5% vs 54.2%；风险下降71%", "PFS HR 0.29；18个月OS 79.2% vs 68.6%；18个月DOR 80.6% vs 40.1%；mOS两组未达到", "安全性与已知Tecvayli特征一致；感染、CRS、低丙球和血液学毒性需管理", "已读出；ASCO/EHA 2026更新；注册库仍显示研究状态需核对", "A/B", link("ClinicalTrials.gov", ctgov("NCT05572515")), "公开资料中部分PFS率和随访口径仍需以正式论文/医学资料最终版为准。"],
    ["talquetamab", "Talvey", "MonumenTAL-3", "NCT05455320", "III", "R/R MM；既往多线治疗", "Tal-DP、Tal-D vs DPd；随机1:1:1", "n=864", "PFS为主要终点；OS、ORR、CR或更好及安全性", "ORR 88.2%、88.5% vs 77.6%；CR或更好71.1%、69.0% vs 34.5%", "24个月PFS 81.3%、77.6% vs 51.2%；PFS HR 0.28、0.33；24个月OS 89.2%、87.9% vs 79.1%；OS HR 0.47、0.51", "3/4级TEAE 94.9%、74.8%、91.5%；3/4级感染37.7%、29.2%、42.4%", "已读出；NEJM 2026；随机三期阳性", "A", link("ClinicalTrials.gov", ctgov("NCT05455320")), "Tal-DP=talquetamab+daratumumab+pomalidomide；Tal-D=talquetamab+daratumumab。"],
    ["talquetamab", "Talvey", "MonumenTAL-5", "NCT05461209", "III", "R/R MM；既往至少2线治疗；与belantamab mafodotin比较", "talquetamab vs belantamab mafodotin；随机开放标签", "注册库实时更新", "ORR或PFS（以注册库最新版本为准）、OS及安全性", "正式随机疗效读出未在本次资料中确认", "尚无成熟随机PFS/OS公开结果纳入本表", "味觉/皮肤指甲毒性、CRS、感染；对照belantamab的眼毒性需区分", "进行中/未确认正式读出；截至2026-09-09", "C", link("ClinicalTrials.gov", ctgov("NCT05461209")), "仅列公开注册设计，避免把研究目标误写成结果。"],
    ["teclistamab + talquetamab", "Tecvayli + Talvey", "MonumenTAL-6", "NCT06208150", "III", "较早线次R/R MM；研究者选择EPd或PVd对照", "Tec-Tal、Tal-P vs研究者选择EPd/PVd；全球随机开放标签", "注册库实时更新；Topline未披露统一n", "PFS/OS、ORR、安全性", "Topline：Tec-Tal降低疾病进展或死亡风险89%；Tal-P ORR>84%，Tec-Tal ORR>77%（公开摘要/特定队列口径）", "Tec-Tal PFS HR约0.11；Tec-Tal OS HR约0.38；风险下降分别约89%和62%", "整体安全性与已知单药特征一致；CRS、感染、低丙球、味觉/皮肤毒性需关注", "已读出topline；2026-07-23公告/后续会议更新", "B", link("ClinicalTrials.gov", ctgov("NCT06208150")), "Topline数据的具体随访、分层和样本量以正式论文/监管资料为准。"],
]


readout_headers = [
    "药物", "商品名", "研究名称", "NCT", "分期", "数据集/随访", "方案/比较", "样本量",
    "缓解/主要疗效", "PFS/OS/DOR/MRD", "关键安全性", "数据状态", "来源链接", "解读/限制",
]


readout_rows = [
    ["cilta-cel", "Carvykti", "LEGEND-2", "NCT03090659", "I", "关键论文；4年长期随访", "LCAR-B38M/cilta-cel单臂", "n=74；原始西安队列n=57", "ORR 87.8%；CR 73.0%", "mPFS约18–19.9个月（队列/随访口径不同）", "CRS常见；长期细胞治疗毒性需结合队列", "已读出", link("PubMed检索", pubmed("LEGEND-2 LCAR-B38M")), "早期中国先导研究，产品命名和分析集需注意。"],
    ["cilta-cel", "Carvykti", "CARTITUDE-1", "NCT03548207", "Ib/II", "mFU约33.4个月；约61.3个月长期更新", "cilta-cel单臂", "n=97", "ORR约97%；早期sCR约80%", "mPFS 34.9个月；mOS 60.7个月；约1/3患者5年无进展", "CRS、ICANS、感染、长期血细胞减少", "已读出", link("PubMed检索", pubmed("CARTITUDE-1 cilta-cel")), "长期随访显示缓解持久性，但为单臂研究。"],
    ["cilta-cel", "Carvykti", "CARTIFAN-1", "NCT03758417", "II", "中国R/R MM；疗效可评估集", "cilta-cel单臂", "n=48可评估", "ORR 89.6%", "mPFS、mOS未达到", "3级CRS约0；感染/血细胞减少需随访", "已读出", link("PubMed检索", pubmed("CARTIFAN-1 cilta-cel")), "小样本中国队列，不能与全球随机三期直接比较。"],
    ["cilta-cel", "Carvykti", "CARTITUDE-2 Cohorts A/B/D", "NCT04133636", "II", "多队列更新；Cohort A/B/D", "cilta-cel单臂多队列", "A n=20；B/D公开队列", "A ORR 95%（19/20）；D ORR约94.1%、sCR约88.2%", "A 24个月PFS 75%；B 24个月PFS约73%", "CRS、ICANS、感染、血细胞减少", "已读出", link("PubMed检索", pubmed("CARTITUDE-2 cilta-cel")), "不同队列治疗线次和既往暴露不同。"],
    ["cilta-cel", "Carvykti", "CARTITUDE-4", "NCT04181827", "III", "初始mFU约16个月；更新mFU约33.6个月", "cilta-cel vs DPd/PVd", "n=419", "ORR 84.6% vs 67.3%", "PFS HR 0.26；12个月PFS 75.9% vs 48.7%；30个月PFS约80.5% vs 59.9%", "CAR-T相关CRS/ICANS、感染、血细胞减少", "已读出", link("PubMed检索", pubmed("CARTITUDE-4 cilta-cel")), "更新数据应与正式论文的分析时间点对应。"],
    ["teclistamab", "Tecvayli", "MajesTEC-1", "NCT03145181", "I/II", "关键队列n=165；长期公开更新", "teclistamab单药", "n=165", "ORR 63.0%；CR或更好约39.4%", "mPFS 11.3个月；mOS约18.3个月；mDOR约24个月", "CRS 72.1%，≥3级约0.6%；ICANS约3%；中性粒细胞减少约65.5%", "已读出", link("PubMed检索", pubmed("MajesTEC-1 teclistamab")), "核心单药注册证据；不同随访版本可能略有差异。"],
    ["teclistamab", "Tecvayli", "MajesTEC-2", "NCT04722146", "Ib", "联合队列；公开分析集/随访不同", "Tec联合Dara、Len/Pom等", "部分资料n约65；队列不同", "早期公开联合队列ORR约88.5%", "部分队列报告深度缓解/MRD，但统一长期PFS/OS未成熟", "CRS、感染、骨髓抑制；联合方案安全性需分队列", "部分读出", link("PubMed检索", pubmed("MajesTEC-2 teclistamab")), "ORR为具体联合队列读出，不能外推为全研究总体。"],
    ["teclistamab", "Tecvayli", "MajesTEC-3", "NCT05083169", "III", "mFU 34.5个月", "Tec-Dara vs DPd/DVd", "n=587（291 vs 296）", "ORR约89% vs 75.3%；MRD阴性CR 58.4% vs 17.1%", "mPFS未达到 vs 18.1个月；PFS HR 0.17；36个月PFS 83.4% vs 29.7%", "严重不良反应、感染、CRS、低丙球和血液学毒性", "已读出", link("研究注册与更新", ctgov("NCT05083169")), "重要随机三期阳性结果；NCT号必须核对为NCT05083169。"],
    ["teclistamab", "Tecvayli", "MajesTEC-4 / EMN30", "NCT05243797", "III", "安全性run-in；ASCT后早期分析", "Tec-Len、Tec vs Len", "SRI小样本；总体n以注册库为准", "ASCT后CR或更好比例接近100%（早期SRI）", "截至2025-09-17：57%仍在治疗，22%完成固定疗程；正式随机PFS/OS未成熟", "SRI总体可管理；CRS、感染、血液学毒性", "部分读出", link("研究注册与更新", ctgov("NCT05243797")), "SRI不能替代正式随机比较。"],
    ["teclistamab + talquetamab", "Tecvayli + Talvey", "MajesTEC-7", "NCT05552222", "III", "安全性run-in", "Tec-DR、Tal-DR vs DRd", "SRI公开数据集", "正式随机疗效未成熟", "CRS约61.5%且均为1级；ICANS约1例1级；3/4级中性粒细胞减少约50%", "感染、血液学毒性、低丙球风险", "部分读出", link("研究注册与更新", ctgov("NCT05552222")), "研究同时涉及Tecvayli与Talvey。"],
    ["teclistamab", "Tecvayli", "MajesTEC-9", "NCT05572515", "III", "ASCO/EHA 2026中期/更新", "teclistamab单药 vs PVd/Kd", "公开随机比较；总n以注册库为准", "ORR 84.5% vs 54.2%；疾病进展/死亡风险下降71%", "PFS HR 0.29；18个月OS 79.2% vs 68.6%；18个月DOR 80.6% vs 40.1%；mOS未达到", "安全性与已知Tecvayli特征一致；感染/CRS/低丙球/血液学毒性", "已读出", link("PubMed检索", pubmed("MajesTEC-9 teclistamab")), "部分PFS率和随访数值以正式论文/医学资料最终版为准。"],
    ["teclistamab", "Tecvayli", "MajesTEC-5", "NCT05695508", "II", "2026年更新；3个诱导队列", "Tec-DR ± bortezomib；移植适合NDMM", "n=49", "ORR 100%（49/49）", "48/49有MRD样本，所有可评估样本NGF阴性；公开资料整体约98.0%", "感染、CRS、血液学毒性和移植相关风险；长期PFS/OS未成熟", "已读出", link("PubMed检索", pubmed("MajesTEC-5 teclistamab")), "小样本多队列数据；MRD口径需区分样本可用性与总体比例。"],
    ["talquetamab", "Talvey", "MonumenTAL-1", "NCT03399799 / NCT04634552", "I/II", "关键pivotal剂量队列", "talquetamab单药；0.4 mg/kg QW与0.8 mg/kg Q2W", "0.4 QW n=143；pivotal合计约n=288", "0.4 QW ORR 74.1%；0.8 Q2W ORR约71.7%", "0.4 QW mPFS 7.5个月；0.8 Q2W mPFS约11.9个月", "CRS、感染、味觉障碍、皮肤/指甲毒性、体重下降", "已读出", link("PubMed检索", pubmed("MonumenTAL-1 talquetamab")), "剂量和队列分开呈现。"],
    ["talquetamab", "Talvey", "TRIMM-2", "NCT04108195", "Ib", "早期联合队列", "talquetamab+daratumumab", "多队列；公开分析集不同", "ORR约71–84%；RP2D队列ORR约82.4%", "统一长期PFS/OS未成熟", "CRS、感染、味觉和皮肤毒性", "部分读出", link("PubMed检索", pubmed("TRIMM-2 talquetamab daratumumab")), "具体ORR随剂量、队列和分析集变化。"],
    ["talquetamab", "Talvey", "MonumenTAL-2", "NCT05050097", "Ib", "约2年随访更新；Cohort E", "talquetamab+pomalidomide", "公开分析集不同", "ORR 85.7%", "长期PFS/OS按后续发表资料核对", "CRS、感染、味觉/皮肤毒性、血细胞减少", "已读出", link("PubMed检索", pubmed("MonumenTAL-2 talquetamab pomalidomide")), "组合方案数据，不等同于Talvey单药。"],
    ["talquetamab", "Talvey", "RedirecTT-1", "NCT04586426", "Ib/II", "Phase I full-dose cohort；数据截止2025-07", "talquetamab+teclistamab", "公开队列不同", "混合R/R MM ORR约79%", "Phase I full-dose cohort mPFS约38.6个月", "CRS、感染、味觉/皮肤毒性、低丙球风险", "部分读出", link("PubMed检索", pubmed("RedirecTT-1 talquetamab teclistamab")), "仅限指定队列，不能外推全部研究人群。"],
    ["talquetamab", "Talvey", "MonumenTAL-3", "NCT05455320", "III", "随机三臂；NEJM 2026", "Tal-DP、Tal-D vs DPd", "n=864", "ORR 88.2%、88.5% vs 77.6%；CR或更好71.1%、69.0% vs 34.5%", "24个月PFS 81.3%、77.6% vs 51.2%；PFS HR 0.28、0.33；24个月OS 89.2%、87.9% vs 79.1%；OS HR 0.47、0.51", "3/4级TEAE 94.9%、74.8%、91.5%；3/4级感染37.7%、29.2%、42.4%", "已读出", link("NEJM文章", "https://www.nejm.org/doi/full/10.1056/NEJMoa2604657"), "截至2026年公开正式三期结果；各臂需按方案拆分。"],
    ["teclistamab + talquetamab", "Tecvayli + Talvey", "MonumenTAL-6", "NCT06208150", "III", "2026-07-23 topline；后续会议/论文待更新", "Tec-Tal、Tal-P vs EPd/PVd", "统一n未在topline公告中披露", "Tec-Tal/Tal-P公开ORR分别>77%/>84%（特定公开摘要口径）", "Tec-Tal PFS HR约0.11（风险下降89%）；OS HR约0.38（风险下降62%）", "整体安全性与已知单药特征一致；CRS、感染、低丙球、味觉/皮肤毒性", "已读出topline", link("研究注册与更新", ctgov("NCT06208150")), "具体样本量、随访和分层结果以正式论文或监管资料为准。"],
]


summary_headers = ["药物/组合", "商品名", "主要靶点/机制", "代表性早期/二期", "代表性三期", "截至2026-09-09已读出核心数据", "未成熟/在研重点", "关键安全性与解读"]
summary_rows = [
    ["cilta-cel", "Carvykti", "BCMA CAR-T；单次细胞治疗", "LEGEND-2；CARTITUDE-1；CARTIFAN-1；CARTITUDE-2", "CARTITUDE-4；CARTITUDE-3/5/6", "CARTITUDE-1 mOS 60.7个月；CARTITUDE-4 PFS HR 0.26；CARTIFAN-1 ORR 89.6%", "NDMM前线和移植适合人群的CARTITUDE-3/5/6正式随机结果", "CRS/ICANS、感染、血细胞减少；长期随访和制造/可及性影响商业化。"],
    ["teclistamab", "Tecvayli", "BCMA×CD3双特异性抗体；现货型T细胞重定向", "MajesTEC-1/2/5；早期联合探索", "MajesTEC-3/4/7/9", "MajesTEC-3 PFS HR 0.17、36个月PFS 83.4%；MajesTEC-9 PFS HR 0.29、ORR 84.5% vs 54.2%；MajesTEC-5 ORR 100%/深度MRD", "MajesTEC-4/7正式随机疗效成熟度；感染、低丙球和持续给药管理", "CRS、感染、低丙球、血液学毒性；长期免疫抑制和给药便利性是关键。"],
    ["talquetamab", "Talvey", "GPRC5D×CD3双特异性抗体；现货型T细胞重定向", "MonumenTAL-1/2；TRIMM-2；RedirecTT-1", "MonumenTAL-3/5/6", "MonumenTAL-3 24个月PFS 81.3%/77.6% vs 51.2%；MonumenTAL-6 Tec-Tal PFS HR约0.11；MonumenTAL-2 ORR 85.7%", "MonumenTAL-5正式读出；MonumenTAL-6完整论文和长期OS", "CRS、感染、味觉障碍、皮肤/指甲毒性、体重下降；生活质量和营养管理重要。"],
]


source_rows = [
    ["注册库", "ClinicalTrials.gov NCT03090659", "LEGEND-2", "分期、方案、状态", link("打开注册页", ctgov("NCT03090659")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT03548207", "CARTITUDE-1", "分期、入排、方案、状态", link("打开注册页", ctgov("NCT03548207")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT03758417", "CARTIFAN-1", "分期、方案、状态", link("打开注册页", ctgov("NCT03758417")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT04133636", "CARTITUDE-2", "分期、多队列方案、状态", link("打开注册页", ctgov("NCT04133636")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT04181827", "CARTITUDE-4", "随机三期设计、对照、终点", link("打开注册页", ctgov("NCT04181827")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT04566419", "CARTITUDE-3", "三期注册设计", link("打开注册页", ctgov("NCT04566419")), "C"],
    ["注册库", "ClinicalTrials.gov NCT04923893", "CARTITUDE-5", "三期注册设计", link("打开注册页", ctgov("NCT04923893")), "C"],
    ["注册库", "ClinicalTrials.gov NCT05257083", "CARTITUDE-6", "三期注册设计", link("打开注册页", ctgov("NCT05257083")), "C"],
    ["注册库", "ClinicalTrials.gov NCT03145181", "MajesTEC-1", "早期研究设计与状态", link("打开注册页", ctgov("NCT03145181")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT04557098", "MajesTEC-1 II期扩展", "II期注册设计", link("打开注册页", ctgov("NCT04557098")), "C"],
    ["注册库", "ClinicalTrials.gov NCT04722146", "MajesTEC-2", "多队列联合方案", link("打开注册页", ctgov("NCT04722146")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT05083169", "MajesTEC-3", "正确NCT号；三期随机设计", link("打开注册页", ctgov("NCT05083169")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT05243797", "MajesTEC-4/EMN30", "三期维持治疗设计", link("打开注册页", ctgov("NCT05243797")), "B/C"],
    ["注册库", "ClinicalTrials.gov NCT05552222", "MajesTEC-7", "三期Tec-DR/Tal-DR vs DRd", link("打开注册页", ctgov("NCT05552222")), "B/C"],
    ["注册库", "ClinicalTrials.gov NCT05572515", "MajesTEC-9", "三期Tec单药 vs PVd/Kd", link("打开注册页", ctgov("NCT05572515")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT05695508", "MajesTEC-5", "II期诱导方案", link("打开注册页", ctgov("NCT05695508")), "B/C"],
    ["注册库", "ClinicalTrials.gov NCT03399799", "MonumenTAL-1", "早期剂量探索", link("打开注册页", ctgov("NCT03399799")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT04634552", "MonumenTAL-1 II期扩展", "II期pivotal队列", link("打开注册页", ctgov("NCT04634552")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT04108195", "TRIMM-2", "Tal+Dara早期联合", link("打开注册页", ctgov("NCT04108195")), "B/C"],
    ["注册库", "ClinicalTrials.gov NCT05050097", "MonumenTAL-2", "Tal+Pom早期联合", link("打开注册页", ctgov("NCT05050097")), "B/C"],
    ["注册库", "ClinicalTrials.gov NCT04586426", "RedirecTT-1", "Tal+Tec双靶向早期联合", link("打开注册页", ctgov("NCT04586426")), "B/C"],
    ["注册库", "ClinicalTrials.gov NCT05455320", "MonumenTAL-3", "三期随机三臂设计", link("打开注册页", ctgov("NCT05455320")), "A/C"],
    ["注册库", "ClinicalTrials.gov NCT05461209", "MonumenTAL-5", "Tal vs belantamab三期设计", link("打开注册页", ctgov("NCT05461209")), "C"],
    ["注册库", "ClinicalTrials.gov NCT06208150", "MonumenTAL-6", "Tec-Tal/Tal-P vs EPd/PVd三期设计", link("打开注册页", ctgov("NCT06208150")), "B/C"],
    ["论文检索", "CARTITUDE-1 / LEGEND-2 / CARTIFAN-1", "cilta-cel早期与长期随访", "ORR、CR/sCR、PFS、OS", link("PubMed检索", pubmed("cilta-cel CARTITUDE-1 LEGEND-2 CARTIFAN-1")), "A/B"],
    ["论文检索", "MajesTEC-1 / MajesTEC-2 / MajesTEC-5", "teclistamab早期、联合及NDMM II期", "ORR、PFS、MRD、安全性", link("PubMed检索", pubmed("teclistamab MajesTEC-1 MajesTEC-2 MajesTEC-5")), "A/B"],
    ["论文/摘要", "MajesTEC-3", "teclistamab+daratumumab三期", "mFU 34.5个月；36个月PFS、MRD、ORR", link("Google检索入口", google("MajesTEC-3 36-month PFS 83.4 2026")), "A/B"],
    ["论文/摘要", "MajesTEC-9", "teclistamab单药三期", "PFS HR、18个月OS/DOR、ORR", link("PubMed检索", pubmed("MajesTEC-9 teclistamab")), "A/B"],
    ["论文/摘要", "MonumenTAL-1 / 2 / TRIMM-2 / RedirecTT-1", "talquetamab早期/联合", "ORR、PFS及安全性", link("PubMed检索", pubmed("talquetamab MonumenTAL-1 MonumenTAL-2 TRIMM-2 RedirecTT-1")), "A/B"],
    ["论文", "MonumenTAL-3", "talquetamab三期随机研究", "PFS、OS、ORR、CR或更好、安全性", link("NEJM文章", "https://www.nejm.org/doi/full/10.1056/NEJMoa2604657"), "A"],
    ["公司公告/会议", "MonumenTAL-6", "Tec-Tal/Tal-P三期topline", "PFS HR约0.11、OS HR约0.38、风险下降89%/62%", link("Google检索入口", google("MonumenTAL-6 July 23 2026 topline")), "B"],
]


def set_link(cell, payload):
    if isinstance(payload, tuple):
        label, url = payload
        cell.value = label
        cell.hyperlink = url
        cell.style = "Hyperlink"
    else:
        cell.value = payload


def write_table(ws, headers, rows, table_name):
    ws.append(headers)
    for row in rows:
        ws.append([None] * len(headers))
        target_row = ws.max_row
        for col, value in enumerate(row, start=1):
            set_link(ws.cell(target_row, col), value)
    end_col = get_column_letter(len(headers))
    ref = f"A1:{end_col}{ws.max_row}"
    table = Table(displayName=table_name, ref=ref)
    table.tableStyleInfo = TableStyleInfo(name="TableStyleMedium2", showFirstColumn=False, showLastColumn=False, showRowStripes=True, showColumnStripes=False)
    ws.add_table(table)
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ref


def style_sheet(ws, header_fill="1F4E78"):
    thin = Side(style="thin", color="D9E2F3")
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=header_fill)
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = Border(bottom=thin)
    ws.row_dimensions[1].height = 34
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
            cell.border = Border(bottom=thin)
    widths = {}
    for col in ws.iter_cols(1, ws.max_column):
        letter = get_column_letter(col[0].column)
        max_len = max(len(str(c.value or "")) for c in col)
        widths[letter] = min(max(max_len * 1.15 + 2, 12), 42)
    for letter, width in widths.items():
        ws.column_dimensions[letter].width = width
    for col in ["F", "G", "I", "J", "K", "L", "M", "N", "P"]:
        if col in ws.column_dimensions:
            ws.column_dimensions[col].width = max(ws.column_dimensions[col].width, 24)
    ws.sheet_view.showGridLines = False
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth = 1
    ws.page_setup.fitToHeight = 0


def add_explanation(wb):
    ws = wb.active
    ws.title = "说明"
    rows = [
        ["项目", "内容"],
        ["文件", OUT.name],
        ["数据截止日", f"{DATA_CUTOFF}；数据以该日可公开检索的ClinicalTrials.gov、论文、会议摘要和公司公告为准。"],
        ["整理范围", "Carvykti/cilta-cel、Tecvayli/teclistamab、Talvey/talquetamab在多发性骨髓瘤中的早期、II期和III期关键临床；同时列已读出和仍在研项目。"],
        ["已读出数据口径", "仅把公开论文、会议摘要、医学资料或公司公告中已经报告的ORR、CR/sCR、MRD、PFS、OS、DOR和安全性列为已读出；研究设计中的预计终点不当作结果。"],
        ["分析集口径", "不同队列、剂量、随访时间、ITT/疗效可评估集和安全性集分开标注；小样本SRI、topline或公司公告数据用‘部分读出’或‘topline’标注。"],
        ["三期新增重点", "纳入MajesTEC-3、MajesTEC-9、MonumenTAL-3、MonumenTAL-6截至2026年的更新；MajesTEC-4/7的SRI与正式随机疗效分开。"],
        ["缩写", "ORR=客观缓解率；CR/sCR=完全缓解/严格完全缓解；PFS=无进展生存；OS=总生存；DOR=缓解持续时间；MRD=微小残留病；CRS=细胞因子释放综合征；ICANS=免疫效应细胞相关神经毒性综合征。"],
        ["证据等级", "A=正式论文/随机三期或成熟公开结果；B=会议摘要、公司公告、医学资料或早期队列；C=仅注册设计/未确认正式读出。"],
        ["使用提示", "点击各表‘来源链接’可打开注册库或文献检索入口；ClinicalTrials.gov页面状态会动态变化，应以打开页面的最新状态为准。"],
    ]
    for row in rows:
        ws.append(row)
    ws.freeze_panes = "A2"
    ws.sheet_view.showGridLines = False
    ws.column_dimensions["A"].width = 22
    ws.column_dimensions["B"].width = 115
    for cell in ws[1]:
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor="1F4E78")
        cell.alignment = Alignment(horizontal="center", vertical="center")
    for row in ws.iter_rows(min_row=2):
        for cell in row:
            cell.alignment = Alignment(vertical="top", wrap_text=True)
    for row in range(2, ws.max_row + 1):
        ws.row_dimensions[row].height = 34


def build():
    wb = Workbook()
    add_explanation(wb)
    for name, headers, rows, table_name in [
        ("早期临床", trial_headers, early_rows, "EarlyTrials"),
        ("二期临床", trial_headers, phase2_rows, "Phase2Trials"),
        ("三期临床", trial_headers, phase3_rows, "Phase3Trials"),
        ("已读出数据", readout_headers, readout_rows, "ReadoutData"),
        ("药物适应症汇总", summary_headers, summary_rows, "DrugSummary"),
        ("来源", ["来源类型", "标题/编号", "支持研究/内容", "主要用途", "来源链接", "证据等级"], source_rows, "Sources"),
    ]:
        ws = wb.create_sheet(name)
        write_table(ws, headers, rows, table_name)
        style_sheet(ws, "1F4E78" if name != "已读出数据" else "548235")
    readout_ws = wb["已读出数据"]
    readout_ws.conditional_formatting.add(f"A2:N{readout_ws.max_row}", FormulaRule(formula=['$L2="已读出"'], fill=PatternFill("solid", fgColor="E2F0D9")))
    readout_ws.conditional_formatting.add(f"A2:N{readout_ws.max_row}", FormulaRule(formula=['ISNUMBER(SEARCH("未成熟",$L2))'], fill=PatternFill("solid", fgColor="FFF2CC")))
    phase3_ws = wb["三期临床"]
    phase3_ws.conditional_formatting.add(f"A2:P{phase3_ws.max_row}", FormulaRule(formula=['ISNUMBER(SEARCH("进行中",$M2))'], fill=PatternFill("solid", fgColor="FFF2CC")))
    wb.properties.title = "Carvykti/Tecvayli/Talvey临床汇总"
    wb.properties.subject = "截至2026-09-09公开临床数据"
    wb.properties.creator = "Codex"
    wb.save(OUT)


if __name__ == "__main__":
    build()
    check = load_workbook(OUT, read_only=True, data_only=False)
    print(OUT)
    print(check.sheetnames)
    for ws in check.worksheets:
        print(ws.title, ws.max_row, ws.max_column)

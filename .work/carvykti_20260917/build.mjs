// ai coding: 创建基线对照与可点击来源链接并保留原始工作表 2026/09/17: 16:42
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const dir='/Users/zendu/Documents/Invest/outputs/carvykti_20260917';
const w=await SpreadsheetFile.importXlsx(await FileBlob.load('/Users/zendu/Documents/Invest/医药/临床/Carvykti.xlsx'));
const s=w.worksheets.add('基线对比');
const q=w.worksheets.add('基线来源');
const S={
 C:['CARVYKTI HCP：CARTITUDE-4 基线表','https://www.carvyktihcp.com/cartitude-4-efficacy/primary-analysis/'],
 M:['Costa等，NEJM，Table 1','https://pmc.ncbi.nlm.nih.gov/articles/PMC13218738/'],
 A:['Costa等，补充附录Table S3，印刷页22–24（PDF页23–25）','https://pmc.ncbi.nlm.nih.gov/articles/instance/13218738/bin/NIHMS2166230-supplement-appendix.pdf'],
 D:['CARTITUDE-4患者报告结局论文：入组时间','https://pubmed.ncbi.nlm.nih.gov/39756844/'],
 P:['Costa等，NEJM正文：试验设计与入排条件','https://amcana.org/Content/User/images/Costa-TEC-3-IA-NEJM-2025.pdf'],
 L:['CARTITUDE-4 ASCO 2023研究者报告：任一PI耐药','https://investors.legendbiotech.com/static-files/ab73e030-4fec-4f00-9d9d-258eea9c2568']
};
const n=(a,b,k)=>({a,b,k});
const t=(v,k)=>({v,k});
const missing=t('未单独报告','A');
const rows=[];
const add=(label,c,m,note='',sub=false)=>rows.push({label,c,m,note,sub});
const section=label=>rows.push({label,section:true});
add('分析人群',t('cilta-cel 随机分组（ITT）','C'),t('Tec-Dara 随机分组（ITT）','M'),'两列均为试验组；并非两项研究的全部入组患者。');
add('入组人数',t(208,'C'),t(291,'M'),'全研究分别419人和587人。');
add('入组时间',t('2020/07/10–2021/11/17','D'),t('2021/10/22–2023/09/29','P'));
add('中位年龄（岁；范围）',t('61.5（27–78）','C'),t('64（36–88）','A'));
add('男性占比',n(116,208,'C'),n(156,291,'A'));
section('种族');
add('亚裔',n(16,208,'C'),n(68,291,'A'),'',true);
add('黑人',n(6,208,'C'),n(13,291,'A'),'',true);
add('白人',n(157,208,'C'),n(190,291,'A'),'',true);
add('其他（排除未提供及未知）',n(1,208,'C'),n(1,291,'A'),'CARTITUDE-4截图5.0%更正为0.5%。MajesTEC-3按附录脚注拆分。',true);
add('未提供或未知',n(28,208,'C'),n(19,291,'A'),'MajesTEC-3：未报告14人＋未知5人；原文合并“其他”20人（6.9%）。',true);
section('ECOG 体能状态');
add('0',n(114,208,'C'),n(167,291,'A'),'',true);
add('1',n(93,208,'C'),n(108,291,'A'),'',true);
add('2',n(1,208,'C'),n(16,291,'A'),'CARTITUDE-4为单采/第1周期前最近一次评分。',true);
section('ISS 多发性骨髓瘤分期');
add('I',n(136,208,'C'),n(182,291,'A'),'',true);
add('II',n(60,208,'C'),n(85,291,'A'),'',true);
add('III',n(12,208,'C'),n(24,291,'A'),'',true);
add('确诊至随机分组（年；中位数及范围）',t('3.0（0.3–18.1）','C'),t('3.7（0.4–20.3）','A'));
add('软组织浆细胞瘤',n(44,208,'C'),n(41,291,'A'),'包含髓外和骨旁病灶；不能等同于单纯髓外病变。');
add('骨髓浆细胞比例 ≥60%',n(42,206,'C'),n(28,286,'A'),'按有骨髓检测数据者为分母。MajesTEC-3截图9.6%更正为9.8%。');
section('细胞遗传学风险');
add('标准风险',n(69,207,'C'),n(126,285,'A'),'两研究定义不同；分母分别207、285。',true);
add('高风险（各研究原定义）',n(123,207,'C'),n(104,285,'A'),'CARTITUDE-4包含gain/amp(1q)；MajesTEC-3不包含。',true);
add('高风险：统一三项异常口径',n(73,207,'C'),n(104,285,'A'),'del(17p)、t(4;14)、t(14;16)任一异常；不计gain/amp(1q)。',true);
add('gain/amp(1q)',n(89,207,'C'),missing,'MajesTEC-3所核资料未单列。',true);
add('del(17p)',n(49,207,'C'),n(61,285,'A'),'',true);
add('t(4;14)',n(30,207,'C'),n(47,285,'A'),'',true);
add('t(14;16)',n(3,207,'C'),n(13,285,'A'),'异常可重叠，三个单项不能直接相加。',true);
add('检测集中未确定/缺失',n(15,207,'C'),n(55,285,'A'),'不含未进入上述检测分母者。',true);
add('未进入细胞遗传学检测分母（人）',t(1,'C'),t(6,'A'),'分别为208−207、291−285；勿与上一行混淆。',true);
add('肿瘤BCMA抗原表达 ≥50%',n(141,208,'C'),missing);
section('既往治疗线数');
add('1线',n(68,208,'C'),n(108,291,'A'),'',true);
add('2线',n(83,208,'C'),n(134,291,'A'),'MajesTEC-3附录可分别披露2线及3线。',true);
add('3线',n(57,208,'C'),n(49,291,'A'),'',true);
section('药物暴露情况');
add('anti-CD38抗体',n(53,208,'C'),n(15,291,'A'),'',true);
add('免疫调节剂',n(208,208,'C'),n(291,291,'A'),'',true);
add('蛋白酶体抑制剂',n(208,208,'C'),n(290,291,'A'),'',true);
add('三类药物暴露',n(53,208,'C'),missing,'三类：PI、IMiD和anti-CD38抗体；MajesTEC-3未单列。',true);
add('五药暴露',n(14,208,'C'),missing,'至少2种PI、2种IMiD及1种anti-CD38抗体。',true);
section('耐药情况');
add('来那度胺 Lenalidomide',n(208,208,'C'),n(240,291,'A'),'',true);
add('泊马度胺 Pomalidomide',n(8,208,'C'),t('未核实','A'),'截图2.4%未获本次正文/表S3支持，不据此填数。',true);
add('硼替佐米 Bortezomib',n(55,208,'C'),missing,'MajesTEC-3的40.2%属于任一PI耐药，见“任一PI”行。',true);
add('卡非佐米 Carfilzomib',n(51,208,'C'),missing,'',true);
add('伊沙佐米 Ixazomib',n(15,208,'C'),missing,'',true);
add('任一蛋白酶体抑制剂（PI）',n(103,208,'L'),n(117,291,'A'),'',true);
add('任一免疫调节剂（IMiD）',n(208,208,'C'),n(247,291,'A'),'CARTITUDE-4全体来那度胺耐药，因此该类耐药为100%。',true);
add('anti-CD38抗体',n(50,208,'C'),t('入组标准排除','P'),'MajesTEC-3排除anti-CD38耐药；不将入排条件当作已报告计数。',true);
add('三类耐药',n(30,208,'C'),missing,'PI、IMiD及anti-CD38各至少一种耐药。',true);
add('五药耐药',n(2,208,'C'),missing,'所核资料未单列不等于0。',true);
add('核对日期',t('2026-09-17','C'),t('2026-09-17','A'),'本页核对基线数据；原文件疗效汇总保留原样，未作为本次结论。');
s.getRange('A1:D1').values=[['指标','CARTITUDE-4','MajesTEC-3','备注']];
q.getRange('A1:I1').values=[['对比表单元格','研究','指标','人数/分子','分母','原始值或说明','来源位置','来源链接','核对日期']];
let sr=2;
for(let i=0;i<rows.length;i++){
 const r=i+2, item=rows[i];
 s.getCell(r-1,0).values=[[item.label]];
 if(item.section)continue;
 s.getCell(r-1,3).values=[[item.note]];
 for(let j=0;j<2;j++){
  const v=j===0?item.c:item.m, address=`${j===0?'B':'C'}${r}`, source=S[v.k];
  q.getRange(`A${sr}:I${sr}`).values=[[address,j===0?'CARTITUDE-4':'MajesTEC-3',item.label,v.a??null,v.b??null,v.v??`${v.a}/${v.b}`,source[0],source[1],'2026-09-17']];
  q.getRange(`H${sr}`).formulas=[[`=HYPERLINK("${source[1]}","${source[1]}")`]];
  if(v.a!==undefined){s.getRange(address).formulas=[[`='基线来源'!D${sr}/'基线来源'!E${sr}`]]; s.getRange(address).setNumberFormat('0.0%');}
  else s.getRange(address).formulas=[[`='基线来源'!F${sr}`]];
  sr++;
 }
}
const last=rows.length+1;
const grid=s.getRange(`A1:D${last}`);
grid.format={font:{name:'Songti SC',size:11,color:'#111111'},fill:'#FFFFFF',rowHeight:24,verticalAlignment:'center',wrapText:true,borders:{preset:'all',style:'thin',color:'#555555'}};
s.getRange(`A1:A${last}`).format.columnWidth=43;
s.getRange(`B1:C${last}`).format.columnWidth=31;
s.getRange(`D1:D${last}`).format.columnWidth=68;
s.getRange(`B2:C${last}`).format.horizontalAlignment='right';
s.getRange('A1:D1').format.font={name:'Arial',bold:true,size:12};
s.getRange('A1:D1').format.horizontalAlignment='center';
s.getRange('A1:D1').format.rowHeight=30;
for(let i=0;i<rows.length;i++){
 const r=i+2,item=rows[i];
 if(item.section){s.getRange(`A${r}:D${r}`).format.font.bold=true;s.getRange(`A${r}:D${r}`).format.rowHeight=26;}
 else {
  s.getRange(`A${r}`).format.font.bold=!item.sub;
  if(item.sub)s.getRange(`A${r}`).format.horizontalAlignment='right';
  const textLen=[item.label.length,item.note.length,item.c?.v?.toString().length??0,item.m?.v?.toString().length??0];
  if(textLen[1]>34||textLen[0]>20||textLen[2]>23||textLen[3]>23)s.getRange(`A${r}:D${r}`).format.rowHeight=38;
 }
}
s.showGridLines=false;s.freezePanes.freezeRows(1);s.freezePanes.freezeColumns(1);
const qr=q.getRange(`A1:I${sr-1}`);
qr.format={font:{name:'Arial',size:10},fill:'#FFFFFF',wrapText:true,verticalAlignment:'center',rowHeight:42,borders:{preset:'all',style:'thin',color:'#BBBBBB'}};
q.getRange(`A1:B${sr-1}`).format.columnWidth=18;
q.getRange(`C1:C${sr-1}`).format.columnWidth=38;
q.getRange(`D1:E${sr-1}`).format.columnWidth=10;
q.getRange(`F1:F${sr-1}`).format.columnWidth=33;
q.getRange(`G1:G${sr-1}`).format.columnWidth=44;
q.getRange(`H1:H${sr-1}`).format.columnWidth=70;
q.getRange(`I1:I${sr-1}`).format.columnWidth=14;
q.getRange('A1:I1').format.font.bold=true;q.showGridLines=false;q.freezePanes.freezeRows(1);
w.recalculate();
const findRow=label=>rows.findIndex(r=>r.label===label)+2;
assert(Math.abs(s.getRange(`C${findRow('骨髓浆细胞比例 ≥60%')}`).values[0][0]-28/286)<1e-10);
assert(Math.abs(s.getRange(`B${findRow('其他（排除未提供及未知）')}`).values[0][0]-1/208)<1e-10);
console.log((await w.inspect({kind:'table',range:'基线对比!A1:D7',include:'values,formulas',tableMaxRows:7,tableMaxCols:4,maxChars:2500})).ndjson);
console.log((await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!|#SPILL!',options:{useRegex:true,maxResults:20},maxChars:1000})).ndjson);
for (const [name,range,file] of [['基线对比','A1:D23','top'],['基线对比',`A24:D${last}`,'bottom'],['基线来源','A1:I6','sources']]){
 const p=await w.render({sheetName:name,range,scale:1.5,format:'png'});
 await fs.writeFile(`${dir}/${file}.png`,new Uint8Array(await p.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(w)).save(`${dir}/Carvykti_基线对比整理.xlsx`);
await fs.writeFile(`${dir}/row-map.json`,JSON.stringify(rows.map((x,i)=>({row:i+2,label:x.label})),null,2));
console.log(JSON.stringify({rows:last,sourceRows:sr-1}));

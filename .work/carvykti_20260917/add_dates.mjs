// ai coding: 核对全研究起止日期并修复来源链接缓存与标题显示 2026/09/17: 16:49
import fs from 'node:fs/promises';
import assert from 'node:assert/strict';
import {FileBlob,SpreadsheetFile} from '@oai/artifact-tool';
const dir='/Users/zendu/Documents/Invest/outputs/carvykti_20260917';
const path=`${dir}/Carvykti_基线对比整理.xlsx`;
const w=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const data=JSON.parse(await fs.readFile('/Users/zendu/Documents/Invest/.work/carvykti_20260917/dates.json','utf8'));
const order=['NCT03090659','NCT03548207','NCT03758417','NCT04133636','NCT04566419','NCT04181827','NCT04923893','NCT05257083','NCT03145181','NCT04557098','NCT04722146','NCT05083169','NCT05243797','NCT05695508','NCT05552222','NCT05572515','NCT03399799','NCT04634552','NCT04108195','NCT05050097','NCT04586426','NCT05455320','NCT05461209','NCT06208150'];
assert.equal(new Set(data.map(x=>x.nct)).size,24);
assert.deepEqual(new Set(order),new Set(data.map(x=>x.nct)));
assert(data.every(x=>!x.error));
const s=w.worksheets.getItem('全部临床起止日期');
s.getRange('A1:L1').unmerge();s.getRange('A2:L2').unmerge();
s.getRange('A1:J1').merge();s.getRange('A1').values=[['全部临床研究起止日期｜核对日 2026-09-17']];
s.getRange('A2:J2').merge();s.getRange('A2').values=[['结束日期采用注册库 Study Completion，包含随访；另列 Primary Completion。与论文患者入组窗口、结果发表日期不同。预计日期不表示已完成；仅披露月份的日期保留月精度。']];
s.getRange('A4:L4').values=[['研究/登记队列','注册号','研究开始日期','开始类型','研究结束日期','结束类型','主要完成日期','主要完成类型','注册状态','备注','注册最后更新','来源（ClinicalTrials.gov）']];
const states={ACTIVE_NOT_RECRUITING:'进行中，不再招募',RECRUITING:'招募中',UNKNOWN:'状态未知',COMPLETED:'已完成',TERMINATED:'已终止',WITHDRAWN:'已撤回'};
const nice={NCT04133636:'CARTITUDE-2（含A/B/D）',NCT03145181:'MajesTEC-1（I/II期）',NCT04557098:'MajesTEC-1（II期扩展）',NCT04722146:'MajesTEC-2',NCT05695508:'MajesTEC-5 / HD10',NCT03399799:'MonumenTAL-1（早期登记）',NCT04634552:'MonumenTAL-1（II期登记）'};
const note={
 NCT03090659:'预计结束日已过；注册最后更新2023-06-12，状态UNKNOWN，未确认实际结束。',
 NCT03548207:'本注册研究已完成；后续长期随访或发表更新不等同于本登记的结束日期。',
 NCT03758417:'登记状态为TERMINATED（已终止），不能表述为正常完成。',
 NCT04133636:'日期属于整个多队列研究，不是A/B/D各队列独立日期。',
 NCT04566419:'原表注册号对应SAMURAI术后氧疗研究，非CARTITUDE-3；按名称检索无匹配，日期待核实。',
 NCT04181827:'注册开始2020-06-12；论文随机入组2020-07-10至2021-11-17，口径不同。',
 NCT05083169:'注册开始2021-10-14；论文随机入组2021-10-22至2023-09-29，口径不同。',
 NCT05257083:'主要完成与研究结束仅披露到月份，未推定具体日。',
 NCT05243797:'主要完成与研究结束仅披露到月份，未推定具体日。',
 NCT05461209:'已撤回，实际入组0人（商业决定）。注册仍列开始/主要完成为实际及旧预计结束日，字段有冲突，不能视为真实开展/完成。'
};
const display=[];
for(let i=0;i<order.length;i++){
 const d=data.find(x=>x.nct===order[i]),r=i+5,bad=d.nct==='NCT04566419';
 const vals=[nice[d.nct]??d.name,d.nct,bad?'待核实':d.start.date,bad?'不适用':(d.start.type==='ACTUAL'?'实际':'预计'),bad?'待核实':d.end.date,bad?'不适用':(d.end.type==='ACTUAL'?'实际':'预计'),bad?'待核实':d.primary.date,bad?'不适用':(d.primary.type==='ACTUAL'?'实际':'预计'),bad?'注册号不匹配':states[d.status]??d.status,note[d.nct]??'',d.updated,d.url];
 s.getRange(`A${r}:L${r}`).values=[vals];
 for(const c of [2,4,6,10]){
  const v=vals[c];
  if(/^\d{4}-\d{2}-\d{2}$/.test(v)){s.getCell(r-1,c).values=[[new Date(`${v}T00:00:00Z`)]];s.getCell(r-1,c).setNumberFormat('yyyy-mm-dd');}
 }
 s.getRange(`L${r}`).values=[[d.url]];
 display.push({name:vals[0],nct:d.nct,start:vals[2],end:vals[4],type:vals[5],status:vals[8],url:d.url});
}
s.getRange('A1:L28').format.font={name:'Arial',size:11,color:'#111111'};
s.getRange('A1:L28').format.verticalAlignment='center';
s.getRange('A1:L28').format.wrapText=true;
s.getRange('A4:L28').format.borders={preset:'all',style:'thin',color:'#777777'};
s.getRange('A4:L4').format.font.bold=true;s.getRange('A4:L4').format.horizontalAlignment='center';
s.getRange('A1').format.font={name:'Arial',size:15,bold:true};
s.getRange('A1:L1').format.rowHeight=30;s.getRange('A2:L2').format.rowHeight=34;
s.getRange('A4:L28').format.rowHeight=58;
for(const [c,width] of [['A',33],['B',18],['C',16],['D',10],['E',16],['F',10],['G',16],['H',14],['I',24],['J',74],['K',18],['L',27]])s.getRange(`${c}4:${c}28`).format.columnWidth=width;
s.getRange('C5:H28').format.horizontalAlignment='center';
for(const nct of ['NCT04566419','NCT05461209','NCT03090659']){
 const r=order.indexOf(nct)+5;
 s.getRange(`J${r}`).format.font.color='#9C3F00';
 if(nct==='NCT05461209')s.getRange(`A${r}:L${r}`).format.rowHeight=86;
}
s.showGridLines=false;s.freezePanes.freezeRows(4);s.freezePanes.freezeColumns(2);
const qs=w.worksheets.getItem('基线来源');
for(let r=2;r<=97;r++){
 const f=qs.getRange(`H${r}`).formulas[0][0];
 if(f?.startsWith('=HYPERLINK('))qs.getRange(`H${r}`).values=[[f.match(/HYPERLINK\("([^"]+)"/)[1]]];
}
w.recalculate();
console.log((await w.inspect({kind:'table',range:'全部临床起止日期!A5:I7',tableMaxRows:3,tableMaxCols:9,maxChars:1800})).ndjson);
console.log((await w.inspect({kind:'match',searchTerm:'#REF!|#DIV/0!|#VALUE!|#NAME\\?|#NUM!',options:{useRegex:true,maxResults:20},maxChars:1000})).ndjson);
for(const [range,file] of [['A1:J16','dates-top'],['A17:L28','dates-bottom']]){
 const p=await w.render({sheetName:s.name,range,scale:1.4,format:'png'});
 await fs.writeFile(`${dir}/${file}.png`,new Uint8Array(await p.arrayBuffer()));
}
await (await SpreadsheetFile.exportXlsx(w)).save(path);
await fs.writeFile('/Users/zendu/Documents/Invest/.work/carvykti_20260917/date-display.json',JSON.stringify(display,null,2));
console.log('Added 24 registration records; 1 mismatched study kept unresolved.');

// ai coding: 检查原始临床工作簿结构并生成整理前预览 2026/09/17: 16:36
import fs from 'node:fs/promises';
import {FileBlob, SpreadsheetFile} from '@oai/artifact-tool';
const w=await SpreadsheetFile.importXlsx(await FileBlob.load('/Users/zendu/Documents/Invest/医药/临床/Carvykti.xlsx'));
console.log((await w.inspect({kind:'workbook,sheet',maxChars:2500})).ndjson);
const p=await w.render({sheetName:'三期临床',range:'A1:F4',scale:1,format:'png'});
await fs.writeFile('/Users/zendu/Documents/Invest/.work/carvykti_20260917/before.png',new Uint8Array(await p.arrayBuffer()));

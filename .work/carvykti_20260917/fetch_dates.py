# ai coding: 从临床注册库读取全部研究起止日期并保留实际预计类型和原始响应 2026/09/17: 16:46
import json,re,urllib.request,concurrent.futures
from pathlib import Path
import openpyxl
base=Path('/Users/zendu/Documents/Invest/.work/carvykti_20260917')
wb=openpyxl.load_workbook('/Users/zendu/Documents/Invest/医药/临床/Carvykti.xlsx')
studies={}
for name in ['早期临床','二期临床','三期临床','已读出数据']:
    for row in list(wb[name].values)[1:]:
        for nct in re.findall(r'NCT\d+',str(row[3])):
            studies.setdefault(nct,{'name':row[2],'drug':row[1],'locations':[]})['locations'].append(name)
def fetch(item):
    nct,meta=item
    url='https://clinicaltrials.gov/api/v2/studies/'+nct
    try:
        with urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=35) as r: raw=r.read()
        (base/(nct+'.json')).write_bytes(raw)
        p=json.loads(raw)['protocolSection']; st=p['statusModule']; identity=p['identificationModule']
        return dict(meta,nct=nct,title=identity.get('briefTitle'),officialTitle=identity.get('officialTitle'),acronym=identity.get('acronym'),start=st.get('startDateStruct'),primary=st.get('primaryCompletionDateStruct'),end=st.get('completionDateStruct'),status=st.get('overallStatus'),updated=st.get('lastUpdatePostDateStruct',{}).get('date'),url='https://clinicaltrials.gov/study/'+nct)
    except Exception as e:return dict(meta,nct=nct,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool: out=list(pool.map(fetch,studies.items()))
(base/'dates.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
for r in out:print(json.dumps(r,ensure_ascii=False))

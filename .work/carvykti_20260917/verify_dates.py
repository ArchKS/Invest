# ai coding: 验证全部日期覆盖和原表完整性并恢复原生来源超链接及首页顺序 2026/09/17: 16:50
from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
from lxml import etree
import json,openpyxl,posixpath
p=Path('/Users/zendu/Documents/Invest/outputs/carvykti_20260917/Carvykti_基线对比整理.xlsx')
wb=openpyxl.load_workbook(p)
ns='http://schemas.openxmlformats.org/spreadsheetml/2006/main'
rn='http://schemas.openxmlformats.org/officeDocument/2006/relationships'
pn='http://schemas.openxmlformats.org/package/2006/relationships'
with ZipFile(p) as z:entries={n:z.read(n) for n in z.namelist()}
root=etree.fromstring(entries['xl/workbook.xml'])
rels=etree.fromstring(entries['xl/_rels/workbook.xml.rels'])
targets={r.get('Id'):r.get('Target') for r in rels}
sheets=root.find('{'+ns+'}sheets')
for name,col,first,last in [('全部临床起止日期','L',5,28),('基线来源','H',2,97)]:
    el=next(x for x in sheets if x.get('name')==name)
    target=targets[el.get('{'+rn+'}id')]
    path=target.lstrip('/') if target.startswith('/') else posixpath.normpath('xl/'+target)
    xml=etree.fromstring(entries[path])
    old=xml.find('{'+ns+'}hyperlinks')
    if old is not None:xml.remove(old)
    links=etree.Element('{'+ns+'}hyperlinks')
    relpath=posixpath.dirname(path)+'/_rels/'+posixpath.basename(path)+'.rels'
    rr=etree.fromstring(entries[relpath]) if relpath in entries else etree.Element('{'+pn+'}Relationships',nsmap={None:pn})
    for r in range(first,last+1):
        address=f'{col}{r}';url=wb[name][address].value;rid=f'clinicalSource{r}'
        etree.SubElement(links,'{'+ns+'}hyperlink',ref=address,attrib={'{'+rn+'}id':rid})
        etree.SubElement(rr,'{'+pn+'}Relationship',Id=rid,Type=rn+'/hyperlink',Target=url,TargetMode='External')
    following={'printOptions','pageMargins','pageSetup','headerFooter','rowBreaks','colBreaks','customProperties','cellWatches','ignoredErrors','smartTags','drawing','legacyDrawing','tableParts','extLst'}
    index=next((i for i,e in enumerate(xml) if etree.QName(e).localname in following),len(xml))
    xml.insert(index,links)
    entries[path]=etree.tostring(xml,xml_declaration=True,encoding='UTF-8',standalone=True)
    entries[relpath]=etree.tostring(rr,xml_declaration=True,encoding='UTF-8',standalone=True)
old=list(sheets);sheets[:]=[x for x in old if x.get('name')=='全部临床起止日期']+[x for x in old if x.get('name')!='全部临床起止日期']
for v in root.findall('{'+ns+'}bookViews/{'+ns+'}workbookView'):v.set('activeTab','0');v.set('firstSheet','0')
entries['xl/workbook.xml']=etree.tostring(root,xml_declaration=True,encoding='UTF-8',standalone=True)
with ZipFile(p,'w',ZIP_DEFLATED) as z:
    for name,data in entries.items():z.writestr(name,data)
out=openpyxl.load_workbook(p);cached=openpyxl.load_workbook(p,data_only=True)
orig=openpyxl.load_workbook('/Users/zendu/Documents/Invest/医药/临床/Carvykti.xlsx')
for sheet in orig:
    for row in sheet:
        for c in row:
            d=out[sheet.title][c.coordinate]
            assert c.value==d.value,(sheet.title,c.coordinate)
            if c.hyperlink:assert d.hyperlink and c.hyperlink.target==d.hyperlink.target
raw={x['nct']:x for x in json.load(open('/Users/zendu/Documents/Invest/.work/carvykti_20260917/dates.json'))}
s=out['全部临床起止日期'];seen=set()
for r in range(5,29):
    nct=s.cell(r,2).value;seen.add(nct)
    assert s.cell(r,12).hyperlink.target==raw[nct]['url']
    if nct=='NCT04566419':assert s.cell(r,3).value=='待核实';continue
    for col,key in [(3,'start'),(5,'end'),(7,'primary')]:
        v=s.cell(r,col).value
        actual=v.strftime('%Y-%m-%d') if hasattr(v,'strftime') else v
        assert actual==raw[nct][key]['date'],(nct,key,actual)
assert seen==set(raw)
assert s.freeze_panes=='C5'
assert abs(cached['基线对比']['C23'].value-28/286)<1e-10
assert out.sheetnames[0]=='全部临床起止日期'
print('PASS：24/24注册号覆盖；23项日期与注册库相符，1项错配留空；原7表与73个链接保留。')

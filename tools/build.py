import csv,json,re,pathlib
root=pathlib.Path(__file__).resolve().parents[1]
source=pathlib.Path(r'C:\Users\lukec\.codex\attachments\63e65072-7796-4d00-bf20-f4c85e4cd1e8\Pasted text.txt')
rows=list(csv.reader(source.read_text(encoding='utf-8-sig').splitlines(),delimiter='\t'))
events=[]; residences=[]; collecting=False; year=None; theme='Aspirations'; fragments=[]
themes={'Narratives':'Life themes','High School Topics':'School subjects','Illness and Injury':'Illness and injury','Places Lived':'Residences','Computer Games':'Computer games','Virtual Reality':'Virtual reality','Youtube':'YouTube','Twitter':'Twitter'}
for n,row in enumerate(rows[2:],3):
 row+=['']*(7-len(row)); lens,other,title,note,date,d1,d2=[x.strip() for x in row[:7]]
 if other in themes: theme=themes[other]
 elif other and theme!='Residences': fragments.append(dict(id=f'fragment-{n}',title=other,type='memory',year=None,date='Dates to confirm',dateBasis='Independent spreadsheet list; no date or event association supplied',note='',theme=theme,sourceRow=n,originalFields=row[:7]))
 if other=='Places Lived': collecting=True
 elif collecting and other=='Computer Games': collecting=False
 elif collecting and other: residences.append(dict(id=f'home-{n}',title=other,type='residence',year=None,note='Listed under Places Lived. Residence dates have not been supplied.',sourceRow=n))
 if not title: continue
 match=re.match(r'^(19\d\d|20\d\d)(?: NYD)?$',title)
 if match: year=int(match[1]); continue
 if re.fullmatch(r'\d+\??',title):
  if not note and not date and not d1 and not d2: continue
  title='Age '+title+' marker'
 kind='move' if re.search(r'move|return|left KG',title,re.I) else 'journey' if re.search(r'visit|trip|singapore|thailand|nepal|sabbah|sippidan|bournemouth|glastonbury|stonehenge|leeds|lumbini|golden temple|golden mount|dharamsala|amritsar|delhi|hyderabad',title,re.I) else 'memory'
 exact=title=='My Live Birth'
 eventyear=1982 if exact else 1983 if title.startswith('1983 NYD') else year
 events.append(dict(id=f'memory-{n}',title=title,type=kind,year=eventyear,early=year is None,date='3 December 1982' if exact else f'Around {eventyear}' if eventyear else 'Childhood; dates to confirm',dateBasis='Date supplied by Luke' if exact else 'Year appears in the entry' if title.startswith('1983 NYD') else 'Candidate year from spreadsheet sequence; needs confirmation' if eventyear else 'Before the 1995 marker; exact year unknown',note=note,originalDate=date,dateRange=[d1,d2],sourceRow=n,originalFields=row[:7]))
for record in events:
 if record['title']=='The Next Great Conversation':
  record.update(year=2013,endYear=2018,date='2013 - 2018',aliases=['iChooseinfinity'],periodsConfirmed=True,dateBasis='Luke confirmed this row has three active periods: 2013–2018, 2020 and 2021–2023.',periods=[{'start':2013,'end':2018},{'start':2020,'end':2020},{'start':2021,'end':2023}],timestamp='ichooseinfinity.com')
data=dict(title="Luke’s lifetime memory map",events=events,residences=residences,fragments=fragments,source='Luke’s pasted life spreadsheet',endYear=2026)
corrections=root/'data'/'author-corrections.json'
if corrections.exists():
 imported=json.loads(corrections.read_text(encoding='utf-8-sig'))
 data=imported['data']
 for collection in ['events','residences','fragments']:
  data[collection]=[{**record,**imported.get('edits',{}).get(record['id'],{})} for record in data.get(collection,[]) if record['id'] not in imported.get('removed',[])]
 data['events']+=imported.get('extras',[])
 data['savedNotes']=imported.get('notes',{})
 data['revision']='Luke-corrected-export-2026-10-01'
uk_period=False
for record in data['events']:
 if record['title']=='Move to England': uk_period=True
 record['ukPeriod']=uk_period
 if record['title']=='Move Home': uk_period=False
current=json.loads((root/'data'/'memories.json').read_text(encoding='utf-8'))
if current.get('anonymousBirths'):
 data['anonymousBirths']=current['anonymousBirths']
 for record in data['events']:
  for key in ['note','timestamp']:
   if re.fullmatch(r'(?:male|female) born\s*|2 more IVF kids sometime',record.get(key,'') or '',re.I): record[key]=''
  if record.get('originalFields'):
   record['originalFields']=['' if re.fullmatch(r'(?:male|female) born\s*|2 more IVF kids sometime',str(v),re.I) else v for v in record['originalFields']]
(root/'data'/'memories.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
(root/'data'/'memories.js').write_text('window.MEMORY_DATA='+json.dumps(data,ensure_ascii=False)+';',encoding='utf-8')
(root/'data'/'source-rows.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'{len(events)} life events; {len(residences)} residence entries; {len(fragments)} independent list fragments; {sum(x["early"] for x in events)} early memories')


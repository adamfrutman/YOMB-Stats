# Reads every CSV in data/ and writes data.json for the website.
import csv, re, json, glob, os
KEEP=['GP','PA','AB','H','1B','2B','3B','HR','RBI','R','BB','SO','HBP','SAC','SF','ROE','FC','SB','CS','QAB','XBH','TB']
rows_out=[]; games={}
allfiles=[os.path.join(d,n) for d,_,ns in os.walk('.') if '.git' not in d.split(os.sep) for n in ns]
print('ALL FILES IN REPO:',sorted(allfiles))
files=sorted(p[2:] for p in allfiles if p.lower().endswith('.csv'))
print('CSV files found:',files)
for f in files:
    m=re.match(r'(.+?)_(Spring|Summer|Fall|Winter)_(\d{4})',os.path.basename(f))
    if not m: print('SKIPPED (name should look like YOMB_Fall_2025_Stats.csv):',f); continue
    team,season=m.group(1),f"{m.group(2)} {m.group(3)}"
    try:
        rows=list(csv.reader(open(f,encoding='utf-8-sig')))
        h=rows[1][:rows[1].index('IP')]
        for r in rows[2:]:
            if not any(r) or r[0]=='Glossary': continue
            d=dict(zip(h,r))
            if r[0]=='Totals': games[f"{team}|{season}"]=int(d['GP']); continue
            o={'s':season,'t':team,'n':(r[2]+' '+r[1]).strip(),'no':r[0]}
            for k in KEEP: o[k]=int(float(d[k] or 0))
            rows_out.append(o)
    except Exception as e:
        print('SKIPPED (could not read):',f,e)
if not rows_out:
    raise SystemExit('ERROR: no player rows found - leaving data.json unchanged')
json.dump({'rows':rows_out,'games':games},open('data.json','w'),separators=(',',':'))
print(len(rows_out),'player rows from',len(games),'team-seasons')

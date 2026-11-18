"""Build reports/success-matrix.json from applications.csv (one row per application)."""
import csv, json, re
from datetime import date

TODAY = date.today()
EST = {}  # optional: {'url fragment': estimated callback %}
FAMILIES = [  # role families tuned for analyst jobs: edit the names and regexes for your field
    ('Data science / engineering', r'data scien|engineer|developer|sql dev'),
    ('Business / systems analyst', r'business analyst|systems? analyst|business & systems|solutions analyst|technical ba|application|test analyst|support analyst|it support|projects support'),
    ('Marketing / media', r'marketing|media|digital|coordinator|research|journey'),
    ('Commercial / finance', r'commercial|pricing|financ|fp&a|sales|category|procurement|planning|demand|investment|trading|credit|risk|fraud|surveillance|insolvency|account specialist|merchant|transaction'),
    ('Consulting / graduate', r'consult|graduate|intern|program|associate|talent'),
    ('Data / BI / insights', r'data|bi |\bbi\b|business intelligence|insight|reporting|analyst|administrator'),
]

def family(role):
    r = role.lower()
    if not r or r.startswith('('): return 'Role not recorded'
    for name, pat in FAMILIES:
        if re.search(pat, r): return name
    return 'Other'

def outcome(r):
    s = r['stage'].strip().lower()
    if s in ('interview', 'assessment', 'phone-screen', 'offer'): return 'Interview / assessment'
    if s == 'rejected':
        return 'Interviewed, then rejected' if 'interview' in r['notes'].lower() else 'Rejected'
    if s == 'unclear' or 'expired' in r['notes'].lower() or 'ad closed' in r['notes'].lower(): return 'Closed / unclear'
    return 'Waiting'

def band(m):
    try: m = float(m)
    except ValueError: return 'Not scored'
    return '7–10 (strong)' if m >= 7 else '5–6 (partial)' if m >= 5 else '1–4 (stretch)'

def source(s):
    s = s.strip()
    if s == 'email': return 'Self-applied (seen in email)'
    if s.startswith('Indeed'): return 'Indeed'
    if s in ('LinkedIn', 'SEEK'): return s
    return 'Company site / other'

def applied_on(r):
    m = re.search(r'(?:applied|Applied)[^0-9]{0,25}(\d{4}-\d{2}-\d{2})', r['notes'])
    if m: return m.group(1)
    m = re.search(r'(?:applied|Applied)[^0-9]{0,25}(\d{1,2}) (Oct|Nov)', r['notes'])
    if m: return f"2026-{'10' if m.group(2)=='Oct' else '11'}-{int(m.group(1)):02d}"
    return r['date_found']

rows = []
for r in csv.DictReader(open('applications.csv')):
    st = r['stage'].strip().lower()
    if not (r['status'].startswith('applied') or st in ('applied','received','rejected','phone-screen','assessment','interview','offer','unclear')):
        continue
    when = applied_on(r)
    out = outcome(r)
    days = (TODAY - date.fromisoformat(when)).days
    est = next((v for k, v in EST.items() if k in r['url']), None)
    rows.append({
        'applied': when, 'company': r['company'].strip(), 'role': r['role'].strip() or '(not recorded)',
        'family': family(r['role']), 'source': source(r['source']), 'match': band(r['match_score']),
        'outcome': out, 'responded': 'Yes' if out != 'Waiting' else 'No',
        'days_since': days,
        'status_note': ('No reply 14+ days' if out == 'Waiting' and days >= 14 else ''),
        'est_callback_pct': est,
    })
rows.sort(key=lambda x: x["applied"], reverse=True)
for i, r in enumerate(rows, 1): r["id"] = f"A{i:03d}"
json.dump({'rows': rows, 'meta': [
    {'label': 'Built from', 'value': 'job-hunter/applications.csv (rows with status applied or a reply stage)'},
    {'label': 'As of', 'value': str(TODAY)},
    {'label': 'build_success_matrix.py', 'value': open(__file__).read(), 'type': 'code', 'lang': 'python'},
]}, open('reports/success-matrix.json', 'w'), indent=1)

if __name__ == '__main__':
    from collections import Counter
    assert all(r['outcome'] for r in rows) and len(rows) > 100
    print(len(rows), Counter(r['outcome'] for r in rows))
    print(Counter(r['family'] for r in rows))
    print(Counter((r['family'], r['outcome']) for r in rows if r['outcome']!='Waiting'))

import re, xml.etree.ElementTree as ET, email.utils, datetime, html

now = datetime.datetime.now(datetime.timezone.utc)
for f, label in [("tmp/tc.xml", "TechCrunch"), ("tmp/reg.xml", "TheRegister"), ("tmp/hn.xml", "HN")]:
    try:
        data = open(f, encoding="utf-8", errors="replace").read()
        root = ET.fromstring(data)
    except Exception as e:
        print(label, "PARSE-ERR", e)
        continue
    ns = {'a': 'http://www.w3.org/2005/Atom'}
    items = root.findall('.//item')
    if items:
        for it in items[:25]:
            title = (it.findtext('title') or '').strip()
            link = (it.findtext('link') or '').strip()
            date = (it.findtext('pubDate') or '').strip()
            desc = re.sub('<[^>]+>', '', it.findtext('description') or '')
            desc = html.unescape(desc).strip()[:220]
            age = -1
            try:
                dt = email.utils.parsedate_to_datetime(date)
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=datetime.timezone.utc)
                age = (now - dt).total_seconds() / 3600
            except Exception:
                pass
            print("[%s] age=%.1fh | %s\n   %s\n   %s\n" % (label, age, title, link, desc))
    else:
        for e in root.findall('.//a:entry', ns)[:25]:
            t = (e.findtext('a:title', None, ns) or '').strip()
            upd = (e.findtext('a:updated', None, ns) or '').strip()
            link = ''
            for l in e.findall('a:link', ns):
                if l.get('rel') in (None, 'alternate'):
                    link = l.get('href', '')
                    break
            summ = e.findtext('a:summary', None, ns) or e.findtext('a:content', None, ns) or ''
            summ = re.sub('<[^>]+>', '', html.unescape(summ)).strip()[:220]
            age = -1
            if upd:
                try:
                    dt = datetime.datetime.fromisoformat(upd.replace('Z', '+00:00'))
                    age = (now - dt).total_seconds() / 3600
                except Exception:
                    pass
            print("[%s] age=%.1fh | %s\n   %s\n   %s\n" % (label, age, t, link, summ))

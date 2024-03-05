import json

import pyevaljs3

payload = {
        "cursor_score": "", "num": 31, "refresh_type": 1, "note_index": 35, "unread_begin_note_id": "",
        "unread_end_note_id": "", "unread_note_count": 0, "category": "homefeed_recommend", "search_key": "",
        "need_num": 6, "image_formats": ["jpg", "webp", "avif"]
    }

cookie = 'a1=18c0436e5549rvr1aukayp8l2qjpdrh8f3wz3nlc650000328069;web_session=030037a25201ca6f3b3ef31319224af8cd067a;'

code = open("xhs2.js", encoding="utf-8").read()
code += ';return getXS("/api/sns/web/v1/homefeed", %s, "%s");' % (json.dumps(payload), cookie)
xsxt = pyevaljs3.eval_(code, True)
print(xsxt, type(xsxt))

ctx = pyevaljs3.compile_('xhs2.js')
r = ctx.call('getXS', "/api/sns/web/v1/homefeed", payload, cookie)
print(r, type(r))

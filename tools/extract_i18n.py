# -*- coding: utf-8 -*-
"""Extract all I18N.data keys with zh/en values from index.html.

Outputs tools/i18n_reference.txt for translation work.
"""
import io
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "index.html")
DST = os.path.join(ROOT, "tools", "i18n_reference.txt")

html = io.open(SRC, encoding="utf-8").read()

# Line-based parse: I18N.data.XX['key'] = 'value';
pat = re.compile(r"^I18N\.data\.(zh|en|ar)\['([^']+)'\] = '((?:[^']|\\')*)';")
data = {}
order = []
for line in html.splitlines():
    m = pat.match(line.strip())
    if not m:
        continue
    lang, key, val = m.group(1), m.group(2), m.group(3).replace("\\'", "'")
    if key not in data:
        data[key] = {}
        order.append(key)
    data[key][lang] = val

with io.open(DST, "w", encoding="utf-8") as f:
    for key in order:
        f.write("KEY: {}\n".format(key))
        f.write("  zh: {}\n".format(data[key].get("zh", "")))
        f.write("  en: {}\n".format(data[key].get("en", "")))
        f.write("\n")

print("extracted {} keys -> {}".format(len(order), DST))

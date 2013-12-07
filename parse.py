#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess, re, sys, glob

files = glob.glob("raw/*")
rawcsv = open("nsc_projects.raw.csv", "w")
refinecsv = open("nsc_projects.csv", "w")

head = "計劃年度,主持人,執行機關,所屬大學,計劃名稱,執行起迄,核定金額,案別,學門,學門子分類\n"
rawcsv.writelines(head)
refinecsv.writelines(head)

for f in files:
  result = re.search(r"raw/page-(\d+)-([^-]+)-([^-]+)-(\d+)", f)
  if not result: continue
  anbie,shuemen,shuemen2,page = result.groups()
  print("%s %s %s %s"%(anbie, shuemen, shuemen2, page))
  lines = open(f, "r").readlines()
  for line in lines:
    result = re.search(r'\s+<td align="center">(\d+)</td><td align="left">\s*([^<]+)</td><td align="left">(.+?)</td><td align="left"><span id="[^"]+">計畫名稱：</span><span id="[^"]+">(.+?)</span>.+?(\d+/\d+/\d+~\d+/\d+/\d+).+?([0-9,]+)元', line)
    if not result: continue
    
    year,chair,institute,name,date,budget = map(lambda x: re.sub(r'"',"'",re.sub(r",","，",x)), result.groups())
    budget = re.sub(r"[,，]","", budget)
    college_pos = institute.find("大學")
    college = institute[:college_pos] if college_pos > 1 else ""
    authoridx = "%s-%s"%(chair,institute)

    rawcsv.writelines('"%s","%s","%s","%s","%s","%s","%s","%s","%s"\n'%(
      year, chair, institute, name, date, budget, anbie, shuemen, shuemen2
    ))
    refinecsv.writelines('"%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s"\n'%(
      year, chair, authoridx, institute, college, name, date, budget, anbie, shuemen, shuemen2
    ))
rawcsv.close()
refinecsv.close()

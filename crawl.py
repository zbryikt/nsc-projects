#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess, re, sys

shuemen_hash = {
  "E": [
    "E01", "E02", "E03", "E04", "E05", "E06", "E07", "E08", "E09",
    "E10", "E11", "E12", "E13", "E14", "E15", "E16", "E17", "E18",
    "E19", "E20", "E22", "E23", "E24", "E31", "E32", "E33", "E34",
    "E50", "E57", "E59", "E60", "E61", "E70", "E71", "E72", "E80",
    "E88", "E90", "E92", "E93", "E95", "E97", "E98", "E99", "ENE",
  ],
  "B": [
    "B10", "B20", "B30", "B40", "B50", "B60", "B90", "B99", "BN1",
    "BN2", "BN3", "BN4", "BN5", "BN6", "BN7", "BN8", "BN9", "BNE", "BNF",
  ],
  "H": [
    "H01", "H04", "H05", "H06", "H08", "H09", "H11", "H12", "H13",
    "H14", "H15", "H16", "H17", "H19", "H22", "H23", "H24", "H25",
    "H26", "H27", "H28", "H29", "H30", "H31", "H32", "H33", "H34",
    "H35", "H36", "H37", "H38", "H39", "H40", "H41", "H42", "H43",
    "H44", "H45", "H46", "H47", "H48", "H49", "H50", "H51", "H52",
    "H99", "HA2", "HA3", 
  ],
  "M": [
    "M01", "M02", "M03", "M04", "M05", "M06", "M07", "M10", "M11",
    "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M20", "M21",
    "M22", "M80", "M81", "M98", "M99", "MNE",
  ],
  "S": [
    "S10", "S20", "S30", "S40", "S41", "S42", "S43", "S50", "S51",
    "S52", "S53", "S60", "S70", "S90", "S99", "SA0", "SB0", "SBA",
    "SC0", "SD0", "SE0", "SN0", "SN1", "SNB", "SNE", "SNM", "SP0",
    "SSD", "SSK", "SSN", "SSS", "SZ0"
  ],
}

output = open("nsc.csv", "w")
output.writelines("案別,學門,子類,劃年度,主持人,執行機關,計劃名稱,執行起迄,核定金額\n")
all_count = 0
for anbie in xrange(1,5):
  for shuemen in shuemen_hash:
    for shuemen2 in shuemen_hash[shuemen]:
      total_page = 0
      proc = subprocess.Popen("./cmd-%s %d %s %s %d > .tmp"%(shuemen, anbie,shuemen,shuemen2,0),shell=True)
      proc.communicate(None)
      ret = re.search(r'">共(\d+)頁\(',open(".tmp","r").read())
      if not ret:
        print("[WARN] 案別%d 學門%s 子類%s 找不到頁數資訊,略過"%(anbie,shuemen,shuemen2))
        continue
      total_page = int(ret.group(1))
      print("案別%d 學門%s 子類%s 共%d頁"%(anbie, shuemen, shuemen2, total_page))
      total_count = 0
      for page in xrange(0,total_page):
        f = "raw/page-%d-%s-%s-%d"%(anbie,shuemen,shuemen2,page)
        proc = subprocess.Popen("./cmd-%s %d %s %s %d > %s"%(shuemen, anbie,shuemen,shuemen2,page,f),shell=True)
        proc.communicate(None)
        lines = open(f,"r").readlines()
        count = 0
        for line in lines:
          result = re.search(r'\s+<td align="center">(\d+)</td><td align="left">\s*([^<]+)</td><td align="left">(.+?)</td><td align="left"><span id="[^"]+">計畫名稱：</span><span id="[^"]+">(.+?)</span>.+?(\d+/\d+/\d+~\d+/\d+/\d+).+?([0-9,]+)元', line)
          if not result: continue
          dollar = re.sub(",","", result.group(6))
          output.writelines("%d,%s,%s,%s,%s,%s,%s,%s,%s\n"%(
           anbie, shuemen, shuemen2, 
           result.group(1),result.group(2),result.group(3),result.group(4),result.group(5),dollar))
          count+=1
        if count!=200 and page!=total_page-1: print("[WARN] %s 有問題 (趴出%d筆)"%(f,count))
        total_count += count
      print("一共讀出%d筆資料"%total_count)
      all_count += total_count
output.close()
print("爬蟲程式結束, 一共讀出 %d 筆資料, 請查看 ncs.csv 檔確認."%(all_count))

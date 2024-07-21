import json
import re

from Crypto.Util.number import long_to_bytes as l2b
from z3 import *

#====== step 1

f = open("sequel", "r")
data = json.load(f)
f.close()

entries = data["log"]["entries"]

# arr = []

# for entry in entries:
#   if entry["request"]["method"] == "GET":
#     continue
  
#   if entry["request"]["method"] == "POST":
#     # Get query postdata
    # query = entry["request"]["postData"]["text"]
    # content = entry["response"]["content"]
    # time = entry["timings"]["wait"]
    
    # obj = {
    #   "query": query,
    #   "content": content,
    #   "time": time,
    # }
    
#     if time > 2000 and time < 3000:
#         arr.append(obj)

# valid_queries = []
# for entry in entries:
#     if(entry["request"]["method"] == "POST"):
#         query = (entry["request"]['postData']['text'].lower())
#         fast = True
#         if ("else/**/hex(randomblob(1000000000/2))" in query):
#             fast = False
#         if ((fast and int(entry["time"]) < 3000) or ((not fast) and int(entry["time"]) >= 3000)):
#                 query = entry["request"]["postData"]["text"]
#                 content = entry["response"]["content"]
#                 time = entry["time"]

#                 obj = {
#                   "query": query,
#                   "content": content,
#                   "time": time,
#                 }
          
#                 valid_queries.append(obj)

# f = open("hasil4.json", "w")
# f.write(str(valid_queries))
# f.close()

# f = open("hasil2.json", "w")
# json.dump(arr, f)
# f.close()


# ======= step 2

last_like = r"like (('([\w]).*')|[-\d][\d]*)" #case ignore
find_substr = r"substr\(([\w]*),([-\w]*),1\)"
operation = r"[lL][iI][kK][eE] '%.\w%'\)."

# pattern_when = r'[wW][hH][eE][nN].*'
# pattern_then = r'[tT][hH][eE][nN].*'


# substr = r"substr(.*[^\s])"

# data1 = re.findall(pattern_when, str1)[0]
# data2 = re.findall(find_substr, data1, re.IGNORECASE)
# print(data2)

f = open("hasil4.json", "r")
entries = json.load(f)
f.close()

arr = []
arr_content = []
arr_op = []

for entry in entries:
  query = json.loads(entry["query"])
  query = query['query']
  
  # print(query)

  find = re.findall(last_like, query, re.IGNORECASE)
  find1 = find[0][0].replace("'", "")
  arr.append(find1)

  substr = re.findall(find_substr, query, re.IGNORECASE)
  arr_content.append(substr)

  op = re.findall(operation, query, re.IGNORECASE)
  ops = [x[-1] for x in op]
  arr_op.append(ops)

chrs = []

for ele in arr:
  res = ele
  if len(res) > 4:
    try:
      res = l2b(int(res, 16))  # if isinstance(res, str):
    except:
      pass
  
  chrs.append(res)
    
# print(chrs)

s = Solver()

flag = [Int(f'x{i}') for i in range(0, 0x30)]

real_flag = []
likes = ['52', '6888', '6700', '-22', '5201', '106', '121', '-4994', '297000', '922082', '57', '3436', '49', '-28', '6499', '1', '5151', '5252', '2450', '-2', '122', '18', '2453', '100', '4656', '36', '3231', '5200', '3439', '4', '3538', '943', '5579', '3536', '4896', '252', '4', '-5289', '51', '9603', '3825', '3530', '-5003', '39', '505000', '209', '5094', '155', '32', '2499', '97', '45', '2548', '-91', '1200', '4754', '4144', '5555', '150', '107', '3216', '3530', '153', '2', '143', '-26', '-6', '2805', '-108', '201', '3637', '2800', '101']

for idx, content in enumerate(arr_content):
  pos = []
  for c in content:
    t = c[1]
    try:
      pos.append(((int(t))))
    except:
      pos.append(int(t,16))
  
  for x, p in enumerate(pos):
    if p > 0:
      pos[x] -= 1
  
  el = []
  for p in pos:
    el.append(flag[p])
  
  eq_arr = None
  operator = arr_op[idx]
  
  ctr = 0
  for i in range(len(el)):
    if i == 0:
      eq_arr = el[i]
      continue
    
    if operator[ctr] == "*":
      eq_arr = eq_arr * el[i]
    elif operator[ctr] == "+":
      eq_arr = eq_arr + el[i]
    elif operator[ctr] == "%":
      eq_arr = eq_arr % el[i]
    elif operator[ctr] == "-":
      eq_arr = eq_arr - el[i]
    else:
      print(operator[ctr])

    ctr += 1
  
  eq_arr = eq_arr == (int(likes[idx]))
  print(eq_arr)
  s.add(eq_arr)


print(s.check())
# print(s)
import json
import sys

sys.path.append(r"E:\projects\Python\git-proj\melobot")
from melobot import to_cq_arr

d = to_cq_arr(
    "[CQ:image,id=123456,id2=123456.789a]asdjfa;jfajfa[CQ:image,id=asdjf;a;f,id2=asdjf;a;fa;jfadsf];sdjf;asfj[CQ:image,id=asdjf;a;f,id2=asdjf;a;fa;jfadsf]"
)
print(json.dumps(d, ensure_ascii=False, indent=2))

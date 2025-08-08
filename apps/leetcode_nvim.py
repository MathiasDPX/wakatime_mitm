from apps.classes import *
import re

leetcode = App("LeetCode.nvim")

@leetcode.handle("users/current/heartbeats.bulk")
@leetcode.handle("users/current/heartbeats")
def leetcode_change_proj_name(data:dict):
    for entry in data:
        match = re.match(r'\/.+\/\.local\/share\/nvim\/leetcode\/(\d+)\.', entry.get("entity", ""))

        if match:
            id = match.group(1)
            entry["project"] = f"LeetCode {id}"
            print(entry["project"])

    return data
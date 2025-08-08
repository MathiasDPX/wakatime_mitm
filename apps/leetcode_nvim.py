from apps.classes import *
import re

leetcode = App("leetcode-nvim", priority=10)

@leetcode.handle("users/current/heartbeats.bulk")
@leetcode.handle("users/current/heartbeats")
def leetcode_change_proj_name(headers:dict, data):
    if type(data) != list:
        return data

    for entry in data:
        match = re.match(r'\/.+\/\.local\/share\/nvim\/leetcode\/(\d+)\.', entry.get("entity", ""))

        if match:
            id = match.group(1)
            entry["project"] = f"LeetCode {id}"

    return data
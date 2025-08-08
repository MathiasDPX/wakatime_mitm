from apps.leetcode_nvim import leetcode
from apps.auth import app as auth

raw_apps = [leetcode, auth]

apps = sorted(raw_apps, key=lambda v: v.priority)
from apps.leetcode_nvim import leetcode
from apps.auth import app as auth
from apps.test import app as test

raw_apps = [leetcode, auth, test]

apps = sorted(raw_apps, key=lambda v: v.priority)
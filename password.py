import re


def pswrd(str):
    ln = len(str)
    nums = re.findall(r'[0-9]', str)
    S = re.findall(r'[A-Z]', str)
    s = re.findall(r'[a-z]', str)
    count = 0
    for smbl in str:
        if str.count(smbl) > 1:
            count = 1
            break
    if len(nums) * len(S) * len(s) > 0 and ln - len(nums + S + s) + count == 0 and ln > 7:
        return True
    else:
        return False

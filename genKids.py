import argparse
import sys

# 에러 출력 함수
def printError(case, filename):
    {
        # -f 플래그 미사용
        1: lambda: (print("[-] This tool requires a input file; you missed the '-f' flag."), sys.exit(1)),
        # -o 플래그 미사용
        2: lambda: (print("[-] This tool requires an output file; you missed the '-o' flag."), sys.exit(1)),
        # 인자가 2-3개가 아니면 오류
        3: lambda: (print(f'[-] This tool requires two or three string arguments in {filename}.'), sys.exit(1))
    }.get(case, lambda: None)()

# 인자 핸들링
def getArgs():
    parser = argparse.ArgumentParser(description="username generator v0.3.1")
    parser.add_argument("-f", "--file", required=True, help="username file")
    parser.add_argument("-o", "--output", required=True, help="output file")
    parser.add_argument("-n", "--number", help="extra number", default=None)
    parser.add_argument("-d", "--domain", help="domain name", default=None) 
    args = parser.parse_args()
    return args.file, args.output, args.number, args.domain

# 사용자가 사용한 인자 검증
def checkOptions(userfile, outputfile):
    # userfile, outputfile은 필수적으로 들어가야함
    if userfile is None:
        printError(1, userfile)
    if outputfile is None:
        printError(2, userfile)

    with open(userfile, "r", encoding="utf-8") as f:
        lines = [line.strip().split() for line in f if line.strip()]

    for parts in lines:
        if not (2 <= len(parts) <= 3):
            printError(3, userfile)

def makeUserList(userfile):
    with open(userfile, "r", encoding="utf-8") as f:
        return [line.strip().split() for line in f if line.strip()]

def makeWordlist(argument):
    res = []
    if len(argument) == 2:
        first, last = argument[0], argument[1]
        res.extend([
            first + last,
            first + "." + last,
            first + "." + last[0],
            first[0] + last,
            first[0] + "." + last,
        ])
    elif len(argument) == 3:
        first, middle, last = argument[0], argument[1], argument[2]
        res.extend([
            first + middle + last,
            first + "." + middle + last,
            middle + last + first,
            middle + last + "." + first,
            first + middle[0] + last[0],
            first + "." + middle[0] + last[0],
            middle[0] + last[0] + first,
            middle[0] + last[0] + "." + first,
            first[0] + middle[0] + last[0],
            first[0] + "." + middle[0] + last[0],
            middle[0] + last[0] + first[0],
            middle[0] + last[0] + "." + first[0],
            first[0] + middle + last,
            first[0] + "." + middle + last,
            middle + last + first[0],
            middle + last + "." + first[0],
            middle + last,
        ])
    return res

def getWordlistFromUserList(userlist):
    res = []
    for user in userlist:
        res.extend(makeWordlist(user)) 
    return res

def addNumber(items, number):
    res = []
    number = str(number)
    for item in items:
        res.append(item + number)
    return res

def addDomain(items, domain):
    res = []
    for item in items:
        res.append(item + '@' + domain)
    return res

def saveResult(outputfile, res):
    seen, unique = set(), []
    for s in res:
        if s not in seen:
            seen.add(s)
            unique.append(s)

    with open(outputfile, "w", encoding="utf-8") as f:
        f.write("\n".join(unique))

    print("[*] userId generator v0.3.1 - Copyright 2025 All rights reserved by mick3y")
    print("[+] Success generating username list")
    print(f"[+] output file : {outputfile}")

# 메인 함수
def main():
    userfile, outputfile, number, domain = getArgs()
    checkOptions(userfile, outputfile)
    namelist = makeUserList(userfile)
    res = getWordlistFromUserList(namelist)

    if number is not None:
        res = res + addNumber(res, number)
    if domain is not None:
        res = addDomain(res, domain)

    saveResult(outputfile, res)

if __name__ == "__main__":
    main()

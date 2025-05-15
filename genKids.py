import argparse

parser = argparse.ArgumentParser(description="username generator v0.1",epilog="example:\n genKids.py -f users.txt -o enumeration.txt -d example.com",)
parser.add_argument("-f", "--file", required=True, help="username file")
parser.add_argument("-o", "--output", required=True, help="output file")
parser.add_argument("-n", "--number", help="extra number", default=None)
parser.add_argument("-d", "--domain", help="domain name", default=None)
parser.add_argument("-p", "--phone", help="phone number", action="store_true")
args = parser.parse_args()

userFile = args.file
outputFile = args.output
number = args.number
domain = args.domain

def argumentsCheck():
    with open(userFile, 'r') as file:
        userInputFile = [line.strip().split() for line in file.readlines()]
        
    for idx in range(len(userInputFile)):
        if len(userInputFile[idx]) == 1:
            print(f'[-] This tool requires at least two arguments in {userFile}, But there are only one argument.')
            exit()
        if len(userInputFile[idx]) == 2:
            intCnt = 0
            for item in userInputFile[idx]:
                try:
                    int(item)
                    intCnt += 1
                except ValueError:
                    continue
            if intCnt >= 1:
                print(f'[-] This tool requires at least two string arguments in {userFile}, But there is only one string argument.')
                exit()
        if len(userInputFile[idx]) == 3:
            intCnt = 0
            for item in userInputFile[idx]:
                try:
                    int(item)
                    intCnt += 1
                except ValueError:
                    continue
            if intCnt >= 2:
                print(f'[-] This tool requires at least two string arguments in {userFile}, But there is only one string argument.')
                exit()
        if len(userInputFile[idx]) == 4:
            if not args.phone:
                print(f"[-] Too many arguments in {userFile}. Did you miss a flag '-p' ?")
                exit()
            

def generateNames():
    res = []
    with open(userFile, 'r') as file:
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                first, middle, last = parts[0], parts[1], parts[2]
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
                    middle + last
                ])
            elif len(parts) == 2:
                first, last = parts[0], parts[1]
                res.extend([
                    first + last,
                    first + "." + last[0],
                    first[0] + last,
                    first[0] + "." + last,
                    first + "." + last[0]
                ])
            elif len(parts) == 4:
                first, middle, last, phone = parts[0], parts[1], parts[2], parts[3]
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
                    first + middle + last + phone,
                    first + "." + middle + last + phone,
                    middle + last + first + phone,
                    middle + last + "." + first + phone,
                    first + middle[0] + last[0] + phone,
                    first + "." + middle[0] + last[0] + phone,
                    middle[0] + last[0] + first + phone,
                    middle[0] + last[0] + "." + first + phone,
                    first[0] + middle[0] + last[0] + phone,
                    first[0] + "." + middle[0] + last[0] + phone,
                    middle[0] + last[0] + first[0] + phone,
                    middle[0] + last[0] + "." + first[0] + phone,
                    first[0] + middle + last + phone,
                    first[0] + "." + middle + last + phone,
                    middle + last + first[0] + phone,
                    middle + last + "." + first[0] + phone,
                    middle + last + phone
                ])
    return res

def appendNumber(res, number):
    newRes = []
    for curInfo in res:
        newRes.append(curInfo + number)
    return newRes

def appendDomain(res, domain):
    newRes = []
    for curInfo in res:
        newRes.append(curInfo + '@' + domain)
    return newRes

def main():
    argumentsCheck()
    res = generateNames()
    
    if number is None:
        if domain is not None:
            res = appendDomain(res, domain)
    else:
        if domain is not None:
            res = appendNumber(res, number)
            res = appendDomain(res, domain)
        else:
            res = appendNumber(res, number)
    with open(outputFile, 'w') as file:
        file.write("\n".join(res))

    print(f'[+] Success generating username list')
    print(f'[+] output file : {outputFile}')


if __name__ == "__main__":
    main()

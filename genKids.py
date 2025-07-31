import argparse
import sys

# 에러 출력 함수
def printError(case, filename=None):
    # -f 플래그 미사용
    if case == 1:
        print("[-] This tool requires a input file; you missed the '-f' flag.")
        sys.exit(1)
    # -o 플래그 미사용
    elif case == 2:
        print("[-] This tool requires an output file; you missed the '-o' flag.")
        sys.exit(1)
    # 문자열 인자가 4개 혹은 6개가 아닌 경우
    elif case == 3:
        print(f'[-] This tool requires four or six string arguments in {filename}.')
        sys.exit(1)


# 인자 핸들링
def getArgs():
    parser = argparse.ArgumentParser(description="password generator v0.4.1",epilog="[Example] genPass.py -f users.txt -o passlist.txt -c $$$,&&&",)
    parser.add_argument("-f", "--file", required=True, help="Input file that has usernames")
    parser.add_argument("-o", "--output", required=True, help="Output file you want to save")
    parser.add_argument("-n", "--number", help="Use extra number", default=None)
    parser.add_argument("-c", "--char", type=lambda s: s.split(','), help="Use extra character", default=None)
    args = parser.parse_args()

    input = args.file
    output = args.output
    extNumber = args.number
    extChar = args.char
    return input, output, extNumber, extChar


# 워드리스트에 숫자/특수문자 패턴 추가
def addPattern(wordlist, extNumber):

    # 숫자 패턴
    digits      = [
                    '1234', '1324', '123',  '12',   '11',   '1',    '2',
                  ]
    
    # 특수문자 패턴
    characters  = [
                '!',    '@',    '#',    '!!',   '@@',   '##',   '!@',
                '!@#',  '@#',   '^^',   '~~',   '%',    '%%',   '_',
                '*',    '**',   '$',    '$$',   '+',    '!^'
                  ]


    
    if extNumber is not None:
        digits.append(extNumber)

    result = []

    # 문자 + 특수문자 + 숫자 조합 생성
    temp = []
    for char in characters:
        for digit in digits:
            temp.append(char + digit)
    for item in temp:
        for word in wordlist:
            result.append(word + item)


    # 문자 + 숫자 + 특수문자 조합 생성
    temp = []
    for digit in digits:
        for char in characters:
            temp.append(digit + char)
    for item in temp:
        for word in wordlist:
            result.append(word + item)


    # 특수문자 + 숫자 + 문자 조합 생성
    temp = []
    for char in characters:
        for digit in digits:
            temp.append(char + digit)
    for item in temp:
        for word in wordlist:
            result.append(item + word)


    # 특수문자 + 문자 + 숫자 조합 생성
    temp = []
    for char in characters:
        for word in wordlist:
            temp.append(char + word)

    for item in temp:
        for digit in digits:
            result.append(item + digit)

    # 숫자 + 문자 + 특수문자 조합 생성
    temp = []
    for digit in digits:
        for word in wordlist:
            temp.append(digit + word)

    for item in temp:
        for char in characters:
            result.append(item + char)

    # 숫자 + 특수문자 + 문자 조합 생성
    temp = []
    for digit in digits:
        for char in characters:
            temp.append(digit + char)
    for item in temp:
        for word in wordlist:
            result.append(item + word)


    # 생성한 두가지 조합 리스트를 인자로 전달된 리스트와 결합

    return result


# 사용자가 사용한 인자 검증
def checkOptions(input, output, extNumber, extChar):
    # input / output은 필수적으로 들어가야함
    if input is None:
        printError(1)
    if output is None:
        printError(2)

    # input 파일에 공백 기준 문자열이 6개 미만이면 종료
    with open(input, 'r') as file:
        userInputFile = [line.strip().split() for line in file.readlines()]
        
    for idx in range(len(userInputFile)):

        if len(userInputFile[idx]) == 4:
            intCnt = 0
            for item in userInputFile[idx]:
                try:
                    int(item)
                    intCnt += 1
                except ValueError:
                    continue
            if intCnt >= 1:
                printError(3, input)
        
        elif len(userInputFile[idx]) == 6:
            intCnt = 0
            for item in userInputFile[idx]:
                try:
                    int(item)
                    intCnt += 1
                except ValueError:
                    continue
            if intCnt >= 1:
                printError(3, input)
        else:
            printError(3)

# 사용자가 입력한 input 파일을 읽어 공백 기준으로 리스트로 생성
def splitName(path):
    with open(path, 'r') as file:
        list = [line.strip().split() for line in file.readlines()]
    return list


# 입력한 input 파일로부터 공백 기준으로 나눠 리스트로 관리한 것을 패스워드 게싱 리스트로 변환
def makePasswordList(list):
    result = []

    # 성 + 이름이 2글자 일 때
    if len(list) == 4:
        enFirst, enLast = list[0], list[1]
        koFirst, koLast = list[2], list[3]

        result.extend([
            enFirst + enLast, # yeonwoo
            enFirst.capitalize() + enLast, # Yeonwoo
            enFirst.capitalize() + enLast.capitalize(), # YeonWoo
            koFirst + koLast, # dusdn
            koFirst.capitalize() + koLast, # Dusdn
            koFirst.capitalize() + koLast.capitalize(), # DusDn
            enFirst, # yeon
            enFirst.capitalize(), # Yeon
            enLast, # woo
            enLast.capitalize(), # Woo
            enFirst[0] + enLast[0], # yw
            enFirst[0].upper() + enLast[0], # Yw
            enFirst[0].upper() + enLast[0].upper() # YW
        ])

    # 성 + 이름이 3글자 일 때
    elif len(list) == 6:
        enFirst, enMiddle, enLast = list[0], list[1], list[2]
        koFirst, koMiddle, koLast = list[3], list[4], list[5]

        result.extend([
            enFirst + enMiddle + enLast, # parkyeonwoo
            enFirst.capitalize() + enMiddle + enLast, # Parkyeonwoo
            enFirst.capitalize() + enMiddle.capitalize() + enLast.capitalize(), #ParkYeonWoo
            enFirst, # park
            enFirst.capitalize(), # Park
            enMiddle, # yeon
            enMiddle.capitalize(), # Yeon
            enLast, # woo
            enLast.capitalize(), # Woo
            koFirst + koMiddle + koLast, # qkrdusdn
            koFirst.capitalize() + koMiddle + koLast, #Qkrdusdn
            koFirst.capitalize() + koMiddle.capitalize() + koLast.capitalize(), # QkrDusDn
            koFirst, # qkr
            koFirst.capitalize(), # Qkr
            koMiddle, # dus
            koMiddle.capitalize(), # Dus
            koLast, # dn
            koLast.capitalize(), # Dn
            enFirst[0] + enMiddle[0] + enLast[0], # pyw
            enFirst[0].upper() + enMiddle[0].upper() + enLast[0].upper(), # PYW
            enFirst[0].upper() + enMiddle[0] + enLast[0] # Pyw
        ])
    else:
        printError(3)

    return result


# 사용자가 -c 옵션을 통해 추가한 문자를 리스트로 생성
def makeExtCharWordlist(extChar, extNumber=None):

    # 특수문자 패턴
    characters  = [
                '!',    '@',    '#',    '!!',   '@@',   '##',   '!@',
                '!@#',  '@#',   '^^',   '~~',   '%',    '%%',   '_',
                '*',    '**',   '$',    '$$',   '+',    '!^'
                  ]
    
    # 숫자 패턴
    digits      = [
                '1234',   '1324',     '123',      '12',       '11',
                '1',      '2',        '2015',     '2016',     '2017',
                '2018',   '2019',     '2020',     '2021',     '2022',
                '2023',   '2024',     '2025',     
                  ]
    result      = []

    if extNumber is not None:
        digits.append(str(extNumber))  
    if not extChar:
        return result

    # extChar가 문자열이든 리스트든 모두 리스트로 통일
    tokens = extChar if isinstance(extChar, list) else [extChar]

    # 문자 + 숫자 + 특수문자 조합 생성
    temp = []
    for token in tokens:
        for digit in digits:
            temp.append(token + digit)
            temp.append(token.upper() + digit)
            temp.append(token.capitalize() + digit)
    for item in temp:
        for char in characters:
            result.append(item + char)

    # 문자 + 특수문자 + 숫자 조합 생성
    temp = []
    for token in tokens:
        for char in characters:
            temp.append(token + char)
            temp.append(token.upper() + char)
            temp.append(token.capitalize() + char)
    for item in temp:
        for digit in digits:
            result.append(item + digit)

    # 특수문자 + 문자 + 숫자 조합 생성
    temp = []
    for char in characters:
        for token in tokens:
            temp.append(char + token)
            temp.append(char + token.upper())
            temp.append(char + token.capitalize())
    for item in temp:
        for digit in digits:
            result.append(item + digit)
    
    # 특수문자 + 숫자 + 문자 조합 생성
    temp = []
    for char in characters:
        for digit in digits:
            temp.append(char + digit)
    for item in temp:
        for token in tokens:
            result.append(item + token)
            result.append(item + token.upper())
            result.append(item + token.capitalize())

    # 숫자 + 문자 + 특수문자 조합 생성
    temp = []
    for digit in digits:
        for token in tokens:
            temp.append(digit + token)
            temp.append(digit + token.upper())
            temp.append(digit + token.capitalize())
    for item in temp:
        for char in characters:
            result.append(item + char)

    # 숫자 + 특수문자 + 문자 조합 생성
    temp = []
    for digit in digits:
        for char in characters:
            temp.append(digit + char)
    for item in temp:
        for token in tokens:
            result.append(item + token)
            result.append(item + token.upper())
            result.append(item + token.capitalize())

    return result


def main():

    # 사용자가 입력한 인자 핸들링
    input, output, extNumber, extChar = getArgs()

    # 사용자가 입력한 필수 인자 누락 여부 검사
    checkOptions(input, output, extNumber, extChar)

    # 사용자가 인자로 넣은 파일에서 공백을 기준으로 리스트 생성
    splitNameList = splitName(input) 

    # 생성한 리스트를 기반으로 기본 워드리스트 양식 생성
    wordlist = []
    for part in splitNameList:
        wordlist.extend(makePasswordList(part))

    # 워드리스트에 더할 숫자와 특수문자 추가
    addedWordlist = addPattern(wordlist, extNumber)

    # 자주 사용되는 패스워드 목록
    easyPasswords = [
        'q1w2e3r4',     'qwer1234!',    'password123!',     'Password123!',     '1q2w3e4r', 
        'qwerty123',    '111111',       '12341234',         'qwer!@34',         'qwer12!@',
        '1q2w3e4r#',    'q1w2e3r4@',    'qwer1234@',        '1q2w3e4r!',        '1111',
        '1234',         'asdf1234'          
        ]
    
    # 사용자가 추가로 지정한 회사 이름 등의 문자열 리스트 생성
    if extChar is not None:
        extCharList = makeExtCharWordlist(extChar, extNumber)
        finalWordlist = addedWordlist + easyPasswords + extCharList
    else:
        finalWordlist = addedWordlist + easyPasswords

    # 완성된 목록을 파일로 저장
    with open(output, 'w') as file:
        file.write("\n".join(finalWordlist))
    print(f'[*] password generator v0.4.1 - Copyright 2025 All rights reserved by mick3y')
    print(f'[+] Success generating user password list')
    print(f'[+] output file : {output}')

if __name__ == "__main__":
    main()

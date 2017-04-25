import os
import sys

num_symbol = 0 # symbol의 개수
num_state = 0 # state의 개수
num_delta = 0 # delta 함수 transition 개수

delta_trans = [] #delta 함수 list of dictionary 형태이다.
print_buffer = [] # 입력된 symbol로 부터 만든 한글 출력 buffer
symbol_to_index = {} # symbol을 index로 mapping
state_list = [] # Automata에서 이동한 상태 목록
current_character = [] # 현재 만들고 있는 Character
last_buffer_backup = []

# 유니코드 표의 모음 순서
# 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20
# ㅏ ㅐ ㅑ ㅒ ㅓ ㅔ ㅕ ㅖ ㅗ ㅘ ㅙ ㅚ ㅛ ㅜ ㅝ ㅞ ㅟ ㅠ ㅡ ㅢ ㅣ

# 유니코드 표의 자음 순서
# 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28
# ㄱ ㄲ ㄳ ㄴ ㄵ ㄶ ㄷ ㄸ ㄹ ㄺ ㄻ ㄽ ㄾ ㄿ ㅀ ㅁ ㅂ ㅃ ㅄ ㅅ ㅆ ㅇ ㅈ ㅉ ㅊ ㅋ ㅌ ㅍ ㅎ 유니코드 표의 자음 순서

# 초성이나 중성에 오는 자음은 유니코드 표에 자음에 정의 된 거에서 몇 개가 빠진다.
# 아래 index는 이러한 빠진 자음을 고려하여, 완성된 한글 한 자에서 해당 자음이 몇번 index를 나타내는지 의미.
# -1은 없는 자음이란 뜻이다.
# 종성에서 0 index는 완성된 한글에서 종성이 없는 경우를 나타내므로 아래 변환 list에서는 index가 1부터 시작한다.
index_map_to_chosung = [0,1,-1,2,-1,-1,3,4,5,-1,-1,-1,-1,-1,-1,-1,6,7,8,-1,9,10,11,12,13,14,15,16,17,18]
index_map_to_chongsung = [1,2,3,4,5,6,7,-1,8,9,10,11,12,13,14,15,16,17,-1,18,19,20,21,22,-1,23,24,25,26,27]

'''
    텍스트 파일로 정의된 Automata를 읽는 함수 
'''
def read_automata():
    global delta_trans
    global symbol_to_index
    f = open('dfa.txt','r', encoding='utf-8')
    num_symbol = 0
    while(True): # Symbol 목록을 입력받는다. 각 symbol 에게 0부터 할당된 index를 설정한다.
        c = f.read(1)
        if c == '\n':
            break
        symbol_to_index[c] = num_symbol
        num_symbol+=1

    num_state = int(f.readline()) # state 의 개수와 delta 함수 transition의 개수
    num_delta = int(f.readline())

    delta_trans = [{} for i in range(num_state)]
    for i in range(num_delta):  # 0 ㄱ 1 형태의 transition 입력을 받아서 delta_trans 변수에 설정한다.
        edges = f.readline().split()
        start_state = int(edges[0])
        trans_symbol = edges[1]
        end_state = int(edges[2])

        delta_trans[start_state][trans_symbol] = end_state

    f.close()
    return

# 화면을 clear 하고 업데이트 한다.
def update_screen():
    global current_character
    os.system('cls')
    for character in print_buffer:
        sys.stdout.write(character)
    sys.stdout.write("\nAU한글 자모 입력 후 엔터를 쳐 주세요. [영어 D(d) = Delete, Q(q) = 종료] : ")

'''
새로 들어온 symbol처리 type0
단순히 print_buffer를 하나 늘리고 symbol을 추가해줌.
'''
def process_new_symobl_type0(symbol):
    global current_character
    print_buffer.append(chr(symbol))
    current_character = print_buffer[-2:] if len(print_buffer) > 1 else print_buffer[-1:]
    return

'''
새로 들어온 symbol처리 type1
현재 버퍼에 모음 symbol 하나를 추가해서 변경 하는 경우이다. 예) ㄱ + ㅏ -> 가 or 고 + ㅐ -> 괘
'''
def process_new_symobl_type1(symbol, lastBuffer):
    global current_character
    moum_hapsung = {8:{}, 13:{}, 18:{}}
    moum_hapsung[8]['ㅏ'] = 'ㅘ'
    moum_hapsung[8]['ㅐ'] = 'ㅙ'
    moum_hapsung[8]['ㅣ'] = 'ㅚ'
    moum_hapsung[13]['ㅓ'] = 'ㅝ'
    moum_hapsung[13]['ㅔ'] = 'ㅞ'
    moum_hapsung[13]['ㅣ'] = 'ㅟ'
    moum_hapsung[18]['ㅣ'] = 'ㅢ'

    if (lastBuffer < 44032):
        chosung = index_map_to_chosung[lastBuffer-12593]
        chungsung = symbol - 12623
        newCharacter = (((chosung*21) + chungsung) * 28) + 44032
    else:
        lastBuffer -= 44032
        chosung = int(int(lastBuffer/28)/21)
        chungsung = int(lastBuffer/28)%21
        newchungsung = ord(moum_hapsung[chungsung][chr(symbol)]) - 12623
        newCharacter = (chosung*21 + newchungsung)*28 + 44032

    print_buffer.pop()
    print_buffer.append(chr(newCharacter))

    current_character = print_buffer[-1:]
    return


'''
새로 들어온 symbol처리 type2
자음이 있었는데 자음이 또 들어와서 현재 버퍼와 이전 버퍼 두가지를 변경해야 하는 경우이다.
'''
def process_new_symobl_type2(symbol, lastBuffer):
    global current_character
    kyupjaum_hapsung = {1:{}, 4:{}, 8:{}, 17:{}} # 1:ㄱ , 4:ㄴ, 8:ㄹ, 16:ㅂ
    kyupjaum_hapsung[1]['ㅅ'] = 3 # ㄳ
    kyupjaum_hapsung[4]['ㅈ'] = 5 # ㄵ
    kyupjaum_hapsung[4]['ㅎ'] = 6 # ㄶ
    kyupjaum_hapsung[8]['ㄱ'] = 9  # ㄺ
    kyupjaum_hapsung[8]['ㅁ'] = 10  # ㄻ
    kyupjaum_hapsung[8]['ㅂ'] = 11  # ㄼ
    kyupjaum_hapsung[8]['ㅅ'] = 12  # ㄽ
    kyupjaum_hapsung[8]['ㅌ'] = 13  # ㄾ
    kyupjaum_hapsung[8]['ㅍ'] = 14  # ㄿ
    kyupjaum_hapsung[8]['ㅎ'] = 15  # ㅀ
    kyupjaum_hapsung[17]['ㅅ'] = 18  #ㅄ

    prevBuffer = ord(print_buffer[-2])
    print_buffer.pop()
    print_buffer.pop()

    jongsung = (prevBuffer-44032)%28
    # 마지막 직전 Buffer에 종성이 있던 경우 예: 각ㅅ + ㄱ -> 갃ㄱ
    if (jongsung > 0):
        new_jongsung = kyupjaum_hapsung[jongsung][chr(lastBuffer)]
        newCharacter = prevBuffer-jongsung + new_jongsung
    # 마지막 직전 Buffer에 종성이 없던 경우 예: 가ㄱ + ㄱ -> 각ㄱ
    else:
        newCharacter = prevBuffer + index_map_to_chongsung[lastBuffer-12593]

    print_buffer.append(chr(newCharacter))
    print_buffer.append(chr(symbol))

    current_character = print_buffer[-2:] if len(print_buffer) > 1 else print_buffer[-1:]
    return

# 새로운 symbol을 처리한다.
def process_new_symbol(symbol):
    '''
    출력 글자 목록 Buffer에서 마지막 글자를 보고 type을 정해서 어떤 행동을 할지 결정한다.
    '''
    symbol = ord(symbol)
    type = 0
    if (len(print_buffer) == 0):
        type = 0
    else:
        lastBuffer = ord(print_buffer[-1])
        if (lastBuffer < 44032): # 완성된 한글이 아닌 경우 ( 모음 또는 자음만 있는 경우 )
            if symbol < 12623: # 자음이 추가로 들어온 경우
                type = 2
            else:             # 모음이 추가로 들어온 경우
                type = 1
        else: # 마지막 출력 Buffer가 완성된 한글이고
            if symbol < 12623:
                type = 0 # 자음일 때 ( 초성우선이므로 새로운 Buffer에 쓰는 type 0 )
            else:
                type = 1 # 모음일 때

    '''
    type에 따라서 print_buffer에  변형을 가한다. 
    '''
    if type==0:
        process_new_symobl_type0(symbol)
    elif type==1:
        process_new_symobl_type1(symbol, lastBuffer)
    else:
        process_new_symobl_type2(symbol, lastBuffer)

    return

read_automata()
# 시작스테이트는 0번이다.
now_state = 0
state_list.append(0)
while(True):
    update_screen()
    c = sys.stdin.read(1)
    c = c.strip()
    if (len(c) != 1):
        continue
    if (c=='q' or c=='Q'): # 종료처리
        break
    elif (c=='d' or c=='D'): # Delete를 누르면 마지막 버퍼를 하나 지우고 automata를 시작 상태로 돌린다.
        if (len(print_buffer) > 0):
            print_buffer.pop()
            now_state = 0
    else:
        if (c not in symbol_to_index): # Automat에 정의되지 않은 Symbol이면 무시
            continue
        if (c not in delta_trans[now_state]): # Aytomata에 정의되지 않은 이동이면 무시
            continue

        now_state = delta_trans[now_state][c]
        state_list.append(now_state)
        process_new_symbol(c)


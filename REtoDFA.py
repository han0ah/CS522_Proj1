import sys
from REtoNFA import EpsilonNFA, getNFAfromRegExpStr

class DFA():
    def __init__(self):
        self.num_of_state = 0
        self.transition_list = []   # t = [(1,a,2), (1,b,3) ...] 이런 형식
        self.transition_matrix = [{}] # t[1][a] = 2, t[1][b] = 3 이런 형식
        self.initial_state = 0
        self.final_states = []
        self.symbols = []

mDFA = None
mNFA = None
eClousers = [] # NFA 각 state 들의 epsilon clouser
dfaStateToSetOfNFAStates = [] # 새로 생성될 dfa의 state와 이에 해당하는 NFA State 들 집합의 목록


def hasFinalState(setOfStates):
    for state in setOfStates:
        if (state == mNFA.final_state):
            return True
    return False

# 각 State 마다 epsilonClouser를 BFS 방식으로 구해 놓는다.
def constructEClousers():
    global eClousers

    eClousers = [[] for i in range(mNFA.num_of_state)]
    for i in range(mNFA.num_of_state):
        visit_check = [False]*mNFA.num_of_state
        visit_check[i] = True
        eClousers[i].append(i)
        j = 0
        while j < len(eClousers[i]):
            start = eClousers[i][j]
            for trans in mNFA.delta_transition[start]:
                if trans[0] == 'e' and (not visit_check[trans[1]]):
                    visit_check[trans[1]] = True
                    eClousers[i].append(trans[1])
            j+=1

# NFA State들의 집합들의 epsilon clouser의 합집합을 반환한다.
def getUnionOfEpsilonClouser(setOfStates):
    result = []
    visit_check = [False] * mNFA.num_of_state
    for state in setOfStates:
        for eclouser_state in eClousers[state]:
            if (not visit_check[eclouser_state]):
                visit_check[eclouser_state] = True
                result.append(eclouser_state)
    return result

def isSameState(stateList1, stateList2):
    if (len(stateList1) != len(stateList2)):
        return False # 길이가 같으면 다른 집합이다.
    count = [0]*mNFA.num_of_state
    for i in range(len(stateList1)):
        count[stateList1[i]]+=1
        count[stateList2[i]]+=1

    for value in count:
        if (value == 1): # count가 1나 라는 건 한 집합에만 있는 원소가 있다는 뜻
            return False
    return True

# 기존에 있는 Set of NFA States -> DFA states Numbering 에서 맞는 집합이 있는지 찾는다. 아니면 -1 반환
def getStateNumber(setOfStates):
    for i in range(len(dfaStateToSetOfNFAStates)):
        prevSet = dfaStateToSetOfNFAStates[i]
        if ( isSameState(setOfStates,prevSet) ):
            return i
    return -1

def parseNFAtoDFA():
    i = 0
    while i < mDFA.num_of_state:
        for symbol in mDFA.symbols:
            # i번째 DFA state 에서 symbol을 통해 도달 가능한 모든 NFA State를 찾음
            reachable_states = []
            visit_check = [False]*mNFA.num_of_state

            for state in dfaStateToSetOfNFAStates[i]:
                for trans in mNFA.delta_transition[state]:
                    trans_symbol = trans[0]
                    dest = trans[1]
                    if (trans_symbol == symbol and (not visit_check[dest])):
                        visit_check[dest] = True
                        reachable_states.append(dest)

            if (len(reachable_states) < 1): # 갈 수 있는 곳이 없으면 무시
                continue

            reachable_states = getUnionOfEpsilonClouser(reachable_states)
            new_dfa_state_num = getStateNumber(reachable_states)
            if (new_dfa_state_num == -1): # 기존에 없는 state이면 state 개수 하나를 추가한다.
                dfaStateToSetOfNFAStates.append(reachable_states)
                mDFA.transition_matrix.append({})
                new_dfa_state_num = mDFA.num_of_state
                if (hasFinalState(reachable_states)):
                    mDFA.final_states.append(new_dfa_state_num)
                mDFA.num_of_state += 1

            mDFA.transition_list.append((i, symbol, new_dfa_state_num))
            mDFA.transition_matrix[i][symbol] = new_dfa_state_num

        i += 1

#https://www.tutorialspoint.com/automata_theory/dfa_minimization.htm 참조
def DFAtoMDFA(bigDFA:DFA):
    sameCheck = [[True]*bigDFA.num_of_state for i in range(bigDFA.num_of_state)]

    # Final과 Final이 아닌 것 끼리는 분류
    for i in range(bigDFA.num_of_state-1):
        for j in range(i+1,bigDFA.num_of_state):
            if (i in bigDFA.final_states) !=(j in bigDFA.final_states):
                sameCheck[i][j] = sameCheck[j][i] = False

    while(True):
        thereIsChange = False
        for i in range(bigDFA.num_of_state - 1):
            for j in range(i + 1, bigDFA.num_of_state):
                if not sameCheck[i][j] :
                    continue
                for symbol in bigDFA.symbols:
                    if not sameCheck[i][j]:
                        # sameCheck[i][j]가 원래 True 였어야 여기까지 오는데 변화가 생긴 것이므로 thereIsChange를 True로 해준다.
                        thereIsChange = True
                        break
                    p = bigDFA.transition_matrix[i][symbol] if (symbol in bigDFA.transition_matrix[i]) else -2
                    q = bigDFA.transition_matrix[j][symbol] if (symbol in bigDFA.transition_matrix[j]) else -2

                    if ((p+1)*(q+1) < 0): # 둘 중 하나면 갈 수 있는 곳이 있으면
                        sameCheck[i][j] = sameCheck[j][i] = False

                    if (p > 0 and q > 0):
                        sameCheck[i][j] = sameCheck[j][i] = sameCheck[p][q]

                if not sameCheck[i][j]:
                    thereIsChange = True

        if(not thereIsChange): # 변화가 없으면 반복문 종료
            break

    newDFA = DFA()
    newDFA.symbols = bigDFA.symbols
    newDFA.num_of_state = 1
    new_state_map = [-1]*bigDFA.num_of_state
    new_state_map[0] = 0

    for i in range(1,bigDFA.num_of_state):
        for j in range(0, i):
            if (sameCheck[i][j]):
                new_state_map[i] = new_state_map[j]
        if (new_state_map[i] == -1):
            new_state_map[i] = newDFA.num_of_state
            newDFA.num_of_state += 1

    newDFA.transition_matrix = [{} for i in range(newDFA.num_of_state)]
    for trans in bigDFA.transition_list:
        new_st = new_state_map[trans[0]]
        symbol = trans[1]
        new_en = new_state_map[trans[2]]
        if symbol not in newDFA.transition_matrix[new_st]:
            newDFA.transition_matrix[new_st][symbol] = new_en
            newDFA.transition_list.append((new_st, symbol, new_en))

    return newDFA


regexp = input("정규식을 입력해 주세요 : ")
#regexp = "((ㄱ+ㄴ+ㄷ+ㄹ+ㅁ+ㅂ+ㅅ+ㅇ+ㅈ+ㅊ+ㅋ+ㅌ+ㅍ+ㅎ+ㅃ+ㅉ+ㄸ+ㄲ+ㅆ)(ㅏ+ㅐ+ㅑ+ㅒ+ㅓ+ㅔ+ㅕ+ㅖ+ㅗ+ㅗㅏ+ㅗㅐ+ㅗㅣ+ㅛ+ㅜ+ㅜㅓ+ㅜㅔ+ㅜㅣ+ㅠ+ㅡ+ㅡㅣ+ㅣ)(e+ㄱ+ㄲ+ㄱㅅ+ㄴ+ㄴㅈ+ㄴㅎ+ㄷ+ㄹ+ㄹㄱ+ㄹㅁ+ㄹㅂ+ㄹㅅ+ㄹㅌ+ㄹㅍ+ㄹㅎ+ㅁ+ㅂ+ㅂㅅ+ㅅ+ㅆ+ㅇ+ㅈ+ㅊ+ㅋ+ㅌ+ㅍ+ㅎ))*"
mNFA = getNFAfromRegExpStr(regexp)
if (mNFA == None):
    print('Fail to parse')
    exit(0)

mNFA.buildDeltaTransition()
mNFA.buildSymbols()

constructEClousers() # 각 NFA State 에서의 epsilon clouser를 구한다.
dfaStateToSetOfNFAStates.append(eClousers[0]) # 0번이 startState 이므로

mDFA = DFA()
mDFA.symbols = mNFA.symbols
mDFA.num_of_state = 1 # 일단 시작 상태 1개가 들어간 상태로 시작한다.
if (hasFinalState(eClousers[0])):
    mDFA.final_states.append(0)

parseNFAtoDFA()
mDFA = DFAtoMDFA(mDFA)

f = open('auto_dfa.txt','w',encoding='utf-8')

for symbol in mDFA.symbols:
    f.write(symbol)
f.write("\n%d"%mDFA.num_of_state)
f.write("\n%d"%len(mDFA.transition_list))
for trans in mDFA.transition_list:
    f.write("\n%d %s %d" %(trans[0], trans[1], trans[2]))

print ('Parsing RegExp to DFA Completed!')
f.close()

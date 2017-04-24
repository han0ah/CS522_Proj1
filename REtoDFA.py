import sys
from REtoNFA import EpsilonNFA, getNFAfromRegExpStr

class DFA():
    def __init__(self):
        self.num_of_state = 0
        self.transition_list = []
        self.initial_state = 0
        self.final_states = []
        self.symbols = []


mDFA = None
mNFA = None
eClousers = [] # NFA 각 state 들의 epsilon clouser
dfaStateToSetOfNFAStates = [] # 새로 생성될 dfa의 state와 이에 해당하는 NFA State 들 집합의 목록

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
                new_dfa_state_num = mDFA.num_of_state
                mDFA.num_of_state += 1

            mDFA.transition_list.append((i, symbol, new_dfa_state_num))

        i += 1



regexp = "((ㄱ+ㄴ+ㄷ+ㄹ+ㅁ+ㅂ+ㅅ+ㅇ+ㅈ+ㅊ+ㅋ+ㅌ+ㅍ+ㅎ+ㅃ+ㅉ+ㄸ+ㄲ+ㅆ)(ㅏ+ㅐ+ㅑ+ㅒ+ㅓ+ㅔ+ㅕ+ㅖ+ㅗ+ㅗㅏ+ㅗㅐ+ㅗㅣ+ㅛ+ㅜ+ㅜㅓ+ㅜㅔ+ㅜㅣ+ㅠ+ㅡ+ㅡㅣ+ㅣ)(e+ㄱ+ㄲ+ㄱㅅ+ㄴ+ㄴㅈ+ㄴㅎ+ㄷ+ㄹ+ㄹㄱ+ㄹㅁ+ㄹㅂ+ㄹㅅ+ㄹㅌ+ㄹㅍ+ㄹㅎ+ㅁ+ㅂ+ㅂㅅ+ㅅ+ㅆ+ㅇ+ㅈ+ㅊ+ㅋ+ㅌ+ㅍ+ㅎ))*"
mNFA = getNFAfromRegExpStr(regexp)
mNFA.buildDeltaTransition()
mNFA.buildSymbols()

constructEClousers() # 각 NFA State 에서의 epsilon clouser를 구한다.
dfaStateToSetOfNFAStates.append(eClousers[0]) # 0번이 startState 이므로

mDFA = DFA()
mDFA.symbols = mNFA.symbols
mDFA.num_of_state = 1 # 일단 시작 상태 1개가 들어간 상태로 시작한다.

parseNFAtoDFA()


f = open('auto_dfa.txt','w',encoding='utf-8')

for symbol in mDFA.symbols:
    sys.stdout.write(symbol)
    f.write(symbol)
print("\n%d"%mDFA.num_of_state)
f.write("\n%d"%mDFA.num_of_state)

print("%d"%len(mDFA.transition_list))
f.write("\n%d"%len(mDFA.transition_list))
for trans in mDFA.transition_list:
    print("%d %s %d"%(trans[0], trans[1], trans[2]))
    f.write("\n%d %s %d" %(trans[0], trans[1], trans[2]))


f.close()

from REtoNFA import EpsilonNFA, getNFAfromRegExpStr

class DFA():
    def __init__(self):
        self.num_of_state = 0
        self.delta_transition = []
        self.initial_state = 0
        self.final_states = []


mDFA = DFA()
# NFA 각 state 들의 epsilon clouser
eClousers = []

# 새로 생성될 dfa의 state와 이에 해당하는 NFA State 들 집합의 목록
dfaStateToSetOfNFAStates = []
mNFA = None

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

def isSameState(stateList1, stateList2):
    pass

def getNewStateNumber(setOfStates):
    pass

def parseNFAtoDFA():
    global mDFA
    mDFA.num_of_state = 1


regexp = "((a+b)(c+d))*"
mNFA = getNFAfromRegExpStr(regexp)
mNFA.buildDeltaTransition()

constructEClousers() # 각 NFA State 에서의 epsilon clouser를 구한다.
dfaStateToSetOfNFAStates.append(eClousers[0]) # 0번이 startState 이므로
mDFA.num_of_state = 1 # 일단 시작 상태 1개가 들어간 상태로 시작한다.

parseNFAtoDFA()






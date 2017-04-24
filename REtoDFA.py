from REtoNFA import EpsilonNFA, getNFAfromRegExpStr

class DFA():
    def __init__(self):
        self.num_of_state = 0
        self.delta_transition = []
        self.initial_state = 0
        self.final_states = []
        self.state_map_info = [] #

def isSameState(stateList1, stateList2):
    pass

def getNewStateNumber(setOfStates):
    pass

def parseNFAtoDFA():
    pass

regexp = "((a+b)(c+d))*"
nfa = getNFAfromRegExpStr(regexp)




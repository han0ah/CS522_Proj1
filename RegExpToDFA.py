# 교과서 TP 3.Regular Languages 15~16page를 참고하여 구현하였습니다.

from REtoAST import getASTfromRegExpStr, NodeInAST

class EpsilonNFA():
    def __init__(self):
        self.num_of_state = 0
        self.transition_list = []
        self.initial_state = 0
        self.final_states = []

    def construct(self, node:NodeInAST):
        if node.tag == '*':
            self.constructStar(node)
        elif node.tag == '+':
            self.constructPlus(node)
        elif node.tag == '.':
            self.constructPlus(node)
        else:
            self.constructSymbol(node)

    # M(E*)
    def constructStar(self, node:NodeInAST):
        pass

    #M(E+E)
    def constructPlus(self, node:NodeInAST):
        pass

    #M(E.E)
    def constructConcate(self, node:NodeInAST):
        NFA1 = EpsilonNFA()
        NFA1.construct(node.left_child)

        NFA2 = EpsilonNFA()
        NFA2.construct(node.left_child)

        nfa2StartNum = NFA1.num_of_state
        for transition in NFA2.transition_list:
            transition[0] += nfa2StartNum
            transition[2] += nfa2StartNum


    #M(a), M(epsilon)
    def constructSymbol(self, node:NodeInAST):
        self.num_of_state = 2
        self.transition_list.append((0,node.tag,1))
        self.initial_state = 0
        self.final_states.append(1)

s = "abc"
getASTfromRegExpStr(s)
t = EpsilonNFA(NodeInAST('.'))

debug = 1




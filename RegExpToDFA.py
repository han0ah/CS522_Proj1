# 교과서 TP 3.Regular Languages 15~16page를 참고하여 구현하였습니다.

from REtoAST import getASTfromRegExpStr, NodeInAST

class EpsilonNFA():
    def __init__(self,node:NodeInAST):
        self.num_of_state = 0
        self.transition_list = []
        self.initial_state = 0
        self.final_state = 0
        if node == None:
            return
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

        self.num_of_state = NFA1.num_of_state + NFA2.num_of_state
        nfa2StartNum = NFA1.num_of_state
        # left child NFA의 transition 추가
        for transition in NFA1.transition_list:
            self.transition_list.append(transition)
        # right child NFA의 transition 추가
        for transition in NFA2.transition_list:
            self.transition_list.append(
                (transition[0]+nfa2StartNum, transition[1], transition[2]+nfa2StartNum)
            )
        # left child NFA의 final state를 right child NFA의 start state로 e-move로 연결
        self.transition_list.append( (NFA1.final_state, 'e', nfa2StartNum) )

        self.final_state = NFA2.final_state + nfa2StartNum


    #M(a), M(epsilon)
    def constructSymbol(self, node:NodeInAST):
        self.num_of_state = 2
        self.transition_list.append((0,node.tag,1))
        self.initial_state = 0
        self.final_state = 1

s = "abc"
getASTfromRegExpStr(s)
t = EpsilonNFA(NodeInAST('a'))

debug = 1




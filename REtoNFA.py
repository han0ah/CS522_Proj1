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
            self.constructConcate(node)
        else:
            self.constructSymbol(node)

    # M(E*)
    def constructStar(self, node:NodeInAST):
        NFA1 = EpsilonNFA(node.left_child)
        self.num_of_state = NFA1.num_of_state + 2
        for transition in NFA1.transition_list:
            self.transition_list.append(
                (transition[0]+1, transition[1], transition[2]+1)
            )

        self.transition_list.append((0, 'e', 1))
        self.transition_list.append((NFA1.final_state+1, 'e', 1))
        self.transition_list.append((1, 'e', self.num_of_state-1))

        self.final_state = self.num_of_state-1

    #M(E+E)
    def constructPlus(self, node:NodeInAST):
        NFA1 = EpsilonNFA(node.left_child)
        NFA2 = EpsilonNFA(node.right_child)
        self.num_of_state = NFA1.num_of_state + NFA2.num_of_state

        nfa2StartNum = NFA1.num_of_state

        # left child NFA의 transition 추가
        for transition in NFA1.transition_list:
            self.transition_list.append(transition)
        # right child NFA의 transition 추가
        for transition in NFA2.transition_list:
            self.transition_list.append(
                (transition[0] + nfa2StartNum, transition[1], transition[2] + nfa2StartNum)
            )

        # 위 아래로 epsilon move 추가
        self.transition_list.append((0, 'e', nfa2StartNum))
        self.transition_list.append((NFA2.final_state+nfa2StartNum, 'e', NFA1.final_state))

        self.final_state = NFA1.final_state


    #M(E.E)
    def constructConcate(self, node:NodeInAST):
        NFA1 = EpsilonNFA(node.left_child)
        NFA2 = EpsilonNFA(node.right_child)

        self.num_of_state = NFA1.num_of_state + NFA2.num_of_state - 1
        nfa2StartNum = NFA1.num_of_state-1
        # left child NFA의 transition 추가
        for transition in NFA1.transition_list:
            self.transition_list.append(transition)
        # right child NFA의 transition 추가
        for transition in NFA2.transition_list:
            st = (NFA1.final_state) if (transition[0] == 0) else transition[0] + nfa2StartNum
            en = (NFA1.final_state) if (transition[2] == 0) else transition[2] + nfa2StartNum

            self.transition_list.append((st, transition[1], en))
        self.final_state = NFA2.final_state + nfa2StartNum

    #M(a) or M(epsilon)
    def constructSymbol(self, node:NodeInAST):
        self.num_of_state = 2
        self.transition_list.append((0,node.tag,1))
        self.initial_state = 0
        self.final_state = 1


def getNFAfromRegExpStr(regexp):
    #TODO : 테스트 regexp 설정 제거
    regexp = "((a+b)(c+d))*"
    ast = getASTfromRegExpStr(regexp)
    eNFA = EpsilonNFA(ast)
    return eNFA

'''
# Test Code for epsilon NFA Construction
for trans in eNFA.transition_list:
    print("%d %s %d"%(trans[0], trans[1], trans[2]))
print(eNFA.final_state)
'''

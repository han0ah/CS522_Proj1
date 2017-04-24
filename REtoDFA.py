from REtoNFA import EpsilonNFA, getNFAfromRegExpStr

regexp = "((a+b)(c+d))*"
nfa = getNFAfromRegExpStr(regexp)




from sentenceDAG import *

sentence = "He said, I'm a boy."
rules = { ("i'm",) : { ("i","am"),} }

a = sentenceDAG()
a.wholeWork(sentence, rules)

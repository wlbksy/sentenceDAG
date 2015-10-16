from sentenceDAG import *

sentence = "He said, I'm a boy."
rules = {
            ("i'm",) : { ("i","am"),},
            ("boy",) : { ("boy", "or", "girl"), },
            ("said",) : { ("says", ), }
        }

check = 'he says, "i am a boy".'

gList = feasibleDAGList(sentence, rules)
blame(gList, check)

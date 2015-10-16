import networkx as nx
import re

punctuation = ',.;:"?!'
regex_punc = "[" + punctuation + "]+"

def cut(sentence):
    phrase = re.split(regex_punc, sentence)
    stripped = [i.strip() for i in phrase]
    return [i.lower() for i in stripped if i]

def shatter(phrase):
    words = re.split('\s+', phrase)
    return words

def search4Alternative(canonical, rules):
    try:
        alterSet = rules[canonical]
        return alterSet
    except:
        return set()

def DAG(words, rules):
    EOSIdx = len(words)+1
    g = nx.DiGraph()
    g.add_node(0, label="BOS")
    g.add_node(EOSIdx, label="EOS")
    prevNode = 0
    for idx, word in enumerate(words):
        nodeIdx = idx + 1
        g.add_node(nodeIdx, label=word)
        g.add_edge(prevNode, nodeIdx)
        prevNode = nodeIdx
    g.add_edge(prevNode, EOSIdx)

    nextIdx = EOSIdx
    for itemLen in range(EOSIdx):
        for beginIdx in range(EOSIdx-itemLen-1):
            endIdx = beginIdx+itemLen+1
            canonical = tuple(words[beginIdx:endIdx])
            alterSet = search4Alternative(canonical, rules)
            if alterSet:
                for alterItem in alterSet:
                    prevNode = beginIdx
                    for eachWord in alterItem:
                        nextIdx += 1
                        g.add_node(nextIdx, label=eachWord)
                        g.add_edge(prevNode, nextIdx)
                        prevNode = nextIdx
                    g.add_edge(nextIdx, endIdx+1)

    return g

def feasibleDAGList(sentence, rules):
    gList = []
    phrases = cut(sentence)
    for idx, phrase in enumerate(phrases):
        words = shatter(phrase)
        g = DAG(words, rules)
        gList.append(g)
        # nx.write_dot(g, str(idx)+".dot")
    return gList

def route(g, wordList):
    wordList.append("EOS")
    wordLen = len(wordList)

    prevNode, thisWordIdx = 0, 0

    while thisWordIdx < wordLen:
        thisWord = wordList[thisWordIdx]
        feasibles = [(g.node[i]["label"], i) for i in g.successors(prevNode)]
        fsbWord, fsbNode = zip(*feasibles)
        if fsbWord == ("EOS",):
            return True
        if thisWord in fsbWord:
            prevNode = fsbNode[thisWord.index(thisWord)]
            thisWordIdx += 1
        else:
            return False
    return False

def blame(gList, sentence):
    phrases = cut(sentence)
    if len(phrases)!= len(gList):
        print("标点使用有错误。")
        return False
    for idx, phrase in enumerate(phrases):
        phrase = phrases[0]
        idx=0
        words = shatter(phrase)
        g = gList[idx]
        if not route(g, words):
            print("错误。")
            return False
    print("正确。")
    return True

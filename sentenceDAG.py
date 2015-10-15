import networkx as nx
import re

class sentenceDAG:
    punctuation = ',.;:"?!'
    regex_punc = "[" + punctuation + "]+"

    def cut(self, sentence):
        phrase = re.split(self.regex_punc, sentence)
        stripped = [i.strip() for i in phrase]
        return [i.lower() for i in stripped if i]

    def shatter(self, phrase):
        words = re.split('\s+', phrase)
        return words

    def search4Alternative(self, canonical, rules):
        try:
            alterSet = rules[canonical]
            return alterSet
        except:
            return set()

    def DAG(self, words, rules):
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
                alterSet = self.search4Alternative(canonical, rules)
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

    def wholeWork(self, sentence, rules):
        phrases = self.cut(sentence)
        for idx, phrase in enumerate(phrases):
            words = self.shatter(phrase)
            g = self.DAG(words, rules)
            # nx.write_dot(g, str(idx)+".dot")

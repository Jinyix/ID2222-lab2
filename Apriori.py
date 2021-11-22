
class Apriori:
    def __init__(self, dataset, support=0.5, confidence=0.7):
        self.support = support
        self.confidence = confidence
        self.dataset = list(map(set, dataset))  # convert every transaction into set

        # results
        self.frequentItemsets = None
        #
        # self.frequentItemsets=[[frozenset({1}), frozenset({3}), frozenset({2}), frozenset({5})],
        #      [frozenset({3, 5}), frozenset({1, 3}), frozenset({2, 5}), frozenset({2, 3})], [frozenset({2, 3, 5})]]
        # self.freqCount={frozenset({5}): 0.75, frozenset({3}): 0.75, frozenset({2, 3, 5}): 0.5, frozenset({1, 2}): 0.25,
        #                frozenset({1, 5}): 0.25, frozenset({3, 5}): 0.5, frozenset({4}): 0.25, frozenset({2, 3}): 0.5,
        #                frozenset({2, 5}): 0.75, frozenset({1}): 0.5, frozenset({1, 3}): 0.5, frozenset({2}): 0.75}

    def _generateNewCk(self, Lk_1, L1):
        '''
        Generate new candidate itemsets Ck from Lk-1
        by combining itemsets from Lk-1 and singletons from L1

        @param Lk_1: a list of sets
        @param L1: a list of singleton sets
        @return: a list of sets
        '''
        Ck = []

        for itemset in Lk_1:
            for singleton in L1:
                if not singleton.issubset(itemset):
                    newCandidate = itemset | singleton # create union
                    if newCandidate not in Ck:
                        Ck.append(newCandidate)
        return Ck 


    def _filterLk(self, Ck):
        '''
        Generate truly frequent itemsets Lk from candidate itemsets Ck
        by filtering those itemsets that have support at least self.support from Ck

        @param Ck: a list of sets
        @return: a list of sets
        '''


        for set in self.dataset:
            for candidateSet in Ck:
                if candidateSet.issubset(set):
                    candidateSet = frozenset(candidateSet)
                    if candidateSet not in self.freqCount:
                        self.freqCount[candidateSet] = 0

                    self.freqCount[candidateSet] +=1

        # ready to filter
        totalItemsets = float(len(self.dataset)) # number of all itemsets
        Lk  = [] # used to store "qualified" candidates

        # for each candidate in input Ck
        for candidateSet in self.freqCount:
            # compute its support
            support = self.freqCount[candidateSet] / totalItemsets
            # add it to Lk if it has support at least self.support
            if support >= self.support:
                Lk.append(candidateSet)
        return Lk

    def _computeFrequentItemsets(self):
        # Initialize result list and dict
        self.frequentItemsets = []
        # count frequency for every candidate itemset in Ck
        self.freqCount = {}

        # Initialize C1
        self.C1 = []
        for itemset in self.dataset:
            for item in itemset:
                if {item} not in self.C1:
                    self.C1.append({item})

        # Compute L1
        L1 = self._filterLk(self.C1)
        self.frequentItemsets.append(L1)

        # Start iteration
        while len(self.frequentItemsets[-1]) > 0:
            Ck = self._generateNewCk(self.frequentItemsets[-1], L1)

            Lk = self._filterLk(Ck)

            # until no more Lk exists
            if len(Lk) == 0:
                break

            self.frequentItemsets.append(Lk)
    
    def getFrequentItemset(self):
        if self.frequentItemsets is None:
            self._computeFrequentItemsets()
        
        return self.frequentItemsets

    def calcConf(self, freqSet, elements, brl, minConf=0.7):
        prunedElements = []
        for conseq in elements:
            conf = self.freqCount[freqSet] / self.freqCount[freqSet - conseq]
            if conf >= minConf:
                print(freqSet - conseq, '-->', conseq, 'conf:', conf)
                brl.append((freqSet - conseq, conseq, conf))
                prunedElements.append(conseq)
        return prunedElements

    def rulesFromConseq(self, freqSet, elements, brl, minConf=0.7):
        # length of each element, increase after each recursion
        m = len(elements[0])
        if (len(freqSet) > (m + 1)):
            l = len(elements)
            e1 = []
            # generate itemsets in length m+1 from elements
            for i in range(l):
                for j in range(i + 1, l):
                    L1 = list(self.frequentItemsets[i])[: m - 1]
                    L2 = list(self.frequentItemsets[j])[: m - 1]
                    L1.sort()
                    L2.sort()
                    if L1 == L2 and L1 and L2 :
                        e1.append(set(self.frequentItemsets[i]) | set(self.frequentItemsets[j]))
            # returen itemsets with confidence > minConf
            e1 = self.calcConf(freqSet, e1, brl, minConf)

            if (len(e1) > 1):
                self.rulesFromConseq(freqSet, e1, brl, minConf)

    def generateRules(self, minConf=0.7):
        bigRuleList = []
        for i in range(1, len(self.frequentItemsets)):
            # get each element in a frequent set
            for freqSet in self.frequentItemsets[i]:
                # save each element to a frozenset list
                elements = [frozenset([item]) for item in freqSet]

                if (i > 1): # #elements>2
                    self.rulesFromConseq(freqSet, elements, bigRuleList, minConf)
                else:  # #elements=2
                    self.calcConf(freqSet, elements,  bigRuleList, minConf)

        return bigRuleList



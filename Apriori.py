

class Apriori:
    def __init__(self, dataset, support=0.5, confidence=0.7):
        self.support = support
        self.confidence = confidence
        self.dataset = list(map(set, dataset))  # convert every transaction into set

        # results
        self.frequentItemsets = None
        self.associationRules = None

    
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

        # count frequency for every candidate itemset in Ck
        freqCount = {}
        for tran in self.dataset:
            for candidateSet in Ck:
                if candidateSet.issubset(tran):
                    candidateSet = frozenset(candidateSet)
                    if candidateSet not in freqCount:
                        freqCount[candidateSet] = 0

                    freqCount[candidateSet] +=1

        # ready to filter
        totalItemsets = float(len(self.dataset)) # number of all itemsets
        Lk  = [] # used to store "qualified" candidates

        # for each candidate in input Ck
        for candidateSet in freqCount:
            # compute its support
            support = freqCount[candidateSet] / totalItemsets
            # add it to Lk if it has support at least self.support
            if support >= self.support:
                Lk.append(candidateSet)
        return Lk

    def _computeFrequentItemsets(self):
        # Initialize result list
        self.frequentItemsets = []

        # Initialize C1
        C1 = []
        for itemset in self.dataset:
            for item in itemset:
                if {item} not in C1:
                    C1.append({item})

        # Compute L1
        L1 = self._filterLk(C1)
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

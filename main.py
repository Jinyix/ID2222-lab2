from apriori import Apriori

if __name__ == '__main__':
    s = float(input("Enter support s (default 0.5): ") or 0.5) 

    dataset = []

    with open('T10I4D100K.dat') as file:
        for line in file:
            line_int = list(map(int, line.rsplit()))
            dataset.append(line_int)

    a = Apriori(dataset, support=s)
    print("Frequent itemsets with support = {}:".format(s))
    print(a.getFrequentItemset())

import itertools as it


def brute_force(numbers,k,target):
    for a in it.combinations(numbers,k):
        if sum(a) ==target:
            print(a)
# Brute force solution: checking sum of all possible k-combinations of our list. Time complexity: k*C_n^k


def ksum(numbers,k,target):
    dict1={}
    dict2={}
    if k%2==0:
        for a in it.combinations(numbers,k//2):
            if target-sum(a) in dict1.keys():
                if bool(set(a)&set(dict1[target-sum(a)])) == False:
                    print(a+dict1[target-sum(a)])
                    break
            dict1[sum(a)]=a
    else:
        for a in it.combinations(numbers,(k+1)//2):
            dict2[sum(a)]=a
        for a in it.combinations(numbers, (k-1)//2):
            if target-sum(a) in dict2.keys():
                if bool(set(a)&set(dict2[target-sum(a)])) == False:
                    print(a+dict2[target-sum(a)])
                    break
#Time complexity n^((k+1)/2)

if __name__ == "__main__":
    with open('knumbersinput.txt') as f:
        lines = f.read().splitlines()
    numbers=[]
    # We only need distinct numbers in our list
    for i in range(2,len(lines)):
        numbers.append(int(lines[i]))
    numbers=list(set(numbers))
    k=int(lines[0])
    target=int(lines[1])
    ksum(numbers,k,target)





import time
import itertools
def Eliminate_Redundant(group):
    new_group = []
    for j in group:
        new=[]
        for i in j:
            if i not in new:
                new.append(i)
        new_group.append(new)
    return new_group
                    new_elem[pos] = '-'
                    new_elem = "".join(new_elem)


def Eliminate_Redundant_list(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list


def verify_empty(group):

    if len(group) == 0:
        return True

    else:
        count = 0
        for i in group:
            if i:
                count+=1
        if count == 0:
            return True
    return False

def Prime_Search(Chart):
    prime = []
    for col in range(len(Chart[0])):
        count = 0
        pos = 0
        for row in range(len(Chart)):
            #find essential
            if Chart[row][col] == 1:
                count += 1
                pos = row

        if count == 1:
            prime.append(pos)

    return prime

def All_Zero_Check(Chart):
    for i in Chart:
        for j in i:
            if j != 0:
                return False
    return True
def find_max(l):
    max = -1
    index = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i]
            index = i
    return index

def Multiply(list1, list2):
    list_result = []
    #if empty
    if len(list1) == 0 and len(list2)== 0:
        return list_result
    #if one is empty
    elif len(list1)==0:
        return list2
    #if another is empty
    elif len(list2)==0:
        return list1

    #both not empty
    else:
        for i in list1:
            for j in list2:
                #if two term same
                if i == j:
                    #list_result.append(sorted(i))
                    list_result.append(i)
                else:
                    #list_result.append(sorted(list(set(i+j))))
                    list_result.append(list(set(i+j)))

        
        list_result.sort()
        return list(list_result for list_result,_ in itertools.groupby(list_result))

def MinCostCalculation(Chart, unchecked):
    P_final = []
    #essential_prime = list with terms with only one 1 (Essential Prime Implicants)
    essential_prime = Prime_Search(Chart)
    essential_prime = Eliminate_Redundant_list(essential_prime)

    #print out the essential primes
    if len(essential_prime)>0:
        s = "\nEssential Prime Implicants :\n"
        for i in range(len(unchecked)):
            for j in essential_prime:
                if j == i:
                    s= s+Change_to_letter(unchecked[i])+' , '
        print s[:(len(s)-3)]

        for i in range(len(essential_prime)):
        for col in range(len(Chart[0])):
            if Chart[essential_prime[i]][col] == 1:
                for row in range(len(Chart)):
                    Chart[row][col] = 0

    if All_Zero_Check(Chart) == True:
        P_final = [essential_prime]
        P_cost = []
        for prime in P:
            count = 0
            for i in range(len(unchecked)):
                for j in prime:
                    if j == i:
                        count = count+ CalculateLiteral(unchecked[i])
            P_cost.append(count)


        for i in range(len(P_cost)):
            if P_cost[i] == min(P_cost):
                P_final.append(P[i])
def CompareBinary(s1,s2):
    count = 0
    pos = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count+=1
            pos = i
    if count == 1:
        return True, pos
    else:
        return False, None

def CompareBinarySame(term,number):
    for i in range(len(term)):
        if term[i] != '-':
            if term[i] != number[i]:
                return False
    return True

def PairCombination(group, unchecked):
    #define length
    l = len(group) -1

    #check list
    check_list = []

    next_group = [[] for x in range(l)]

    #go through the groups
    for i in range(l):
        #first selected group
        for elem1 in group[i]:
            #next selected group
            for elem2 in group[i+1]:
                b, pos = CompareBinary(elem1, elem2)
                if b == True:
                    #append the ones used in check list
                    check_list.append(elem1)
                    check_list.append(elem2)
                    #replace the different bit with '-'
                    new_elem = list(elem1)
                    print new_elem
                    next_group[i].append(new_elem)
    for i in group:
        for j in i:
            if j not in check_list:
                unchecked.append(j)

    return next_group, unchecked


def CalculateLiteral(s):
    count = 0
    for i in range(len(s)):
        if s[i] != '-':
            count+=1

    return count

def Change_to_letter(s):
    out = ''
    c = 'a'
    more = False
    n = 0
    for i in range(len(s)):
        #if it is a range a-zA-Z
        if more == False:
            if s[i] == '1':
                out = out + c
            elif s[i] == '0':
                out = out + c+'\''

        if more == True:
            if s[i] == '1':
                out = out + c + str(n)
            elif s[i] == '0':
                out = out + c + str(n) + '\''
            n+=1
        #conditions for next operations
        if c=='z' and more == False:
            c = 'A'
        elif c=='Z':
            c = 'a'
            more = True

        elif more == False:
            c = chr(ord(c)+1)
    return out



#main function
def main(n_var,minterms ):


    a = minterms.split()
    #put the numbers in list in int form
    a = map(int, a)

    #make a group list
    group = [[] for x in range(n_var+1)]

    for i in range(len(a)):
        #convert to binary
        a[i] = bin(a[i])[2:]
        if len(a[i]) < n_var:
            #add zeros to fill the n-bits
            for j in range(n_var - len(a[i])):
                a[i] = '0'+ a[i]
        #if incorrect input
        elif len(a[i]) > n_var:
            print '\nError : Choose the correct number of variables(bits)\n'
            return
        #count the num of 1
        index = a[i].count('1')
        #group by num of 1 separately
        group[index].append(a[i])


    all_group=[]
    unchecked = []
    #combine the pairs in series until nothing new can be combined
    while verify_empty(group) == False:
        all_group.append(group)
       # print all_group
        next_group, unchecked = PairCombination(group,unchecked)
        group = Eliminate_Redundant(next_group)

    s = "\nPrime Implicants :\n"
    for i in unchecked:
        s= s + Change_to_letter(i) + " , "
    print s[:(len(s)-3)]

    #make the prime implicant chart
    Chart = [[0 for x in range(len(a))] for x in range(len(unchecked))]
    for i in range(len(a)):
        for j in range (len(unchecked)):
            #term is same as number
            if CompareBinarySame(unchecked[j], a[i]):
               Chart[j][i] = 1
    #prime contains the index of the prime implicant terms
    #prime = Eliminate_Redundant_list(MinCostCalculation(Chart))
    primes = MinCostCalculation(Chart, unchecked)
    primes = Eliminate_Redundant(primes)
    print "\n--  Answers --\n"
    for prime in primes:
        s=''
        for i in range(len(unchecked)):
            for j in prime:
                if j == i:
                    s= s+Change_to_letter(unchecked[i])+' + '
        print s[:(len(s)-3)]
if __name__ == "__main__":
file = open(“testfile.text”,”r”)
    if(!file):
	print(“Cannot open input file”)
    raw_input(file, “%d %d” n_var,minterms)
    start_time=time.time()
    main(n_var,minterms)
    print "time elapsed: {:.2f}ms".format(int(round((time.time() - start_time)*1000)))
file.close()
    



def join(arr):  # O(m) # joins an array eg- ["a","b","c'",None] returns "abc'"
    answer = []
    for i in arr:
        if (i):
            answer.append(i)
    if (len(answer) == 0):
        return None 
    return ''.join(answer)

twopowers = {}
def islegal(terms): # O(mn + m + n)
    global combined
    n = len(terms)
    no_of_none = terms.count(None)
    if no_of_none not in twopowers:         
        power = 2**no_of_none
        twopowers[no_of_none] = power
    else:
        power = twopowers[no_of_none]
    count = 0
    for i in combined:
        counter = True
        for j in range(n):
            if terms[j] is None:
                pass 
            elif (terms[j] != i[j]):
                counter = False 
                break 
        
        if (counter):
            count += 1
        if (count == power):
            break
    return count == power 
        
def parse(string,n):  # O(m) # generates an array; eg-"abc'" returns ["a","b","c'"]
    answer = [None] * n
    m = len(string)
    cnt = 0
    i = 0
    while (cnt < n and i < m):
        if ( chr(ord("a") + cnt) == string[i]):
            if (i+1 < m and string[i+1] == "'" ):
                answer[cnt] = string[i]+string[i+1] 
                i+=1 
            else:
                answer[cnt] = string[i] 
            i+=1

        
        cnt+=1
    return answer 
        
def parse2(string):    # O(m) generates an array; eg-"abc'" returns ["a","b","c'"]
    answer = []
    for i in range(len(string)):
        if (i != len(string) - 1 and string[i+1] == "'"):
            answer.append(string[i]+string[i+1])
        elif (string[i] != "'" ):
            answer.append(string[i]) 
    return answer 

class DigitalTree:

    def __init__(self,term):
        self.term = term  
        n = len(term) 
        self.no_of_var = n 
        self.tree = self.make_tree(term) 
    class Node:
        def __init__(self,term):
            self.term = term 
            self.no_of_var = len(term)
            self.children = [] 
        
        def __str__(self):
            return join(self.term) 
        
    def make_tree(self,arr):  # O(m*n!)
        x = self.Node(arr)  
        
        temp = arr[:] 
        for i in range(len(arr)): 
            if (arr[i] is not None):
                y = temp[i]
                temp[i] = None 
                if (islegal(temp)):
                    x.children.append(self.make_tree(temp[:])) 
                temp[i] = y 
                
            else:
                pass 
        return x  
    
    def helper_display_tree(self,node):
        
        print(join(node.term))
        for i in node.children:
            self.helper_display_tree(i)  

    def display_tree(self):
        self.helper_display_tree(self.tree)

    def display_children(self):
        for i in self.tree.children:
            print(join(i.term)) 
    
    def find_max_helper(self,tree):   

        max = tree.term 
        for i in tree.children:
            x = self.find_max_helper(i) 
            if (max.count(None) < x.count(None)):
                max = x 
        return max 
    
    def find_max(self): #O(m*m!) 
        return self.find_max_helper(self.tree) 

# term = ["a","b","c","d"] 
# tree = DigitalTree(term) 

# tree.display_tree()

def find_maximal(one,dontcare):  # O(n*m*m!)
    global combined 
    if len(one) == 0:
        return one
    else:
        ones = [parse2(i) for i in one] 
        ans =  []
        combined = [x for x in ones]
        combined += [parse2(x) for x in dontcare]  #O(mn)

        for i in ones:
            tree = DigitalTree(i)  
            max = tree.find_max()
            ans.append(join(max)) 
    
    return ans 

def generate_terms(region,answer): # O(m*2^m)
    if not None in region:
        answer.append(region)
    else: 
        for i in range(len(region)):
            if region[i] == None:
                a = region[:]
                b = region[:]
                a[i] = chr(ord("a") + i)
                b[i] = a[i] + "'"
                generate_terms(a, answer)
                generate_terms(b, answer)
                break
# usage of the function is as follows
# answer = []
# generate_terms(a, answer)


def my_key(string):
    n = len(string)
    return n

def get_first(dict):
    ans = ''
    for e in dict:
        ans = e
        break  
    return ans 

def opt_function_reduce(func_TRUE,func_DC):
    
    if (len(func_TRUE) == 0):
        return []

    answer = find_maximal(func_TRUE,func_DC) # O(n*m*m!)
    reduced_answer = list(set(answer)) # O(n)
    #print('answer of comb_function_expansion is',reduced_answer)
     
    n = len(reduced_answer)
    reduced_answer.sort(key = my_key,reverse = True) # O(nlgn)
    m = len(parse2(func_TRUE[0]))
    dict = {}
    # making the dictionary 
    for i in range(n): # O(n^2*2^m) 
        cells = []
        generate_terms(parse(reduced_answer[i],m),cells)

        
        for j in cells: #O(n*2^m)
            j_string = join(j)
            if j_string in dict:
                dict[j_string].add(reduced_answer[i])
            else:
                dict[j_string] = set([reduced_answer[i]]) 
    
    #print(dict)
    final_answer = []

    for i in range(n): # O(n^2*2^m)
        cells = [] 
        generate_terms(parse(reduced_answer[i],m),cells) # O(m*2^m)
        to_be_deleted = True
        for cell in cells: # O(n*2^m)
            if ((join(cell) in func_DC) or len(dict[join(cell)]) >= 2):
                pass 
             
            else:
                # print(f'{get_first(dict[join(cell)])} cant be deleted as the cell {join(cell)} is present only in {get_first(dict[join(cell)])}')
                # print()
                to_be_deleted = False
                break 
        if (to_be_deleted): # O(m*2^m) 
            #print(f'{reduced_answer[i]} to be deleted')
            cnt = 1
            for cell in cells:
                #print(f'Term {cnt} : {join(cell)}')
                dict[join(cell)].remove(reduced_answer[i])
                # if (join(cell) not in func_DC):
                #     print(f'Covering region: {get_first(dict[join(cell)])}')
                # else:
                #     print(f'this term is a dont care, so ignored.')
                cnt += 1 
            #print() 
        else:
            final_answer.append(reduced_answer[i]) 
    
    
    return final_answer 



# func_TRUE = ["a'b'c'd'e'", "a'bc'd'e'", "abc'd'e'", "ab'c'd'e'", "abc'de'", "abcde'", "a'bcde'", "a'bcd'e'", "abcd'e'", "a'bc'de", "abc'de", "abcde", "a'bcde", "a'bcd'e", "abcd'e", "a'b'cd'e", "ab'cd'e"]
# func_DC = []

# func_TRUE = ["a'b'c'd", "a'b'cd", "a'bc'd", "abc'd'", "abc'd", "ab'c'd'", "ab'cd"]
# func_DC = ["a'bc'd'", "a'bcd", "ab'c'd"]

# func_TRUE = ["a'bc'd'", "abc'd'", "a'b'c'd", "a'bc'd", "a'b'cd"] 
# func_DC = ["abc'd"]

# func_TRUE = ["a'b'c", "a'bc", "a'bc'", "ab'c'"] 
# func_DC = ["abc'"]

# func_TRUE = ["a'b'c","a'bc"]
# func_DC = ["ab'c"] 
# print(opt_function_reduce(func_TRUE,func_DC)) 
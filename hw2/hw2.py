import sys
import math


def get_parameter_vectors():
    '''
    This function parses e.txt and s.txt to get the  26-dimensional multinomial
    parameter vector (characters probabilities of English and Spanish) as
    descibed in section 1.2 of the writeup

    Returns: tuple of vectors e and s
    '''
    #Implementing vectors e,s as lists (arrays) of length 26
    #with p[0] being the probability of 'A' and so on
    e=[0]*26
    s=[0]*26

    with open('e.txt',encoding='utf-8') as f:
        for line in f:
            #strip: removes the newline character
            #split: split the string on space character
            char,prob=line.strip().split(" ")
            #ord('E') gives the ASCII (integer) value of character 'E'
            #we then subtract it from 'A' to give array index
            #This way 'A' gets index 0 and 'Z' gets index 25.
            e[ord(char)-ord('A')]=float(prob)
    f.close()

    with open('s.txt',encoding='utf-8') as f:
        for line in f:
            char,prob=line.strip().split(" ")
            s[ord(char)-ord('A')]=float(prob)
    f.close()

    return (e,s)


def shred(filename):
    #Using a dictionary here. You may change this to any data structure of
    #your choice such as lists (X=[]) etc. for the assignment
    X=dict()

    with open (filename,encoding='utf-8') as f:
        # TODO: add your code here
        for line in f:
            line = line.upper() #convert line to uppercase
            #iterate through each char to increment the correct letter count
            for ch in line:
                if ch.isalpha():
                    if ch in X:
                        X[ch] = X[ch] + 1
                    else:
                        X[ch] = 1
                    
    return X


# TODO: add your code here for the assignment
# You are free to implement it as you wish!
# Happy Coding!
P_ENGLISH = 0.6
P_SPANISH = 1 - P_ENGLISH
(E, S) = get_parameter_vectors()
X = shred('letter.txt')

'''
This function will calculate the log value for any pair of count and probability.
The count is the number of a certain letter.
The probability is the probablity of that letter appearing in English or Spanish.
'''
def calculate_log(count, probability):
    return count * math.log(probability)

'''
This function will calculate the F value for the specified language.
Language is either English ('E') or Spanish ('S')
'''
def calculate_F(language):
    lang_prob = E
    lang = P_ENGLISH
    if (language == "S"):
        lang_prob = S
        lang = P_SPANISH

    #add up log values
    i = 0
    result = 0
    for i in range(26):
        if chr(i+65) in X:
            result += calculate_log(X.get(chr(i+65)), lang_prob[i])
        else:
            result += calculate_log(0, lang_prob[i])
        i+=1

    result += math.log(lang)
    return result

'''
This function will calculate the conditional probability that the letter is in English
based on the given evidence of the shredded letter counts.
'''
def calculate_prob_eng():
    FE = calculate_F('E')
    FS = calculate_F('S')

    #for large values
    if (FS - FE >= 100):
        return 0
    elif (FS - FE <= -100):
        return 1
    else:
        #actual calculation
        return 1 / (1 + math.e**(FS-FE))
        
'''
Main function that has all of the print statements formatted for the outputs
'''
def main():
    #Q1: counts of each letter
    print("Q1")
    i = 0
    for i in range(26):
        if chr(i+65) in X:
            print(chr(i+65), X.get(chr(i+65)))
        else:
            print(chr(i+65), "0")
        i+=1

    #Q2: log value of letter A in both English and Spanish
    print("Q2")
    #English:
    XE = 0
    if 'A' in X:
        XE = calculate_log(X.get('A'), E[0])
    print('%.4f' % XE)
    #Spanish:
    XS = 0
    if 'A' in X:
        XS = calculate_log(X.get('A'), S[0])
    print('%.4f' % XS)

    #Q3: F() values for English and Spanish
    print("Q3")
    print('%.4f' % calculate_F('E'))
    print('%.4f' % calculate_F('S'))

    #Q4: Probability letter is written in English
    print("Q4")
    print('%.4f' % calculate_prob_eng())


#calling main
main()


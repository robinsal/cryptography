'''
    First we need to create a way to determine the index of 
    coincidence for a given string. First we will count the
    frequency of each letter in the string. Then compute
    the IC based on those frequencies.
'''

# returns a hash for each character to the number of times
# it appears in the text along with the length of the text
def generate_hashtable(text):
    dic = {}
    for c in text:
        if c not in dic:
            dic[c] = 1
        else:
            dic[c] += 1
    return dic, len(text)

# returns the index of coincedence for the english alphabet
# on a given frequency hash (produced by fcn above)
def coincidence_index((freqs, length)):
    total = 0.
    for i in freqs:
        total += freqs[i] * (freqs[i] - 1)
    total /= length * (length - 1)
    
    return total * 26

'''
To determine the size of the keyword, we should arrange the text into
'columns' of various sizes until we get a rough distribution
where the index of coincidence of the characters in each column is 
about 1.73 (the expected index of coincidence for the English language)
'''

# returns the given string as a list of strings which can be thought
# of as 'columns'. For example, given "abcdefghij" and the int 3
# this will return ["adgj", "beh", "cfi"]
def split_text(text, num):
    lst = []
    for i in range(0, num):
       lst.append(text[i::num])
    return lst

# text is the string to be examined
# num_of_columns is the number of 'columns' to break the text into
# returns the average IC between each column of text
def get_IC(text, num_of_columns):
    text_cols = split_text(text, num_of_columns)
    ic_list = [coincidence_index(generate_hashtable(x)) for x in text_cols]
    return sum(ic_list) / num_of_columns


'''
    Now that we have functions to perform the operations, we need
    a procedure that returns the possible lengths of the keyword.
    I will assume the keyword length is less than 100, though
    it is worth noting that it might not be. Should the following
    procedures not crack the cipher, the key length is probably
    more than 100.
'''

def get_possible_key_lengths():
    f = open('cipher1.txt', 'r')
    contents = f.read()
    # To find the probable key length, we want the value that is closest
    # to 1.73, which is the index of coincidence of English according
    # to Wikipedia. However, we will need to test a few keylengths to
    # be sure we have selected the correct one.
    probable_lengths = []
    for i in range(2, 100):
        ic = get_IC(contents, i)
        if abs(ic - 1.73) < .1:
            probable_lengths.append(i)
            
    # the above for loop gathers all key length values that are within .1 of
    # the English IC
    f.close()
    return probable_lengths

# Finally this is a function that will return the smallest length key that 
# evenly divides all the largest possibilities. This is not guaranteed
# to return the correct key length, but it is pretty likely that it will.
def determine_most_likely():
    possibilities = get_possible_key_lengths()
    for i in range(len(possibilities)):
        divides_everything_else = True
        for j in range(i+1, len(possibilities)):
            if possibilities[j] % possibilities[i] != 0:
                divides_everything_else = False
        if divides_everything_else:
            return possibilities[i]
    return possiblities[-1]

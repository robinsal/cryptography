'''
	Steps of decryption:
		Find the length of key
		Determine the key itself
		Decrypt the message using the key

	This python file is used to find the probable length of a key
'''

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
# on a given frequency hash (produced by the fcn above)
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
# of as 'columns'. For example, given "abcdefghij" and the int 3 (for 3 columns)
# this will return ["adgj", "beh", "cfi"]
def split_text(text, num):
    lst = []
    for i in range(0, num):
       lst.append(text[i::num])
    return lst

# text is the string to be examined
# num_of_columns is the number of 'columns' to break the text into
# returns the average index of coincidence between each column of text
def get_IC(text, num_of_columns):
    text_cols = split_text(text, num_of_columns)
    ic_list = [coincidence_index(generate_hashtable(x)) for x in text_cols]
    return sum(ic_list) / num_of_columns


'''
    Now that we have functions to perform the operations, we need
    a procedure that returns the possible lengths of the keyword.
    I will assume the keyword length is less than 100, though
    it is worth noting that it might not be. Should the following
    procedures not determine any probable lengths, the key length is
    most likely more than 100.
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

'''
	To use this file, generate the probable key lengths with get_possible_key_lengths
	inputting the ciphertext file. This will return a list of possibilities and it
	is up to the user to determine which ones are worth testing out.

	Anything that is a multiple of previous possibilities is probably not the key.
	For example, if the possibilities are [3, 6, 9, 12, ...], then the key is almost
	certainly 3, because splitting it into 3k columns will satisfy the function's
	test.
	
	To drive the point home, if the key is 'key', then 'keykey' will encrypt the
	text in the same way.
'''

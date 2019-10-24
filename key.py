from keylength import determine_most_likely, split_text
from collections import deque
import math

f = open('cipher1.txt', 'r')
contents = f.read()
f.close()

key_length = determine_most_likely()
groupings = split_text(contents, key_length)

# Create a table with the frequencies in English of each letter
english_frequencies = [0.082, 0.014, 0.028, 0.038, 0.131, 0.029, 
        0.020, 0.053, 0.064, 0.001, 0.004, 0.034, 0.025, 0.071, 
        0.080, 0.020, 0.001, 0.068, 0.061, 0.105, 0.025, 0.009, 
        0.015, 0.002, 0.020, 0.001]

keyword = []
for g in groupings:
    num_of_chars = float(len(g))
    expected_occurrences = [x * num_of_chars for x in english_frequencies]
    freqs = deque([0] * 26)
    for c in g:
        freqs[ord(c) - ord('a')] += 1
    min_chi = 1000000000000000000 # some astronomical number 
    shift_by = 0
    for i in range(26):
        curr_chi = 0
        for j in range(26):
            curr_chi += (freqs[j] - expected_occurrences[j])**2 / expected_occurrences[j]
        if curr_chi < min_chi:
            min_chi = curr_chi
            shift_by = i
        freqs.rotate(1)
    keyword.append(shift_by)

keyword = [x + ord('a') for x in keyword]
keyword = [chr(x) for x in keyword]
keyword = ''.join(keyword)
print(keyword)

f = open('keyword1.txt', 'w')
f.write(keyword)
f.close()

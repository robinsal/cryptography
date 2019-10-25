def decrypt(text, key):
    ctext = []
    offset = ord('a')
    for i in range(len(text)):
        c = ord(text[i]) - offset
        k = ord(key[i % len(key)]) - offset
        new_character = chr((c + k) % 26 + offset)
        ctext.append(new_character)
    return ''.join(ctext)
    
cipher = open('cipher1.txt', 'r')
contents = cipher.read()
cipher.close()

key = open('keyword1.txt', 'r')
k = key.read()
key.close()

f = open('message1.txt', 'w')
f.write(decrypt(contents, k))
f.close()

from itertools import permutations

from Crypto.Util.number import long_to_bytes

string = "mew brr mew meaw mrr mrr meaw meeaw mew meaw meeaw mew meaw meeaw meeaw mew meow brr mew meeaw mEEEwr meaw meeaw brr meaw mrr mEEEwr meaw mrr awr meaw meeaw ssh mew meeaw mEEEwr meaw mrr awr meaw meeaw ssh mew meeaw mEEEwr mew ssh meow meaw meaw ssh meaw meeaw brr mew mEEEwr meaw mew meeaw mEEEwr mew brr meaw mew meeaw mEEEwr meaw mrr mEEEwr meaw meaw ssh meaw meow meaw meaw mrr mrr mew meeaw mEEEwr meaw meaw ssh mew meeaw mEEEwr meaw meeaw ssh meaw mrr mrr meaw mrr mew meaw meeaw awr meaw mrr mrr meaw meeaw brr mew meeaw mEEEwr meaw meeaw meaw meaw mrr mrr meaw meeaw ssh meaw meeaw ssh meaw meaw ssh meaw mrr meow meaw mrr mrr mew meeaw mEEEwr meaw mrr meeaw meaw meeaw meeaw meaw meeaw awr mew meeaw mEEEwr meaw meow meow meaw meeaw meeaw meaw meow mew mew meow brr mew meeaw mEEEwr meaw meeaw brr meaw mrr mEEEwr meaw mrr mrr mew meeaw mEEEwr meaw meeaw ssh meaw mrr mrr meaw mrr mew meaw meeaw awr meaw mrr mrr meaw meeaw brr mew meeaw mEEEwr meaw meeaw meaw meaw mrr mrr meaw meeaw ssh meaw meeaw ssh meaw meaw ssh meaw mrr meow meaw mrr mrr mew meeaw mEEEwr meaw mrr awr meaw meeaw ssh mew meeaw mEEEwr mew meeaw ssh mew ssh mrr mew meeaw mEEEwr meaw mrr mew meaw meaw ssh meaw meeaw brr mew meeaw mEEEwr meaw mrr awr meaw meeaw ssh mew meeaw mEEEwr meaw meaw ssh mew meeaw mEEEwr meaw meeaw ssh meaw meeaw meaw meaw meaw ssh meaw meeaw mew meaw meeaw mew mew meow brr mew meeaw mEEEwr meaw meeaw brr meaw meow meow meaw meeaw meow meaw mrr awr meaw mrr mew meaw meaw ssh meaw meeaw mew meaw meeaw mew meaw meow meow mew meeaw mEEEwr meaw mrr meeaw meaw meow mew meaw meeaw awr meaw meeaw awr meaw meow meow mew meow brr mew meeaw mEEEwr meaw mrr mew meaw meaw ssh meaw meeaw awr meaw meeaw mrr meaw mrr awr meaw meow meaw meaw meeaw meeaw meaw meeaw awr meaw meeaw meeaw meaw meow mew meaw meeaw ssh mew meeaw mEEEwr meaw meeaw meaw meaw meaw ssh meaw meeaw meaw meaw meeaw meaw meaw meaw ssh meaw meeaw mew mew mEEEwr meaw mew meeaw mEEEwr mew brr meaw meaw meeaw brr mew meeaw mEEEwr meaw mrr awr meaw meeaw ssh mew meeaw mEEEwr meaw meeaw meeaw meaw mrr meeaw meaw meeaw brr meaw mrr mrr meaw meeaw mrr mew meeaw mEEEwr meaw mrr brr meaw mrr mrr meaw meeaw meow meaw meeaw brr mew meeaw mEEEwr meaw meaw ssh meaw meeaw ssh mew meeaw mEEEwr meaw meaw ssh mew meeaw mEEEwr meaw meeaw meow meaw mrr mrr meaw meeaw brr mew meeaw mEEEwr meaw mrr awr meaw meeaw mrr mew meeaw mEEEwr meaw meeaw meaw meaw meaw ssh meaw meeaw mrr meaw meow meow mew meeaw mEEEwr meaw mrr mEEEwr meaw meeaw meeaw meaw meow mew meaw meeaw ssh meaw mrr mrr meaw mrr mEEEwr meaw meeaw meeaw meaw meeaw mew meaw mrr meaw meaw meeaw ssh mew meow brr mew meeaw mEEEwr meaw meaw brr meaw meow mew meaw meeaw brr mew meeaw mEEEwr meaw mrr mew meaw meaw ssh meaw meeaw mrr mew meeaw mEEEwr meaw meaw ssh meaw meeaw mew meaw meeaw ssh meaw meeaw meeaw mew meeaw mEEEwr meaw meaw brr meaw mrr mrr mew meeaw mEEEwr meaw mrr meeaw meaw meeaw meeaw meaw meow mew meaw meeaw mrr meaw mrr meaw mew meeaw mEEEwr meaw mrr awr meaw meeaw mrr mew meeaw mEEEwr meaw meeaw brr meaw mrr mEEEwr meaw mrr mrr mew meeaw mEEEwr meaw meow mrr meaw mrr awr meaw meeaw mew meaw mrr meaw mew mEEEwr meaw mew meeaw mEEEwr meaw meeaw meow meaw meeaw ssh meaw meeaw ssh meaw meeaw ssh mew meow brr mew meeaw mEEEwr meaw mrr mEEEwr meaw mrr mrr meaw meeaw awr meaw mrr mrr meaw meeaw ssh mew meeaw mEEEwr meaw meow meow meaw meeaw meeaw meaw meow mew meaw meeaw awr mew meeaw mEEEwr meaw mrr meeaw meaw meeaw mew meaw meaw ssh meaw mrr meow mew meeaw mEEEwr mew brr mrr mew ssh meow meaw mew meeaw mew ssh ssh mew mEEEwr mEEEwr mew mEEEwr meeaw mew mEEEwr mEEEwr mew mEEEwr awr meaw meow awr meaw mrr mew mew mEEEwr ssh meaw meeaw brr meaw meaw mEEEwr meaw mrr awr meaw meeaw ssh meaw meaw mEEEwr meaw mrr mew meaw meow mew meaw meeaw brr mew mEEEwr awr meaw meow brr mew meeaw mEEEwr mew ssh meow meaw meaw ssh meaw meeaw brr meaw meeaw ssh mew meeaw mEEEwr meaw meaw ssh meaw meeaw awr meaw mrr mrr mew meeaw mEEEwr meaw mrr brr meaw meeaw mrr meaw meeaw meeaw meaw meow mrr meaw meeaw mrr mew meeaw mEEEwr meaw mrr meeaw meaw meeaw meeaw meaw meeaw awr mew meeaw mEEEwr meaw meeaw brr meaw mrr mEEEwr meaw mrr mrr meaw mrr awr meaw meeaw awr mew meeaw mEEEwr meaw meaw ssh meaw mrr meow meaw mrr awr meaw meeaw mew meaw mrr awr meaw meeaw brr meaw meow meow mew meow brr mew meeaw mEEEwr meaw mrr meow meaw meeaw awr meaw meaw ssh meaw mrr mew meaw mrr mrr mew meow brr mew meeaw mEEEwr meaw meaw ssh meaw meeaw mrr meaw mrr meaw mew meeaw mEEEwr meaw meeaw brr meaw mrr mEEEwr meaw mrr mrr meaw mrr awr meaw meeaw awr mew meeaw mEEEwr meaw meaw ssh meaw meaw brr meaw mrr awr meaw meeaw mew meaw mrr awr meaw meeaw brr meaw meow meow mew meeaw mEEEwr meaw meeaw brr meaw meeaw meeaw mew meeaw mEEEwr meaw mrr mEEEwr meaw meow mew meaw meeaw mrr meaw meeaw brr mew meeaw mEEEwr meaw meeaw ssh meaw meeaw meaw meaw meaw ssh meaw meeaw mew meaw meeaw mew mew meeaw mEEEwr meaw meeaw meow meaw meeaw awr meaw mrr mrr meaw meow meow mew meeaw mEEEwr meaw meeaw ssh meaw meow mew meaw mrr mew meaw mrr mEEEwr mew meeaw mEEEwr meaw meaw ssh meaw meeaw ssh mew meeaw mEEEwr meaw meeaw awr meaw meeaw meeaw meaw mrr meaw meaw mrr mrr meaw meeaw mrr meaw meeaw brr meaw meeaw ssh mew meeaw mEEEwr meaw meaw ssh meaw meeaw mrr meaw mrr meaw mew meeaw mEEEwr meaw meaw brr meaw mrr awr meaw meeaw awr meaw mrr meaw meaw meeaw ssh mew mEEEwr meaw mew meeaw mEEEwr meaw mew meeaw meaw mrr mEEEwr meaw mrr mrr meaw meow meow mew meeaw mEEEwr meaw mrr mEEEwr meaw meaw ssh meaw meow meaw meaw mrr mrr mew meeaw mEEEwr meaw meaw ssh mew meeaw mEEEwr meaw meeaw awr meaw mrr mrr meaw meeaw meow meaw meow mew meaw meeaw brr meaw meaw ssh meaw meeaw brr meaw mrr awr meaw meeaw meeaw meaw meeaw mrr mew meeaw mEEEwr meaw mrr meeaw meaw meeaw meeaw meaw meeaw awr mew meeaw mEEEwr meaw meaw brr meaw mrr mrr meaw mrr awr meaw meeaw mrr meaw mrr meow mew meeaw mEEEwr meaw mrr awr meaw meeaw mrr meaw mrr meaw meaw mrr mrr meaw meeaw meow meaw mrr mrr meaw meeaw mrr meaw mrr meaw meaw mrr mrr meaw meeaw mrr meaw meeaw brr mew meeaw mEEEwr meaw meaw ssh meaw meeaw mrr meaw mrr meaw mew meeaw mEEEwr meaw meaw ssh meaw meeaw mew meaw meeaw meeaw meaw meeaw meeaw meaw mrr meeaw mew meow brr mew meeaw mEEEwr meaw meaw brr meaw meow mew meaw meeaw brr mew meeaw mEEEwr meaw mrr mew meaw meaw ssh meaw meeaw mrr mew meeaw mEEEwr meaw meaw ssh meaw meeaw mew meaw meeaw ssh meaw meeaw meeaw mew meeaw mEEEwr meaw meaw brr meaw mrr mrr mew meeaw mEEEwr meaw meaw ssh meaw mrr meeaw meaw mrr meeaw meaw mrr mrr meaw mrr mew meaw meeaw brr meaw mrr awr meaw meeaw meeaw meaw meeaw mrr meaw meaw ssh meaw meeaw brr meaw mrr mrr mew meeaw mEEEwr meaw meaw ssh meaw meeaw mrr meaw mrr meaw mew meeaw mEEEwr meaw meeaw meow meaw meeaw mew meaw meaw ssh meaw meow meow meaw mrr meeaw meaw meow mew meaw meeaw mew mew meeaw mEEEwr meaw meow mrr meaw mrr awr meaw meeaw brr meaw mrr mEEEwr mew meeaw mEEEwr meaw meeaw brr meaw mrr mEEEwr meaw mrr mrr meaw mrr awr meaw meeaw awr mew meeaw mEEEwr meaw meeaw meeaw meaw meow mrr meaw meeaw mrr meaw mrr mrr meaw meeaw awr meaw meeaw ssh mew mEEEwr meaw mew meeaw mEEEwr meaw mew meeaw meaw mrr mEEEwr meaw mrr mrr meaw meeaw awr meaw mrr mrr mew meeaw mEEEwr meaw meaw ssh meaw meeaw awr meaw mrr mrr mew meeaw mEEEwr meaw meeaw meaw meaw meaw ssh meaw meeaw mrr meaw meow meow mew meeaw mEEEwr meaw mrr meaw meaw mrr awr meaw mrr meeaw meaw mrr meeaw meaw mrr mrr meaw meeaw awr meaw mrr mrr meaw meeaw mrr meaw meeaw brr mew meeaw mEEEwr meaw meaw brr meaw meeaw awr meaw mrr mrr meaw mrr mrr meaw mrr meaw meaw meeaw ssh mew meeaw mEEEwr meaw meeaw meeaw meaw mrr meeaw mew meeaw mEEEwr meaw mrr mew meaw meaw ssh meaw meeaw brr meaw meeaw ssh mew meow brr mew meeaw mEEEwr meaw mrr mrr meaw meaw ssh meaw mrr mew meaw mrr mEEEwr mew meeaw mEEEwr meaw meow mrr meaw mrr awr meaw meeaw brr meaw mrr mEEEwr mew meeaw mEEEwr meaw meeaw brr meaw mrr mEEEwr meaw mrr mrr meaw mrr awr meaw meeaw awr mew meeaw mEEEwr meaw meeaw meeaw meaw meow mrr meaw meeaw mrr mew meeaw mEEEwr meaw meow mew meaw meeaw mrr meaw mrr awr meaw meeaw mEEEwr meaw meow mew meaw mrr mrr mew meeaw mEEEwr meaw meeaw meow meaw mrr mEEEwr meaw meow meow meaw meeaw ssh meaw mrr awr meaw mrr mew meaw meaw ssh meaw meeaw mew mew meeaw mEEEwr meaw meaw ssh meaw meeaw mrr meaw mrr meaw mew meeaw mEEEwr meaw meaw brr meaw mrr mrr meaw mrr mEEEwr meaw meaw ssh meaw meow meaw meaw mrr awr meaw meeaw meeaw meaw meeaw awr meaw meaw ssh meaw meeaw mew mew meeaw mEEEwr meaw mrr mew meaw mrr mEEEwr meaw meaw ssh meaw meeaw awr meaw meaw ssh meaw mrr mew meaw meeaw brr meaw mrr mrr meaw meeaw awr meaw mrr awr meaw meeaw ssh meaw meeaw brr meaw mrr awr meaw mrr mew meaw meeaw ssh mew mEEEwr meaw mew meeaw ssh mew meaw meaw "

# Split the string into a list of words
words = string.split()
print(len(words))
distinct_words = list(set(words))
print(distinct_words)
print(len(distinct_words))
perms = permutations(distinct_words)
ctr = 0
for perm in perms:
    word_to_num = {word: i for i, word in enumerate(perm)}
    encoded_str = "".join(str(word_to_num[word]) for word in words)
    text = int(encoded_str, 9)
    decoded_str = long_to_bytes(text)
    if b"JCTF" in decoded_str or b"jctf" in decoded_str:
        print(decoded_str)
        break
    print(decoded_str)
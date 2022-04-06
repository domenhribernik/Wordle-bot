import nltk
# nltk.download()
from nltk.corpus import words
from nltk.corpus import brown
freqs = nltk.FreqDist([w.lower() for w in brown.words()])
word_list = sorted(words.words(), key=lambda x: freqs[x.lower()], reverse=True)
# word_list = words.words()
arr = []
for word in word_list:
  if len(word) == 5:
    arr.append(word.lower())
arr_set = set(arr)
# 9972 words
print(len(arr_set))
# import nltk
# nltk.download()

from nltk.corpus import words
word_list = words.words()
# prints 236736
print (len(word_list))
arr = []
for word in word_list:
  if len(word) == 5:
    arr.append(word.lower())
print(len(arr))
arr_set = set(arr)
print(len(arr_set))

for word in arr_set:
  if len(word) == 5:
    if word[0] == 't' or word[0] == 'e' or word[0] == 'r' or word[0] == 'o' or word[0] == 'p':
      if word[1] == 't' or word[1] == 'e' or word[1] == 'r' or word[1] == 'o' or word[1] == 'p':
        if word[2] == 'o':
          if word[3] == 'p':
            if word[3] == 't' or word[3] == 'e' or word[3] == 'r' or word[3] == 'o' or word[3] == 'p':
              print(word)
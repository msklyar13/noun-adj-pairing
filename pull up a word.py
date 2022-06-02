# coding=utf-8
import re

noun_adj_dict = {}
with open('noun_adj_dict.txt', 'r', encoding='utf-8') as f:
    for line in f:
        num_words = 0
        words = line.split()
        num_words += len(words)
        if num_words >= 2:
            key = line.split(': ')[0]
            val = line.split(': ')[1].strip('\n').split(', ')
            noun_adj_dict[str(key)] = val
        else:
            key = line.split(': ')[0]
            val = line.split(': ')[1].strip('\n')
            noun_adj_dict[str(key)] = val

def pull_up_adj(word, dictionary):
    if word in dictionary:
        return dictionary[word]
    else:
        return 'Слово відсутнє в словнику.'

def adj_frequency(word, dictionary):
    f = 0
    if word in dictionary:
        adj = input ('Введіть прикметник, що вас цікавить: ')
        for item in dictionary[word]:
            f = f + 1
        adj_f = round(dictionary[word].count(adj) / f, 2)
        return str('Частота прикметника ' + adj + ': ' + str(adj_f))
    else:
        return 'Прикметники до слова відсутні.'

word_req = input ('Введіть слово для пошуку: ')
print(pull_up_adj(word_req, noun_adj_dict))
print(adj_frequency(word_req, noun_adj_dict))

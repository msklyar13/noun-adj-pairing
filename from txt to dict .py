# coding=utf8
import re
import pymorphy2
morph = pymorphy2.MorphAnalyzer(lang='uk')
import stanza
nlp = stanza.Pipeline(lang='uk', processors='tokenize,mwt,pos,lemma,depparse')

file = open('input_text.txt', encoding='utf-8')
text = file.read().replace('\n', ' ')
file.close()
doc = nlp(text)

#read whatever's already in the .txt dictionary
noun_adj_dict = {}
with open('noun_adj_dict.txt') as f:
    for line in f:
        num_words = 0
        words = line.split()
        num_words += len(words)
        if num_words > 2:
            key = line.split(': ')[0]
            val = line.split(': ')[1].strip('\n').split(', ')
            noun_adj_dict[str(key)] = val
        else:
            key = line.split(': ')[0]
            val = line.split(': ')[1].strip('\n')
            noun_adj_dict[str(key)] = val

#assemble noun-adjectives pairs into dict, avoid repeated keys
def set_key(dictionary, key, value):
    if key not in dictionary:
        dictionary[key] = value
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]

#def gender
def gender(word):
    p = morph.parse(word)[0]
    properties = str(p.tag)
    base_gender = re.compile('masc|femn|neut|plur')
    match_obj = base_gender.search(properties)
    if match_obj == None:
        pass
    else:
        return match_obj.group()

#adjust the gender of adj to noun
def adjust_gender (nn, adj_to_change):
    if gender(nn) == 'masc':
        return adj_to_change
    elif gender(nn) == 'plur':
        plur_adj = re.sub('ий', 'і', adj_to_change)
        return plur_adj
    elif adj_to_change.endswith('ий'):
        if gender(nn) == 'femn':
            femn_adj = re.sub('ий', 'а', adj_to_change)
            return femn_adj
        elif gender(nn) == 'neut':
            neut_adj = re.sub('ий', 'е', adj_to_change)
            return neut_adj
    elif adj_to_change.endswith('ій'):
        if gender(nn) == 'femn':
            femn_adj = re.sub('ій', 'я', adj_to_change)
            return femn_adj
        elif gender(nn) == 'neut':
            neut_adj = re.sub('ій', 'є', adj_to_change)
            return neut_adj
    else:
        pass

answer = [f'id: {word.id}\tword: {word.text}\tlemma: {word.lemma}\thead id: {word.head}\thead: {sent.words[word.head-1].text if word.head > 0 else "root"}\tdeprel: {word.deprel}' for sent in doc.sentences for word in sent.words]

for item in answer:
    if 'deprel: amod' in item:
        item_list = re.split(r': ', item)
        adj = re.sub('\\t.*$', '', item_list[3])
        raw_noun = re.sub('\\t.*$', '', item_list[5])

        doc = nlp(raw_noun)
        noun_to_lemma = [f'word: {word.text+" "}\tlemma: {word.lemma}' for sent in doc.sentences for word in sent.words]
        for element in noun_to_lemma:
            element_list = re.split(r': ', element)
            noun = element_list[-1]
        adj = adjust_gender(noun, adj)

        set_key(noun_adj_dict, noun, adj)

'''print(noun_adj_dict)'''

with open('noun_adj_dict.txt', 'w', encoding="utf-8") as f:
#with open('noun_adj_dict.txt', 'w', encoding="utf-8") as f:
    for item in noun_adj_dict.items():
        for subitem in item:
            if isinstance(subitem, list):
                list_item = list(item)
                list_item[1] = ', '.join(str(word) for word in subitem)
                item = tuple(list_item)
            else:
                pass
        print(': '.join([str(s) for s in item]), file=f)

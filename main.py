# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import nltk
from nltk import pos_tag
nltk.download('averaged_perceptron_tagger')
from nltk import RegexpParser
import re
import spacy
from spacy.matcher import Matcher
import textacy

# Load English tokenizer, tagger, parser and NER
nlp = spacy.load("en_core_web_sm")

file_name = "tectonic_plates.txt"

file_text = open(file_name).read()
doc = nlp(file_text)
from spacy.util import filter_spans

sentences = list(doc.sents)

print("Number of sentences in file: " + str(len(sentences)))


# sentences = re.split('!|\.|\?', text)

# for sentence in sentences:
#     print(sentence)


    # tokens_tag = pos_tag(sentence)
    # print(tokens_tag)




# Analyze syntax
print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])


patterns=[{'POS': 'VERB', 'OP': '?'},
 {'POS': 'ADV', 'OP': '*'},
 #{'OP': '*'}, # additional wildcard - match any text in between
 {'POS': 'VERB', 'OP': '+'}]

# instantiate a Matcher instance
matcher = Matcher(nlp.vocab)
matcher.add("Verb phrase", [patterns])

# call the matcher to find matches
matches = matcher(doc)
spans = [doc[start:end] for _, start, end in matches]

print("Verb phrases: ")
print(filter_spans(spans))





# Find named entities, phrases and concepts
for entity in doc.ents:
    print(entity.text, entity.label_)



# tokens_tag = pos_tag(text)
# print("After Token:",tokens_tag)
#patterns= """mychunk:{<NN.?>*<VBD.?>*<JJ.?>*<CC>?}"""
#chunker = RegexpParser(patterns)
#print("After Regex:",chunker)
#output = chunker.parse(tokens_tag)
#print("After Chunking",output)
# print(tokens_tag)


# split_sentence = ['This', 'is', 'a', 'sample', 'sentence']
# tag = nltk.pos_tag(split_sentence)
# print(tag)

#Output: [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('sample', 'JJ'), ('sentence', 'NN')]

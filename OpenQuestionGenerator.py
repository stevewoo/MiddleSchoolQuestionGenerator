import nltk
from nltk import pos_tag
nltk.download('averaged_perceptron_tagger')
from nltk import RegexpParser
import re
import spacy
from spacy.util import filter_spans
from spacy.matcher import Matcher
import textacy
from collections import Counter



class OpenQuestionGenerator:

    def __init__(self):
        self.text = "not set"

    def load_text_string(self, text):
        self.text = text

    def load_text_from_file(self, file_name):

        file_text = open(file_name).read()
        self.text = file_text

    def generate_questions(self, number_of_questions):

        # Load English tokenizer, tagger, parser and NER
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(self.text)

        sentences = list(doc.sents)
        print("Number of sentences: " + str(len(sentences)))

        # get most common words (from: https://spacy.io/usage/spacy-101)
        words = [token.text for token in doc
            if not token.is_stop and not token.is_punct]

        word_frequency = Counter(words)

        common_words = word_frequency.most_common(5)

        print("Common: " + str(common_words))


        print("Hot words:")
        print(get_hotwords(self.text, nlp))


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

        extract_svo(doc)





        # Find named entities, phrases and concepts
        for entity in doc.ents:
            print(entity.text, entity.label_)


        sentences_SVO = []
        SVO = []

        #get token dependencies from https://stackoverflow.com/questions/37297399/subject-object-identification-in-python
        for text in doc:
            subject = ""
            indirect_object = ""
            direct_object = ""

            # subject would be
            if text.dep_ == "nsubj":
                subject = text.orth_
            # iobj for indirect object
            if text.dep_ == "iobj":
                indirect_object = text.orth_
            # dobj for direct object
            if text.dep_ == "dobj":
                direct_object = text.orth_



            SVO = [subject, indirect_object, direct_object]

            #print(SVO)

            sentences_SVO.append(SVO)

            # print(subject)
            # print(direct_object)
        # print(indirect_object)







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



def extract_svo(doc): # from https://github.com/Dimev/Spacy-SVO-extraction/blob/master/main.py


    # object and subject constants
    OBJECT_DEPS = {"dobj", "dative", "attr", "oprd"}
    SUBJECT_DEPS = {"nsubj", "nsubjpass", "csubj", "agent", "expl"}
    # tags that define wether the word is wh-
    WH_WORDS = {"WP", "WP$", "WRB"}

    sub = []
    at = []
    ve = []
    for token in doc:
        # is this a verb?
        if token.pos_ == "VERB":
            ve.append(token.text)
        # is this the object?
        if token.dep_ in OBJECT_DEPS or token.head.dep_ in OBJECT_DEPS:
            at.append(token.text)
        # is this the subject?
        if token.dep_ in SUBJECT_DEPS or token.head.dep_ in SUBJECT_DEPS:
            sub.append(token.text)

    print("Subjects: ")
    print(sub)
    print("Verbs: ")
    print(ve)
    print("Objects: ")
    print(at)
    #return " ".join(sub).strip().lower(), " ".join(ve).strip().lower(), " ".join(at).strip().lower()


# from https://betterprogramming.pub/extract-keywords-using-spacy-in-python-4a8415478fbf
def get_hotwords(text, nlp):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
    doc = nlp(text.lower()) # 2

    for token in doc:
        # 3
        if(token.text in nlp.Defaults.stop_words ):#or token.text in punctuation):
            continue
        # 4
        if(token.pos_ in pos_tag):
            result.append(token.text)

    return Counter(result).most_common(10) # 5





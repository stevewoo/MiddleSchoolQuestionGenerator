import string

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
        self.question_list = [] #[(question, target_text, sentence_number)]

    def load_text_string(self, text):
        self.text = text

    def load_text_from_file(self, file_name):

        file_text = open(file_name).read()
        self.text = file_text

    def add_question(self, question_text, target_text, sentence_number):
        self.question_list.append((question_text, target_text, sentence_number))

    def test_me(self):

        print("Tester!")

    def generate_questions(self, number_of_questions):

        # Load English tokenizer, tagger, parser and NER
        nlp = spacy.load("en_core_web_md")
        doc = nlp(self.text)

        self.add_question("Is this a sample question?", "Sample target", 0)

        sentences = list(doc.sents)
        print("Number of sentences: " + str(len(sentences)))

        # get topic(s)
        print("Hot words:")
        hot_words = get_hotwords(self.text, nlp, 5)
        print(hot_words)


        # match questions with most important words


        # generate question for each sentence

        #sentences = [sentences[0]]



        for sentence_number in range(len(sentences)):

            sentence = sentences[sentence_number]
            print("\n" + str(sentence))



            noun_phrases = [chunk.text for chunk in sentence.noun_chunks]

            # for token in sentence:
            #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)



            # define main concepts
            for hot_word in hot_words:
                for noun_phrase in noun_phrases:
                    if hot_word in noun_phrase:
                        #print(hot_word + " is found in nounphrase:" + noun_phrase)
                        question = "Understand: How would you define " + str.lower(noun_phrase) + "?"
                        question_target = noun_phrase
                        self.add_question(question, question_target, sentence_number)

                        question = "Understand: How would you describe " + str.lower(noun_phrase) + "?"
                        question_target = noun_phrase
                        self.add_question(question, question_target, sentence_number)


            # entity questions
            # extract named entities, phrases and concepts
            for entity in sentence.ents:
                print(entity.text, entity.label_)

                # locations
                if entity.label_ is "LOC":
                    question = "Remember: Where is " + entity.text + "?"
                    question_target = entity.text
                    self.add_question(question, question_target, sentence_number)

                # Persons
                elif entity.label_ is "PERSON":
                    question = "Remember: Who is " + entity.text + "?"
                    question_target = entity.text
                    self.add_question(question, question_target, sentence_number)

                    question = "Apply: What questions would you ask " + entity.text + "?"
                    question_target = entity.text
                    self.add_question(question, question_target, sentence_number)

                # Organisation
                elif entity.label_ is "ORG":
                    question = "Understand: What are the goals of " + entity.text + "?"
                    question_target = entity.text
                    self.add_question(question, question_target, sentence_number)












            # tokens_tag = pos_tag(sentence)
            # print(tokens_tag)





        return self.question_list










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
def get_hotwords(text, nlp, number_of_hotwords):
    result = []
    pos_tag = ['PROPN', 'ADJ', 'NOUN'] # 1
    doc = nlp(text.lower())

    for token in doc:
        if(token.text in nlp.Defaults.stop_words ):#or token.text in punctuation):
            continue
        if(token.pos_ in pos_tag):
            result.append(token.lemma_) # or token.text?

    hotword_counts = Counter(result).most_common(number_of_hotwords)
    print(hotword_counts)

    hotwords = [x[0] for x in hotword_counts]

    return hotwords






def other_stuff():
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

import random
import string
import nltk
from nltk import pos_tag
#nltk.download('averaged_perceptron_tagger')
from nltk import RegexpParser
import re
import spacy
from spacy.util import filter_spans
from spacy.matcher import Matcher
from spacy.tokenizer import Tokenizer
from spacy.attrs import POS
from collections import Counter
from spacy_wordnet.wordnet_annotator import WordnetAnnotator
from nltk.corpus import wordnet

from wordfreq import word_frequency

import bs4 as bs
import urllib.request
import re
import json
from transformers import T5Config, T5ForConditionalGeneration, T5Tokenizer

class OpenQuestionGenerator:

    def __init__(self):
        self.text = "not set"
        self.question_set = set()
        self.question_list = [] #[(question, target_text, sentence_number, allow_duplicate)]

        # setup question gen model
        model_name = "allenai/t5-small-squad2-question-generation"
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)

    def load_text_from_string(self, text):
        self.text = text

    def load_text_from_file(self, file_name):
        print("Loading from file: " + file_name)

        file_text = open(file_name).read()
        self.text = file_text

    def load_from_URL(self, URL): # from https://stackabuse.com/text-summarization-with-nltk-in-python
        print("Loading from URL: " + str(URL))

        scraped_data = urllib.request.urlopen(URL)
        article = scraped_data.read()

        parsed_article = bs.BeautifulSoup(article,'lxml')

        paragraphs = parsed_article.find_all('p')

        article_text = ""

        for p in paragraphs:
            article_text += p.text

        # Removing Square Brackets and Extra Spaces in wikipedia pages
        article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)
        article_text = re.sub(r'\s+', ' ', article_text)

        self.text = article_text

    def add_question(self, bloom_level, question_text, target_text, sentence_number, allow_duplicate):

        question = (question_text, target_text, sentence_number, bloom_level)

        # if uncustomised without article words, allow duplicates
        if allow_duplicate:
            self.question_list.append(question)

        # use set to prevent duplicates
        elif question_text not in self.question_set:
            self.question_set.add(question_text)
            self.question_list.append(question)

    def test_me(self):

        print("Tester!")

        # get all synonyms (no domain knowledge)
        # for syn in wordnet.synsets("good"):
        #     for name in syn.lemma_names():
        #         print(name)

        # Load an spacy model (you need to download the spacy pt model)
        #nlp = spacy.load("en_core_web_md")

    def run_model(self, input_string, **generator_args):
        input_ids = self.tokenizer.encode(input_string, return_tensors="pt")
        res = self.model.generate(input_ids, **generator_args)
        output = self.tokenizer.batch_decode(res, skip_special_tokens=True)
        #print(output)
        return(output)

    def generate_questions(self, number_of_questions):

        # Load English tokenizer, tagger, parser and NER
        nlp = spacy.load("en_core_web_md")
        doc = nlp(self.text)
        tokenizer = Tokenizer(nlp.vocab)

        vocab_difficulty_threshold = 0.000007



        #self.add_question("Understand: Is this a sample question?", "Sample target", 0, False)

        sentences = list(doc.sents)
        print("Number of sentences: " + str(len(sentences)))

        # get topic(s)
        print("Hot words:")
        hot_words = get_hotwords(self.text, nlp, 5)

        #sentences = [sentences[0], sentences[1], sentences[2]] # for debugging

        # generate question for each sentence
        for sentence_number in range(len(sentences)):

            sentence = sentences[sentence_number]
            sentence_no_stop_no_punct = [token for token in sentence if not (token.is_stop or token.is_punct)]
            #sentence_no_punct = [token for token in sentence if not token.is_punct]
            tokens = tokenizer(str(sentence))
            #print("Tokens: " + str(list(tokens)))
            #print("\n" + str(sentence))


            # only do every n sentence to improve speed
            # ai question generator from
            # https://huggingface.co/allenai/t5-small-squad2-question-generation/blob/main/README.md
            if sentence_number % 1 == 0:

                #print("Hugging face:")

                # remove brackets
                #sentence = sentence.replace('(','').replace(')','')
                #print(sentence)
                question = self.run_model(str(sentence))

                question = "Understand: " + question[0] # is this safe?
                print(question)
                question_target = str(sentence)
                self.add_question(2.5, question, question_target, sentence_number, False)

            noun_phrases = [chunk for chunk in sentence.noun_chunks] # was [chunk.text for chunk in sentence.noun_chunks]

            # for token in sentence:
            #     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

            # define / decribe main concepts
            for hot_word in hot_words:
                for noun_phrase in noun_phrases:
                    if hot_word in noun_phrase.text:

                        #print(hot_word + " is found in nounphrase:" + noun_phrase)
                        question = "Understand: How would you define `" + noun_phrase.text + "`?"
                        question_target = noun_phrase
                        self.add_question(2, question, question_target, sentence_number, False)

                        question = "Understand: How would you describe `" + noun_phrase.text + "`?"
                        question_target = noun_phrase
                        self.add_question(2, question, question_target, sentence_number, False)

                        question = "Understand: How would you explain `" + noun_phrase.text + "`?"
                        question_target = noun_phrase
                        self.add_question(2, question, question_target, sentence_number, False)

                        question = "Understand: What does `" + noun_phrase.text + "` mean?"
                        question_target = noun_phrase
                        self.add_question(2, question, question_target, sentence_number, False)

            # define difficult words
            difficult_words = []

            for token in sentence_no_stop_no_punct:

                if token.pos_ == "NOUN" or token.pos_ == "VERB" or token.pos_ == "ADJ" or token.pos_ == "ADV":
                    if word_frequency(token.lemma_, 'en') < vocab_difficulty_threshold:
                        difficult_words.append(token)

            # print("Difficult words:")
            # print(difficult_words)
            for token in difficult_words:
<<<<<<< HEAD
                question = "Understand: What is the meaning of the word '" + token.text + "'?"
=======
                question = "Understand: What is the meaning of the word " + token.text + "?"
>>>>>>> 3899fb89b4fca2da5aa6e9d5d8d54c9d616610f3
                question_target = token.text
                self.add_question(2, question, question_target, sentence_number, False)

            # compare / relations - one (with wordnet) # https://pypi.org/project/spacy-wordnet/
            #sentence = self.get_synonyms(nlp, sentence)

            # extract nouns
            # nouns = []
            #
            # for token in sentence: # collect nouns
            #     if token.pos_ == "NOUN":
            #         nouns.append(token)
            #
            # for hot_word in hot_words:
            #     for noun_b in nouns:
            #         if hot_word != noun_b.text:
            #             question = "Analyse: What is the connection between " + hot_word + " and " + noun_b.text +"?"
            #             question_target = str(sentence)
            #             self.add_question(question, question_target, sentence_number, False)

            # entity questions
            # extract named entities: locations, persons, organisations
            org = None
            person = None

            for entity in sentence.ents:

                #print(entity.text, entity.label_)
                # locations
                if entity.label_ == "LOC":
                    question = "Remember: Where is " + entity.text + "?"
                    question_target = entity.text
                    self.add_question(1, question, question_target, sentence_number, False)

                    question = "Remember: Have you ever been to " + entity.text + "?"
                    question_target = entity.text
                    self.add_question(1, question, question_target, sentence_number, False)

                # Persons
                elif entity.label_ == "PERSON":

                    question = "Remember: Who is " + entity.text + "?"
                    question_target = entity.text
                    self.add_question(1, question, question_target, sentence_number, False)

                    question = "Apply: What questions would you ask " + entity.text + "?"
                    question_target = entity.text
                    self.add_question(3, question, question_target, sentence_number, False)

                    if org:
                        question = "Analyse: What is the relationship between " + entity.text + " and " + org.text + "?"
                        question_target = entity.text
                        self.add_question(4, question, question_target, sentence_number, False)


                    if person and person.text not in entity.text:
                        question = "Analyse: Describe the relationship between " + person.text + " and " + entity.text + "?"
                        question_target = entity.text
                        self.add_question(4, question, question_target, sentence_number, False)

                    person = entity # store for next person / org

                # Organisation
                elif entity.label_ == "ORG":

                    question = "Understand: What are the goals of " + entity.text + "?"
                    question_target = entity.text
                    self.add_question(2, question, question_target, sentence_number, False)

                    if person:
                        question = "Analyse: Describe the relationship between " + person.text + " and " + entity.text + "?"
                        question_target = entity.text
                        self.add_question(4, question, question_target, sentence_number, False)

                    org = entity # store it for next person

            # specific keywords

            # problem / issue / dilemma / crisis
            problem_keywords = ["problem", "issue", "crisis", "dilemma"]

            for word in problem_keywords:
                if word in str(sentence):

                    question = "Create: What would you suggest to solve this?"
                    question_target = str(sentence)
                    self.add_question(6, question, question_target, sentence_number, True)

                    question = "Create: What possible solutions do you see here?"
                    question_target = str(sentence)
                    self.add_question(6, question, question_target, sentence_number, True)

                    question = "Create: What changes would you make to solve this?"
                    question_target = str(sentence)
                    self.add_question(6, question, question_target, sentence_number, True)

            # desire / want to / trying to
            if "want" in str(sentence) or "desire" in str(sentence) or "trying to" in str(sentence):
                question = "Analyse: What could be the motivation here?"
                question_target = str(sentence)
                self.add_question(4, question, question_target, sentence_number, True)

            # solution
            if "solution" in str(sentence) or "solve" in str(sentence) or "fix" in str(sentence):
                question = "Evaluate: What are the alternatives?"
                question_target = str(sentence)
                self.add_question(5, question, question_target, sentence_number, True)

            # due to
            if "due to" in str(sentence):
                question = "Analyse: What other reasons can you think of?"
                question_target = str(sentence)
                self.add_question(4, question, question_target, sentence_number, True)

            # process
            if "process" in str(sentence) or "development" in str(sentence) or "method" in str(sentence) or "technique" in str(sentence):
                question = "Create: How would you demonstrate this?"
                question_target = str(sentence)
                self.add_question(4, question, question_target, sentence_number, True)

            # because
            for token in sentence:
                lower_token = str.lower(token.text)
                if lower_token == "because":
                    question = "Analyse: What other reasons can you think of?"
                    question_target = str(sentence)
                    self.add_question(4, question, question_target, sentence_number, True)

            # opinion language
            for opinion_phrase in opinion_vocab:
                if opinion_phrase in str(sentence):

                    question = "Evaluate: Do you believe this? Why or why not?"
                    question_target = str(sentence)
                    self.add_question(5, question, question_target, sentence_number, True)

                    question = "Evaluate: Is this fact or opinion?"
                    question_target = str(sentence)
                    self.add_question(5, question, question_target, sentence_number, True)

                    question = "Evaluate: How could you verify this?"
                    question_target = str(sentence)
                    self.add_question(5, question, question_target, sentence_number, True)

                    question = "Evaluate: What is the evidence supporting this?"
                    question_target = str(sentence)
                    self.add_question(5, question, question_target, sentence_number, True)

        print("Total questions generated: " + str(len(self.question_list)))

        # try to even out bloom_levels
        remember_questions = 0
        understand_questions = 0
        understand_hf_questions = 0
        apply_questions = 0
        analyse_questions = 0
        evaluate_questions = 0
        create_questions = 0

        max_questions_per_bloom_level = 10

        spread_questions  = []

        for question in self.question_list:

            if question[3] == 1 and remember_questions < max_questions_per_bloom_level:
                remember_questions += 1
                spread_questions.append(question)
            elif question[3] == 2 and understand_questions < max_questions_per_bloom_level:
                understand_questions += 1
                spread_questions.append(question)
            elif question[3] == 2.5 and understand_hf_questions < max_questions_per_bloom_level:
                understand_hf_questions += 1
                spread_questions.append(question)
            elif question[3] == 3 and apply_questions < max_questions_per_bloom_level:
                apply_questions += 1
                spread_questions.append(question)
            elif question[3] == 4 and analyse_questions < max_questions_per_bloom_level:
                analyse_questions += 1
                spread_questions.append(question)
            elif question[3] == 5 and evaluate_questions < max_questions_per_bloom_level:
                evaluate_questions += 1
                spread_questions.append(question)
            elif question[3] == 6 and create_questions < max_questions_per_bloom_level:
                create_questions += 1
                spread_questions.append(question)




        #chosen_questions = self.question_list # for debugging

        #chosen_questions = random.sample(self.question_list, number_of_questions)
        if len(spread_questions) <= number_of_questions: # prevent sample error if too few questions
            chosen_questions = spread_questions
        else:
            chosen_questions = random.sample(spread_questions, number_of_questions)

        questions = []

        # make list of dictionaries for json
        for i in range(len(chosen_questions)):

            question_dict = {}

            question = chosen_questions[i]

            question_dict["question"] = str(question[0])#.replace("'", '"')
            question_dict["target"] = str(question[1])#.replace("'", '"')
            #question_dict["sentence_number"] = str("\"" + question[2] + "\"")

            # question_dict["question"] = question[0]
            # question_dict["target"] = question[1]
            question_dict["sentence_number"] = question[2]

            #print(question_dict)

            questions.append(question_dict)




        #print(questions)

        #jsonAll = json.dumps(str(questions))

        # write to file
        # with open('data.json', 'w', encoding='utf-8') as file:
        #     json.dump(str(questions), file, ensure_ascii=False, indent=4)

        #print(jsonAll)

        chosen_questions = questions

        return chosen_questions

    def get_context_synonyms_sentence(self, nlp, sentence):
        if "spacy_wordnet" not in nlp.pipe_names:  # https://blog.dominodatalab.com/natural-language-in-python-using-spacy/
            nlp.add_pipe("spacy_wordnet", after='tagger', config={'lang': nlp.lang})
        text = str(sentence)
        science_domains = ['pure_science', 'applied_science',
                           'social_science']  # https://wndomains.fbk.eu/hierarchy.html
        enriched_sentence = []
        sentence = nlp(text)
        # For each token in the sentence TODO remove verbs
        for token in sentence:
            # We get those synsets within the desired domains
            synsets = token._.wordnet.wordnet_synsets_for_domain(science_domains)
            if not synsets:
                enriched_sentence.append(token.text)
            else:
                lemmas_for_synset = [lemma for s in synsets for lemma in s.lemma_names()]
                # If we found a synset in the economy domains
                # we get the variants and add them to the enriched sentence
                enriched_sentence.append('({})'.format('|'.join(set(lemmas_for_synset))))
        # Let's see our enriched sentence
        print(' '.join(enriched_sentence))
        return sentence

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

def get_synonyms(word): # get all synonyms (no domain knowledge)

    synonyms = []
    for syn in wordnet.synsets(word):
        for name in syn.lemma_names():
            print(name)
            synonyms.append(name)

    return synonyms

opinion_vocab = ["opinion", "important", "point of view", "belief", "would say", "impression", "feeling", "doubt", "guess", "conviction", "agree", "disagree", "incorrect", "think", "share the view", "think", "same mind", "one mind", "wrong", "false", "true", "truth", "argument", "debate", "my view", "certain", "convince", "believe", "likely", "unlikely", "generally accepted", "surprise"]

def old_stuff():
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

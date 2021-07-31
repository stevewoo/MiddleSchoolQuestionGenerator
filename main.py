from OpenQuestionGenerator import OpenQuestionGenerator
from time import perf_counter


def run():

    # create generator agent
    generator = OpenQuestionGenerator()

    # generator.test_me() # for debugging

    # load resource
    resource_load_start = perf_counter()

    file_name = "tectonic_plates.txt"
    #file_name = "ferns_and_ants_work_together.txt"
    generator.load_text_from_file(file_name)

    generator.load_from_URL('https://en.wikipedia.org/wiki/cat')
    resource_load_stop = perf_counter()
    print("Resource load time:", round(resource_load_stop-resource_load_start, 4), " seconds")

    # generate questions
    question_gen_start = perf_counter()
    questions = generator.generate_questions(100)
    question_gen_stop = perf_counter()
    print("Question gen time:", round(question_gen_stop-question_gen_start, 4), " seconds")

    # display questions

    print("## Bloom's level: Question ## Target word(s) or sentence ## Sentence number ##")

    for question in questions:
        print(question)

if __name__ == '__main__':
    run()

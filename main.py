from OpenQuestionGenerator import OpenQuestionGenerator

# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    generator = OpenQuestionGenerator()

    generator.test_me()

    file_name = "tectonic_plates.txt"
    #file_name = "ferns_and_ants_work_together.txt"
    generator.load_text_from_file(file_name)

    questions = generator.generate_questions(3)

    for question in questions:
        print(question)



# See PyCharm help at https://www.jetbrains.com/help/pycharm/


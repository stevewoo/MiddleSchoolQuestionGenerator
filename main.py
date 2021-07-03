from OpenQuestionGenerator import OpenQuestionGenerator

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    generator = OpenQuestionGenerator()

    file_name = "tectonic_plates.txt"
    generator.load_text_from_file(file_name)

    generator.generate_questions(3)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


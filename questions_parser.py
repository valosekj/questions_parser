#######################################################################
#
# Script for converting set of questions and answers from .docx to
# utf8 .txt
#
# USAGE:
#   python questions_parser.py -i input_file.docx -o output_file.txt
#
# Example of input file:
#       1. Some question:
#       Answer I
#       Answer II
#       Answer III (correct answer - written in bold text)
#       Answer IV
#       Answer V
#
# Example of output file:
#       Some question:
#       A. Answer I
#       B. Answer II
#       C. Answer III
#       D. Answer IV
#       E. Answer V
#       ANSWER: C
#
# Correct answer is selected from original answers based on bold text.
# Answers in new file are shown in alphabetical list and correct answer
# is denoted below answers.
# Script also clear multiple spaces in question and answers.
#

# KNOWN BUG:
# - it looks that python-docx package does nut fully support automatic numbering
# https://stackoverflow.com/questions/52094242/is-there-any-way-to-read-docx-file-include-auto-numbering-using-python-docx

#######################################################################
#   Jan Valosek, fMRI laboratory
#######################################################################

import sys
import argparse
import codecs
import re
import os.path
from docx import Document


class QuestionsParser():

    def __init__(self):
        self.counter = 0

    def remove_multiple_spaces(self, input_sentence):
        """
        remove multiple spaces from sentence
        :param input_sentence: str: input sentence which can contain multiple spaces
        :return: str: sentence without multiple spaces
        """
        return re.sub(' +', ' ', input_sentence)

    def remove_single_space(self, input_sentence):
        """
        clear sentence - remove single spaces from input sentence
        this step is better for comparison (finding correct answer)
        # TODO - check if this function can be merged with remove_multiple_spaces function
        :param input_sentence: str: input sentence to be cleared
        :return: str: sentence without any space
        """
        # delete all spaces (sometimes are spaces at unexpected positions -> better to clean them)
        if input_sentence.count(" ") != 0:
            input_sentence = input_sentence.replace(" ", "")

        return input_sentence

    def remove_lowercase_letters(self, input_sentence):
        # if input answers start with lower-case letters, delete them
        return re.sub('[a-e]\s{0,1}[\.\)]\s{0,1}', '', input_sentence)  # delete 'a. ' or 'a . '

    def remove_number(self, input_sentence):
        # if input question starts with number, delete it
        return re.sub('[0-9]{1,2}\s{0,1}\.\s', '', input_sentence)  # delete '5. ' or '5 . '

    def write_paragraph(self, question, answers, bold_sentence, output):
        """
        write parsed (reformatted and cleared) question and answers into utf-8 file
        :param question: str - line containing question
        :param answers: list - all answers
        :param bold_sentence: str - line written in bold (correct answer)
        :param output: name of output .txt file
        :return:
        """
        letters = ["A", "B", "C", "D", "E"]
        correct_answer = str()

        output.write("{}\n".format(question))         # write question to file

        answers_dict = (dict(zip(letters, answers)))  # combine letters and answers into dict
        # loop across answers
        for key, value in answers_dict.items():

            value = self.remove_lowercase_letters(value)        # clear answer
            output.write("{}. {}\n".format(key, value))         # write letter and answer to file

            # FIND correct answer letter (i.e. compare correct answer with all other answers)
            value = self.remove_single_space(value)                  # remove spaces (better for comparison with correct answer)
            bold_sentence = self.remove_lowercase_letters(bold_sentence)        # clear correct answer
            bold_sentence = self.remove_single_space(bold_sentence)                  # remove spaces from correct asnwer
            if bold_sentence == value:  # get letter for correct answer
                #print(bold_sentence)
                correct_answer = key

        output.write("ANSWER: {}\n\n".format(correct_answer))  # write letter for correct answer to file

        # Progress counter
        self.counter += 1
        sys.stdout.write("\rNumber of successfully processed questions: %s" % (self.counter))
        sys.stdout.flush()

        # used for unittest
        return self.counter

    def main(self, argv=None):

        # Get parser args
        parser = self.get_parser()
        self.arguments = parser.parse_args(argv)

        if os.path.isfile(self.arguments.i):
            document = Document(self.arguments.i)
        else:
            sys.exit("ERROR: Input file {} does not exist or path is wrong.".format(self.arguments.i))

        output = codecs.open(self.arguments.o, "w", "utf-8")

        counter = int()
        question = str()
        bold_sentence = str()
        answers = list()

        # Loop across individual lines in input document
        for paragraph in document.paragraphs:

            if paragraph.text != "":                                # check if line != empty
                if paragraph.text[0].isdigit():                     # check if line begins with digit (find question)
                    question = paragraph.text                       # get line containing question
                elif paragraph.runs[0].italic is None:              # exclude chapter titles written in italic
                    answer = self.remove_multiple_spaces(paragraph.text)
                    answers.append(answer)                  # save all other lines to answer list

                    # Loop across individual words in given line
                    for run in paragraph.runs:
                        # Skip line if it is question (sometimes question can be bold, better to skip it)
                        if paragraph.text[0].isdigit():
                            continue
                        if run.bold:                    # extract bold words
                            bold_sentence += run.text   # create line from individual bold words

            # Invoke exception if correct answer is not set (i.e., not set in bold)
            elif bold_sentence == "" and len(answers) == 5:

                sys.exit("\nERROR: Question number {} does not have set correct answer in bold.".
                         format(self.counter + 1))

            # If line is empty (after question and set of answers), call function for writing to file
            # update - there could be space between individual input answers -> added len(answers) condition
            elif paragraph.text is "" and bold_sentence != "" and len(answers) == 5:

                question = self.remove_multiple_spaces(question)
                question = self.remove_number(question)
                bold_sentence = self.remove_multiple_spaces(bold_sentence)

                counter = self.write_paragraph(question, answers, bold_sentence, output)
                answers = list()
                bold_sentence = str()

        output.close()      # close output txt file
        print()  # go to new line when counter finish

        # used for unittest
        return counter


    def get_parser(self):

        parser = argparse.ArgumentParser(
            description='Script for converting set of questions and answers from .docx to utf8 .txt.\n'
                        'Jan Valosek, 2020-2021',
            add_help=False,
            prog=os.path.basename(__file__))

        mandatory = parser.add_argument_group("MANDATORY ARGUMENTS")
        mandatory.add_argument(
            "-i",
            metavar='<input_file>',
            help="Name of existing input .docx file.",
            required=True,
            )
        mandatory.add_argument(
            "-o",
            metavar='<name_of_output_file>',
            help="Name of output .txt file. This file will be created.",
            required=True,
            )

        optional = parser.add_argument_group("OPTIONAL ARGUMENTS")
        optional.add_argument(
            "-h",
            "--help",
            action="help",
            help="Show this help message and exit.")

        return parser


if __name__ == "__main__":
    questions_parser = QuestionsParser()
    questions_parser.main(sys.argv[1:])

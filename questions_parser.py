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
#       1. Some question:
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
#
#######################################################################
#   Jan Valosek, fMRI laboratory, VER=09-04-2020
#######################################################################

import sys
import argparse
import codecs
import os.path
from docx import Document


class QuestionsParser():

    def __init__(self):
        self.counter = 0

    def write_paragraph(self, question, answers, bold_sentence, output):
        """
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
        for key, values in answers_dict.items():
            # if input answers start with lower-case letters, delete them
            if values.startswith('a.') or values.startswith('b.') or values.startswith('c.') or values.startswith('d.') \
                    or values.startswith('e.'):
                output.write("{}. {}\n".format(key, values[3:]))    # write letter and answer to file
            else:
                output.write("{}. {}\n".format(key, values))  # write letter and answer to file

            # FIND correct answer letter (i.e. compare correct answer with all other answers)
            # delete spaces from answers
            if values.count(" ") != 0:
                values = values.replace(" ","")
            # if input answers start with lower-case letters, delete them
            if values.startswith('a.') or values.startswith('b.') or values.startswith('c.') or values.startswith(
                    'd.') or values.startswith('e.'):
                values = values[2:]
            # delete spaces from correct answer
            if bold_sentence.count(" ") != 0:
                bold_sentence = bold_sentence.replace(" ","")
            # if correct answer starts with lower-case letters, delete it
            if bold_sentence.startswith('a.') or bold_sentence.startswith('b.') or bold_sentence.startswith('c.') or \
                    bold_sentence.startswith('d.') or bold_sentence.startswith('e.'):
                bold_sentence = bold_sentence[2:]
            if bold_sentence == values:  # get letter for correct answer
                #print(bold_sentence)
                correct_answer = key

        output.write("ANSWER: {}\n\n".format(correct_answer))  # write letter for correct answer to file

        # Progress counter
        self.counter += 1
        sys.stdout.write("\rNumber of successfully processed questions: %s" % (self.counter))
        sys.stdout.flush()

    def main(self):

        # Get parser args
        parser = self.get_parser()
        self.arguments = parser.parse_args()

        if os.path.isfile(self.arguments.i):
            document = Document(self.arguments.i)
        else:
            sys.exit("ERROR: Input file {} does not exist or path is wrong.".format(self.arguments.i))

        output = codecs.open(self.arguments.o, "w", "utf-8")


        question = str()
        bold_sentence = str()
        answers = list()

        # Loop across individual lines in input document
        for paragraph in document.paragraphs:

            if paragraph.text != "":                                # check if line != empty
                if paragraph.text[0].isdigit():                     # check if line begins with digit (find question)
                    question = paragraph.text                       # get line containing question
                elif paragraph.runs[0].italic is None:              # exclude chapter titles written in italic
                    answers.append(paragraph.text)                  # save all other lines to answer list

                # Loop across individual words in given line
                for run in paragraph.runs:
                    # Skip line if it is question (sometimes question can be bold, better to skip it)
                    if paragraph.text[0].isdigit():
                        continue
                    if run.bold:                    # extract bold words
                        bold_sentence += run.text   # create line from individual bold words

            # If line is empty (after question and set of answers), call function for writing to file
            # update - there could be space between individual input answers -> added len(answers) condition
            elif paragraph.text is "" and bold_sentence != "" and len(answers) == 5:
                self.write_paragraph(question, answers, bold_sentence, output)
                answers = list()
                bold_sentence = str()

        output.close()      # close output txt file
        print()  # go to new line when counter finish


    def get_parser(self):

        parser = argparse.ArgumentParser(
            description='Parser for exam questions. See code for whole help. '
                        'Jan Valosek, 2020',
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
    questions_parser.main()
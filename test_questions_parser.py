#######################################################################
#
# A few tests for questions_parser.py
#
# RUN BY:
#   python -m pytest -v test_questions_parser.py
#######################################################################

import os
from questions_parser import QuestionsParser


def test_remove_multiple_spaces():
    """
    test of removing of multiple spaces
    """
    questions_parser = QuestionsParser()
    assert questions_parser.remove_multiple_spaces('Sentence  with  multiple     spaces') == 'Sentence with multiple spaces'


def test_clear_sentence():
    """
    test of removing single spaces (this step is better for comparison)
    """
    questions_parser = QuestionsParser()
    assert questions_parser.remove_single_space('this is a test answer') == 'thisisatestanswer'


def test_remove_lowercase_letters():
    """
    test of removing lowercase letters at the beginning of answers
    """
    questions_parser = QuestionsParser()
    assert questions_parser.remove_lowercase_letters('a. this is a test answer') == 'this is a test answer'
    assert questions_parser.remove_lowercase_letters('b) this is a test answer') == 'this is a test answer'


def test_check_if_output_file_exists():
    """
    test if output .txt file is created
    """
    input_file = os.path.join(os.getcwd(), 'tests', 'input_test_file.docx')
    output_file = os.path.join(os.getcwd(), 'tests', 'output_test_file.txt')

    questions_parser = QuestionsParser()
    questions_parser.main(argv=['-i', input_file, '-o', output_file])
    assert os.path.exists(output_file)
    os.unlink(output_file)


def test_check_number_of_questions_in_output_file():
    """
    test to check number of questions in output .txt file
    """
    input_file = os.path.join(os.getcwd(), 'tests', 'input_test_file.docx')
    output_file = os.path.join(os.getcwd(), 'tests', 'output_test_file.txt')

    questions_parser = QuestionsParser()
    assert questions_parser.main(argv=['-i', input_file, '-o', output_file]) == 2
    os.unlink(output_file)

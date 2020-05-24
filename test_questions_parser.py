#######################################################################
#
# A few tests for questions_parser.py
#
# RUN BY:
#   python -m pytest -v test_questions_parser.py
#######################################################################

from questions_parser import QuestionsParser

# ---------------------------------
# test of removing of multiple spaces
# ---------------------------------
def test_remove_multiple_spaces_1():
    questions_parser = QuestionsParser()
    assert questions_parser.remove_multiple_spaces('Sentence  with  multiple     spaces') == 'Sentence with multiple spaces'

def test_remove_multiple_spaces_2():
    questions_parser = QuestionsParser()
    assert questions_parser.remove_multiple_spaces('Sentence  with  multiple     spaces') == 'Sentence   with multiple spaces'

# ---------------------------------
# test of removing spaces and initial lower-case letter (this step is better for comparison)
# ---------------------------------
def test_clear_sentence():
    questions_parser = QuestionsParser()
    assert questions_parser.clear_sentence('a. this is  test answer') == 'thisistestanswer'
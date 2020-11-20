## Questions parser
Python script for converting set of questions and answers from .docx format to utf8 .txt format to be compatible with learning management system [Moodle](https://en.wikipedia.org/wiki/Moodle).

#### INSTALL:
clone repository:

`git clone https://github.com/valosekj/questions_parser.git`

`cd questions_parser`

create virtual environment:

OSX:
`python3 -m venv venv`

Linux:
`virtualenv -p /usr/bin/python3 venv`

activate virtual environment:

`source venv/bin/activate`

install required packages:

`pip install -r requirements.txt`

#### REQUIREMENTS:
`python-docx`

#### USAGE:
`python questions_parser.py -i input_file.docx -o output_file.txt`

#### Example of input and output files:
Example of input file (answers can start with lowercase letters):
    
       1. Some question: (question can be in bold text but it is not necessary)
       Answer I
       Answer II
       Answer III (correct answer - written in bold text)
       Answer IV
       Answer V
or
       
       1. Some question: (question can be in bold text but it is not necessary)
       a. Answer I
       b. Answer II
       c. Answer III (correct answer - written in bold text)
       d. Answer IV
       e. Answer V
 or
   
       1. Some question: (question can be in bold text but it is not necessary)
       a) Answer I
       b) Answer II
       c) Answer III (correct answer - written in bold text)
       d) Answer IV
       e) Answer V


 Example of output file:
 
       Some question:
       A. Answer I
       B. Answer II
       C. Answer III
       D. Answer IV
       E. Answer V
       ANSWER: C
       
Question is detected based on the numbering. Correct answer is selected from original answers based on bold text.
Answers in new file are shown in alphabetical list and correct answer is denoted below answers.

#### AUTHOR:
Jan Valosek, fMRI laboratory Olomouc

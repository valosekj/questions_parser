## Questions parser
Python script for converting set of questions and answers from .docx to utf8 .txt

#### INSTALL:
`git clone https://github.com/valosekj/questions_parser.git`

`cd questions_parser`

OSX:
`python3 -m venv venv`

Linux:
`virtualenv -p /usr/bin/python3 venv`

`source venv/bin/activate`

`pip install -r requirements.txt`

#### USAGE:
`python questions_parser.py -i input_file.docx -o output_file.txt`

#### REQUIREMENTS:
`python-docx`

#### Example of input and output files:
Example of input file:
    
       1. Some question:
       Answer I
       Answer II
       Answer III (correct answer - written in bold text)
       Answer IV
       Answer V


 Example of output file:
 
       1. Some question:
       A. Answer I
       B. Answer II
       C. Answer III
       D. Answer IV
       E. Answer V
       ANSWER: C
       
Correct answer is selected from original answers based on bold text.
Answers in new file are shown in alphabetical list and correct answer is denoted below answers.

#### Author:
Jan Valosek, fMRI laboratory Olomouc

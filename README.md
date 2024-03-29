# Questions parser
Python script for converting set of questions and answers from .docx format to utf8 .txt format to be compatible with learning management system [Moodle](https://en.wikipedia.org/wiki/Moodle).

## INSTALL:
1. clone repository:

```console
git clone https://github.com/valosekj/questions_parser.git
cd questions_parser
```

2. create virtual environment, activate it and install required packages - manual [here](https://gist.github.com/valosekj/8052b227bd3f439a615a33804beaf37f#venv-enviroment)

## USAGE:

```console
python questions_parser.py -i input_file.docx -o output_file.txt
```

## Example of input and output files:
Example of input file:
    
       1. Some question: (question can be in bold text but it is not necessary)
       Answer I
       Answer II
       Answer III (correct answer - written in bold text)
       Answer IV
       Answer V
or (answers can start with a., b., etc.)
       
       1. Some question: (question can be in bold text but it is not necessary)
       a. Answer I
       b. Answer II
       c. Answer III (correct answer - written in bold text)
       d. Answer IV
       e. Answer V
 or (answers can start with a), b), etc.)
   
       1. Some question: (question can be in bold text but it is not necessary)
       a) Answer I
       b) Answer II
       c) Answer III (correct answer - written in bold text)
       d) Answer IV
       e) Answer V

 
## Example of output file:
 
       Some question:
       A. Answer I
       B. Answer II
       C. Answer III
       D. Answer IV
       E. Answer V
       ANSWER: C
       
Question is detected based on the numbering. Correct answer is selected from original answers based on bold text.
Answers in new file are shown in alphabetical list and correct answer is denoted below answers.

## AUTHOR:
Jan Valosek, fMRI laboratory, Department of Neurology, Palacký University Olomouc and University Hospital Olomouc, Olomouc, Czechia

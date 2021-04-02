'''
Utility functions to add inputs.
'''

import re

def add_input(word, char_to_replace, replacement):
    '''
    This method finds specific strings and replaces them with '<input type="text">'.
    '''
    letters = list(word)
    letters[letters.index(char_to_replace)] = replacement

    for letter in enumerate(letters):

        if char_to_replace in letter[1]:
            letters[letter[0]] = ''

    return letters


def add_leading_spaces(worksheet_text):
    leading_spaces_added = re.sub('\\r\\n', ' \\r\\n', worksheet_text)
    return leading_spaces_added

def transform_to_answers(worksheet, student_answers):
    with_leading_space = add_leading_spaces(worksheet.worksheet.original_text)
    split_worksheet = with_leading_space.split(' ')
    counter_number = -1

    for word in enumerate(split_worksheet):
        thing_to_remove = None
        if '……' in word[1]:
            thing_to_remove = '…'
            counter_number +=1
        elif '__' in word[1]:
            thing_to_remove = '_'
            counter_number +=1
        elif '....' in word[1]:
            thing_to_remove = '.'
            counter_number +=1
        elif '….' in word[1]:
            thing_to_remove = '…'
            counter_number +=1
        elif '.…' in word[1]:
            thing_to_remove = '…'
            counter_number +=1

        if thing_to_remove:
            student_answer = student_answers[counter_number]
            student_answer = f'<span style="font-weight:bold">{student_answer}</span>'

            new_letters = add_input(
                word[1],
                thing_to_remove,
                student_answer,
                )
            split_worksheet[word[0]] = ''.join(new_letters).replace('.', '')


    new_worksheet = ' '.join(split_worksheet)

    return new_worksheet

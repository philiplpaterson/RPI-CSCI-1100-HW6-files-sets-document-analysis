# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 23:15:33 2022

@author: Philip Paterson
HW 06

This program compares the sophistication of two documents through different
measures, which it then outputs in formatted data.
"""

# Defining the functions
def remove_non_alpha(word):
    '''
    This function removes characters that are either non-alpha or non-ascii
    from a string, a returns the string without the characters.

    Parameters
    ----------
    word : STR
        The given string.

    Returns
    -------
    new_word : STR
        The given string without characters that are either non-alpha or
        non-ascii.

    '''
    char_list = list(word)
    new_char_list = []
    for char in char_list:
        if char.isalpha() and char.isascii():
            new_char_list.append(char.lower())
    new_word = ''.join(new_char_list)
    return new_word


def associated_words_print(word_list):
    '''
    This functions formats and prints words in a single line, with a single
    space in between.

    Parameters
    ----------
    word_list : LIST
        A list of the the associated words.

    Returns
    -------
    None.

    '''
    for word in word_list:
        print('', word, end= '')
    return


def calc_jaccard(set0, set1):
    '''
    This function calculates the jaccard of two sets, which is the ratio of
    the length of the set formed by the intersection of the two given sets 
    divided by the length of the set formed by the union of the two given
    sets.
    

    Parameters
    ----------
    set0 : SET
        The first given set.
    set1 : SET
        The second given set.

    Returns
    -------
    jaccard : FLOAT
        The jaccard of the two given sets.

    '''
    if len(set0) > 0 and len(set1) > 0:
        jaccard = len(set0 & set1) / len(set0 | set1)
    else:
        jaccard = 0
    return jaccard


def get_words(file_name):
    '''
    This functions parses the words of a file name, with no non-alpha
    characters, that do not match the stop-words provided in the stop.txt 
    file. 

    Parameters
    ----------
    file_name : STR
        The name of the file.

    Returns
    -------
    word_list : LIST
        The list of words matching the aforementioned conditions.

    '''
    # Opening the given file
    f = open(file_name)
    s = f.read()
    old_word_list = s.split()
    # Opening the stop file
    stop_file = open("stop.txt")
    stop_file_content = stop_file.read()
    stop_word_list = set(stop_file_content.split())
    stop_words = set()
    # Modifying the stop words
    for stop_word in stop_word_list:
        new_stop_word = remove_non_alpha(stop_word)
        stop_words.add(new_stop_word)
    # Parsing the word list
    word_list = []
    for word in old_word_list:
        modified_word = remove_non_alpha(word)
        if modified_word != '' and modified_word not in stop_words:
            word_list.append(modified_word)
    # Ending function
    f.close()
    stop_file.close()
    return word_list


def calc_avg_word_len(word_list):
    '''
    This function calculates the average word length of a given list of
    words.

    Parameters
    ----------
    word_list : LIST
        The given list of words.

    Returns
    -------
    avg_word_len : FLOAT
        The average word length.

    '''
    total_chars = 0
    for word in word_list:
        total_chars += len(word)
    avg_word_len = total_chars / len(word_list)
    return avg_word_len


def calc_distinct_word_ratio(word_list):
    '''
    This function calculates the distinct word ratio of a given list of
    words.

    Parameters
    ----------
    word_list : LIST
        The given list of words.

    Returns
    -------
    ratio : FLOAT
        The distinct word ratio.

    '''
    word_set = set(word_list)
    ratio = len(word_set) / len(word_list)
    return ratio


def get_words_with_len(word_list):
    '''
    This function analyzes a given word list and associates the words
    in there with their lengths.

    Parameters
    ----------
    word_list : LIST
        The given list.

    Returns
    -------
    words_lengths : DICT
        A dictionary with the word lengths as keys and sets of the words
        with those lengths as values.

    '''
    words_with_lengths = dict()
    for word in word_list:
        word_len = len(word)
        if word_len > 0:
            if word_len not in words_with_lengths:
                words_with_lengths[word_len] = set()
            words_with_lengths[word_len].add(word)
    words_with_lengths_keys = list(words_with_lengths.keys())
    words_with_lengths_keys.sort()
    words_lengths = dict()
    i = 1
    while i <= words_with_lengths_keys[-1]:
        if i not in words_with_lengths:
            words_lengths[i] = {}
        else:
            words_lengths[i] = words_with_lengths[i]
        i += 1
    return words_lengths


def words_with_len_print(words_with_lengths):
    '''
    This function prints the lengths of words, up to the longest length,
    and the associated words to that length.

    Parameters
    ----------
    words_with_lengths : DICT
        A dictionary with the word lengths as keys and sets of the words
        with those lengths as values.

    Returns
    -------
    None.

    '''
    i = 1
    while i <= max(words_with_lengths):
        print("{0:4d}:{1:4d}:".format(i, len(words_with_lengths[i])), end='')
        associated_words = list(words_with_lengths[i])
        associated_words.sort()
        if len(associated_words) <= 6:
            associated_words_print(associated_words)
        else:
            associated_words_print(associated_words[:3])
            print('', '...', end= '')
            associated_words_print(associated_words[-3:])
        print()
        i += 1
    return
        

def get_pairs(word_list, separation_max, pairs_type):
    '''
    This function gets the word pairs from a word_list, which consists
    of the words that are at and less than the max separation. If the
    pairs_type is "distinct", it returns the distinct pairs. If not, the
    function returns all the pairs.

    Parameters
    ----------
    word_list : LIST
        The given list of words.
    separation_max : INT
        The max separation at and between the words for the word pairs.
    pairs_type : STR
        Specifies whether or not the pairs to be outputted should be
        "distinct".

    Returns
    -------
    pairs : LIST
        A list of the two-tuples of the word pairs.

    '''
    pairs = []
    i = 1
    while i < len(word_list):
        if i < separation_max:
            j = i
        else:
            j = 0
        for n in range(1, separation_max + 1 - j):
            pair = [word_list[i], word_list[i - n]]
            pair.sort()
            pair = tuple(pair)
            if pairs_type == 'distinct': # Determines whether the pairs should be distinct or not
                if pair not in pairs:
                    pairs.append(pair)
            else:
                pairs.append(pair)
        i += 1
    pairs.sort()
    return pairs


def analyze_doc(fname, separation_max):
    '''
    This function analyzes the document with the given file name for
    its sophistication based on five measurements:
        1. Average word length
        2. Ratio of distinct words to total words
        3. The associated word lengths
        4. THe word pairs of the documents
        5. The ratio of distinct word pairs to total word pairs

    Parameters
    ----------
    fname : STR
        The name of the file to analyze.
    separation_max : INT
        The max separation at and between the words for the word pairs.

    Returns
    -------
    fname : STR
        The given file name.
    avg_word_len : FLOAT
        The average word length of the document.
    words : LIST
        The list of proper words in the document.
    associated_words_lengths : DICT
        The dictionary of the word lengths and their associated words.
    distinct_pairs : LIST
        The list of two-tuples of distinct word pairs.

    '''
    # Compiling the data for the document
    words = get_words(fname)
    avg_word_len = calc_avg_word_len(words)
    word_ratio = calc_distinct_word_ratio(words)
    associated_words_lengths = get_words_with_len(words)
    distinct_pairs = get_pairs(words, sep_max, "distinct")
    total_pairs = get_pairs(words, sep_max, "all")
    pair_ratio = len(distinct_pairs) / len(total_pairs)
    
    print("\nEvaluating document", fname)
    print("1. Average word length: {0:.2f}".format(avg_word_len))
    print("2. Ratio of distinct words to total words: {0:.3f}".format(word_ratio))
    print("3. Word sets for document {0}:".format(fname))
    words_with_len_print(associated_words_lengths)
    print("4. Word pairs for document", fname)
    print("  {} distinct pairs".format(len(distinct_pairs)))
    if len(distinct_pairs) > 10:
        for pair in distinct_pairs[:5]:
            print("  {0} {1}".format(pair[0], pair[1]))
        print("  ...")
        for pair in distinct_pairs[-5:]:
            print("  {0} {1}".format(pair[0], pair[1]))
    else:
        for pair in distinct_pairs:
            print("  {0} {1}".format(pair[0], pair[1]))
    print("5. Ratio of distinct word pairs to total: {0:.3f}".format(pair_ratio))
    return (fname, avg_word_len, words, associated_words_lengths, distinct_pairs)


def compare_docs(doc_data_0, doc_data_1):
    '''
    This function compares the sophistication of two documents based on:
        1. Average word length
        2. Overall word use similarity
        3. Word use similarity by length
        4. Word pair similiarity

    Parameters
    ----------
    doc_data_0 : TUPLE
        A tuple of the data from the first document, with the file name,
        average word length, the list of proper words in the document,
        the dictionary of the word lengths and their associated words,
        and the list of distinct pairs.
    doc_data_1 : TYPE
        A tuple of the data from the second document, with the file name,
        average word length, the list of proper words in the document,
        the dictionary of the word lengths and their associated words,
        and the list of distinct pairs.

    Returns
    -------
    None.

    '''
    # Extracting the information from the document data.
    if doc_data_0[1] > doc_data_1[1]:
        more_avg_len = doc_data_0[0]
        less_avg_len = doc_data_1[0]
    else:
        more_avg_len = doc_data_1[0]
        less_avg_len = doc_data_0[0]
    words_set_0 = set(doc_data_0[2])
    words_set_1 = set(doc_data_1[2])
    words_jaccard = calc_jaccard(words_set_0, words_set_1)
    if len(doc_data_0[3]) > len(doc_data_1[3]):
        more_lengths = doc_data_0[3]
        less_lengths = doc_data_1[3]
    else:
        more_lengths = doc_data_1[3]
        less_lengths = doc_data_0[3]
    less_lengths_keys = list(less_lengths.keys())
    less_lengths_keys.sort()
    pairs0 = set(doc_data_0[4])
    pairs1 = set(doc_data_1[4])
    pairs_jaccard = calc_jaccard(pairs0, pairs1)
    # The first three measurements printed
    print("\nSummary comparison")
    print("1. {0} on average uses longer words than {1}".format(more_avg_len, less_avg_len))
    print("2. Overall word use similarity: {0:.3f}".format(words_jaccard))
    print("3. Word use similarity by length:")
    # Calculating and printing the jaccard similarities for each length
    more_lengths_keys = list(more_lengths.keys())
    more_lengths_keys.sort()
    for key in more_lengths_keys:
        if key in less_lengths:
            words_length_jaccard = calc_jaccard(more_lengths[key], less_lengths[key])
        else:
            words_length_jaccard = calc_jaccard(more_lengths[key], {})
        print("{0:4d}: {1:.4f}".format(key, words_length_jaccard))
    
    print("4. Word pair similarity: {0:.4f}".format(pairs_jaccard))
    
    
# Main Body of the Code
if __name__ == "__main__":
    
    # Asking for the Inputs
    fname0 = input("Enter the first file to analyze and compare ==> ").strip()
    print(fname0)
    fname1 = input("Enter the second file to analyze and compare ==> ").strip()
    print(fname1)
    sep_max = input("Enter the maximum separation between words in a pair ==> ").strip()
    print(sep_max)
    sep_max = int(sep_max)
    
    # Acquiring the data for the two documents
    data0 = analyze_doc(fname0, sep_max)
    data1 = analyze_doc(fname1, sep_max)
    
    # Comparing the sophistication of the two documents utilizing the data
    compare_docs(data0, data1)
    
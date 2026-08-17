'''
Adapted from:

Project Namesake: a Python tool for detecting lexical similarity in identifier names

Author: Naser Al Madi (nsalmadi@colby.edu)
Last Modified: August 26, 2022 

Paper Citation: 
Naser Al Madi. 2022. Namesake: A Checker of Lexical Similarity in Identifier Names. 
In Proceedings of The 37th IEEE/ACM International Conference on Automated Software 
Engineering Workshops (ASEW 2022).
'''

import pickle
import eng_to_ipa as p
from fuzzywuzzy import fuzz
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import nltk
#nltk.download('wordnet')
from nltk.corpus import wordnet


def get_orthographic_similarity(name1, name2, lexicon):
    ''' compare orthographic similarity of two identifiers '''

    sum_similarity = 0

    shorter_name = min(len(name1), len(name2))
    longer_name = max(len(name1), len(name2))

    for i in range(shorter_name):

        if name1[i] == name2[i]:
            sum_similarity += 1
        elif lexicon.get(name1[i] + name2[i], -1) != -1:
            sum_similarity += lexicon[name1[i] + name2[i]]

    return ((sum_similarity - (longer_name - shorter_name)) / shorter_name) / longer_name


def get_all_orthographic_similarities(identifiers, lexicon):
    ''' compare orthographic similarity of all identifiers '''

    orthographic_similarity = []
    
    for i in range(len(identifiers)):
        for j in range(i+1, len(identifiers)):
            orthographic_similarity.append((
                                    get_orthographic_similarity(identifiers[i], identifiers[j], lexicon),
                                    identifiers[i],
                                    identifiers[j],
                                    ))
    
    return orthographic_similarity


def get_phonological_similarity(name1, name2):

    name1_ipa = p.convert(name1)
    name2_ipa = p.convert(name2)

    return fuzz.ratio(name1_ipa, name2_ipa) / 100


def  get_all_phonological_similarities(split_identifiers):
    ''' compare phonological similarity of all identifiers '''

    phonological_similarity = []

    for i in range(len(split_identifiers)):
        for j in range(i+1, len(split_identifiers)):
            phonological_similarity.append((
                                    get_phonological_similarity(split_identifiers[i], split_identifiers[j]),
                                    split_identifiers[i],
                                    split_identifiers[j],
                                    ))

    return phonological_similarity


def get_wordnet_similarity(name1, name2):
    ''' compare the meaning of the first variable to the meaning of 
    the second variable returning a value between 0 and 1.
    0 indicates no similarity, 1 indicates identical meanings.
    '''

    # cast to lowercase for readability
    first = name1.lower()
    second = name2.lower()

    # get list of synonyms
    w1 = wordnet.synsets(first)
    w2 = wordnet.synsets(second)
    
    # for calculating final score
    wup_score_list = []
    count = 0
    
    # compare each synonym of first to each synonym of second
    for syn1 in w1:

        for syn2 in w2:
            
            # check that part of speech match
            if syn1.name().split('.')[1] == syn2.name().split('.')[1]:

                score = syn1.wup_similarity(syn2)

                # if score is not None then add it to final score
                if score != None:
                    wup_score_list.append(score)
                    count += 1
    
    result = 0
    
    if len(wup_score_list) == 0:
        result = 0
    else:
        result = max(wup_score_list)

    return result


def get_semantic_similarity(name1, name2, df, x, y):
    ''' compare the semantic similarity of the first variable to the
    semantic similarity of the second variable returning a value
    between 0 and 1. 0 indicates no similarity, 1 indicates identical
    meanings.'''
    
    # check if name1, name2 in df
    if df.isin([name1]).any().any() and df.isin([name2]).any().any(): 
        v1 = [df[name1].to_list()]
        v2 = [df[name2].to_list()]
    
        # if single-letter name use Python2Vec only
        if len(name1) == 1 and len(name2) == 1:
            return cosine_similarity(v1, v2)
        else:
            # if identifier names are multi-letter words use Python2Vec and Wordnet
            return max(cosine_similarity(v1, v2), get_wordnet_similarity(name1, name2))

    else:
        return get_wordnet_similarity(name1, name2)


def get_compound_similarity(sentence1, sentence2, df, x, y):
    """ compute the compound similarity using Wordnet """

    #print(sentence1, sentence2)
    longer = max(len(sentence1), len(sentence2))
    shorter = min(len(sentence1), len(sentence2))

    # cast every word in sentences to lowercase
    sentence1 = [word.lower() for word in sentence1]
    sentence2 = [word.lower() for word in sentence2]

    scores = []

    for i in range(shorter):
        if sentence1[i] == sentence2[i]:
            scores.append(1)
        else:
            scores.append(get_semantic_similarity(sentence1[i], sentence2[i], df, x, y))

    return sum(scores) / (len(scores) + (longer - shorter))


def get_all_semantic_similarities(split_identifiers, df, x, y):
    ''' compare semantic similarity of all identifiers '''

    semantic_similarity = []

    for i in range(len(split_identifiers)):
        for j in range(i+1, len(split_identifiers)):

            # check if either i or j is a list
            if len(split_identifiers[i]) > 1 or len(split_identifiers[j]) > 1:
                # compound variable name
                semantic_similarity.append((
                                    get_compound_similarity(split_identifiers[i], split_identifiers[j], df, x, y),
                                    split_identifiers[i],
                                    split_identifiers[j],
                                    ))               
            else:

                identifier1 = "".join(split_identifiers[i])
                identifier2 = "".join(split_identifiers[j])
                # single token variable name
                semantic_similarity.append((
                                    get_semantic_similarity(identifier1, identifier2, df, x, y),
                                    identifier1,
                                    identifier2,
                                    ))

    return semantic_similarity


def get_identifier_line(name, identifiers_lines):
    ''' get the line of the identifier '''

    for id, line in identifiers_lines:
        if name == id:
            return line


def print_orthographic_warnings(orthographic_similarity, threshold):
    ''' print warnings for orthographic similarity '''

    count = 0

    print("\northographic similarity:")

    for item in orthographic_similarity:
        if item[0] > threshold:
            print(f'{item[1]} and {item[2]} are visually similar.')
            count += 1

    return count

def print_phonological_warnings(phonological_similarity, threshold):
    ''' print warnings for phonological similarity '''

    count = 0

    print("\nphonological similarity:")

    for item in phonological_similarity:
        if item[0] > threshold:
            print(f'{item[1]} and {item[2]} are phonologically similar.')
            count += 1
    
    return count


def print_semantic_warnings(semantic_similarity, threshold):
    ''' print warnings for semantic similarity '''

    count = 0

    print("\nsemantic similarity:")

    for item in semantic_similarity:
        if item[0] > threshold:

            name1, name2 = item[1], item[2]

            if isinstance(item[1], list):
                name1 = "_".join(item[1])

            if isinstance(item[2], list):
                name2 = "_".join(item[2])

            print(f'{name1} and {name2} are similar in meaning.')
            count += 1

    return count


def run_namesake(unique_identifiers, orthographic_threshold = 0.75, phonologic_threshold = 0.75, semantic_threshold = 0.75):
    split_identifiers = []

    # split compound identifiers 
    for s in unique_identifiers:
        split_identifiers.append(s.split('_'))

    lexicon = {}
    # set up a dictionary to store the orthographic similarity
    with open('namesake/letter_lexicon.pickle', 'rb') as handle:
        lexicon = pickle.load(handle)

    # set up Python2vec model
    df = pd.read_json('namesake/blog_model.json')

    # transposing the dataframe
    x = df.T.values
    y = df.columns.tolist()

    # compare orthographic similarity of identifiers
    orthographic_similarity = get_all_orthographic_similarities(unique_identifiers, lexicon)
    print_orthographic_warnings(orthographic_similarity, orthographic_threshold)

    # compare phonological similarity of identifiers
    phonological_similarity = get_all_phonological_similarities(unique_identifiers)
    print_phonological_warnings(phonological_similarity, phonologic_threshold)

    # compare semantic similarity of identifiers
    semantic_similarity = get_all_semantic_similarities(split_identifiers, df, x, y)
    print_semantic_warnings(semantic_similarity, semantic_threshold)
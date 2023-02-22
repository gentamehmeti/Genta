import re
from numpy import dot
from numpy.linalg import norm
#import exisiting libraries

stopwords = {"s", "a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost",
             "alone", "along", "already", "also", "although", "always", "am", "among", "amongst", "amoungst", "amount",
             "an", "and", "another", "any", "anyhow", "anyone", "anything", "anyway", "anywhere", "are", "around", "as",
             "at", "back", "be", "became", "because", "become", "becomes", "becoming", "been", "before", "beforehand",
             "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom", "but",
             "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail",
             "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven", "else", "elsewhere",
             "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few",
             "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found",
             "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he",
             "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself",
             "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "it",
             "its", "itself", "keep", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me",
             "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my",
             "myself", "name", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none",
             "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "on", "once", "one", "only",
             "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own", "part",
             "per", "perhaps", "please", "put", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems",
             "serious", "several", "she", "should", "show", "side", "since", "sincere", "six", "sixty", "so", "some",
             "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take",
             "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter",
             "thereby", "therefore", "therein", "thereupon", "these", "they", "thick", "thin", "third", "this", "those",
             "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward",
             "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was",
             "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas",
             "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever",
             "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your",
             "yours", "yourself", "yourselves", "the"}

def word_checker(w):
    '''
    :param w: word in file
    :return: string, word more than 3 characters length and not in the stopwords list
    '''
    if len(w) >= 3 and w not in stopwords:
        return w

def get_similarity_of_array(result):
    '''
    :param result: get dictionary with keys as a parameter defined as result.
    result is a dictionary of two keys (words being compared), both keys have a dictionary of
    their own, which contain list of all words in the ref sentence.txt. These dictionaries also include indexes,
    which are updated every time a condition is met.
    :return smiliarity value (cosine similarity) between two vectors'''
    for i, item in enumerate(result): #needed an index, to see which word is the first element and which one the second
        if i == 0: #if first element, populate the first_vector with a list of its values
            first_vector = list(result[item].values())
        elif i == 1: #if second element, populate the second_vector with a list of its values
            second_vector = list(result[item].values())

    cos_sim = dot(first_vector , second_vector) / (norm(first_vector) * norm(second_vector)) #calculate cosine similarity formula
    print(cos_sim)

def compare_array(words_to_compare):
    '''
    :param words_to_compare: accept two words only, that you want to compare, two strings
    :return: float value, return the result of cosine similarity
    '''
    if words_to_compare[0] == words_to_compare[1]: #if words are the same you can not compare them
        raise Exception("Sorry, can not compare same words") #raise exeption
    content = open("/Users/gentamehmeti/PycharmProjects/Exercises/Homework1/ref-sentences.txt") #read file
    result = {
        w: {} for w in words_to_compare
    } #created a dictionary with words to compare as keys. These words have their own dictionaries.
    for sentence in content: #iterating through all the content
        lowercase_sentence = re.sub("[.,;':?!]+", "", sentence.lower()) # making all the sentences lowercase and without ., etc.
        array_sentence = lowercase_sentence.split()  #turning the sentence into an array
        for c_word in words_to_compare: #looping through all the words we are comparing (in this case canada and switzerland)
            for word in array_sentence: #looping through all the words in all the sentences
                if word_checker(word): #checking if word that is being iteratated has more than three characters and is not a stopword
                    if word not in result[c_word]: #if word does not exist in the dict of the result[canada]
                        # or result[switzerland] (depending which one we are iterating in)
                        if c_word in array_sentence: #if the iterating word is in a sentence with the compared word (canada or switzerland)
                            result[c_word][word] = 1 #start its value with 1, because the word is already found in the loop
                        else:
                            result[c_word][word] = 0 #if not, start with 0, since its not part of the sentence with canada or switzerland
                    elif c_word in array_sentence and word != c_word: #if the word being iterated is already part of the dict of comparable word
                        # then check if comparable word is in this sentence and the word is different from coparable word (canada or switzerland)
                        # in that case, update the value of the word +1
                        result[c_word][word] += 1

    return get_similarity_of_array(result)

compare_array(["canada", "switzerland"])

# Importing Packages
import math
from nltk import pos_tag
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer

# =======================================================================================================================
# Finding the score from the list of sentences
# =======================================================================================================================


def sentence_scoring(soup, cleaned_sentences, position_score):  # argument as soup_object, sentences_list, positionscore_list_of_sentences in same order
    # =========================================================================================
    # Initialisation parameters for scoring
    # ========================================================================================

    # TfIdf weight calculation for words
    tfidf_vectorizer = TfidfVectorizer(max_df=1.0, min_df=1)
    try:
        tfidf_matrix = tfidf_vectorizer.fit_transform(cleaned_sentences)
    except:
        return None
    tfidf_dense = tfidf_matrix.toarray()  # Creating dense matrix of words and weights
    vocab = tfidf_vectorizer.vocabulary_

    # Creating list of headings
    h1 = list()
    h2 = list()
    h3 = list()
    for title in soup.find_all('h1'):
        h1.append(title.text)
    for heading in soup.find_all('h2'):
        h2.append(heading.text)
    for sub_heading in soup.find_all('h3'):
        h3.append(sub_heading.text)

    # Flattening heading names
    h1 = [x.lower() for y in [word_tokenize(x) for x in h1] for x in y]
    h2 = [x.lower() for y in [word_tokenize(x) for x in h2] for x in y]
    h3 = [x.lower() for y in [word_tokenize(x) for x in h3] for x in y]
    h = h1 + h2 + h3

    # Giving weights for words based on headings
    heading_rank = {'h1': 3, 'h2': 2, 'h3': 1}
    tags_rank = {'NNP': 4, 'NN': 3, 'JJ': 2, 'JJR': 2, 'JJS': 2, 'RB': 1, 'RBR': 1, 'RBS': 1}
    headingscore_list = list()
    tagscore_list = list()
    wordlengthscore_list = list()
    tfidfscore_list = list()
    sentencescore_list = list()

    # ==============================================================================================
    # Calculation of scores
    # ==============================================================================================
    for i, sentence in enumerate(cleaned_sentences):
        word_tokens = word_tokenize(sentence)

        # TF-Idf Score vector
        tfidf_score = [tfidf_dense[i, vocab[word]] if word in list(vocab.keys()) else 0 for word in word_tokens]
        tfidfscore_list.append(tfidf_score)

        # word length weight vector
        total_length = 0

        for word in word_tokens:
            total_length = total_length + len(word)

        wordlength_score = [len(word) / total_length for word in word_tokens]
        wordlengthscore_list.append(wordlength_score)

        # POS Tag score vector
        tagged = pos_tag(word_tokens)
        tags = [indiv_tags[1] for indiv_tags in tagged]
        tags_score = [tags_rank[tag] / len(tags_rank) if tag in list(tags_rank.keys()) else 0 for tag in tags]
        tagscore_list.append(tags_score)

        # Occurrence of heading score vector
        headings_score = list()
        for word in word_tokens:
            if word in h1:
                headings_score.append(heading_rank['h1'] / len(heading_rank))
            elif word in h2:
                headings_score.append(heading_rank['h2'] / len(heading_rank))
            elif word in h3:
                headings_score.append(heading_rank['h3'] / len(heading_rank))
            else:
                headings_score.append(0)
        headingscore_list.append(headings_score)

        # Vector addition of each score vector of sentence and Scalar multiplication of position score
        score = [(tfidf_score[wordnum] + wordlength_score[wordnum] + tags_score[wordnum] + headings_score[wordnum]) *
                 position_score[i] for wordnum in range(len(word_tokens))]  # Calculating Score for individual word

        # Magnitude of the score vector
        sentence_score = 0
        for i in range(len(score)):
            sentence_score += math.pow(score[i], 2)  # Calculating Score for sentence
        sentencescore_list.append(math.sqrt(sentence_score))  # Creating score list for the given list of sentences in the same order

    return sentencescore_list

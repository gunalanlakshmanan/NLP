# Importing packages
import re
import string
from nltk import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from timelinepage import scoring
from timelinepage import temporal_extraction
from timelinepage import wikiscrap


# =================================================================================================================
# Creating timeline from the wikipedia articles
# ===================================================   ===============================================================


def timeline(word, n):
    # Intialisation
    punct = list(string.punctuation)
    punct.remove('-')
    stop_words = stopwords.words('english')
    exclude = ['i', 'he', 'she']
    removals = [word for word in stop_words if
                word not in exclude] + punct  # Removing pronouns and combining punctuation

    soup, sentences_df = wikiscrap.scraping(word)  # Creating Dataframe of sentence and position score and soup object
    if soup == None:
        return [{'sentence':"No article found", 'year':404}]
    position_score = sentences_df['Position Score'].tolist()  # Creating a list of position score

    # Function for Preprocessing of Sentences
    def cleaning(text):
        text = str(text)
        wordnet_lemmetizer = WordNetLemmatizer()
        tokens = word_tokenize(text)
        tokens = [token.lower() for token in tokens]
        tokens = [(wordnet_lemmetizer.lemmatize(token, pos='v')) for token in tokens if token not in removals]
        sentence = " ".join(tokens)
        sentence = re.sub("-", "", sentence)
        sentence = re.sub("\ufeff", "", sentence)
        sentence = re.sub("'s", "", sentence)
        return sentence

    sentences_df['Cleaned_Sentences'] = sentences_df['Original_Sentences'].apply(
        lambda x: cleaning(x))  # Preprocessing of sentences
    cleaned_sentences = sentences_df['Cleaned_Sentences'].tolist()  # Creating a list of cleaned sentences
    sentences_df['sentence_score'] = scoring.sentence_scoring(soup, cleaned_sentences,
                                                              position_score)  # Creating a score column for the sentences
    if sentences_df['sentence_score'].isnull().all():
        return [{'sentence':"Enter specific article", 'year':"Many article found"}]

    sentencesorted_df = sentences_df[
        ['Original_Sentences', 'sentence_score']].copy()  # Copying Original Sentences and the sentence score
    sentencesorted_df = sentencesorted_df.sort_values('sentence_score',
                                                      ascending=False)  # Sorting based on sentence score
    sentencesorted_df = sentencesorted_df.reset_index()
    sorted_sentences = sentencesorted_df['Original_Sentences'].tolist()

    extract_dictlist = temporal_extraction.extract(
        sorted_sentences)  # Extracting the temporal sentences from the sentence list

    best_sentence = extract_dictlist[0:n]  # Extracting the first n(user specified) sentences after sentence ranking
    best_sentence_sorted = sorted(best_sentence, key=lambda i: i['year'])  # Sorting based on chronological order

    best_sentence_list = list()
    for sentence_dict in best_sentence_sorted:
        sentence_year = str(sentence_dict['year']) + ' - ' + str(sentence_dict['sentence'])
        best_sentence_list.append(sentence_year)  # Creating a list of  best sentences with year in chronological order
    if best_sentence_sorted == []:
        return [{'sentence':"Timeline cannot be created for this article name", 'year':"Please enter different article name"}]
    else:
        return best_sentence_sorted

# Importing Packages
import urllib.request
from bs4 import BeautifulSoup
import re
import sys
import pandas as pd


# ========================================================================================================
# Scraping the article data from Wikipedia page and creating Dataframe with sentence and position score
# ========================================================================================================


def scraping(word):
    wiki = "https://en.wikipedia.org/wiki/%s" % word
    try:
        wikipage = urllib.request.urlopen(wiki)  # opening the webpage
    except:
        return None, None

    # Creating a soup object for parsing html data
    soup = BeautifulSoup(wikipage, 'lxml')

    # Getting the paragraph text in the page under each sub headings
    paragraphs = list()
    first_para = str()
    para = soup.find('p')
    for elem in para.next_siblings:  # Getting the paragraph before the starting of sub headings
        if elem.name and elem.name.startswith('h'):
            break
        if elem.name == 'p':
            first_para = first_para + elem.text
    paragraphs.append(first_para)

    for header in soup.find_all('h2'):  # Getting the paragraph under <h2> heading
        heading_para = str()
        for elem in header.next_siblings:
            if elem.name and elem.name.startswith('h2'):
                break
            if elem.name == 'p':
                heading_para = heading_para + elem.text
        if heading_para is not '':
            paragraphs.append(heading_para)

    # Data Pre processing/Data cleaning of paragraphs
    def preprocessing(data):
        data = re.sub(r"\[.*?\]", "", data)
        data = re.sub(r"\(.*?\)", "", data)
        data = re.sub("\n", " ", data)
        data = re.sub(r"\b\w+\.\w+\.[comrgin]+\b", "", data)
        sub_text = re.findall("\w\.\s\w\.\s", data)
        for text in sub_text:
            data = data.replace(text, text.replace('.', ''))
        data = re.sub("\s+", " ", data)
        return data

    # Creating the list of processed paragraphs
    cleaned_paragraphs = list()
    for paragraph in paragraphs:
        cleaned_paragraph = preprocessing(paragraph)
        cleaned_paragraphs.append(cleaned_paragraph)

    # Calculating the position score for each sentence in the paragraphs
    sentence_position = list()
    for paragraph in cleaned_paragraphs:
        sentences = paragraph.split(". ")
        for i, sentence in enumerate(sentences):
            if len(sentence) != 0:
                temp = dict()
                temp['sentence'] = sentence
                temp['position_score'] = (len(sentences) - i) / len(sentences) # calculation of position score [(total sentence-position-1)/total sentence)]
                sentence_position.append(temp)

    # Creating Dataframe to save sentences and position score
    sentence_list = [indiv_dict['sentence'] for indiv_dict in sentence_position]
    position_score = [indiv_dict['position_score'] for indiv_dict in sentence_position]
    sentences_df = pd.DataFrame()
    sentences_df['Original_Sentences'] = sentence_list
    sentences_df['Position Score'] = position_score

    return soup, sentences_df

# Importing packages
import re
import datetime


# =====================================================================================
# Extracting the temporal sentences from the list of sentences
# =====================================================================================

def extract(sentences):  # argument as list of sentences
    extract_sentence = list()

    for i, sentence in enumerate(sentences):

        year_dict = dict()
        current = datetime.datetime.now()
        current_year = int(current.year)

        # Creating Regex patterns for tagging
        week_day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
        month = "(january|february|march|april|may|june|july|august|september| \
                october|november|december)"
        dmy = "(year|day|week|month)"
        rel_day = "(today|yesterday|tomorrow|tonight|tonite)"
        exp2 = "(this|next|last)"
        iso = "\d+[/-]\d+[/-]\d+"
        year = "((?<=\s)\d{4}|^\d{4})"
        regxp2 = "(" + exp2 + " (" + dmy + "|" + week_day + "|" + month + "))"

        reg1 = re.compile(regxp2, re.IGNORECASE)
        reg2 = re.compile(rel_day, re.IGNORECASE)
        reg3 = re.compile(iso)
        reg4 = re.compile(year)

        # Variations of this thursday, next year, etc
        found1 = reg1.search(sentence)
        # today, tomorrow, etc
        found2 = reg2.search(sentence)
        # ISO
        found3 = reg3.search(sentence)
        # Year
        found4 = reg4.search(sentence)

        # Getting the year from the found patterns
        if found1:
            tempo = found1.group()
            if 'year' not in tempo:
                year_dict['year'] = current_year
                year_dict['sentence'] = sentence
            if 'year' in tempo:
                if 'this' in tempo:
                    year_dict['year'] = current_year
                    year_dict['sentence'] = sentence
                if 'last' in tempo:
                    year_dict['year'] = current_year - 1
                    year_dict['sentence'] = sentence
                if 'next' in tempo:
                    year_dict['year'] = current_year + 1
                    year_dict['sentence'] = sentence

        if found2:
            year_dict['year'] = current_year
            year_dict['sentence'] = sentence

        if found3:
            tempo = found3.group()
            year = (re.search(r"\d+[/-]\d+[/-](\d+)", tempo)).group(1)
            year_dict['year'] = int(year)
            year_dict['sentence'] = sentence

        if found4:
            year_dict['year'] = int(found4.group())
            year_dict['sentence'] = sentence

        if not found1 and not found2 and not found3 and not found4:
            continue

        extract_sentence.append(year_dict)  # Creating the dictionary of year and sentences from the extracted sentences

    return extract_sentence

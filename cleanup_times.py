
def string_sim(str1, str2):
    '''
    Crude similarity function for strings.
    Compares letter values at each string's positions and returns a ratio of similarity.
    If the ratio is greater than than a certain threshold, then the function outputs True, else False.
    '''
    
    lst1 = list(str1)
    lst2 = list(str2)
    
    lst1_no_spaces = []
    lst2_no_spaces = []
    
    problem_chars = [" ", "_"]
    
    for elem in lst1:
         if elem not in problem_chars:
            lst1_no_spaces.append(elem)
    
    for elem in lst2:
        if elem not in problem_chars:
            lst2_no_spaces.append(elem)
                
    smaller = min ( len(lst1_no_spaces), len(lst2_no_spaces) )
    
    if smaller == len(lst1_no_spaces):
        smaller_lst = lst1_no_spaces
        larger_lst = lst2_no_spaces
    else:
        smaller_lst = lst2_no_spaces
        larger_lst = lst1_no_spaces
        
    for i in range(len(larger_lst) - len(smaller_lst)):
        smaller_lst.append('X')
                
    count = 0
    
    if smaller > 3:
        for elem1, elem2 in zip(lst1_no_spaces, lst2_no_spaces):
        # print elem1, elem2
            if elem1 == elem2:
                count += 1
    
    return count/float(len(larger_lst)) >= 0.6


def find_similar(dic_values):
    '''
    Function to iterate through dictionary values of [dic_values] to find all
    similar values and print them.
    '''

    count_fun = 0

    for values_1 in dic_values:
        for values_2 in dic_values:
            
            # make sure the strings are alphabetical and start with the same letter: this ensures some smartness
            # in terms of the algorithms
            if (values_1.isalpha() and values_2.isalpha() and values_1 != values_2 and values_1[0] == values_2[0]):
                
                if (count_fun <= NUM_TAGS and string_sim(values_1, values_2)):
                    
                    print "Value 1:", values_1
                    print "Value 2:", values_2
                    count_fun += 1



update_times = {
        '24': "'24/7", # extra apostrophe to prevent conversion of 24/7 to 24 July
        'mo': 'Monday',
        'mon': 'Monday',
        'tu': 'Tuesday',
        'we': 'Wednesday',
        'wed' 'Wednesday'
        'th': 'Thursday',
        'thur': 'Thursday',
        'fr': 'Friday',
        'sa': 'Saturday',
        'sat': 'Saturday',
        'su': 'Sunday',
        'sun': 'Sunday',
        'a.m': 'AM',
        'a.m.': 'AM',
        'am': 'AM',
        'p.m': 'PM',
        'p.m.': 'PM',
        'pm': 'PM',
        'to': '-'
    }


def cleanup_times(word):
    '''
    Function to cleanup the time format as per standards listed in above cells
    '''    
    # separate characters such as '10am' to obtain '10 am' for parsing
    needs_spacing = re.compile('[0-9][a-z]')
    space_pos = needs_spacing.findall(word)
    
    for phrases in space_pos:
        word_pos = word.find(phrases)
        word = word[:word_pos + 1] + " " + word[word_pos + 1:]
        
    # find all instances of 24 hour time and convert them
    time_format = re.compile('[0-9]+:[0-9]+')
    time_lst = time_format.findall(word)

    for times in time_lst:
    
        start = word.find(times)
        length = len(times)
        end = start + length
    
        colon = times.find(":")
        hour_int = int(times[:colon])
        minute_str = times[colon:end]
    
        if hour_int >= 12:
            if hour_int != 12:
                hour_int -= 12
            time_str = str(hour_int)
            time_str += minute_str
        else:
            time_str = str(hour_int)
            time_str += minute_str    
        
        word = word[:start] + time_str + word[end:] 
    
    # separate characters such as '-' from individual words for better parsing
    new_word = ""
    
    for letter_pos in range(len(word)):
    
        if word[letter_pos] in ["-", ","]:
            if word[letter_pos - 1] != " " and word[letter_pos + 1] == " ":
                new_word += " " + word[letter_pos]
            
            elif word[letter_pos - 1] == " " and word[letter_pos + 1] != " ":
                new_word += word[letter_pos] + " "
                
            elif word[letter_pos - 1] != " " and word[letter_pos + 1] != " ":
                new_word += " " + word[letter_pos] + " "
                        
        else:
            new_word += word[letter_pos]
    
    # update words as per dictionary values
    sentence_lst = new_word.split()
    
    answer_lst = []

    
    for words in sentence_lst:
        
        # lower
        words = words.lower()
        
        # check if in dict
        if words in update_times:
            answer_lst.append(update_times[words])
        else:
            answer_lst.append(words)
    
    extra_spaces_word =  " ".join(answer_lst)
    
    final_word = ""
    
    # remove extra spaces fromm commas
    for letter_pos in range(len(extra_spaces_word)):
        if extra_spaces_word[letter_pos] == " " and extra_spaces_word[letter_pos + 1] == ",":
            pass
        elif extra_spaces_word[letter_pos] == "," and extra_spaces_word[letter_pos + 1] != " ":
            final_word += ", "
        
        else:
            final_word += extra_spaces_word[letter_pos]
            
    return final_word

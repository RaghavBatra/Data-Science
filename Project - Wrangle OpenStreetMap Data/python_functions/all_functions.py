# libraries that will be used 

# for SQL connections to the database
import MySQLdb

# for parsing the XML tree (library is built with C) and converting it into the CSV
import xml.etree.cElementTree as ET
import csv
import codecs

# validator library
import cerberus

#validation schema
import schema_osm

# dictionary module for simplifying life
from collections import defaultdict

# pretty printing
import pprint

# regular expressions
import re

# measuring time periods
import time

# osm file to convert
OSM_FILE = 'new-delhi_01.osm'


def view_xml_tags(counter):
    '''
    view [counter] lines of xml_tags
    '''
    
    num_of_lines = 0

    for event, elem in ET.iterparse(OSM_FILE, events=("start",)):
        if (num_of_lines <= counter):
            num_of_lines += 1
            print elem.tag
            print elem.attrib


NUM_TAGS = 10000



def get_keys(num_tags):
    '''
    Function that returns a dictionary of the first [num_tags] 'key' attributes of "tag" tags.
    '''
    
    count = 0
    dic_keys = {} 
    
    if (count <= num_tags):
        for event, elem in ET.iterparse(OSM_FILE, events=("start",)):
            count += 1
            if elem.tag == "tag":
                
                # check if in map
                if 'k' and 'v' in elem.attrib:
                    map_key = elem.attrib['k']
                    if map_key in dic_keys:
                        dic_keys[map_key] += 1
                    else:
                        dic_keys[map_key] = 1
    return dic_keys


def get_values(num_tags):
    '''
    Function that returns a dictionary of the first [num_tags] 'value' attributes of "tag" tags.
    '''

    count = 0
    dic_values = {}

    if (count <= num_tags):
        for event, elem in ET.iterparse(OSM_FILE, events=("start",)):
            count += 1
            if elem.tag == "tag":
                
                # check if in map
                if 'k' and 'v' in elem.attrib:
                    map_key = elem.attrib['v']
                    if map_key in dic_values:
                        dic_values[map_key] += 1
                    else:
                        dic_values[map_key] = 1
                        
    return dic_values


def get_alpha_values(dic):
    '''
    Function that returns a dictionary of only the alphabetical keys of dictionary [dic].
    '''

    dic_alpha = defaultdict(set)
    
    for values in dic:
        values_lower = values.lower()
        if values_lower.isalpha(): 
            first_letter = values_lower[0]
            dic_alpha[first_letter].add(values)

    return dic_alpha


def find_tag(attr_name, search_string, number_of_results = 20, number_of_searches = NUM_TAGS):
    '''
    Function that finds and prints tags whose attribute [attr_name] contains the string [search_string] as long 
    as the number of results is fewer than [number_of_results] and the number of tags searched is 
    fewer than [number_of_searches].
    
    The found tag attributes and its parent tag are printed for ease of access.
    '''
    
    results = 0
    searches = 0
    
    if results < number_of_results and searches < number_of_searches:
        
        for event, elem in ET.iterparse(OSM_FILE, events=("start",)):
            if elem.tag == "node":
                for children in elem:
                    
                # checking the conditions listed in the doc string
                    searches += 1
                    
                    if children.attrib[attr_name].find(search_string) != -1 :
                        
                        print children.attrib
                        print elem.attrib
                        
                        results += 1


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


def fix_extra_a(str1, set_of_values):
    set_of_values.add(str1)
    if str1[-1] == "a" and str1[:-1] in set_of_values:
        return str1[:-1]
    return str1


def format_string_dtc(value):
    return "Delhi Transport Corporation ( DTC )"


"""
After auditing is complete the next step is to prepare the data to be inserted into a SQL database.
To do so you will parse the elements in the OSM XML file, transforming them from document format to
tabular format, thus making it possible to write to .csv files.  These csv files can then easily be
imported to a SQL database as tables.

The process for this transformation is as follows:
- Use iterparse to iteratively step through each top level element in the XML
- Shape each element into several data structures using a custom function
- Utilize a schema and validation library to ensure the transformed data is in the correct format
- Write each data structure to the appropriate .csv files


## Shape Element Function
The function should take as input an iterparse Element object and return a dictionary.

### If the element top level tag is "node":
The dictionary returned should have the format {"node": .., "node_tags": ...}

The "node" field should hold a dictionary of the following top level node attributes:
- id
- user
- uid
- version
- lat
- lon
- timestamp
- changeset
All other attributes can be ignored

The "node_tags" field should hold a list of dictionaries, one per secondary tag. Secondary tags are
child tags of node which have the tag name/type: "tag". Each dictionary should have the following
fields from the secondary tag attributes:
- id: the top level node id attribute value
- key: the full tag "k" attribute value if no colon is present or the characters after the colon if one is.
- value: the tag "v" attribute value
- type: either the characters before the colon in the tag "k" value or "regular" if a colon
        is not present.

Additionally,

- if the tag "k" value contains problematic characters, the tag should be ignored
- if the tag "k" value contains a ":" the characters before the ":" should be set as the tag type
  and characters after the ":" should be set as the tag key
- if there are additional ":" in the "k" value they and they should be ignored and kept as part of
  the tag key. For example:

  <tag k="addr:street:name" v="Lincoln"/>
  should be turned into
  {'id': 12345, 'key': 'street:name', 'value': 'Lincoln', 'type': 'addr'}

- If a node has no secondary tags then the "node_tags" field should just contain an empty list.

The final return value for a "node" element should look something like:

{'node': {'id': 757860928,
          'user': 'uboot',
          'uid': 26299,
       'version': '2',
          'lat': 41.9747374,
          'lon': -87.6920102,
          'timestamp': '2010-07-22T16:16:51Z',
      'changeset': 5288876},
 'node_tags': [{'id': 757860928,
                'key': 'amenity',
                'value': 'fast_food',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'cuisine',
                'value': 'sausage',
                'type': 'regular'},
               {'id': 757860928,
                'key': 'name',
                'value': "Shelly's Tasty Freeze",
                'type': 'regular'}]}

### If the element top level tag is "way":
The dictionary should have the format {"way": ..., "way_tags": ..., "way_nodes": ...}

The "way" field should hold a dictionary of the following top level way attributes:
- id
-  user
- uid
- version
- timestamp
- changeset

All other attributes can be ignored

The "way_tags" field should again hold a list of dictionaries, following the exact same rules as
for "node_tags".

Additionally, the dictionary should have a field "way_nodes". "way_nodes" should hold a list of
dictionaries, one for each nd child tag.  Each dictionary should have the fields:
- id: the top level element (way) id
- node_id: the ref attribute value of the nd tag
- position: the index starting at 0 of the nd tag i.e. what order the nd tag appears within
            the way element

The final return value for a "way" element should look something like:

{'way': {'id': 209809850,
         'user': 'chicago-buildings',
         'uid': 674454,
         'version': '1',
         'timestamp': '2013-03-13T15:58:04Z',
         'changeset': 15353317},
 'way_nodes': [{'id': 209809850, 'node_id': 2199822281, 'position': 0},
               {'id': 209809850, 'node_id': 2199822390, 'position': 1},
               {'id': 209809850, 'node_id': 2199822392, 'position': 2},
               {'id': 209809850, 'node_id': 2199822369, 'position': 3},
               {'id': 209809850, 'node_id': 2199822370, 'position': 4},
               {'id': 209809850, 'node_id': 2199822284, 'position': 5},
               {'id': 209809850, 'node_id': 2199822281, 'position': 6}],
 'way_tags': [{'id': 209809850,
               'key': 'housenumber',
               'type': 'addr',
               'value': '1412'},
              {'id': 209809850,
               'key': 'street',
               'type': 'addr',
               'value': 'West Lexington St.'},
              {'id': 209809850,
               'key': 'street:name',
               'type': 'addr',
               'value': 'Lexington'},
              {'id': '209809850',
               'key': 'street:prefix',
               'type': 'addr',
               'value': 'West'},
              {'id': 209809850,
               'key': 'street:type',
               'type': 'addr',
               'value': 'Street'},
              {'id': 209809850,
               'key': 'building',
               'type': 'regular',
               'value': 'yes'},
              {'id': 209809850,
               'key': 'levels',
               'type': 'building',
               'value': '1'},
              {'id': 209809850,
               'key': 'building_id',
               'type': 'chicago',
               'value': '366409'}]}
"""

NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
# WAYS_PATH = "ways.csv"
# WAY_NODES_PATH = "ways_nodes.csv"
# WAY_TAGS_PATH = "ways_tags.csv"

SCHEMA = schema_osm.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']

NODE_ATTRIB = ['id', 'lat', 'lon', 'user', 'uid', 'version', 'changeset', 'timestamp']
NODE_TAG_ATTRIB = ['k', 'v']
WAY_ATTRIB = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SET_OF_VALUES = set()

def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    node_attribs = {}
    way_attribs = {}
    way_nodes = []
    tags = []  # Handle secondary tags the same way for both node and way elements
    
    elem = element
    
    # print elem.tag
    if elem.tag == "node":
        node_attribs = {}
        for attributes in NODE_ATTRIB:
            node_attribs[attributes] = elem.attrib[attributes]
                
            # children "tag" elements
            tags = []
            
        # deleting extraneous time info
        extra_pos = node_attribs['timestamp'].find('T')
        node_attribs['timestamp'] = node_attribs['timestamp'][:extra_pos]
            
    count = 0
    for child in elem:
        
        if child.tag == "tag":    
            node_tag_attrib_dict = {}

            for attributes in NODE_TAG_ATTRIB:
                
                node_tag_attrib_dict[attributes] = child.attrib[attributes]   
                node_tag_attrib_dict['id'] = elem.attrib['id']

                # filter
                colon_pos = child.attrib["k"].find(":") 
                # problematic

                if colon_pos == -1:
                    node_tag_attrib_dict['type'] = "regular"
                else:
                    node_tag_attrib_dict['type'] = child.attrib["k"][:colon_pos]
                    node_tag_attrib_dict['k'] = child.attrib["k"][colon_pos + 1:]

            node_tag_attrib_dict['key'] = node_tag_attrib_dict['k']
            del node_tag_attrib_dict['k']

            node_tag_attrib_dict['value'] = node_tag_attrib_dict['v']
            del node_tag_attrib_dict['v']
               
            if node_tag_attrib_dict['key'] == "opening_hours":
                node_tag_attrib_dict['value'] = cleanup_times(node_tag_attrib_dict['value'])
                
            node_tag_attrib_dict['value'] = fix_extra_a(node_tag_attrib_dict['value'], SET_OF_VALUES)    
            
            if node_tag_attrib_dict['key'] == "DTC":
                format_string_dtc(node_tag_attrib_dict['value'])

            # add to list
            tags.append(node_tag_attrib_dict)
        
    if element.tag == 'node':
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)
        
        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    with codecs.open(NODES_PATH, 'w') as nodes_file,          codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file:
#          codecs.open(WAYS_PATH, 'w') as ways_file, \
#          codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
#          codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
#         ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
#         way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
#         way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        nodes_writer.writeheader()
        node_tags_writer.writeheader()
#         ways_writer.writeheader()
#         way_nodes_writer.writeheader()
#         way_tags_writer.writeheader()

        validator = cerberus.Validator()

        for element in get_element(file_in, tags=('node', 'way')):
            el = shape_element(element)
            if el:
                if validate is True:
                    validate_element(el, validator)

                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


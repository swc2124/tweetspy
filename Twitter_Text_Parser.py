
import matplotlib

from nltk.tokenize import word_tokenize
matplotlib.use('Agg')
import json
import matplotlib.pyplot as plt
import nltk
import os
import socket
import sys
import time

from astropy.table import Table
from collections import Counter
from time import gmtime
from time import sleep
from time import strftime
#--[PROGRAM-OPTIONS]------------------------------------------------------#
hostname = socket.gethostname()
if hostname == 'sol-Linux':
    OUT_PUT_PATH = '/home/sol/CLUSTER_RAID/Tweet_Output/Clean_Words/'
    All_Words_PATH = '/home/sol/CLUSTER_RAID/Tweet_Code/dictionary.txt'
    Table_PATH = '/home/sol/CLUSTER_RAID/Tweet_Output/'
else:
    OUT_PUT_PATH = '/root/SHARED/Tweet_Output/Clean_Words/'
    All_Words_PATH = '/root/SHARED/Tweet_Code/dictionary.txt'
    Table_PATH = '/root/SHARED/Tweet_Output/'
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def ct(text, colour=WHITE):
    seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
    return seq


def list_files(path):
    # returns a list of names (with extension, without full path) of all files
    # in folder path
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files


Names = {'PRP$': 'pronoun, possessive', 'VBG': 'verb, present participle or gerund',
         'VBD': 'verb, past tense', 'VBN': 'verb, past participle', 'VBP': 'verb, present tense not 3rd person singular',
                'WDT': 'determiner, WH', 'JJ': 'adjective or numeral, ordinal', 'WP': 'pronoun, WH',
                'VBZ': 'verb, present tense 3rd person singular', 'DT': 'determiner', 'RP': 'particle',
                'NN': 'noun, common, singular or mass', 'TO': '"to" as preposition or infinitive marker',
                'PRP': 'pronoun, personal', 'RB': 'adverb', 'NNS': 'noun, common plural', 'NNP': 'noun, proper singular',
                'VB': 'verb, base form', 'WRB': 'adverb, WH', 'CC': 'conjunction, coordinating', 'RBR': 'adverb, comparative',
                'CD': 'cardinal numeral', '-NONE-': 'No matching tags found', 'EX': 'existential, there there',
                'IN': 'conjunction or subordinating preposition', 'WP$': 'pronoun, possessive WH',
                'MD': 'modal auxiliary', 'JJS': 'adjective, superlative', 'JJR': 'adjective, comparative',
                'PDT': 'pre-determiner', 'RBS': 'adverb, superlative', 'FW': 'foreign word',
                'NNPS': 'noun, proper plural', 'UH': 'interjection'}
Color_Keys = {'NN': GREEN, 'NNS': GREEN, 'NNP': GREEN, 'NNPS': GREEN,
              'JJR': YELLOW, 'JJS': YELLOW,  'JJ': YELLOW,
              'VBG': BLUE, 'VBD': BLUE, 'VBN': BLUE, 'VBP': BLUE, 'VBZ': BLUE, 'VB': BLUE,
              'RBS': MAGENTA, 'RBR': MAGENTA, 'RB': MAGENTA, 'WRB': MAGENTA,
              'PRP$': CYAN, 'PRP': CYAN, 'WP': CYAN, 'WP$': CYAN}
names = ['time', 'weekday', 'PRP$', 'VBG', 'VBD',
         'VBN', 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT',
         'RP', 'NN', 'TO', 'PRP', 'RB', 'NNS', 'NNP',
         'VB', 'WRB', 'CC', 'RBR', 'CD', '-NONE-',
         'EX', 'IN', 'WP$', 'MD', 'JJS', 'JJR',
         'PDT', 'RBS', 'FW', 'UH']
dtypes = ['float', 'S10', 'int', 'int', 'int',
          'int', 'int', 'int', 'int', 'int', 'int',
          'int', 'int', 'int', 'int', 'int', 'int',
          'int', 'int', 'int', 'int', 'int', 'int',
          'int', 'int', 'int', 'int', 'int', 'int',
                        'int', 'int', 'int', 'int', 'int', 'int']
Record_book_keys = ['PRP$', 'VBG', 'VBD',
                    'VBN', 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT',
                    'RP', 'NN', 'TO', 'PRP', 'RB', 'NNS', 'NNP',
                    'VB', 'WRB', 'CC', 'RBR', 'CD', '-NONE-',
                    'EX', 'IN', 'WP$', 'MD', 'JJS', 'JJR',
                    'PDT', 'RBS', 'FW', 'UH']
plt_clrs = ['indigo', 'gold', 'hotpink', 'firebrick', 'indianred', 'sage', 'yellow', 'mistyrose',
            'darkolivegreen', 'olive', 'darkseagreen', 'pink', 'tomato', 'lightcoral', 'orangered', 'navajowhite', 'lime', 'palegreen',
            'darkslategrey', 'greenyellow', 'burlywood', 'seashell', 'fuchsia', 'papayawhip', 'chartreuse', 'dimgray',
            'black', 'peachpuff', 'springgreen', 'aquamarine', 'orange', 'lightsalmon', 'darkslategray', 'brown',
            'indigo', 'gold', 'hotpink', 'firebrick', 'indianred', 'sage', 'yellow', 'mistyrose']
Word_Type_Table = Table.read(
    Table_PATH+'Word_Type_Table.hdf5', path='Word_Type_Table')
Top_One_Hundred_Table = Table.read(
    Table_PATH+'Top_One_Hundred_Table.hdf5', path='Top_One_Hundred_Table')
top_names = ['month', 'day']
top_dtypes = ['S10', 'S10']
for i in range(100):
    top_dtypes.append('S10')
    top_names.append(str(i+1))
#Word_Type_Table = Table( names=names, dtype=dtypes)
#Top_One_Hundred_Table = Table( names=top_names, dtype=top_dtypes)
All_Words_PATH = '/home/sol/CLUSTER_RAID/Tweet_Code/dictionary.txt'
All_Words = {}.fromkeys(Record_book_keys, 0)
'''
csv.field_size_limit(sys.maxsize)
with open('/root/SHARED/Tweet_Output/wordbook.txt','rb') as f:
    for key,val in csv.reader(f):
        All_Words[key] = val
'''
first_run = True
unknown_keys = []
try:
    while True:
        Date = strftime("%Y%b%a%d%H", gmtime())
        date = strftime("%Y%b%a%d%H", gmtime())
        if first_run == False:
            month, day = strftime('%b %a', gmtime()).split(' ')
            Top_One_Hundred_Table_row = [month, day]
            for word, number in count_all.most_common(100):
                Top_One_Hundred_Table_row.append(word)
            Top_One_Hundred_Table.add_row(Top_One_Hundred_Table_row)
            Top_One_Hundred_Table.write(Table_PATH+'Top_One_Hundred_Table.hdf5', format='hdf5',
                                        path='Top_One_Hundred_Table', append=True,
                                        overwrite=True)
            os.system('clear')
            # print Top_One_Hundred_Table
            # print Word_Type_Table
        count_all = Counter()
        first_run = False
        while date == Date:
            Record_book = {}.fromkeys(Record_book_keys, 0)
            for word_set in list_files(OUT_PUT_PATH):
                processed = False
                with open(OUT_PUT_PATH+word_set, 'r') as f:
                    page = f.read()
                    # print page
                    if len(page) < 10000:
                        continue
                #os.system('cat ~/SHARED/wordsloded.txt')
                f = open(OUT_PUT_PATH+word_set, 'w')
                f.close()
                processed = True
                #os.system('cat ~/SHARED/cleaning.txt')
                words = [tweet.replace('\n', '').replace('[', '').replace(']', '').replace('"', '').replace(' ', '')
                         for tweet in page.split(',')]
                os.system('clear')
                # print word_set, 'has ', len(words)
                # sleep(3)
                # print words
                #os.system('cat ~/SHARED/counting.txt')
                count_all.update(words)
                tagged = nltk.pos_tag(words)
                for i in Counter(tagged).most_common(50):
                    if i[0][1] in Color_Keys.keys():
                        color = Color_Keys[i[0][1]]
                        print ct(str(i[1]), CYAN), ' ', ct(i[0][0], WHITE), '   ', ct(Names[i[0][1]], color)
                    else:
                        print i[1], ' ', i[0][0], ' ', Names[i[0][1]]
                    sleep(.05)
                # print tagged
                #os.system('cat ~/SHARED/adding.txt')
                for word, word_type in tagged:
                    try:
                        All_Words[str(word_type)] += 1
                        Record_book[str(word_type)] += 1
                        # print word_type, Record_book[str(word_type)]
                    except KeyError as e:
                        error = str(e).replace("'", '')
                        # print e
                        if not error in unknown_keys:
                            unknown_keys.append(error)
                #os.system('cat ~/SHARED/adding.txt')
                # os.system('clear')
                # if len(Word_Type_Table)<21: print Word_Type_Table
                # else: print Word_Type_Table[-20]
                # print '\n\n'
                # if len(Top_One_Hundred_Table)<21: print Top_One_Hundred_Table
                # else: print Top_One_Hundred_Table[-20]
                # print date
                # print '\n\n[UNKNOWN KEYS] :',unknown_keys
                #os.system('cat ~/SHARED/done.txt')
            if processed:
                try:
                    date = strftime("%Y%b%a%d%H", gmtime())
                    t = time.gmtime()
                    row = [t[3]*3600+t[4]*60+t[5], strftime('%a', gmtime())]
                    for key in Record_book.keys():
                        row.append(Record_book[key])
                    Word_Type_Table.add_row(row)
                    Word_Type_Table.write(Table_PATH+'Word_Type_Table.hdf5', format='hdf5',
                                          path='Word_Type_Table', append=True,
                                          overwrite=True)
                    fig = plt.figure()
                    ax = fig.add_subplot(111)
                    for i, key in enumerate(Word_Type_Table.keys()):
                        if key == 'time':
                            continue
                        if key == 'weekday':
                            continue
                        ax.scatter(
                            Word_Type_Table['time'], Word_Type_Table[key], c=plt_clrs[i])
                        ax.set_ylim([0, 5000])
                    fig.savefig(Table_PATH+'/Plots/testplot.png')
                    plt.close()
                except IOError, e:
                    print e
                    continue
except KeyboardInterrupt:
    with open(All_Words_PATH, 'wb') as f:
        writer = csv.writer(f)
        for key, val in All_Words.items():
            writer.writerow([key, val])
    sys.exit(0)
'''
                    for key, number in count_all.most_common():
                        try:
                            print Record_book[key], 'new added value is : ',value 
                            Record_book[key[1]] += value
                        except KeyError:
                            print key
                    row = [time.asctime( time.localtime(time.time()) )]
                    for key in Record_book.keys():
                        print Record_book[key]
                        row.append(Record_book[key])
                    if len(rows) == len(names):
                        T.add_row(row)
                        T.write(Table_PATH, format='hdf5',
                            path='data', append=True, 
                            overwrite=True)
                    os.system('clear')
                    print T
            with open(All_Words_PATH,'wb') as f:
                writer = csv.writer(f)
                for key, val in type_dict.items():
                    writer.writerow([key, val])
'''

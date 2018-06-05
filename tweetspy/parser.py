#SOl Courtney Columbia U Department of Astronomy and Astrophysics NYC 2016
#swc2124@columbia.edu

#--[DESCRIPTION]---------------------------------------------------------#

'''
Date: May 2016

Handeler for twitter text parsing
'''

#--[IMPORTS]--------------------------------------------------------------#

from nltk.tokenize import word_tokenize

import matplotlib
matplotlib.use('agg')


import matplotlib.pyplot as plt
plt.ioff()

from time import gmtime, strftime, sleep

from astropy.table import Table

from collections import Counter
import numpy as np
import nltk, time, os,sys,json,socket
from datetime import datetime
import csv


#--[PROGRAM-OPTIONS]------------------------------------------------------#

nltk.data.path.append('/root/SHARED/nltk_data/')

hostname = socket.gethostname()


if hostname == 'sol-Linux':
    OUT_PUT_PATH    = '/home/sol/CLUSTER_RAID/Tweet_Output/Clean_Words/'
    All_Words_PATH  = '/home/sol/CLUSTER_RAID/Tweet_Code/dictionary.txt'
    Table_PATH      = '/home/sol/CLUSTER_RAID/Tweet_Output/'

else:
    OUT_PUT_PATH    = '/root/SHARED/Tweet_Output/Clean_Words/'
    All_Words_PATH  = '/root/SHARED/Tweet_Code/dictionary.txt'
    Table_PATH      = '/root/SHARED/Tweet_Output/'

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


Names = {'PRP$':'pronoun, possessive','VBG':'verb, present participle or gerund',
        'VBD':'verb, past tense','VBN':'verb, past participle','VBP':'verb, present tense not 3rd person singular',
        'WDT':'determiner, WH','JJ':'adjective or numeral, ordinal','WP': 'pronoun, WH',
        'VBZ':'verb, present tense 3rd person singular','DT':'determiner','RP':'particle',
        'NN':'noun, common, singular or mass','TO':'"to" as preposition or infinitive marker',
        'PRP':'pronoun, personal','RB':'adverb','NNS':'noun, common plural','NNP':'noun, proper singular',
        'VB':'verb, base form','WRB':'adverb, WH', 'CC':'conjunction, coordinating', 'RBR':'adverb, comparative',
        'CD':'cardinal numeral','-NONE-':'No matching tags found','EX':'existential, there there',
        'IN':'conjunction or subordinating preposition','WP$':'pronoun, possessive WH',
        'MD':'modal auxiliary', 'JJS':'adjective, superlative', 'JJR':'adjective, comparative',
        'PDT': 'pre-determiner','RBS':'adverb, superlative', 'FW': 'foreign word',
        'NNPS': 'noun, proper plural', 'UH': 'interjection'}


Color_Keys = {'NN':GREEN, 'NNS':GREEN, 'NNP':GREEN, 'NNPS':GREEN, 'MD':YELLOW,
              'JJR': YELLOW, 'JJS': YELLOW,  'JJ': YELLOW, 'DT': YELLOW,
              'VBG':BLUE,'VBD':BLUE,'VBN':BLUE,'VBP':BLUE,'VBZ':BLUE,'VB':BLUE,
              'RBS': MAGENTA,'RBR': MAGENTA,'RB': MAGENTA,'WRB': MAGENTA,
              'PRP$':CYAN, 'PRP':CYAN, 'WP':CYAN, 'WP$':CYAN, "IN": RED,
              }

names = [ 'time', 'weekday','PRP$', 'VBG', 'VBD',
            'VBN', 'VBP', 'WDT', 'JJ', 'WP', 'VBZ', 'DT',
            'RP', 'NN', 'TO', 'PRP', 'RB', 'NNS', 'NNP',
            'VB', 'WRB', 'CC', 'RBR', 'CD', '-NONE-',
            'EX', 'IN', 'WP$', 'MD', 'JJS', 'JJR',
            'PDT', 'RBS' , 'FW', 'UH']

dtypes = [ 'float','S10','int', 'int', 'int',
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
            'PDT', 'RBS' , 'FW', 'UH']

plt_clrs = ['indigo','gold','hotpink','firebrick','indianred','sage','yellow','mistyrose',
            'darkolivegreen','olive','darkseagreen','pink','tomato','lightcoral','orangered','navajowhite','lime','palegreen',
            'darkslategrey','greenyellow','burlywood','seashell','fuchsia','papayawhip','chartreuse','dimgray',
            'black','peachpuff','springgreen','aquamarine','orange','lightsalmon','darkslategray','brown',
            'indigo','gold','hotpink','firebrick','indianred','sage','yellow','mistyrose']


try:
    os.system('clear')
    fig = plt.figure(figsize=(20, 10))
    ax = fig.add_subplot(111)
    last_total_words = 0
    total_words = 0
    while True:
        Date = datetime.now().strftime("%a_%b_%d_%Y_%H_%M")
        date = Date
        count_all = Counter()
        words = []
        print ct("-" * 70, WHITE)
        print ct(datetime.now().strftime("%a %b %d, %Y %H:%M"), BLUE) + "\t -- \tlast n_words: " + ct(str(last_total_words), RED)

        while date == Date:

            for word_set in list_files(OUT_PUT_PATH):
                with open(OUT_PUT_PATH+word_set,'r') as f:
                    page = f.read()
                with open(OUT_PUT_PATH+word_set,'w') as f:
                    pass
                    #os.system('cat ~/SHARED/wordsloded.txt')

                #os.system('cat ~/SHARED/cleaning.txt')
                new_words = [tweet.replace('\n','').replace('[','').replace(']','').replace('"','').replace(' ','') for tweet in page.split(',') ]

                words += [i for i in new_words if i != '']
                #print word_set, 'has ', len(words)
                #sleep(3)
                #print words
                #os.system('cat ~/SHARED/counting.txt')
                sys.stdout.write("\r" + ct(datetime.now().strftime("%H:%M:%S"), BLUE) + " :\t" +  ct(str(len(words)), GREEN))

            date = datetime.now().strftime("%a_%b_%d_%Y_%H_%M")

        last_total_words = total_words
        total_words = len(words)
        sys.stdout.write("\n")
        sys.stdout.flush()

        print ct("Tagging...", BLUE)
        tagged = nltk.pos_tag(words)
        print ct("Counting...", BLUE)
        count_all.update(tagged)

        os.system('clear')
        print "\t", ct("Number", CYAN), "\t", ct("Word", WHITE), " " * 11, ct("Type", WHITE)
        print ct("-" * 70, WHITE)
        for i in Counter(tagged).most_common(50):
            _space = 15 - len(i[0][0])
            if i[0][1] in  Color_Keys.keys():
                color = Color_Keys[i[0][1]]
                print "\t", ct(str(i[1]), CYAN),'\t',ct(i[0][0], WHITE),' ' * _space,ct(Names[i[0][1]], color)
            else:
                print "\t", ct(str(i[1]), RED),'\t',ct(i[0][0], RED),' ' * _space,ct(Names[i[0][1]], RED)
            sleep(0.01 + (np.random.ranf()/1e1))

        wrd_type_keys = []
        plot_data = []
        for (w, k), n in count_all.most_common():
            if k in wrd_type_keys:
                continue
            else:
                wrd_type_keys.append(k)

        for wrd_typ in wrd_type_keys:
            num = 0
            for (w, k), n in count_all.most_common():
                if k == wrd_typ:
                    num += n
            plot_data.append((wrd_typ, num))
        # print plot_data


        for wrd_typ, num in plot_data:
            _num = round(np.log10(num), 1)
            # print wrd_typ, _num
            ax.bar(wrd_typ, _num, align='center')
        ax.set_title("Word Type Frequency\ntotal words:" + str(total_words) + "\n" + datetime.now().strftime("%a %b %d, %Y %H:%M"))
        ax.axes.tick_params(labelrotation=90)
        fig.savefig(Table_PATH + "plot")
        ax.clear()
        # plt.show()
except KeyboardInterrupt:
    os.system('clear')
    sys.exit(0)

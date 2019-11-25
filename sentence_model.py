from gensim.models import KeyedVectors
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import numpy as np
import pandas as pd
import re
import string
from fpdf import FPDF
from random import randint

def map_category(input_category,refernce_dict):
    for k,v in refernce_dict.items():
        if input_category in v:
            return k

wordmodelfile="D:/Pycharm Projects/MAX.bin"

wordmodel = KeyedVectors.load_word2vec_format(wordmodelfile, binary = True, limit=200000)

wordmodel.init_sims(replace=True) # Normalizes the vectors in the word2vec class.

level_3_dict = {
    'hw': ['collection point not attended properly', 'solid waste management swm related', 'equipment related solid waste management swm civic', 'providing removing replacing dustbins', 'removal of debris', 'garbage lorry not reported for service lorry not covered', 'garbage not lifted from road authorised collection point', 'schemes policies in civic issues related', 'drainage related', 'equipments related drainage civic', 'miscellaneous issues related', 'compensation rehabilitation', 'nuisance due to stray dogs monkeys etc ', 'electricity related miscellaneous issues in civic civic', 'hawkers at unauthorized place', 'license related', 'nuisance due to unauthorized hawkers on roads footpaths', 'unauthorised food selling preparation license ', 'moh related license ', 'unauthorised stalls on roads footpaths', 'unauthorised workshop or garage', 'unauthorised banners advt on road', 'municipal corporation related municipal corporation council related civic', 'infrastructure equipment', 'human resource related', 'street lighting', 'parking related', 'relaying and repairs of roads', 'water supply related', 'borewell well', 'providing water tap and hand pumps', 'unauthorised construction development', 'unauthorised alteration of bldg flat etc', 'buildings related', 'fogging', 'cleaning removal of silt from nullah cross culverts etc ', 'flooding during monsoon', 'garden related', 'toilet urinal related', 'municipal school related', 'infrastructure issues', 'vaccination', 'health service related', 'health infrastructure related', 'human resources related human resources health', 'tax related', 'solid waste management swm civic scams corruption scams corruption', 'naming renaming of roads chowks monuments buildings stations related']
}

level_2_dict = {
    'solid waste management swm': ['collection point not attended properly', 'solid waste management swm related', 'equipment related solid waste management swm civic', 'providing removing replacing dustbins', 'removal of debris', 'garbage lorry not reported for service lorry not covered', 'garbage not lifted from road authorised collection point'],
    'schemes policies in civic issues': ['schemes policies in civic issues related'],
    'drainage': ['drainage related', 'equipments related drainage civic'],
    'miscellaneous issues in civic': ['miscellaneous issues related', 'compensation rehabilitation', 'nuisance due to stray dogs monkeys etc ', 'electricity related miscellaneous issues in civic civic'],
    'license civic': ['hawkers at unauthorized place', 'license related', 'nuisance due to unauthorized hawkers on roads footpaths', 'unauthorised food selling preparation license ', 'moh related license ', 'unauthorised stalls on roads footpaths', 'unauthorised workshop or garage', 'unauthorised banners advt on road'],
    'municipal corporation council related': ['municipal corporation related municipal corporation council related civic', 'infrastructure equipment', 'human resource related'],
    'roads': ['street lighting', 'parking related', 'relaying and repairs of roads'],
    'water supply': ['water supply related', 'borewell well', 'providing water tap and hand pumps'],
    'buildings': ['unauthorised construction development', 'unauthorised alteration of bldg flat etc', 'buildings related'],
    'pest control': ['fogging'],
    'storm water drainage': ['cleaning removal of silt from nullah cross culverts etc ', 'flooding during monsoon'],
    'garden': ['garden related'],
    'toilet': ['toilet urinal related'],
    'municipal school': ['municipal school related', 'infrastructure issues'],
    'treatment medicines': ['vaccination'],
    'health related issues': ['health service related'], 
    'infrastructure health': ['health infrastructure related'], 
    'human resources health': ['human resources related human resources health health'],
    'tax': ['tax related'],
    'civic scams corruption': ['solid waste management swm civic scams corruption scams corruption'],
    'naming renaming of roads chowks monuments buildings stations': ['naming renaming of roads chowks monuments buildings stations related']
}

level_1_dict = {
    'civic': ['solid waste management swm', 'schemes policies in civic issues', 'drainage', 'miscellaneous issues in civic', 'license civic', 'municipal corporation council related', 'roads', 'water supply', 'buildings', 'pest control', 'storm water drainage', 'garden', 'toilet'],
    'education': ['municipal school'],
    'health': ['treatment medicines', 'health related issues', 'infrastructure health', 'human resources health'],
    'revenue': ['tax'],
    'scams corruption': ['civic scams corruption'],
    'social culturalconcerns': ['naming renaming of roads chowks monuments buildings stations']
}

output_comments=[]
output_categories_3=[]
output_categories_2=[]
output_categories_1=[]

hw_comments = open('eng_translated_pdf_text.txt', 'r',encoding='utf-8').readlines()
print(len(hw_comments))
distances=[]
count=1
for comment in hw_comments:
    if (comment=='') or (comment=='\n') :
        count+=1
    else:
        count+=1
        single_comment=comment.lower()

        single_comment=single_comment.lower().translate(str.maketrans(string.punctuation,' '*len(string.punctuation)))
        single_comment=re.sub(r"\s+", ' ',single_comment)
        single_comment=single_comment.lstrip()
        print("Comment is: \n",single_comment)
        output_comments.append(single_comment)

        cwords = single_comment.split(' ')
        cwords = set(cwords)
        for word in cwords.copy():
            if word in stopwords.words('english'):
                cwords.remove(word)
            
        cwords = list(cwords)
        
        wmd = []
        for keyword in level_3_dict['hw']:
            keyword=keyword.lower().translate(str.maketrans(string.punctuation,' '*len(string.punctuation)))
            keyword=re.sub(r"\s+", ' ',keyword)
            keyword=keyword.lstrip()
            swords = keyword.split()
            swords = set(swords)
            for word in swords.copy():
                if word in stopwords.words('english'):
                    swords.remove(word)
            swords = list(swords)
            distance = wordmodel.wmdistance(cwords, swords)
            wmd.append(distance)

        distances.append(wmd)
        minIndex = np.array(wmd).argmin()
        category = level_3_dict['hw'][minIndex]
        print('Category: ', category)
        output_categories_3.append(category)
        level_2_cat=map_category(category, level_2_dict)
        output_categories_2.append(level_2_cat)  
        output_categories_1.append(map_category(level_2_cat, level_1_dict)) 
output_dict={'English comment':output_comments,'Level 1':output_categories_1, 'Level 2': output_categories_2, 'Level 3': output_categories_3}

df = pd.DataFrame(output_dict)
df.to_csv('level_3_bottom_up_srategy.csv',encoding="utf-8",index=False)

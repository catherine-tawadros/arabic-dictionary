# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 23:22:47 2022

@author: ctawa
"""

from flask import Flask
from flask import render_template
from flask import request
import pandas as pd
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST' and 'searchword' in request.form:
        word = request.form.get('word1')
        write(search_by_word(word))
        return render_template('search result.html')
    if request.method == 'POST' and 'searchcat' in request.form:
        cat = request.form.get('word1')
        write(search_by_cat(cat))
        return render_template('search result.html')
    if request.method == 'POST' and 'quiz' in request.form:
        quiz()
        return render_template('quiz.html')
    if request.method == 'POST' and 'home' in request.form:
        return render_template('index.html')
    return render_template('index.html')
    
def quiz():
    
    arabic_dict = pd.read_csv('arabic words.csv')
    arabic_dict = arabic_dict.fillna('')
    
    contents = None
    # line_index = 1
    with open('templates/quiz.html', 'r', encoding='utf-8') as f:
        contents = f.readlines()
        
    row = random.randint(0, len(arabic_dict)-1)
    contents[31] = '\t\t'+str(arabic_dict.iloc[row,0]) + '\n'
    contents[15] = '\t\t'+str(arabic_dict.iloc[row,1]) + '\n'
    # contents[8] = '\t<p>'+str(arabic_dict.iloc[1,0])+'\n'
    # contents[9] = '\t<p>'+arabic_dict.iloc[1,0]+'\n'

    with open('templates/quiz.html', 'w', encoding='utf-8') as f:
        f.writelines(contents)  
        # f.write(str(len(contents)))
        '''
        f.seek(0,0)
        f.write(str(f.tell()))
        f.write('first')
        f.readline()
        f.write('last')
        '''
        f.close()
        

def write(table):
    
    with open("templates/search result.html",'r+') as file:
        file.truncate(0)
        
    if len(table) == 0:
        with open("templates/search result.html", "w", encoding="utf-8") as f:
            f.write('''<link rel="stylesheet" type="text/css" href= "{{ url_for(\'static\',filename=\'styles/stylev1.32.css\') }}">\n
                    <head>\n
                    <meta charset="utf-8">\n
                    <title>Search Result</title>\n
                    <link rel="icon" type="image/x-icon" href="../static/images/bookv2.png">
</head>\n''')
            f.write('No results')
            f.close()
            return
        
    html = table.to_html()
    with open("templates/search result.html", "w", encoding="utf-8") as f:
        f.write('<link rel="stylesheet" type="text/css" href= "{{ url_for(\'static\',filename=\'styles/stylev1.32.css\') }}">\n')
        f.write(html)
        f.close()
    
def search_by_word(word):
    arabic_dict = pd.read_csv('arabic words.csv')
    arabic_dict = arabic_dict.fillna('')
    
    if word=='':
        return arabic_dict
    
    real_word = arabic_dict.loc[arabic_dict.ENGLISH == word]
    hasword = arabic_dict.apply(lambda x: word in x[0], axis=1).values
    close_word = arabic_dict.loc[hasword]
    related = None
    farrelated = None
    word = real_word if len(real_word) > 0 else close_word if len(close_word) > 0 else None
    if word is not None:
        samecat = arabic_dict.apply(lambda x: x['CATEGORY']==word.iloc[0].CATEGORY, axis=1).values
        related = arabic_dict.loc[samecat]
        allcats = [x.strip() for x in word.iloc[0].CATEGORY.split(',')]
        relatedcat = arabic_dict.apply(lambda x: sum(cat in x.CATEGORY for cat in allcats), axis=1).sort_values(ascending=False)
        relatedcat = relatedcat.loc[relatedcat > 0]
        farrelated = arabic_dict.iloc[relatedcat.index]
    result = pd.concat([real_word, close_word, related, farrelated])
    result = result.drop_duplicates(ignore_index=True)
    result = result.reset_index(drop=True)
    return result.iloc[:10]

def search_by_cat(category):
    arabic_dict = pd.read_csv('arabic words.csv')
    arabic_dict = arabic_dict.fillna('')
    
    allcats = [x.strip() for x in category.split(',')]
    relatedcat = arabic_dict.apply(lambda x: sum(cat in x.CATEGORY for cat in allcats), axis=1).sort_values(ascending=False)
    relatedcat = relatedcat.loc[relatedcat > 0]
    return arabic_dict.iloc[relatedcat.index].reset_index(drop=True)

if __name__ == '__main__':
    app.run(debug=True)
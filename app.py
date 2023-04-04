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
import datetime
# import datetime

app = Flask(__name__)

#### MAIN FUNCTIONS ####

@app.route('/', methods=['GET', 'POST'])
def root():
    if request.method == 'POST':
        # search functions
        if 'searchword' in request.form:
            word = request.form.get('word1')
            write(search_by_word(word))
            return render_template('search result.html')
        if 'searchcat' in request.form:
            cat = request.form.get('word1')
            write(search_by_cat(cat))
            return render_template('search result.html')
        
        # quiz functions
        if 'start-quiz' in request.form:
            cat = request.form.get('quiz-cat')
            start_date = datetime.datetime.strptime(
                     request.form.get("start-date"),
                     '%Y-%m-%d')
            end_date = datetime.datetime.strptime(
                     request.form.get("end-date"),
                     '%Y-%m-%d')
            chapter = request.form.get("chapter-number")
            current_quiz = Quiz(c=str(cat), sd=start_date, ed=end_date, ch=chapter)
            worked = make_quiz(current_quiz)
            if worked:
                return render_template('quiz.html')
            else:
                return render_template('quizerror.html')
        if 'next-quiz' in request.form:
            # current_quiz = get_quiz()
            worked = make_quiz()
            if worked:
                return render_template('quiz.html')
            else:
                return render_template('quizerror.html')
        
        # nav bar
        if 'home' in request.form:
            return render_template('index.html')
        if 'quiz_page' in request.form:
            return render_template('quiz_page.html')
        if 'chart_page' in request.form:
            return render_template('chart_page.html')
        
    return render_template('index.html')


#### QUIZ FEATURES ####
    
class Quiz:
    def __init__(self, sd=None, ed=None, c='', ch=None):
        self.start_date = sd
        self.end_date = ed
        self.category = c
        self.chapter = ch
        FIRST = datetime.datetime.strptime("09-21-2022",'%m-%d-%Y')
        LAST =  datetime.datetime.strptime("04-03-2023",'%m-%d-%Y')
        if self.start_date == FIRST and self.end_date == LAST:
            self.include_all_dates = True
        else:
            self.include_all_dates = False
            
        '''
        with open('quiz_params.txt', 'w', encoding='utf-8') as f:
            contents = [self.start_date+'\n', self.end_date+'\n', self.category+'\n']
            f.writelines(contents)
            f.close()
        '''
        
        self.table = pd.read_csv('arabic words.csv')
        if self.category != '':
            self.table = self.table[self.table['CATEGORY'].notna()]
            self.table = self.table.loc[self.table.apply(lambda x: True if c in x[3] else False, axis=1)]
        if not self.include_all_dates:
            self.table = self.table.loc[self.table["DATE"] != ""]
            self.table["DATE"] = pd.to_datetime(self.table["DATE"], format="%d.%m.%y")
            self.table = self.table.loc[self.table["DATE"] >= self.start_date].loc[self.table["DATE"] <= self.end_date]
        if self.chapter != "" and self.chapter is not None:
            self.table = self.table.loc[self.table["SOURCE"].notna()]
            self.table = self.table.loc[self.table["SOURCE"].str.contains("chapter "+self.chapter)]
            
        with open('quiz_params.txt', 'w', encoding='utf-8') as f:
            contents = self.table.to_csv(index=False)
            f.writelines(contents)
            f.close()
            
            
    def get_sd(self):
        return self.start_date
    def get_ed(self):
        return self.end_date
    def get_cat(self):
        return self.category
    def get_table(self):
        return self.table

'''
def get_quiz():
    contents = None
    # CHANGE ALL THIS
    
    with open('quiz_params.txt', 'r', encoding='utf-8') as f:
        contents = f.readlines()
        params = ['' for i in range(3)]
        for i in range(3):
            el = contents[i]
            if el is not None and el != '':
                params[i] = el[:len(el)-1]
        f.close()
    
    return Quiz(sd=params[0], ed=params[1], c=params[2])
'''

def make_quiz(q=None):
    
    if q is not None:
        arabic_dict = q.get_table()
    else:
        arabic_dict = pd.read_csv("quiz_params.txt")
    # null check
    arabic_dict = arabic_dict.fillna('')
    
    if len(arabic_dict) == 0:
        return False
    
    contents = None
    with open('templates/quiz.html', 'r', encoding='utf-8') as f:
        contents = f.readlines()
        f.close()
        
    row = random.randint(0, len(arabic_dict)-1)
    contents[38] = '\t\t'+str(arabic_dict.iloc[row,0]) + '\n'
    contents[28] = '\t\t'+str(arabic_dict.iloc[row,1]) + '\n'

    with open('templates/quiz.html', 'w', encoding='utf-8') as f:
        f.writelines(contents)  
        # f.write(str(len(contents)))
        f.close()
    
    return True
        
        
#### SEARCH FEATURES ####

def write(table):
    
    with open("templates/search result.html",'r+') as file:
        file.truncate(0)
        
    with open("templates/search result.html", "w", encoding="utf-8") as f:
            f.write('''<link rel="stylesheet" type="text/css" href= "{{ url_for(\'static\',filename=\'styles/stylev1.6.css\') }}">
                    <script src="{{ url_for('static',filename='js/functions.js') }}"></script>
                    <script src="https://kit.fontawesome.com/9772f3f43d.js" crossorigin="anonymous"></script>
                    <head><meta charset="utf-8"><title>Search Result</title>
                    <link rel="icon" type="image/x-icon" href="../static/images/bookv2.png"></head>
                    <html class="charts"><div class="topnav" id="Topnav">
                    <button href="javascript:void(0);" class="icon" onclick="reverseDiv('options')">
                    <i class="fa fa-bars"></i></button>
                    <form class="topnav" style="display:none" id="options" method="post">
                    <button href="#home" name="home">Home</button>
                    <button href="#news" name="quiz_page">Quiz</button>
                    <button href="#contact" name="chart_page" class="active">Charts</button>
                    </form></div>''')
            if len(table) == 0:
                f.write('No results')
            else:
                html = table.to_html()
                f.write(html)
            f.close()
            return
    
def search_by_word(word):
    arabic_dict = pd.read_csv('arabic words.csv')
    arabic_dict = arabic_dict.fillna('').drop(columns=["SOURCE","DATE","EQUIVALENTS"])
    
    if word=='':
        return arabic_dict
    
    word = word.lower()
    
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
    arabic_dict = arabic_dict.fillna('').drop(columns=["SOURCE","DATE","EQUIVALENTS"])
    
    category = category.lower()
    
    allcats = [x.strip() for x in category.split(',')]
    relatedcat = arabic_dict.apply(lambda x: sum(cat in x.CATEGORY for cat in allcats), axis=1).sort_values(ascending=False)
    relatedcat = relatedcat.loc[relatedcat > 0]
    return arabic_dict.iloc[relatedcat.index].reset_index(drop=True)

if __name__ == '__main__':
    app.run(debug=True)
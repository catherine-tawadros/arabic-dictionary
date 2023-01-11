# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 01:58:09 2023

@author: ctawa
"""

import pandas as pd

def main():
    pronouns = pd.read_csv('arabic pronouns.csv').fillna('')
    poss_end = pd.read_csv('possessive endings.csv').fillna('')
    pt_end = pd.read_csv('past tense endings.csv').fillna('')
    
    contents = None
    with open('templates/chart_page.html', 'r+', encoding='utf-8') as f:
        contents = f.readlines()
        f.close()
    # contents = contents.append(pronouns.to_html()).append(poss_end.to_html()).append(pt_end.to_html())
    with open('templates/chart_page.html', 'w+', encoding='utf-8') as f:
        f.writelines(contents)
        f.write(pronouns.to_html())
        f.write(poss_end.to_html())
        f.write(pt_end.to_html())
        f.close()
  
main()
    
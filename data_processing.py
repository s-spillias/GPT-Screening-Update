import pandas as pd
import numpy as np
import re
from itertools import zip_longest

def clean_string(s):
    s = str(s)
    return re.sub(r'\W+', '', s).lower()

def find_column(df, column_name):
    """Find a column that contains the given name (case-insensitive)"""
    for col in df.columns:
        if column_name in col.lower():
            return col
    return None

def load_papers(excel_sheet, debug=False):
    papers = pd.read_excel(excel_sheet).replace(np.nan, '')
    
    title_column = find_column(papers, 'title')
    abstract_column = find_column(papers, 'abstract')
    
    if not title_column or not abstract_column:
        raise ValueError("Could not find suitable columns for 'title' and 'abstract'")
    
    papers['Title_Clean'] = papers[title_column].apply(clean_string)
    papers = papers.drop_duplicates(subset='Title_Clean')
    
    n_studies = 3 if debug else len(papers)
    
    return papers, title_column, abstract_column, n_studies

def load_screening_criteria():
    return pd.read_csv('ScreeningCriteria.csv').to_dict('records')

def prepare_headers(n_agents, screening_criteria):
    headers = []
    for _ in range(n_agents):
        header = ['Title', 'Abstract', 'Paper Number']
        for SC_num, SC in enumerate(screening_criteria, 1):
            col_decision = f"Final Decision - SC{SC_num}: {SC['type']}"
            col_rationale = f"Initial Decision - SC{SC_num}: {SC['type']}"
            col_thoughts = f"Thoughts - SC{SC_num}: {SC['type']}"
            header.extend([col_rationale, col_decision, col_thoughts])
        headers.append(header)
    return headers

def collate_data(list1, list2, list3):
    max_length = max(len(list1), len(list2), len(list3))
    result = [item for sublist in zip_longest(list1, list2, list3, fillvalue=None) for item in sublist]
    return result

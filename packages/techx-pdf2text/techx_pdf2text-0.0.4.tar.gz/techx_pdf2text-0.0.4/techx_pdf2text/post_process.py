import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pandas as pd
from urllib.parse import urlparse
import os
from PyPDF2.errors import PdfReadError
import fitz

def chunker(text, size = 300, overlap = 30) -> list:
    custom_text_splitter = RecursiveCharacterTextSplitter(
        # Set custom chunk size
        chunk_size = size,
        chunk_overlap  = overlap,
        # Use length of the text as the size measure
        length_function = len,
        # Use only "\n\n" as the separator
        separators = ['\n']
    )

    custom_texts = custom_text_splitter.create_documents([text])

    pypdf_list = []
    for i in range(len(custom_texts)):
        custom_text_all = custom_texts[i].page_content
        pypdf_list.append(custom_text_all)
        
    return pypdf_list

def text_to_chunk(json_result:json) -> json:
    parsed_result = json.loads(json_result)
    for idx,doc in enumerate(parsed_result):
        text = doc['text']
        chucked_text = chunker(text)
        parsed_result[idx]['text'] = chucked_text
    
    json_output = json.dumps(parsed_result,ensure_ascii=False)
    return json_output
        
#convert text or list of text to DataFrame.        
def text_to_df(text_list) -> pd.DataFrame:
    if type(text_list) is not list:
        text_list = [text_list]

    df = pd.DataFrame({"text": text_list})
    return df

# ------------------------------------------------------------------------------------------
# collect data
def create_table_postpro(file_path,text, num_id) -> pd.DataFrame:
    
    df_clean = text_to_df(text)
    db_name_lst = []
    table_name_lst = []
    issue_date_lst = []
    expiration_date_lst = []
    file_name_lst = []
    document_id_lst = []
    url_lst = []
    domain_lst = []
    source_type_lst = []
    lang_lst = []
    category_1_lst = []
    category_2_lst = []
    title_lst = []
    description_lst = []
    section_lst = []
    par_lst = []
    updated_date_lst = []

    for i in range(len(df_clean)):
        db_name_lst.append('llm_ivx')
        table_name_lst.append('llm_ivx_pdf')
        issue_date_lst.append('null')
        expiration_date_lst.append('null')
        
        url_lst.append(file_path) # this

        a = urlparse(url_lst[0])
        file_name_lst.append(os.path.basename(a.path))

        # domain_lst.append('null')
        source_type_lst.append('pdf')
        lang_lst.append('th')
        category_1_lst.append('null')
        category_2_lst.append('null')
        title_lst.append('null')
        description_lst.append('null')
        section_lst.append('null')
        updated_date_lst.append('null')

    df_clean['db_name'] = db_name_lst
    df_clean['table_name'] = table_name_lst
    df_clean['issue_date'] = issue_date_lst
    df_clean['expiration_date'] = expiration_date_lst
    df_clean['file_name'] = file_name_lst
    df_clean['url'] = url_lst
    df_clean['source_type'] = source_type_lst
    df_clean['lang'] = lang_lst
    df_clean['category_1'] = category_1_lst
    df_clean['category_2'] = category_2_lst
    df_clean['title'] = title_lst
    df_clean['description'] = description_lst
    df_clean['section'] = section_lst
    df_clean['updated_date'] = updated_date_lst

    for k in range(len(df_clean)):
        document_id_lst.append(file_name_lst.index(df_clean['file_name'].values[0]) + num_id) # this
    df_clean['document_id'] = document_id_lst

    res = df_clean.reset_index().groupby('document_id').agg(lambda x: x.nunique())
    for j in range(res['index'].values[0]):
        num_str = str(j+1)
        par_num = 'par' + num_str
        par_lst.append(par_num)
    df_clean['paragraph/chunk'] = par_lst

    domain = urlparse(url_lst[0]).netloc
    df_clean['domain'] = domain

    new_cols = ['db_name', 'table_name', 'issue_date', 'expiration_date', 'file_name', 'document_id', 'url','domain', 'source_type', 'lang', 'category_1', 'category_2', 'title', 'description', 'section', 'paragraph/chunk', 'text', 'updated_date']

    df_clean = df_clean[new_cols]
    return df_clean

def json_to_df(json_result:json) -> pd.DataFrame:
    parsed_result = json.loads(json_result)
    
    output_list = []

    
    for idx,doc in enumerate(parsed_result):
        try:
            x = create_table_postpro(parsed_result[idx]['pdf_path'],parsed_result[idx]['text'],parsed_result[idx]['document_id'] )
            output_list.append(x)
        except PdfReadError as e1:
            print("Error creating table for: %s - %s" %(parsed_result[idx], e1))
        except fitz.FileDataError as e2:
            print("Error creating table for: %s - %s" %(parsed_result[idx], e2))

    final = pd.concat(output_list)
    return final


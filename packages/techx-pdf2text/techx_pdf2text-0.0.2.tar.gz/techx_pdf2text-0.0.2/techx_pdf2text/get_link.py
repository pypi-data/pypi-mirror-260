import requests
from bs4 import BeautifulSoup
import io
from PyPDF2 import PdfFileReader
import time
import random

def read_content(paths):
    # created an empty list for putting the pdfs 
    list_of_pdf = []
    for i in range(len(paths)):
        read = requests.get(paths[i])
        html_content = read.content
        soup = BeautifulSoup(html_content, "html.parser")
        l = soup.find('table')
        a = l.find_all('a')
        # print(len(a))
        for link in a:
            pdf_link = "https://res.innovestxonline.com/" + (link.get('href')[:-4]) + ".pdf"
            list_of_pdf.append(pdf_link)
            time.sleep(random.uniform(2, 5))
    list_of_pdf.sort(reverse=True)
    return list_of_pdf
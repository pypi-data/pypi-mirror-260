try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
    
setup(
  name = 'techx_pdf2text',        
  packages=['techx_pdf2text'],  
  version = '0.0.7',     
  license='MIT',       
  description = 'PDF2TEXT LIBRARY : Update extract text from img pdf(edit json indent) ', 
  author = 'TETE',                  
#   author_email = 'your.email@domain.com',    
#   url = 'https://github.com/user/reponame',   
#   download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',  
  keywords = ['PDF', 'TEXT', 'PDF2TEXT','PDF2TechX','techx_pdf2text'],   
  install_requires=[         
          'PyPDF2',
          'PyMuPDF',
          'pythainlp',
          'bs4',
          'langchain==0.0.208',
          'langchainplus-sdk',
          'Pillow',
          'easyocr',
          'fitz',
  
         
          
      ],
  classifiers=[
    'License :: OSI Approved :: MIT License',  
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
  ],
)
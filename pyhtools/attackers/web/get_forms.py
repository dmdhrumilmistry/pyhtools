import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Beta Tool
def remove_escape_seq(content:str)->str:
    '''removes \r \t \n from the html parsed content if present.
    
    Args: 
        content (str): html content of webpage

    Returns: 
        str: returns escaped html code
    '''
    return content.replace(r'\n','').replace(r'\t','').replace(r'\r','')


def get_page_content(url:str):
    '''extracts html code of the webpage 
    
    Args: 
        url (str): webpage URL

    Returns: 
        str: HTML content of the webpage
    '''
    response = requests.get(url)
    content = str(response.content)
    content = remove_escape_seq(content)
    return content


def fuzz_forms(target_url:str):
    '''get forms from html page, send post request and return html response 
    
    Args: 
        target_url (str): webpage URL containing forms

    Returns: 
        str: returns html content of page after sending fuzzed form request
    '''
    page_content = get_page_content(target_url)

    # remove\r \t \n from the page content
    page_content = remove_escape_seq(page_content)

    page_html = BeautifulSoup(page_content,'html.parser')
    forms = page_html.find_all(name='form')
    for form in forms:
        action = form.get('action')
        post_url = urljoin(target_url, action)
        # print(post_url)
        
        # method = form.get('method')

        post_data_dict = {}
        inputs = form.find_all('input')
        for input in inputs:
            inp_name = input.get('name') 
            inp_type = input.get('type')
            inp_value = input.get('value')

            if inp_type == 'text':
                inp_value = 'pyhtools-form-test'

            elif inp_type == 'password':
                inp_value = 'pyhtools-P#$$Wd!!!'

            post_data_dict[inp_name]=inp_value

        post_response = requests.post(url=post_url, data=post_data_dict)
        post_response_content = remove_escape_seq(str(post_response.content))
        post_content = BeautifulSoup(post_response_content, 'html.parser')

        return str(post_content.prettify())
    
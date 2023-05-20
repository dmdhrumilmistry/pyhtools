from os.path import isfile
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')


def read_file_lines(file_path: str) -> list[str]:
    '''reads file and returns as list of str
    
    Args:
        file_path (str): path of file to be read

    Returns:
        list: lines read from file as list of str 
    '''
    lines = []

    if isfile(file_path):
        with open(file_path, 'r') as f:
            lines = [line.strip() for line in f.readlines()]
            logging.debug(f"File Read: {file_path}")

    else:
        logging.error(f"File Not found at {file_path}")

    return lines

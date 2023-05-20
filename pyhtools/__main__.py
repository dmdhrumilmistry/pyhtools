from . UI import functions as UI
from asyncio import run

def start():
    '''Starts PyHtools UI

    Args:
        None

    Returns:
        None
    '''
    UI.banner()
    try:
        run(UI.run())
    except Exception as e:
        print(e)

if __name__ == '__main__':
    start()
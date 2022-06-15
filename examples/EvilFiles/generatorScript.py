from pyhtools.evil_files.exec_generator import (Compilers, ExecutableGenerator)
from os import getcwd

exe = ExecutableGenerator(
    file_path = r'D:\GithubRepos\pyhtools\examples\EvilFiles\generatorScript.py', # evil program file path
    output_filename = 'evil_file', # output filename without extension, adding extension might raise error
    output_dir = getcwd(), # output directory
    compiler = Compilers.DEFAULT, # compile using DEFAULT, CLANG, MINGW
    onefile = True, # creates single exe file
    remove_output = True, # deletes all compiled files and retains only exe
)

return_code = exe.generate_executable()
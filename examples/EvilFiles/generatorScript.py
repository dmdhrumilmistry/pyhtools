from pyhtools.evil_files.exec_generator import (Compilers ,ExecutableGenerator)

exe = ExecutableGenerator(
    file_path=r'D:\GithubRepos\pyhtools\examples\EvilFiles\Malwares\key_logger.py', # evil program file path
    output_filename='evil_file', # output filename without extension, adding extension might raise error
    output_dir='.', # output directory
    compiler=Compilers.DEFAULT, # compile using DEFAULT, CLANG, MINGW
    onefile=True, # creates single exe file
    remove_output=True, # deletes all compiled files and retains only exe
)

if exe.generate_executable() == 0:
    print("[*] Process Completed.")
else:
    print("[!] Error Occurred")
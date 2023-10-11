import os
import datetime

import time


# gets the filename date modified values and file size
def get_file_info(file_path):
    file_size_kb = os.path.getsize(file_path)
    file_size_kb = f'{file_size_kb // 1024} KB'

    file_date = os.path.getmtime(file_path)
    file_date = datetime.datetime.fromtimestamp(file_date).strftime('%Y-%m-%d %I:%M %p')
    return file_size_kb, file_date

# Retain only the last folder and the filename a file.
# For example, if the file_path is /home/user/folder/file.txt,
# the function will return folder/file.txt

# Retain only the last folder and the filename a file.
# For example, if the file_path is /home/user/folder/file.txt,
# the function will return folder/file.txt
def extract_last_folder_and_filename(file_path):
    # Use the os.path.split() function to split the file path into a tuple containing
    # the directory path and the filename.
    directory, filename = os.path.split(file_path)

    # Now, use os.path.basename() to get the last folder from the directory path.
    last_folder = os.path.basename(directory)

    # Finally, return the combination of the last folder and the filename.
    result = os.path.join(last_folder, filename)

    return result


# function for text file writer
def write_to_txt(file_path, data):
    with open(file_path, 'w') as file:
        file.write(data)
        file.close()


# function for text file reader
def read_from_txt(file_path):
    with open(file_path, 'r') as file:
        data = file.read()
        file.close()
        return data

#function for delete all content in a folder
def delete_folder_content(folder_path):
    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")








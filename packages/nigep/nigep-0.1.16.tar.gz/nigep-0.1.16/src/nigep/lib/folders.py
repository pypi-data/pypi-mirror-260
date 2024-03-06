import os


def mkdir_output():
    output_folder_path = f'{os.getcwd()}/output'

    try:
        if not os.path.exists(output_folder_path):
            os.mkdir(output_folder_path)

    except FileExistsError:
        pass


def get_directory_name(name, x=0):
    dir_name = (name + ('_' + str(x) if x != 0 else '')).strip()
    if not os.path.exists(dir_name):
        return dir_name
    else:
        return get_directory_name(name, x + 1)

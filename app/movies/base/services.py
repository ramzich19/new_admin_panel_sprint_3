import os


def delete_old_file(path_file):
    """ Удаление старого файла
    """
    if os.path.exists(path_file):
        os.remove(path_file)
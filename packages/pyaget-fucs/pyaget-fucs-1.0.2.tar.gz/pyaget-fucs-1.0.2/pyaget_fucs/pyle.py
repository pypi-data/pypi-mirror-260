import os

def createFolder(pathFolder: str) -> (None):
    # Disconsider the filename
    pathFolder = dirname(pathFolder)

    # Adjust the input data
    pathFolder = pathFolder.rstrip(' /\\')

    if '/' in pathFolder or '\\' in pathFolder:
        # Split path in subfolders
        folders = pathFolder.split('/')\
            if '/' in pathFolder\
            else pathFolder.split('\\')
    else:
        # Put input data in list
        folders = [pathFolder]

    # String to acumulate the folders
    totalPath = ''

    if not any(folders[0]):
        # Access the root
        totalPath += "/"

        folders = folders[1:]

    # Looping in folders
    for folder in folders:
        # Update the total path
        totalPath += f'{folder}/'

        # Create resepctive folder if not exist
        if not exists(totalPath):
            mkdir(totalPath)

    return None


def mkdir(path: str) -> (None):
    try:
        os.mkdir(path)
    except FileExistsError:
        pass
    return None


def exists(path: str) -> (bool):
    return os.path.exists(path)


def dirname(path: str) -> (str):
    return os.path.dirname(path)


def basename(path: str) -> (str):
    return os.path.basename(path)


def get_ext(filename: str) -> (str):
    return os.path.splitext(filename)[1][1:]

def rm(filename: str, path: str = ".") -> (str):
    path = path.rstrip('/\\') # Adjust path
    filePath = f"{path}/{filename}"
    os.remove(filePath)
    return filePath
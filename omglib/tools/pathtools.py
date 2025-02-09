import os
from pathlib import Path
import shutil
import tempfile
import hashlib


class PathTools:
    # === General Path Operations ===
    @staticmethod
    def get_home_directory():
        """Returns the user's home directory."""
        return Path.home()

    @staticmethod
    def join_paths(*paths):
        """Joins multiple paths into one."""
        return os.path.join(*paths)

    @staticmethod
    def get_absolute_path(path):
        """Returns the absolute path of the given path."""
        return str(Path(path).resolve())

    @staticmethod
    def is_path_exists(path):
        """Checks if a given path exists."""
        return Path(path).exists()

    @staticmethod
    def is_file(path):
        """Checks if the given path is a file."""
        return Path(path).is_file()

    @staticmethod
    def is_directory(path):
        """Checks if the given path is a directory."""
        return Path(path).is_dir()

    @staticmethod
    def create_directory(path, parents=True, exist_ok=True):
        """Creates a directory."""
        Path(path).mkdir(parents=parents, exist_ok=exist_ok)

    @staticmethod
    def delete_path(path):
        """
        Deletes a file or directory.
        Automatically handles whether the path is a file or directory.
        """
        path_obj = Path(path)
        if path_obj.is_file():
            path_obj.unlink()
        elif path_obj.is_dir():
            shutil.rmtree(path)
        else:
            raise FileNotFoundError(f"{path} does not exist.")

    @staticmethod
    def get_parent_directory(path):
        """Returns the parent directory of the given path."""
        return str(Path(path).parent)

    # === File Operations ===
    @staticmethod
    def read_file(path, encoding="utf-8"):
        """Reads and returns the content of a file."""
        with open(path, 'r', encoding=encoding) as file:
            return file.read()

    @staticmethod
    def write_to_file(path, content, mode='w', encoding="utf-8"):
        """Writes content to a file."""
        with open(path, mode, encoding=encoding) as file:
            file.write(content)

    @staticmethod
    def append_to_file(path, content, encoding="utf-8"):
        """Appends content to a file."""
        PathTools.write_to_file(path, content, mode='a', encoding=encoding)

    @staticmethod
    def get_file_size(path):
        """Returns the size of the file in bytes."""
        return Path(path).stat().st_size

    @staticmethod
    def copy_file(source, destination):
        """Copies a file to the destination."""
        shutil.copy(source, destination)

    @staticmethod
    def move_file(source, destination):
        """Moves a file or directory to the destination."""
        shutil.move(source, destination)

    @staticmethod
    def get_file_hash(path, algorithm="sha256"):
        """
        Calculates and returns the hash of a file.
        Supported algorithms: 'md5', 'sha1', 'sha256', etc.
        """
        hash_func = hashlib.new(algorithm)
        with open(path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()

    # === Directory Operations ===
    @staticmethod
    def list_directory(path, recursive=False, include_files=True, include_dirs=True):
        """
        Lists all files and directories in the given directory.
        :param recursive: If True, searches subdirectories recursively.
        :param include_files: If True, includes files in the result.
        :param include_dirs: If True, includes directories in the result.
        """
        dir_path = Path(path)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory.")

        items = []
        if recursive:
            for item in dir_path.rglob("*"):
                if (include_files and item.is_file()) or (include_dirs and item.is_dir()):
                    items.append(str(item))
        else:
            for item in dir_path.iterdir():
                if (include_files and item.is_file()) or (include_dirs and item.is_dir()):
                    items.append(str(item))
        return items

    @staticmethod
    def find_files_by_name(directory, name):
        """
        Finds files with a specific name in a directory (non-recursive).
        """
        dir_path = Path(directory)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"{directory} is not a directory.")
        return [str(item) for item in dir_path.glob(name)]

    @staticmethod
    def delete_directory_contents(directory):
        """Deletes all contents inside a directory but keeps the directory itself."""
        dir_path = Path(directory)
        if dir_path.is_dir():
            for item in dir_path.iterdir():
                if item.is_file():
                    item.unlink()
                elif item.is_dir():
                    shutil.rmtree(item)
        else:
            raise NotADirectoryError(f"{directory} is not a directory.")

    # === Symbolic Links ===
    @staticmethod
    def create_symlink(source, destination):
        """
        Creates a symbolic link pointing from source to destination.
        """
        os.symlink(source, destination)

    @staticmethod
    def is_symlink(path):
        """Checks if the given path is a symbolic link."""
        return Path(path).is_symlink()

    # === Temporary Files and Directories ===
    @staticmethod
    def create_temp_file(prefix="tmp", suffix=".txt"):
        """
        Creates a temporary file and returns its path.
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, prefix=prefix, suffix=suffix)
        return temp_file.name

    @staticmethod
    def create_temp_directory(prefix="tmp"):
        """
        Creates a temporary directory and returns its path.
        """
        return tempfile.mkdtemp(prefix=prefix)

    # === Advanced Utilities ===
    @staticmethod
    def get_file_extension(path):
        """Returns the file extension of the given path."""
        return Path(path).suffix

    @staticmethod
    def change_file_extension(path, new_extension):
        """Changes the file extension of the given path."""
        file_path = Path(path)
        if file_path.is_file():
            new_path = file_path.with_suffix(new_extension)
            file_path.rename(new_path)
            return str(new_path)
        else:
            raise FileNotFoundError(f"{path} is not a file.")

    @staticmethod
    def count_files_and_dirs(path):
        """
        Counts the number of files and directories in a given directory.
        :returns: Tuple (num_files, num_dirs)
        """
        dir_path = Path(path)
        if not dir_path.is_dir():
            raise NotADirectoryError(f"{path} is not a directory.")
        num_files = sum(1 for item in dir_path.iterdir() if item.is_file())
        num_dirs = sum(1 for item in dir_path.iterdir() if item.is_dir())
        return num_files, num_dirs

    @staticmethod
    def compare_files(file1, file2):
        """
        Compares two files byte by byte.
        :returns: True if files are identical, False otherwise.
        """
        return filecmp.cmp(file1, file2, shallow=False)

def smart_path(path:str,joinpath:str):
    return Path(path).joinpath(joinpath)
def smart_paths(path:str,*paths:str):
    temp_path = path
    for p in paths:
        temp_path = Path(temp_path).joinpath(p)
    return temp_path

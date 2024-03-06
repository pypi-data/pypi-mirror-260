import os
import shutil


class Pyxplorer:
    def __init__(self, path: str = None) -> None:
        """
        Initialize Pyxplorer class

        :param path:
        :type path: str
        :return None:
        """
        self.path = path

        self.__files = []
        self.__folders = []
        self.__extensions = []

        if self.path:
            self.__explore()

    def __explore(self) -> None:
        """
        Explore the path
        :return None:
        """
        for root, dirs, files in os.walk(self.path):
            for file in files:
                self.__files.append(os.path.join(root, file))
                self.__extensions.append(file.split(".")[-1])
            for folder in dirs:
                self.__folders.append(os.path.join(root, folder))

    def get_files(self, path: str = None, absolute: bool = False) -> list:
        """
        Get files

        :param path:
        :param absolute:
        :type path: str
        :type absolute: bool
        :return list:
        """
        if path:
            self.path = path
            self.__explore()

        if absolute:
            return self.__files

        return [os.path.basename(file) for file in self.__files]

    def get_folders(self, path: str = None, absolute: bool = False) -> list:
        """
        Get folders

        :param absolute:
        :param path:
        :type path: str
        :type absolute: bool
        :return list:
        """
        if absolute and path:
            return self.__folders

        if path:
            self.path = path
            self.__explore()

        return (
            [os.path.basename(folder) for folder in self.__folders]
            if not absolute
            else self.__folders
        )

    def get_extensions(self) -> list:
        """
        Get extensions
        :return list:
        """
        return self.__extensions

    @staticmethod
    def copy(path: str = None, destination: str = None) -> None:
        """
        Copy files to destination

        :param path:
        :type path: str
        :param destination:
        :type destination: str
        :return None:
        """
        if path and destination:
            shutil.copy(path, destination)

    @staticmethod
    def move(path: str = None, destination: str = None) -> None:
        """
        Move files to destination

        :param path:
        :type path: str
        :param destination:
        :type destination: str
        :return None:
        """
        if path and destination:
            shutil.move(path, destination)

    def create_folder(self, folder: str = None) -> None:
        """
        Create folder

        :param folder:
        :type folder: str
        :return None:
        """
        if folder is None:
            raise ValueError("Folder name is required")

        if folder in self.__folders:
            raise ValueError("Folder already exists")
        elif folder:
            os.mkdir(os.path.join(self.path, folder))

    def __delete(self, path: str = None) -> None:
        """
        Delete files

        :param path:
        :type path: str
        :return None:
        """
        if os.path.basename(path) in self.__files:
            os.remove(path)
        else:
            raise ValueError("File does not exist")

    def __delete_folder(self, path: str = None) -> None:
        """
        Delete folder

        :param path:
        :type path: str
        :return None:
        """
        if os.path.basename(path) in self.__folders:
            shutil.rmtree(path)
        else:
            raise ValueError("Folder does not exist")

    def __repr__(self) -> str:
        """
        Representation of Pyxplorer class
        :return str:
        """
        return f"{self.__class__.__name__}({self.path})"

    def __str__(self) -> str:
        """
        String representation of Pyxplorer class
        :return str:
        """
        return f"{self.__class__.__name__}({self.path})"

    def __len__(self) -> int:
        """
        Length of Pyxplorer class
        :return int:
        """
        return len(self.__files)

    def __getitem__(self, index, absolute: bool = False) -> str:
        """
        Get item from Pyxplorer class

        :param index:
        :param absolute:
        :type index:int
        :type absolute: bool
        :return str:
        """
        if absolute:
            return self.__files[index]

        return os.path.basename(self.__files[index])


class Sweepy(Pyxplorer):
    """
    This class is used to sweep files and folders.
    """

    def __init__(self, path: str) -> None:
        """
        Initialize Sweepy class

        :param path:
        :type path: str
        :return None:
        """
        super().__init__(path)

    def extension_sort(self, path: str = None, rem: bool = True) -> None:
        """
        Sort files by extensions

        :param path:
        :param rem:
        :type path: str
        :type rem: bool
        :return None:
        """

        if path:
            self.path = path
            self.__explore()

        files = self.get_files()
        folders = self.get_folders()
        extensions = self.get_extensions()

        if folders != extensions:
            for file in files:
                full_path = os.path.join(self.path, file).replace("/", "\\")
                dest_folder = os.path.join(self.path, file.split(".")[-1]).replace("/", "\\")
                if file.split(".")[-1] not in folders:
                    os.mkdir(dest_folder)
                    folders.append(file.split(".")[-1])

                dest_path = os.path.join(dest_folder, os.path.basename(file))
                if not os.path.exists(dest_path):
                    if rem:
                        self.move(full_path, dest_folder)
                    else:
                        self.copy(full_path, dest_folder)
                else:
                    # Handle case when the destination file already exists
                    print(
                        f"File '{os.path.basename(file)}' already exists in '{dest_folder}'. Skipping..."
                    )

    # def date_created_sort(self) -> None:
    #     """
    #     Sort files by date created
    #     """
    #     # TODO: Implement date_created_sort method
    #     pass

    def reverse(self, path: str = None) -> None:
        """
        Reverse the files and folders

        :param path:
        :type path: str
        :return None:
        """

        if path:
            self.path = path

        folders = self.get_folders()
        files = self.get_files()

        for folder in folders:
            for file in files:
                if file.split(".")[-1] == folder:
                    # fmt: pass
                    self.move(os.path.join(self.path, f"{folder + "/" + file}").replace('/', '\\'),
                              f"{(self.path + '/').replace('/', '\\')}")

            os.rmdir(os.path.join(self.path, folder).replace("/", "\\"))


if __name__ == "__main__":
    p = Pyxplorer("C:\\Users\\Asus-Users\\PycharmProjects\\sorters\\pysorters_prj")

    print(p.get_files())
    print(p.get_folders())
    print(p.get_extensions())

    print(len(p))

    print(p[0])

    print(p)

    sweepy = Sweepy("C:\\TEST_FOLDER")

    sweepy.extension_sort()

    # p.create_folder('test')
    #
    # p.move(path='C:\\Users\\Asus-Users\\PycharmProjects\\sorters\\pysorters_prj\\testing.py',
    #        destination='C:\\Users\\Asus-Users\\PycharmProjects\\sorters\\pysorters_prj\\test')

import os

from filepy import Pyxplorer


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
    sweeper = Sweepy("C:/TEST_FOLDER")
    sweeper.extension_sort()
    # sweeper.reverse()
    # sweeper.date_created_sort()

import pytest

from pysorters import Sorter, gran_array_int, gran_array_float
from pysorters import Sweepy, Pyxplorer


def test_bubble_sort_man():
    sort = Sorter()
    array = [5, 3, 8, 6, 7, 2]

    sorted_array = sort.bubble_sort(array)
    assert sorted_array == [2, 3, 5, 6, 7, 8]


def test_merge_sort_man():
    sort = Sorter()
    array = [5, 3, 8, 6, 7, 2]

    sorted_array = sort.merge_sort(array)
    assert sorted_array == [2, 3, 5, 6, 7, 8]


def test_bubble_sort_gen():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.bubble_sort(array)
    array.sort()

    assert sorted_array == array


def test_merge_sort_gen():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.merge_sort(array)
    array.sort()

    assert sorted_array == array


def test_quick_sort_man():
    sort = Sorter()
    array = [5, 3, 8, 6, 7, 2]

    sorted_array = sort.quick_sort(array)
    assert sorted_array == [2, 3, 5, 6, 7, 8]


def test_quick_sort_gen():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.quick_sort(array)
    array.sort()

    assert sorted_array == array


def test_thunder_methods():
    sort = Sorter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

    assert sort.__repr__() == "Sorter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])"
    assert sort.__str__() == "Sorter([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])"
    assert sort.__len__() == 10
    assert sort.__getitem__(0) == 1
    assert sort.__getitem__(9) == 10
    assert sort.__contains__(5) is True
    assert sort.__contains__(11) is False
    assert sort.__delitem__(0) is None

    sort.__setitem__(0, 1)
    assert sort.__getitem__(0) == 1
    assert sort.__len__() == 9


def test_quick_sort_gen_float():
    sort = Sorter()
    array = gran_array_float()

    sorted_array = sort.quick_sort(array)
    array.sort()

    assert sorted_array == array


def test_bubble_sort_gen_float():
    sort = Sorter()
    array = gran_array_float()

    sorted_array = sort.bubble_sort(array)
    array.sort()

    assert sorted_array == array


def test_merge_sort_gen_float():
    sort = Sorter()
    array = gran_array_float()

    sorted_array = sort.merge_sort(array)
    array.sort()

    assert sorted_array == array


def test_quick_sort_reverse():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.quick_sort(array, reverse=True)
    array.sort(reverse=True)

    assert sorted_array == array


def test_bubble_sort_reverse():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.bubble_sort(array, reverse=True)
    array.sort(reverse=True)

    assert sorted_array == array


def test_merge_sort_reverse():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.merge_sort(array, reverse=True)
    array.sort(reverse=True)

    assert sorted_array == array


def test_sweepy_pyxplorer():
    sweep = Sweepy()
    plorer = Pyxplorer()

    plorer.path = "C:\\"

    folders: list[str] = plorer.get_folders(path="C:\\TEST_FOLDER", absolute=False)
    files: list[str] = plorer.get_files(path="C:\\TEST_FOLDER", absolute=False)

    folders_t: list[str] = sweep.get_folders(path="C:\\TEST_FOLDER", absolute=True)
    files_t: list[str] = sweep.get_files(path="C:\\TEST_FOLDER", absolute=True)

    assert folders_t == []
    assert files_t == [
        "C:\\TEST_FOLDER\\L01.pdf",
        "C:\\TEST_FOLDER\\L02.pdf",
        "C:\\TEST_FOLDER\\L03.pdf",
        "C:\\TEST_FOLDER\\laba_final.s",
        "C:\\TEST_FOLDER\\laba_try.exe",
        "C:\\TEST_FOLDER\\Machine Learning-A-Z-Codes-Datasets.zip",
        "C:\\TEST_FOLDER\\Mizhnarodna-Sistema-Odinic-SI.pdf",
        "C:\\TEST_FOLDER\\Mizhnarodna-Sistema-Odinic-SI.pptx",
        "C:\\TEST_FOLDER\\photo_2023-11-09_20-03-43 (2).jpg",
        "C:\\TEST_FOLDER\\photo_2023-11-09_20-03-43.jpg",
        "C:\\TEST_FOLDER\\photo_2023-11-09_20-03-44.jpg",
        "C:\\TEST_FOLDER\\photo_2023-11-09_20-03-45.jpg",
        "C:\\TEST_FOLDER\\RGR3 V16.pdf",
        "C:\\TEST_FOLDER\\RGR3 V19.mcdx",
        "C:\\TEST_FOLDER\\Screenshot 2023-12-16 235650.png",
        "C:\\TEST_FOLDER\\StatCounter-social_media-UA-monthly-202212-202312.png",
        "C:\\TEST_FOLDER\\Trepalin_Yegor.jpg",
        "C:\\TEST_FOLDER\\Trepalin_Yegor_Web2_Calculator.xlsx",
        "C:\\TEST_FOLDER\\ts_cp_2.ms12",
        "C:\\TEST_FOLDER\\untitled.png",
        "C:\\TEST_FOLDER\\untitled2.png",
        "C:\\TEST_FOLDER\\Інтерференція (відновлено автоматично).docx",
        "C:\\TEST_FOLDER\\Вимірювання_фокусних_відстаней_лінз.docx",
        "C:\\TEST_FOLDER\\Вимірювання_фокусних_відстаней_лінз_ФЕ-21_Трепалін_Єгор_Перевірено.docx",
        "C:\\TEST_FOLDER\\ГС_Протокол_КП_1_Трепалін_Єгор.docx",
        "C:\\TEST_FOLDER\\Дифракція_ФЕ-21_Трепалін_Єгор.docx",
        "C:\\TEST_FOLDER\\Книга1.xlsx",
        "C:\\TEST_FOLDER\\Книга1234234.xlsx",
        "C:\\TEST_FOLDER\\Контрольне завдання 3 ФЕ-21 Трепалін Єгор.pdf",
    ]
    assert folders == []
    assert files == [
        "L01.pdf",
        "L02.pdf",
        "L03.pdf",
        "laba_final.s",
        "laba_try.exe",
        "Machine Learning-A-Z-Codes-Datasets.zip",
        "Mizhnarodna-Sistema-Odinic-SI.pdf",
        "Mizhnarodna-Sistema-Odinic-SI.pptx",
        "photo_2023-11-09_20-03-43 (2).jpg",
        "photo_2023-11-09_20-03-43.jpg",
        "photo_2023-11-09_20-03-44.jpg",
        "photo_2023-11-09_20-03-45.jpg",
        "RGR3 V16.pdf",
        "RGR3 V19.mcdx",
        "Screenshot 2023-12-16 235650.png",
        "StatCounter-social_media-UA-monthly-202212-202312.png",
        "Trepalin_Yegor.jpg",
        "Trepalin_Yegor_Web2_Calculator.xlsx",
        "ts_cp_2.ms12",
        "untitled.png",
        "untitled2.png",
        "Інтерференція (відновлено автоматично).docx",
        "Вимірювання_фокусних_відстаней_лінз.docx",
        "Вимірювання_фокусних_відстаней_лінз_ФЕ-21_Трепалін_Єгор_Перевірено.docx",
        "ГС_Протокол_КП_1_Трепалін_Єгор.docx",
        "Дифракція_ФЕ-21_Трепалін_Єгор.docx",
        "Книга1.xlsx",
        "Книга1234234.xlsx",
        "Контрольне завдання 3 ФЕ-21 Трепалін Єгор.pdf",
        "L01.pdf",
        "L02.pdf",
        "L03.pdf",
        "laba_final.s",
        "laba_try.exe",
        "Machine Learning-A-Z-Codes-Datasets.zip",
        "Mizhnarodna-Sistema-Odinic-SI.pdf",
        "Mizhnarodna-Sistema-Odinic-SI.pptx",
        "photo_2023-11-09_20-03-43 (2).jpg",
        "photo_2023-11-09_20-03-43.jpg",
        "photo_2023-11-09_20-03-44.jpg",
        "photo_2023-11-09_20-03-45.jpg",
        "RGR3 V16.pdf",
        "RGR3 V19.mcdx",
        "Screenshot 2023-12-16 235650.png",
        "StatCounter-social_media-UA-monthly-202212-202312.png",
        "Trepalin_Yegor.jpg",
        "Trepalin_Yegor_Web2_Calculator.xlsx",
        "ts_cp_2.ms12",
        "untitled.png",
        "untitled2.png",
        "Інтерференція (відновлено автоматично).docx",
        "Вимірювання_фокусних_відстаней_лінз.docx",
        "Вимірювання_фокусних_відстаней_лінз_ФЕ-21_Трепалін_Єгор_Перевірено.docx",
        "ГС_Протокол_КП_1_Трепалін_Єгор.docx",
        "Дифракція_ФЕ-21_Трепалін_Єгор.docx",
        "Книга1.xlsx",
        "Книга1234234.xlsx",
        "Контрольне завдання 3 ФЕ-21 Трепалін Єгор.pdf",
    ]

    assert sweep.__repr__() == "Sweepy(C:\\TEST_FOLDER)"
    assert sweep.__str__() == "Sweepy(C:\\TEST_FOLDER)"
    assert sweep.__len__() == 29

    sweep = Sweepy("C:\\TEST_FOLDER")
    assert sweep.__repr__() == "Sweepy(C:\\TEST_FOLDER)"
    assert sweep.__str__() == "Sweepy(C:\\TEST_FOLDER)"

    result = sweep.get_folders()
    assert result == []


def test_insertion_sort():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.insertion_sort(array)
    array.sort()

    assert sorted_array == array


def test_selection_sort():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.selection_sort(array)
    array.sort()

    assert sorted_array == array


def test_heap_sort():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.heap_sort(array)
    array.sort()

    assert sorted_array == array


def test_counting_sort():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.counting_sort(array)
    array.sort()

    assert sorted_array == array


def test_radix_sort():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.radix_sort(array)
    array.sort()

    assert sorted_array == array


def test_bucket_sort():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.bucket_sort(array)
    array.sort()

    assert sorted_array == array


def test_tim_sort():
    sort = Sorter()
    array = gran_array_int()

    sorted_array = sort.tim_sort(array)
    array.sort()

    assert sorted_array == array


def test_folder_creation():
    plorer = Pyxplorer()
    plorer.path = "C:\\TEST_FOLDER"
    plorer.create_folder("TEST_FOLDER2")
    assert plorer.get_folders(path="C:\\TEST_FOLDER", absolute=False) == [
        "TEST_FOLDER2"
    ]


def test_extension_sort():
    sweep = Sweepy("C:\\TEST_FOLDER")
    sweep.extension_sort()
    assert sweep.get_folders() == ["TEST_FOLDER2"]


def test_reverse_extension_sort():
    sweep = Sweepy("C:\\TEST_FOLDER")
    sweep.reverse_ext()
    assert sweep.get_folders() == [
        "docx",
        "exe",
        "jpg",
        "mcdx",
        "ms12",
        "pdf",
        "png",
        "pptx",
        "s",
        "TEST_FOLDER2",
        "xlsx",
        "zip",
    ]


if __name__ == "__main__":
    pytest.main()

import os


def rename_filename_to_lower(folder_path):
    files = os.listdir(folder_path)
    for file in files:
        old_path = os.path.join(folder_path, file)

        new_filename = file.lower()

        new_path = os.path.join(folder_path, new_filename)

        os.rename(old_path, new_path)

        print("Renamed " + file + " to " + new_filename)


folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))

rename_filename_to_lower(folder_path)

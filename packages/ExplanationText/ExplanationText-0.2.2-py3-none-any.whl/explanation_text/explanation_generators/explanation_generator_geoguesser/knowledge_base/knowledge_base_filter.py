import os
import fileinput



def remove_string_from_txt_files(folder_path, string_to_remove):
    if not folder_path.endswith('/'):
        folder_path += '/'

    # List all files in the folder
    txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    # Process each .txt file
    for file_name in txt_files:
        file_path = os.path.join(folder_path, file_name)

        # Read the content of the file
        with open(file_path, 'r') as file:
            content = file.read()

        # Remove the specified string from the content
        modified_content = content.replace(string_to_remove, '')

        # Write the modified content back to the file
        with open(file_path, 'w') as file:
            file.write(modified_content)

    print(f'String "{string_to_remove}" removed from all .txt files in {folder_path}')




def remove_single_empty_lines(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it's a .txt file
        if filename.endswith(".txt"):
            print(f"Processing file: {filename}")

            # Read the file and remove single empty lines
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Write back to the file, preserving multiple empty lines
            with open(file_path, 'w') as file:
                consecutive_empty_lines = 0
                for line in lines:
                    if line.strip() == '':
                        consecutive_empty_lines += 1
                        if consecutive_empty_lines <= 1:
                            file.write(line)
                    else:
                        file.write(line)
                        consecutive_empty_lines = 0

    print("Processing complete.")



def add_empty_lines_on_first_empty_line(folder_path):
    # Check if the folder path exists
    if not os.path.exists(folder_path):
        print(f"Error: Folder '{folder_path}' does not exist.")
        return

    # Loop through all files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        # Check if it's a .txt file
        if filename.endswith(".txt"):
            print(f"Processing file: {filename}")

            # Read the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Write back to the file, adding 4 empty lines at the first empty line
            with open(file_path, 'w') as file:
                empty_line_found = False
                for line in lines:
                    if line.strip() == '':
                        if not empty_line_found:
                            file.write('\n' * 4)  # Add 4 empty lines
                            empty_line_found = True
                    else:
                        file.write(line)
                        empty_line_found = False

    print("Processing complete.")



# Example usage
folder_path = 'countries'
string_to_remove = 'NOTE: '
remove_single_empty_lines(folder_path)

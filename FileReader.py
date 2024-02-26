# imports

# global variables for object


# class definition

class FileReader:
    def __init__(self, file_path):
        self.file_path = file_path
    
    def read_x_lines(self, n_of_lines):
        try:
            with open(self.file_path, 'r') as file:
                for line in range(n_of_lines):
                    line = next(file)
                    yield line.strip()
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
        except Exception as e:
            print(f"Error occurred during reading of file: '{e}'")
    def read_lines(self):
        try:
            with open(self.file_path, 'r') as file:
                for line in file:
                    #line = next(file)
                    #print(line)
                    
                    yield line.strip()
        except FileNotFoundError:
            print(f"Error: File '{self.file_path}' not found.")
        except Exception as e:
            print(f"Error occurred during reading of file: '{e}'")
    def process_rows(self, rows):
        row_Num = 0
        for row in rows:
            try:
                # In case we have empty line
                if not row.strip():
                    raise ValueError("Empty line")
                # Split to filter and parse the data
                fields = row.split(',')
                name_title = fields[0].strip()
                # Certain names contains titles such as Prof. or Dr. this counts the number of spaces in the name field
                num_of_spaces = name_title.count(' ')
                # If there are two spaces then there is a title else there is just first_name last_name
                if num_of_spaces > 1:
                    title, name = name_title.split(maxsplit=1)
                else:
                    title = "N/A"
                    name = name_title
                    #print(name_title)
                # Prints empty on any row that may contain and empty column field.
                if any(not field for field in fields):
                    print("Empty field, skipping line")
                else:
                    print(f"{row_Num}: {title}, {name}, {', '.join(fields[1:])}")
                    # Counts only valid fields now, this is for internal use for my namedTuple.
                    row_Num = row_Num + 1
            except ValueError as ve:
                print(f"Skipping empty line")
            except Exception as e:
                print(f"Error occurred while processing file at line {row_Num}: {str(e)}")
                break

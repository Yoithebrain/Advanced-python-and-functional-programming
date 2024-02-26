###
# Main file to process the data and analyse it
# - CLYNGE 260224 - 
#### 
# Imports
import collections
from FileReader import FileReader

# global variables

file_path = None
reader = FileReader('files\\big_file_with_errors.txt')

# My collection - immutable structure - to be used for later :3
DanishPerson = collections.namedtuple('DanishPerson', ['name', 'job', 'phone_number', 'address', 'postcode'])

# Function layer

# Function to get specific number of lines from start of file - Useful for debgugging filereader object
def get_n_lines (n_of_lines):
    for line in reader.read_x_lines(n_of_lines):
        print(line)

###
# Moved the processing of lines into the file reader
# - CLY 260224 - 
###
'''
# Function to get all lines within file 
def get_lines ():
    # Row number
    row_Num = 0
    # Loop to get a single line at a time via the generator object
    for line in reader.read_lines():
        try:
            # In case we have empty line
            if not line.strip():
                raise ValueError("Empty line")
            # Split to filter and parse the data
            fields = line.split(',')
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
'''
print("READING FILE:")
#get_line(5)
#get_lines()
lines = reader.read_lines()
reader.process_rows(lines)
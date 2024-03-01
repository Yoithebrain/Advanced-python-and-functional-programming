###
# Main file to process the data and analyse it
# - CLYNGE 260224 - 
#### 
# Imports
import collections
from FileReader import FileReader
import cProfile
import multiprocessing

# global variables
file_path = None

# My collection - immutable structure - to be used for later :3
DanishPerson = collections.namedtuple('DanishPerson', ['name', 'job', 'phone_number', 'address', 'postcode'])

# Function layer

# Function to get specific number of lines from start of file - Useful for debgugging filereader object
''''
def get_n_lines (n_of_lines):
    for line in reader.read_x_lines(n_of_lines):
        print(line)
'''
# Function for read file process, takes a reader. Queue is used to allow the second process to process the line
def read_file(reader, queue):
    for line in reader.read_lines():
        queue.put(line)
    queue.put("END")


def process_lines(queue, reader):
    line_count = 0
    while True:
        line = queue.get()
        if line == "END":
            break
        reader.process_rows([line])
        line_count += 1
        print(f"Processed {line_count} lines", end="\r")
###
# Trying to multiprocess this now, for better performance
# - CLY 290224 -
####
###
# Update - Found a bottleneck in reading the file, therefore no multiprocessing gets applied to this step. Hopefully this stops the threads going ballistic over who gets to lock the file
# for the next line.
# - CLY 010324 -
####
def main ():
    # Init profiler
    pr = cProfile.Profile()
    pr.enable()
    # Perform file reading and processing here
    reader = FileReader('files\\really_big_file_with_errors.txt')
    # queue an pool setup
    queue = multiprocessing.Manager().Queue()
    pool = multiprocessing.Pool(processes=1)
    # Pool applies to functions
    #pool.apply_async(read_file, args=(reader, queue))

    pool.apply_async(process_lines, args=(queue, reader))

    # Have to add this down here instead - Enqueuing happens here
    for line in reader.read_lines():
        queue.put(line)
    queue.put("END")
    # Ending of pool resources
    pool.close()  # No more tasks will be added to the pool
    pool.join()   # Wait for all processes to complete
    
    pr.disable()
    pr.print_stats(sort='cumulative')

    #print("READING FILE:")
    #get_line(5)
    #get_lines()
    #remove_empty_row = lambda row: all(field for field in row.split(','))
    #lines = reader.read_lines()
    #reader.process_rows(lines)
if __name__ == "__main__":
    main()
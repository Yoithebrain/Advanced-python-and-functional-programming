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
# Function for read file process, takes a queue and a filepath. Queue is used to allow the second process to process the line
def read_file (reader, queue):
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
def main ():
    # Init profiler
    pr = cProfile.Profile()
    pr.enable()
    reader = FileReader('files\\really_big_file_with_errors.txt')
    # The number of proccesors
    # num_of_processors = 2
    ###
    # This code turned out to be slower, issue might be due to the fact that the queue fills faster than it can be emptied.
    # - CLY 290224 -
    ###
    # Creates queue for processors to communicate between
    queue = multiprocessing.Queue()
    # Create a process that reads the file
    reader_process = multiprocessing.Process(target=read_file, args=(reader, queue))
    reader_process.start()
    # Create a process that handles processing the lines from the queue
    line_processing_process = multiprocessing.Process(target=process_lines, args=(queue, reader))
    line_processing_process.start()

    

    # Wait for the processors to finish
    reader_process.join()
    line_processing_process.join()
   
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
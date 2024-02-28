# imports
import matplotlib.pyplot as plt
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
    def process_rows(self, rows, filter_func=None):
        row_Num = 0
        for row in rows:
            try:
                # Apply filtering function if provided
                if filter_func and not filter_func(row):
                    continue  # Skip processing if the row doesn't meet the filtering criteria
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
    def analyze_rows_plot_rows(self, rows, plot_types=['histogram']):
        # Analysis and plot generation logic goes here
        for plot_type in plot_types:
            if plot_type == 'histogram':
                job_titles = []
                for row in rows:
                    fields = row.split(',')
                    if len(fields) >= 2:  # Assuming job title is at index 1
                        job_titles.append(fields[1].strip())
                plt.hist(job_titles, bins=20)
                plt.xlabel('Job Titles')
                plt.ylabel('Frequency')
                plt.title('Distribution of Job Titles')
                yield plt
            elif plot_type == 'bar':
                # Add logic for generating bar plot
                pass
            elif plot_type == 'pie':
                # Add logic for generating pie chart
                pass
            else:
                print(f"Unsupported plot type: {plot_type}")

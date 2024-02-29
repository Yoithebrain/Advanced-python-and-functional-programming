# imports
import matplotlib.pyplot as plt
import os
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
    def analyze_rows_plot_rows(self, rows, plot_types=['histogram'], output_dir='plots', x_field=None, y_field=None):
        # Define the fields to search for, taken from parameters. Defaults to none.
        x_target_field = x_field 
        y_target_field = y_field
        # Process rows to extract x and y values
        x_values_list = []
        y_values_list = []
        for row in rows:
            fields = row.split(',')
            # Search for the target field in the row
            x_value = None
            y_value = None
            for field in fields:
                key, value = field.split(':')  # Assuming fields are in key:value format
                if key.strip() == x_target_field:
                    x_value = float(value.strip())  # Convert to appropriate data type if necessary
                elif key.strip() == y_target_field:
                    y_value = float(value.strip())  # Convert to appropriate data type if necessary
                # If both x and y values are found, break the loop
                if x_value is not None and y_value is not None:
                    break
            # Add x and y values to their respective lists
            if x_value is not None and y_value is not None:
                x_values_list.append(x_value)
                y_values_list.append(y_value)

        # Combine x and y values into a list of tuples (each tuple represents one set of x and y values)
        xy_values = list(zip(x_values_list, y_values_list))
        # Creation of folder
        os.makedirs(output_dir, exist_ok=True)

        # Analysis and plot generation logic goes here
        for plot_type in plot_types:
            if plot_type == 'histogram':
                if xy_values:
                    for i, (x_values, y_values) in enumerate(xy_values):
                        plt.hist2d(x_values, y_values, bins=20)
                        plt.xlabel('X Label')
                        plt.ylabel('Y Label')
                        plt.title('2D Histogram Plot')
                        plot_filename = f"histogram_plot_{x_field}_{y_field}.png"
                        plot_filepath = os.path.join(output_dir, plot_filename)
                        plt.savefig(plot_filepath)
                        plt.close()
                        yield plot_filepath
                else:
                    print("Please provide both x_values and y_values for the histogram plot.")
            elif plot_type == 'bar':
                # Add logic for generating bar plot
                pass
            elif plot_type == 'pie':
                # Add logic for generating pie chart
                pass
            else:
                print(f"Unsupported plot type: {plot_type}")

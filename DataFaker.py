from faker import Faker
import random

fake = Faker()

# Faker file generator 
def generate_file (file_path, num_of_entries, error_rate):
    with open(file_path, 'a') as file:
        for _ in range(num_of_entries):
            # Faker dataset
            name = fake.name().replace('\n', ' ')
            address = fake.address().replace('\n', ' ')
            phone_number = fake.phone_number().replace('\n', ' ')
            job = fake.job()
            postcode = fake.postcode().replace('\n', ' ')
            ssn = fake.ssn()
            taxPaid = random.randint(0, 1)
            taxesOwed = fake.random.uniform(-10000, 10000)
            #ssn = fake.ssn()
            #email = fake.email()
            if ',' in job:
            # Split the job title by comma and take the first part
                job = job.split(',')[0].strip()
            '''
            # Introducing errors randomly based on the error rate
            if random.random() < error_rate:
                # Simulate an error in the email address
                email = ''  # Change the email to an invalid format
            '''
            # Error simulation for more real life accuracy
            if random.random() < error_rate:
                # Simulate an error in the phone number entry
                phone_number = ''  # Change the phone number to an invalid format
            
            if random.random() < error_rate:
                # Simulate an error in the job entry
                job = ''  # Change the phone number to an invalid format
            
            if random.random() < error_rate:
                # Simulate missing SSN
                ssn = ''
            # Makes sure that entries are only one line long, this will make it easier for reading the file one line at a time
            entry = ','.join([name,job,phone_number,address,postcode,ssn,str(taxPaid),str(taxesOwed)])

            # Write the data to file
            file.write(entry + "\n")

# Generate small data set to see if this works and to begin work on auctual assignment

file_path = "Files\\really_big_file_with_errors.txt"
num_of_entries = 10000000
error_rate = 0.1

generate_file(file_path, num_of_entries, error_rate)

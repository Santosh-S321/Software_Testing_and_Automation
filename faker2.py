from faker import Faker
from openpyxl import Workbook

# Create Faker object
fake = Faker("en_IN")  

# Create a new Excel workbook
workbook = Workbook()
sheet = workbook.active
sheet.title = "Fake Data"

# Add column headers
sheet.append(["Sl. No.", "Name", "Email ID", "Phone No."])

# Number of fake records to generate
num_records = 20

# Generate fake data
for i in range(1, num_records + 1):
    name = fake.name()
    email = fake.email()
    phone = fake.phone_number()

    # Add data to Excel
    sheet.append([i, name, email, phone])

# Save the workbook
workbook.save("Fake_Data.xlsx")

print(f"{num_records} fake records have been saved to 'Fake_Data.xlsx'")
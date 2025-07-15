import streamlit as st
import pandas as pd
import random
from faker import Faker
from io import BytesIO
import time

# ------------------ Data Generators ------------------ #
def general_data(n):
    fake = Faker()
    data = {
        "name": [],
        "age": [],
        "job": [],
        "company": [],
        "address": []
    }
    for _ in range(int(n)):
        data["name"].append(fake.name())
        data["age"].append(fake.random_int(min=18, max=65))
        data["job"].append(fake.job())
        data["company"].append(fake.company())
        data["address"].append(fake.address().replace("\n", ", "))
    return pd.DataFrame(data)

def medical_data(n):
    fake = Faker()
    blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    genders = ['Male', 'Female']
    data = {
        "Patient_ID": [],
        "Name": [],
        "Gender": [],
        "Age": [],
        "Date_of_Birth": [],
        "Blood_Type": [],
        "Contact_Number": [],
        "Email": [],
        "Address": [],
        "Emergency_Contact": []
    }
    for i in range(int(n)):
        gender = random.choice(genders)
        dob = fake.date_of_birth(minimum_age=18, maximum_age=90)
        age = pd.Timestamp('today').year - dob.year
        name = fake.name_male() if gender == 'Male' else fake.name_female()
        username = name.lower().replace(" ", ".").replace("'", "")
        domain = random.choice(["gmail.com", "yahoo.com", "outlook.com"])
        email = f"{username}@{domain}"
        data["Patient_ID"].append(f"P{1000+i:04d}")
        data["Name"].append(name)
        data["Gender"].append(gender)
        data["Age"].append(age)
        data["Date_of_Birth"].append(dob)
        data["Blood_Type"].append(random.choice(blood_types))
        data["Contact_Number"].append(fake.phone_number())
        data["Email"].append(email)
        data["Address"].append(fake.address().replace("\n", ", "))
        data["Emergency_Contact"].append(fake.phone_number())
    return pd.DataFrame(data)

def finance_data(n):
    fake = Faker()
    account_types = ['Savings', 'Checking', 'Credit', 'Investment']
    currencies = ['USD', 'EUR', 'INR', 'GBP', 'JPY']
    data = {
        "Customer_ID": [],
        "Name": [],
        "Account_Type": [],
        "Account_Number": [],
        "Balance": [],
        "Currency": [],
        "Bank_Name": [],
        "Branch": [],
        "Email": [],
        "Phone_Number": [],
        "Address": []
    }
    for i in range(int(n)):
        name = fake.name()
        email = fake.email()
        account_type = random.choice(account_types)
        currency = random.choice(currencies)
        balance = round(random.uniform(100.0, 100000.0), 2)
        data["Customer_ID"].append(f"C{1000+i:04d}")
        data["Name"].append(name)
        data["Account_Type"].append(account_type)
        data["Account_Number"].append(fake.bban())
        data["Balance"].append(balance)
        data["Currency"].append(currency)
        data["Bank_Name"].append(fake.company() + " Bank")
        data["Branch"].append(fake.city())
        data["Email"].append(email)
        data["Phone_Number"].append(fake.phone_number())
        data["Address"].append(fake.address().replace("\n", ", "))
    return pd.DataFrame(data)

def ecommerce_data(n):
    fake = Faker()
    product_categories = ['Electronics', 'Fashion', 'Books', 'Home & Kitchen', 'Sports', 'Toys']
    payment_methods = ['Credit Card', 'Debit Card', 'Net Banking', 'UPI', 'Cash on Delivery']
    data = {
        "Order_ID": [],
        "Customer_Name": [],
        "Product_Name": [],
        "Category": [],
        "Quantity": [],
        "Price_per_Unit": [],
        "Total_Amount": [],
        "Payment_Method": [],
        "Order_Date": [],
        "Shipping_Address": []
    }
    for i in range(int(n)):
        qty = random.randint(1, 5)
        price = round(random.uniform(10.0, 500.0), 2)
        total = round(qty * price, 2)
        data["Order_ID"].append(f"O{1000+i:05d}")
        data["Customer_Name"].append(fake.name())
        data["Product_Name"].append(fake.word().capitalize() + " " + fake.word().capitalize())
        data["Category"].append(random.choice(product_categories))
        data["Quantity"].append(qty)
        data["Price_per_Unit"].append(price)
        data["Total_Amount"].append(total)
        data["Payment_Method"].append(random.choice(payment_methods))
        data["Order_Date"].append(fake.date_between(start_date='-2y', end_date='today'))
        data["Shipping_Address"].append(fake.address().replace("\n", ", "))
    return pd.DataFrame(data)

# ------------------ Streamlit UI ------------------ #
with st.sidebar:
    st.button("Messy data")  # Placeholder, can be wired later

st.header("Fake Dataset Generator")

choice = st.selectbox("Select domain to generate relevant datasets", ("General", "Medical", "Finance", "Ecommerce", "Custom"))

# ------------------ Custom Dataset Builder ------------------ #
if choice == "Custom":
    fake = Faker()
    faker_fields = {
        "First Name": lambda: fake.first_name(),
        "Last Name": lambda: fake.last_name(),
        "Email": lambda: fake.email(),
        "City": lambda: fake.city(),
        "Country": lambda: fake.country(),
        "Phone Number": lambda: fake.phone_number(),
        "Job Title": lambda: fake.job(),
        "Integer (1-100)": lambda: random.randint(1, 100),
        "Float (0.0-1.0)": lambda: round(random.uniform(0.0, 1.0), 2),
    }

    if "fields" not in st.session_state:
        st.session_state.fields = []

    if st.button("Add Field"):
        st.session_state.fields.append({"name": "", "type": "First Name"})

    fields_to_remove = []
    for i, field in enumerate(st.session_state.fields):
        col1, col2, col3 = st.columns([4, 4, 1])
        field["name"] = col1.text_input("Field Name", value=field["name"], key=f"name_{i}")
        field["type"] = col2.selectbox("Type", list(faker_fields.keys()), index=list(faker_fields.keys()).index(field["type"]), key=f"type_{i}")
        if col3.button("❌", key=f"del_{i}"):
            fields_to_remove.append(i)

    for i in sorted(fields_to_remove, reverse=True):
        st.session_state.fields.pop(i)

# ------------------ Data Generation Trigger ------------------ #
n = st.number_input("Enter number of data rows", min_value=1, max_value=1000, value=10)
gen = st.button("Click to generate")

if gen:
    stat = st.empty()
    stat.write("Generating data, please wait...")
    time.sleep(1.5)

    if choice == "General":
        st.session_state.df = general_data(n)
    elif choice == "Medical":
        st.session_state.df = medical_data(n)
    elif choice == "Finance":
        st.session_state.df = finance_data(n)
    elif choice == "Ecommerce":
        st.session_state.df = ecommerce_data(n)
    elif choice == "Custom":
        if not st.session_state.fields:
            st.warning("⚠️ Please add at least one field.")
        else:
            data = {}
            for field in st.session_state.fields:
                field_name = field["name"] if field["name"] else field["type"]
                generator_func = faker_fields[field["type"]]
                data[field_name] = [generator_func() for _ in range(int(n))]
            st.session_state.df = pd.DataFrame(data)

    stat.empty()

if "df" in st.session_state and st.session_state.df is not None:
    df = st.session_state.df
    st.subheader("Preview of Dataset")
    st.dataframe(df.head())

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, sheet_name="FakeData", index=False)
    st.download_button("Download Excel", data=output.getvalue(), file_name="fake_data.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", data=csv, file_name="fake_data.csv", mime="text/csv")

    json_data = df.to_json(orient="records", indent=2)
    st.download_button("Download JSON", data=json_data, file_name="fake_data.json", mime="application/json")

    tsv = df.to_csv(index=False, sep='\t').encode('utf-8')
    st.download_button("Download TSV", data=tsv, file_name="fake_data.tsv", mime="text/tab-separated-values")
else:
    st.info("Generate a dataset to preview and download it.")
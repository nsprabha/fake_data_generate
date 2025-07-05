#v2
import streamlit as st
import pandas as pd
import random
from faker import Faker
from io import BytesIO 
#def createdf():

def general_data(n):
    fake=Faker()
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
    df=pd.DataFrame(data)
    return df
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

        # Gender-specific name
        name = fake.name_male() if gender == 'Male' else fake.name_female()

        # Email from name
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

    df = pd.DataFrame(data)
    return df
st.header("Fake Data")
choice=st.selectbox("Select domain to generate relevant datasets",("General","Medical","Finance","Ecommerce"))
n=st.number_input("Enter no.of data")
gen=st.button("Click to generate")
if gen:
    st.write("Generating data, please wait...")
    #st.write(choice)
    if choice=="General":
        df=general_data(n)
    if choice=="Medical":
        df=medical_data(n)
    if choice=="Finance":
        pass
    if choice=="Ecommerce":
        pass
 
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    output.seek(0)  
    st.download_button(
        label="Download as Excel",
        data=output,
        file_name="fake_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

#down=st.download_button("Download dataset",data)
import streamlit as st
import pandas as pd
import random
from faker import Faker
from io import BytesIO 
#def createdf():
st.header("Fake Data")
n=st.number_input("Enter no.of data")
gen=st.button("Click to generate")
if gen:
    fake=Faker()
    data = {
        "name": [],
        "age": [],
        "job": [],
        "company": [],
        "address": []
    }

    st.write("Generating data, please wait...")

    for _ in range(int(n)):
        data["name"].append(fake.name())
        data["age"].append(fake.random_int(min=18, max=65))
        data["job"].append(fake.job())
        data["company"].append(fake.company())
        data["address"].append(fake.address().replace("\n", ", "))

    #from io import BytesIO\

    df=pd.DataFrame(data)
    #output = BytesIO()
    #df.to_excel("output.xlsx", index=False, engine='openpyxl')
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    #with pd.ExcelWriter(output, engine='openpyxl') as writer:
    #    df.to_excel(writer, index=False)
    output.seek(0)  # Reset pointer to start

    # Use this output for download button
    st.download_button(
        label="Download as Excel",
        data=output,
        file_name="fake_data.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

#down=st.download_button("Download dataset",data)
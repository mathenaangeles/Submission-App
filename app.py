import os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

load_dotenv()

azure_storage_account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
azure_storage_account_key = os.getenv("AZURE_STORAGE_ACCOUNT_KEY")
blob_service_client = BlobServiceClient.from_connection_string(
    f"DefaultEndpointsProtocol=https;AccountName={azure_storage_account_name};AccountKey={azure_storage_account_key}"
)

azure_storage_container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")

def upload_to_azure_storage(container_name, folder_name, file):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"{folder_name}/{file.name}")
    blob_client.upload_blob(file, overwrite=True)
    st.success(f"{file.name} has been successfully uploaded to the {folder_name} folder.")

def file_exists(container_name, folder_name, file_name):
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=f"{folder_name}/{file_name}")
    return blob_client.exists()

st.title("DigiChallenge 2024 Forecasting Challenge Submissions")
st.markdown("""
##### :open_file_folder: Submission File Format: :blue-background[submission_team number_market.csv] 
Please note that your submission file must containing the following columns, where the :orange-background[highlighted] columns are your predicted variables.
            
- **UK**: PromoIDText, TUEAN, WeekSkID, :orange-background[ActualPromoSalesVolumeSellOut]
- **ID**: Customer, PromoIDText, ProductNameSku_PPH, WeekSkID, :orange-background[ActualNetPromoSalesVolumeSellOut]
            """)

uk_file = st.file_uploader("Please upload your UK CSV file.", type=["csv"], key="uk_file_uploader")

if uk_file is not None:
    st.write(f"File name: {uk_file.name}")
    st.write(f"File size: {uk_file.size} bytes")
    if file_exists(azure_storage_container_name, "uk", uk_file.name):
        st.warning("This file already exists and will be overwritten.")
    if st.button("Upload to UK submission folder", key="upload_uk"):
        upload_to_azure_storage(azure_storage_container_name, "uk", uk_file)

id_file = st.file_uploader("Please upload your ID CSV file.", type=["csv"], key="id_file_uploader")

if id_file is not None:
    st.write(f"File name: {id_file.name}")
    st.write(f"File size: {id_file.size} bytes")
    if file_exists(azure_storage_container_name, "id", id_file.name):
        st.warning("This file already exists and will be overwritten.")
    if st.button("Upload to ID submission folder", key="upload_id"):
        upload_to_azure_storage(azure_storage_container_name, "id", id_file)

st.markdown("""
# Submission Guidelines
### :white_check_mark: Evaluation Script Job Runs
- Submission will be eveluated once a day at **23:59 GMT+00:00**. 
- Submitting a new file above will overwrite your previous submission, if any.
- Only the most recent submission from each team will be considered at every job run. This is the score that will be reflected in the leaderboard.
### :trophy: Leaderboard
##### [PowerBI DigiChallenge 2024 Leaderboard](https://app.powerbi.com/groups/af629249-ad5b-42c4-8953-0f312d335990/reports/b5a6d2a5-953d-4b92-bfa2-3b6853c5bc3e?ctid=f66fae02-5d36-495b-bfe0-78a6ff9f8e6e&pbi_source=linkShare&bookmarkGuid=76c41688-3064-496c-9477-59b29875d78c)
- Teams are encouraged to submit predictions for both markets since the winners will be chosen based on whichever team has the **highest cumulatize score** from both markets.
- The public leaderboard compares the predictions with 50% of the actual sales volumes in the validation sets. The final submissions will be compared against 100% of the actual sales volumes in the validation sets. The final results will not be announced until the end of the challenge.
- Please see the scoring criteria below: 
            """)

data = {
    "UK": [50, 35, 25, 20, 15, 10, 5],
    "ID": [50, 35, 25, 20, 15, 10, 5]
}
index = ["1st", "2nd", "3rd", "4th", "5th", "6th-10th", "11th-onwards"]
df = pd.DataFrame(data, index=index)

html_table = df.to_html(classes='styled-table')

st.markdown("""
    <style>
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
    }
    .styled-table th, .styled-table td {
        border: 1px solid #dddddd;
        text-align: center;
        padding: 8px;
        width: 100px;
    }
    .styled-table th {
        font-weight: bold;
    }
    .styled-table tbody th {
        text-align: left;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown(html_table, unsafe_allow_html=True)
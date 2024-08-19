# Submission App

This is a submission app that uploads files to **Azure Blob Storage**.

## Getting Started
1. Create a virtual environment inside the repository.
2. Run `pip install -r requirements.txt`.
3. Create a `.env` file with the following contents:
```
AZURE_STORAGE_ACCOUNT_NAME = <YOUR STORAGE ACCOUNT NAME>
AZURE_STORAGE_ACCOUNT_KEY = <YOUR STORAGE ACCOUNT KEY>
AZURE_STORAGE_CONTAINER_NAME = <YOUR STORAGE CONTAINER NAME>
```
4. Run `streamlit run app.py`.
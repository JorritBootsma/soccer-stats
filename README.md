# Description 
Application to store and visualize soccer stats.

## Tech-stack
- FastAPI backend  
- Streamlit frontend  
- PostgreSQL database  

## Environment
A conda `environment.yml` is present in the repository. Create your environment with 
`conda env create -f environment.yml` and activate it with 
`conda activate soccers_stats`.

## Usage
The application currently functions with a PostgreSQL database that is running locally.
Make sure to define local environment variables `DB_SERVER` and `DB_USER`.  

Run the application by, firstly, starting the FastAPI backend using:  
`uvicorn endpoints:app --reload`  

and, secondly, the Streamlit frontend using:  
`streamlit run Main_Page.py`  

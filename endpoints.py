from fastapi import FastAPI

app = FastAPI(debug=True)


@app.post("/send_to_database")
def send_to_database():
    """
    Placeholder for the request that sends the match data to the database.

    :return:
    """
    return ""
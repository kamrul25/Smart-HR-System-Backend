from fastapi import FastAPI

new = FastAPI()
# main_logic = FastAPI()

# @main_logic.get("/")
@new.get('/')
def root():
    return{"Hi! How are you?"}


# To run the server use :
    # uvicorn app.new:new --reload 
    # uvicorn app.new:main_logic --reload 
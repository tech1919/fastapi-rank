import os

try:
    SQLALCHEMY_DATABASE_URL = os.environ.get("RANK_DATABASE_URL")
except:
    from dotenv import load_dotenv
    load_dotenv()
    
    SQLALCHEMY_DATABASE_URL = os.environ.get("RANK_DATABASE_URL")






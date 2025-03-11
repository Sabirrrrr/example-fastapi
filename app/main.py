# ***************************************************************************
'''
Libs
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post,user, auth,vote, google_auth, food

# ***************************************************************************


# ***************************************************************************
'''
Db connection
'''
# models.Base.metadata.create_all(bind=engine) # create all artık buna ihtiyacımız kalmadı sqlalchemy ile işe başlarken lazımdı artık alembic var gerek kalmadı
# ***************************************************************************

# ***************************************************************************
'''
Creating instance of fastapi
'''
app = FastAPI() 

origins = [
    "http://localhost:3000",  # Frontend development URL
    "http://127.0.0.1:3000",  # Alternative frontend URL
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ***************************************************************************

# ***************************************************************************
'''
Burasinda ise router ile alakali tanimlamalar yapiyoruz.
Bu kodlarin en basta olmasi gerektigini unutma.
'''
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
app.include_router(google_auth.router)
app.include_router(food.router)
# ***************************************************************************

# ***************************************************************************
'''
def root(): its a function. name itself it doesnt matter
@ its a decorator. act like an api we need decorator. 
Reference fastapi instance which is "app". 
"get" is a http method. 
("/") ---> it is a "url"
It is a regular function, name does not matter
Fastapi automatically converts this dict to json.
'''
@app.get("/")                                       
async def root():                                   
    return {"message": "Hello World this is Constantine and i think everything is ok for now :) try1."}               
# ***************************************************************************

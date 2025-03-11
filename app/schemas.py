from pydantic import BaseModel,ConfigDict, ValidationError, EmailStr, conint
from datetime import datetime
from typing import Optional, List

'''
Bir sınıf oluşturduk.
Pydantic-docs.helpmanuel
bir takım sınırlar belirleyeceğiz.
işe yardı pip install typing dedim.
user eğer bir şey seçmezse published için True gönderir.
'''
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None   

    model_config = {"from_attributes": True}

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional[int] = None 

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True
#     # rating: Optional[int] = None 


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None   

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id: int
    email : EmailStr
    created_at: datetime
    
    model_config = {"from_attributes": True}



# class PostUpdate(PostBase):
#     pass


'''
bu modeli kullanırken bir şema kullanarak requestleri yapıyoruz
ancak gelen responselarıda bir şema kullanarak yapabiliriz
üye girişlerini düşün

aşağıdaki yapılandırmayı yaptığın zaman postman üzerinde göreceksin ki 3 alanın hepside gelmiş olacaktır.
bu şekilde geri dönecek veriyi sınırlandırabiliriz
binlerce sütun olduğu zaman hepsini yazmak zor olacaktır dolayısıyla PostBase den inherit edersen postbasede tanımlı olan herşeyi alacaktır.
'''
# class Post(BaseModel):
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id : int
    owner : UserOut
    # id de postmande geliyor ancak biz bunu döndürmemeyi düşündük.
    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    email: EmailStr # bunun için pip install email-validator yaptık.
    password: str



class UserLogin(BaseModel):
    email : EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    # 


class Vote(BaseModel):
    post_id: int
    dir: conint(le=1) #conint(le=1)  # ----> anything less than 1 allowed negatif number # dir burada direction demektir.

class PostOut(BaseModel):
    Post: Post
    votes: int

    model_config = {"from_attributes": True}

# Yiyecek ve besin değerleri için şemalar
class Nutrient(BaseModel):
    id: int
    name: str
    unit_name: str
    amount: float = 0.0
    
    model_config = {"from_attributes": True}

class FoodNutrient(BaseModel):
    nutrient: Nutrient
    amount: float
    
    model_config = {"from_attributes": True}

class FoodBase(BaseModel):
    description: str
    
    model_config = {"from_attributes": True}

class FoodDetail(FoodBase):
    fdc_id: int
    data_type: Optional[str] = None
    food_category_id: Optional[int] = None
    publication_date: Optional[datetime] = None
    # scientific_name sütunu veritabanında yok, kaldırıyoruz
    # scientific_name: Optional[str] = None
    
    model_config = {"from_attributes": True}

class FoodNutrientResponse(BaseModel):
    food: FoodDetail
    nutrients: List[Nutrient]
    
    model_config = {"from_attributes": True}

class MacroNutrients(BaseModel):
    calories: float = 0.0
    protein: float = 0.0
    fat: float = 0.0
    carbohydrates: float = 0.0
    
    model_config = {"from_attributes": True}

class MicroNutrients(BaseModel):
    vitamins: List[Nutrient] = []
    minerals: List[Nutrient] = []
    
    model_config = {"from_attributes": True}

class Phytochemicals(BaseModel):
    compounds: List[Nutrient] = []
    
    model_config = {"from_attributes": True}

class NutrientSummary(BaseModel):
    food: FoodDetail
    macronutrients: MacroNutrients
    micronutrients: MicroNutrients
    phytochemicals: Phytochemicals
    
    model_config = {"from_attributes": True}
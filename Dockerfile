FROM python:3.13.0

WORKDIR /usr/src/app

COPY requirements.txt ./ 
# "./ ----> /usr/src/app "  ./ ifadesi workdir i gösterir.

RUN pip install --no-cache-dir -r requirements.txt  
# ---> tüm dependencies leri yükler

COPY . .
#current directory

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000" ]

FROM python:3.11

# maintainer: Sebastian
# USER root

WORKDIR /app

# RUN apt update && apt install -y unicorn

ADD requirements.txt . 

RUN ulimit -a
# install libs
# RUN python -m pip install --upgrade pip 
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .  
RUN cd src
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

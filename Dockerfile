# FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

# ENV LISTEN_PORT=8000
# EXPOSE 8000

# COPY /flaskbackend /flaskbackend


FROM python:3

WORKDIR /app

COPY './requirements.txt' .

RUN pip install --upgrade pip

# RUN export TMPDIR=$HOME/tmp

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install torch===1.4.0 torchvision===0.5.0 -f https://download.pytorch.org/whl/torch_stable.html

# RUN TMPDIR=/data/vincents/ pip install --cache-dir=/data/vincents/ --build /data/vincents/ requirements.txt

COPY . .

WORKDIR /app/flaskbackend

CMD ["python", "main.py"]



# FROM python:3

# WORKDIR /usr/src/app

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD [ "python", "./flaskbackend/main.py" ]


# FROM python:3.8.0

# WORKDIR /user/src/app

# COPY './requirements.txt' .

# RUN pip install -r requirements.txt

# COPY /flaskbackend .

# ENTRYPOINT [ "python", "main.py"]


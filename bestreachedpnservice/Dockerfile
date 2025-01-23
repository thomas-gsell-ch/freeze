FROM python:3.11-alpine3.21
# FROM python:3.14-rc-slim-bookworm

WORKDIR /bestreachedpnservice

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5001

#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# App-Skript kopieren
COPY app.py ./

# Einstiegspunkt setzen
CMD ["sh", "-c", "sleep 15 && python3 app.py"]
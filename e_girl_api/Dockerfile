# FROM python:3.7

# EXPOSE 80
# # RUN mkdir /app/api/app
# COPY . /app/api/
# RUN pip install -r/app/api/requirements.txt

# WORKDIR /app/api

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

FROM python:3.7

EXPOSE 9000
COPY . /app/api
RUN pip install -r /app/api/requirements.txt

WORKDIR /app/api
CMD ["uvicorn", "e_girl_api.main:app", "--host", "0.0.0.0", "--port", "9000", "--reload"]
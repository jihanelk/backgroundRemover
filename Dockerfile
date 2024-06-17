FROM python:3.9 

ADD app.py .

WORKDIR /usr/app/src

# copy the requirements file
COPY requirements.txt .

# install pip dependencies
RUN pip --no-cache-dir install -r requirements.txt

COPY . .

# expose the port the app runs on
EXPOSE 5000

# run the app
CMD ["python", "app.py"]

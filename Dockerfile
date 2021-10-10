# I had this image already on my system
# Feel free to use any other
FROM python:3.9.7-buster

# Set the workdir to /app
# All the app stuff will live here
WORKDIR /app

# Install the requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy the blueprint,
# and the flask app
COPY kosync.py kosync.py
COPY app.py app.py

# Forward this port to interact with it
EXPOSE 5000

CMD [ "flask", "run" ]
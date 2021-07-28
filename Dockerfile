# python3.8
FROM python:3.8

# working directory
WORKDIR /points

# copy all files to the container
COPY .  .

# Install pip requirements
RUN python -m pip install --no-cache-dir -r requirements.txt

# port number to expose
EXPOSE 5000

# run the command
CMD ["python3", "app.py"]

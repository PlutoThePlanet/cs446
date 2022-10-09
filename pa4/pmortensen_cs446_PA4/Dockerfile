# Derive the latest python base image (FROM)
FROM python:3.8.10
# Set the working directory (WORKDIR) as the directory that you are currently in (<netid>_CS446_PA4)
WORKDIR /pmortensen_cs446_PA4
# COPY the provided python script  into your working directory
COPY pythonCode2.py .
# COPY your created requirements.txt file into your working directory
COPY requirements.txt .
# Use the RUN command to pip3 install all of your required libraries to the container using the requirements.txt file
RUN pip3 install -r requirements.txt
# Use the CMD instruction to run the python script with any appropriate command line arguments
CMD ["python3", "pythonCode2.py"]

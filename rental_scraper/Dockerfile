# Use an official Python runtime as a parent image
FROM python:3

ENV security_updates_as_of 2014-07-06

# Install security updates and required packages
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get -y install -q build-essential && \
    apt-get -y install -q python-dev libffi-dev libssl-dev python-pip

# Set the working directory to /app
WORKDIR /rental

# Copy the current directory contents into the container at /app
ADD ./rental /rental

COPY requirements.txt /rental

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["python3"]

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["rental_server.py"]

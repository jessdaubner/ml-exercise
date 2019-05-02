# Use an official Python runtime as a parent image
FROM python:3.7.3

# Copy the current directory contents into the container at /ml-exercise
COPY . /python_debugging

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r python_debugging/requirements.txt

# Set the working directory to /predictor
WORKDIR python_debugging/

CMD "bash"

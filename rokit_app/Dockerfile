FROM python:3.9
# Copy the requirements file to the container
COPY requirements.txt requirements.txt
# Install the required dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt
# Set the working directory
WORKDIR /
# Copy the entire rokit_app directory into the container
COPY ./rokit_app ./rokit_app
# Set up a volume mount to reflect changes in the local rokit_app directory
VOLUME /rokit_app
# Specify the command to run when the container starts
CMD [ "uvicorn", "rokit_app.rokitAPI.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
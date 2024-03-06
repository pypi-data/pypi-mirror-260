# Use the official Python image as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /Verba

# Install git
RUN apt-get update && apt-get install -y git

# Clone the specific repository into the working directory
RUN git clone https://github.com/thompsonson/Verba .

# to get a specific version
# RUN git clone https://github.com/thompsonson/Verba . \
#     && git checkout <specific_commit_or_tag>

# Install the project dependencies
# RUN pip install -e .
RUN pip install -e '.[huggingface]'

# Inform Docker the container listens on the specified network port at runtime
EXPOSE 8000

# Define the command to run the application
CMD ["verba", "start"]

# Use the official Python image with Python 3.11
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    swig \
    sqlite3 \
    libqt5widgets5 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Initialize the database if necessary
RUN python initialize_db.py

# Install the package
RUN python setup.py install

# Expose port if needed (for a web-based app)
EXPOSE 8000

# Command to run the application
ENTRYPOINT ["prism_viewer"]
CMD ["main"]

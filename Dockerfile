# Use Python official image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install virtualenv
RUN pip install virtualenv

# Create and activate virtual environment
RUN virtualenv venv
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies in virtual environment
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (adjust if your app uses a different port)
EXPOSE 6999

# Command to run the application
CMD ["python", "app.py"]
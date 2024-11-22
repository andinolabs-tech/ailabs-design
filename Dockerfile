# Use Python official image as base
FROM python:3.11-slim-bookworm

# Set working directory
WORKDIR /app

# Install virtualenv
RUN pip install virtualenv

# Create and activate virtual environment
RUN virtualenv venv
ENV PATH="/app/venv/bin:$PATH"

# Copy requirements first to leverage Docker cache
# Install PyTorch CPU version
# RUN pip install torch==2.1.2 -f https://download.pytorch.org/whl/cpu/torch_stable.html

COPY requirements.txt .

# Install other requirements
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (adjust if your app uses a different port)
EXPOSE 6999

# Command to run the application
CMD ["python", "-u", "app.py"]
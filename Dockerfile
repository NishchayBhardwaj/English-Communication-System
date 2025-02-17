# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files
COPY model/speech-recognition.py model/speech-recognition.py
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port (optional, if you're running a web app)
EXPOSE 5000

# Fetch environment variables from GitHub Actions and run the script
CMD ["sh", "-c", "echo \"$ENV_FILE\" > .env && python model/speech-recognition.py"]

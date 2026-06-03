FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY . .

# Expose port 7860 which is required by Hugging Face Spaces
EXPOSE 7860

# Run the application with gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:7860", "app:app"]

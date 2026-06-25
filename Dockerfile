
FROM python:3.9-slim


RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn  # Production server ke liye


COPY . .

# 6. Port expose karein
EXPOSE 5000


# 300 seconds = 5 Minutes ka timeout
CMD ["gunicorn", "-w", "2", "--timeout", "300", "-b", "0.0.0.0:5000", "app:app"]
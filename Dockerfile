# 1. Base Image (Python 3.9 Slim version - Light & Fast)
FROM python:3.9-slim

# 2. System dependencies install karein (gcc waghaira)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 3. Work Directory set karein
WORKDIR /app

# 4. Requirements copy aur install karein
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn  # Production server ke liye

# 5. Saara code copy karein
COPY . .

# 6. Port expose karein
EXPOSE 5000

# 7. App chalane ki command (Gunicorn use karenge jo fast hai)
# 300 seconds = 5 Minutes ka timeout
CMD ["gunicorn", "-w", "2", "--timeout", "300", "-b", "0.0.0.0:5000", "app:app"]
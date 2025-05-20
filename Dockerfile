# Use Python 3.10 as the base image
FROM python:3.10-slim

WORKDIR /DOTSERMODZ

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python3","bot.py"]
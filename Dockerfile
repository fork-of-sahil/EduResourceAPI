FROM python:3.8

WORKDIR /app

COPY . /app

# Install necessary packages as defined in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 7755
EXPOSE 7755

# Define environment variable
ENV FLASK_APP=core/server.py

CMD ["bash", "run.sh"]

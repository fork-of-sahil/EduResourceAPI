FROM python:3.8

WORKDIR /app


COPY . /app

# make and activate a virtual environment
RUN pip install virtualenv && \
    python -m virtualenv env && \
    /bin/bash -c "source env/bin/activate"

# Install necessary packages as defined in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 and 7755
EXPOSE 7755
EXPOSE 5000

# Define environment variable
ENV FLASK_APP=core/server.py


CMD ["bash", "run.sh"]

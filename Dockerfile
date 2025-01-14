# Use the official Python 3.12 image as a base
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY ./requirements/requirements.txt requirements/requirements.txt

# Install dependencies
RUN pip install --no-deps -v -r requirements/requirements.txt

# Copy the rest of the application code
RUN groupadd --gid 10000 appuser \
    && useradd --uid 10001 --gid appuser --shell /bin/bash -c 'appuser' -m appuser \
    && chown -R appuser:appuser /app
COPY --chown=appuser:appuser . .

# Expose the port the app runs on
EXPOSE 8000

USER appuser
# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

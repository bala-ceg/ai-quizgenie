# Use Apify's Python base image
FROM apify/actor-python:3.13

# Set a writable directory for browserforge fingerprint data
ENV BROWSERFORGE_DATA_DIR="/home/apify/browserforge_data"

# Copy just requirements.txt first to improve build caching
COPY requirements.txt ./

# Install dependencies
RUN echo "Python version:" \
 && python --version \
 && echo "Pip version:" \
 && pip --version \
 && echo "Installing dependencies:" \
 && pip install -r requirements.txt \
 && echo "All installed Python packages:" \
 && pip freeze

# Copy the rest of the app code
COPY . ./

# Compile Python files to ensure runnability
RUN python3 -m compileall -q .
# Ensure the writable directory exists and is owned by the `apify` user
RUN mkdir -p /home/apify/browserforge_data && \
    chown -R apify:apify /home/apify/browserforge_data

# Create and run as a non-root user
RUN useradd --create-home apify && \
    mkdir -p /home/apify/browserforge_data && \
    chown -R apify:apify /home/apify
USER apify

# Run the Actor
CMD ["python3", "-m", "src"]

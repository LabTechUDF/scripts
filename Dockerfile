FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install dependencies manually
RUN pip install --no-cache-dir \
    pandas==2.2.3 \
    flask==3.0.3 \
    graphene<3.0 \
    flasgger==0.9.7.1 \
    flask-graphql==2.0.1 \
    openpyxl==3.1.5 \
    diagrams==0.23.4 \
    pymongo==4.10.1 \
    python-dotenv==1.0.1

# Copy project files
COPY . .

# Create directory for new collections if it doesn't exist
RUN mkdir -p processamento_planilha/jsonfiles


# Command to run when container starts
# You can override this with docker run command
CMD ["python", "-c", "import os; print('Available scripts:'); print('\\n'.join([f for f in os.listdir('.') if f.endswith('.py')]))"]

# Usage examples (add as comments for reference):
# To run load_sheet_to_mongodb.py: docker run --env-file ../.env -v /path/to/sheet.xlsx:/app/sheet.xlsx your-image-name python load_sheet_to_mongodb.py
# To run extract_collections.py: docker run -v /path/to/sheet.xlsx:/app/sheet.xlsx your-image-name python extract_collections.py
# To run upload_collections.py: docker run --env-file ../.env your-image-name python upload_collections.py
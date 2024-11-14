FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY environment.yml .
RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "pythonapp", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import fastapi"

# The code to run when container is started:
COPY app_analisis_financiero.py .
COPY . .    
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "pythonapp", "python", "app.py"]


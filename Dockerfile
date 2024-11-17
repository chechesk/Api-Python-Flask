FROM continuumio/miniconda3

WORKDIR /app

# Create the environment:
COPY env.yml .
COPY .env .
RUN conda env create -f env.yml

# Make RUN commands use the new environment:
SHELL ["conda", "run", "-n", "pythonapp", "/bin/bash", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

# The code to run when container is started:
COPY app.py .
COPY . .    

EXPOSE 8000

ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "pythonapp", "python", "app.py"]


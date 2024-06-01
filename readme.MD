# Run with docker

## Build the Docker image

```bash
docker build -t background-remover .
```

## Run the Docker container

```bash
docker run -p 5000:5000 background-remover
```

# Run locally

## Set Up Virtual Environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  ( On Windows use `venv\Scripts\activate` )
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run App

```bash
python main.py
```

# CICD-Model-Deployement-AWS

## Overview

This project demonstrates deploying a machine learning model as a FastAPI web service on AWS EC2 using Docker and GitHub Actions for CI/CD. The API predicts restaurant tips based on customer and bill information.

## Features

- FastAPI-based REST API for tip prediction
- Model loaded from AWS S3
- Dockerized application for easy deployment
- Automated CI/CD pipeline with GitHub Actions
- Secure deployment to AWS EC2

## API Endpoints

- `GET /` — Health check
- `GET /info` — Project information
- `GET /view` — Sample people data
- `POST /add` — Add two numbers
- `POST /predict` — Predict restaurant tip

## Input Example for `/predict`

```json
{
  "total_bill": 25.5,
  "sex": "Male",
  "smoker": "No",
  "day": "Sat",
  "time": "Dinner",
  "size": 3
}
```

## Setup

1. **Clone the repository**
   ```sh
   git clone https://github.com/abhi227070/CICD-Model-Deployement-AWS.git
   cd CICD-Model-Deployement-AWS
   ```

2. **Install dependencies**
   ```sh
   pip install -r requirements.txt
   ```

3. **Configure AWS credentials**
   - Create a `.env` file:
     ```
     AWS_ACCESS_KEY=your-access-key
     AWS_SECRET_KEY=your-secret-key
     ```
   - Ensure your model file (`tips_rf_model.pkl`) is in the specified S3 bucket.

4. **Run locally**
   ```sh
   uvicorn app:app --reload
   ```

## Docker Usage

1. **Build Docker image**
   ```sh
   docker build -t tip-app .
   ```

2. **Run Docker container**
   ```sh
   docker run -d -p 8000:8000 --env-file .env --name tip-app tip-app
   ```

## CI/CD Pipeline

- Automated deployment to AWS EC2 via GitHub Actions ([`.github/workflows/deploy.yml`](.github/workflows/deploy.yml))
- On push to `main`, the workflow builds and deploys the Docker container to EC2

## Project Structure

```
.
├── app.py
├── requirements.txt
├── Dockerfile
├── .env
├── .gitignore
├── .dockerignore
├── .github/
│   └── workflows/
│       └── deploy.yml
├── README.md
└── ...
```

## License

MIT License. See [LICENSE](LICENSE) for details.

## Author

Abhijeet Maharana
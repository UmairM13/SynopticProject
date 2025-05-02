# Off-season Travel Recommendation System

This project is a machine learning powered travel recommendation system designed to suggest budget-friendly, off-season destinations based on user preferences. It combines hybrid recommendation techniques with real-world data integration, offering users meaningful and explainable suggestions.

## Features

- Hybrid Recommendation Engine: Combines KNN feature similarity with collaborative filtering.

- Off-season Weighting: Prioritizes destinations with lower peak-season traffic.

- Modern Web Frontend: Built using React + Vite for fast and responsive user experience.

- Robust Backend API: FastAPI framework with clear, modular architecture.

- Persistent Data Storage: MySQL database

- Dockerised Deployment: Easily deployable using Docker and Docker Compose.

## Requirements

- Python 3.8+
- MySQL server
- Node
- Docker (optional, for containerized deployment)

## Setup Instructions

`cd SynopticProject`

1. Set up a virtual environment

```
python -m venv venv
source venv/bin/activate # macOS/Linux
venv\Scripts\activate # Windows
```

2. Install Dependencies

`pip install -r requirements.txt`

3. Configure the database connection

Edit the .env file to match your MySQL server:

`DB_USER=YourUsername`
`DB_PASSWORD=YourPassword`
`DB_HOST=localhost` If not running on localhost change to your host name
`DB_NAME=travelmate`

## Running the system

If your database is empty and has no data you can run:

```
cd recommendation_engine
cd database
python create_tables.py
python dummy_data.py
```

If you have data make sure you are in the root directory.

`python -m recommendation_engine.start`

That will start the server which should run on port 8000.

## Running the frontend

```
cd travel_frontend
npm install
npm run dev
```

Access it at http://localhost:5173

## Optional: Run with Docker Compose

`docker-compose up --build`

## Testing

`pytest tests/`

## Future Improvements

- Integrate hotel pricing APIs
- Add user feedback loops for continuous improvement
- Enhance accessibility and multi-language support
- Improve explainability and transparency of recommendations.

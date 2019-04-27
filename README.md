# ml-exercise
This repo contains code the debugs a faulty Python function (`python_debugger`) and builds a prototype to make product recommendations (`product_recommendations`).

## Setup
Clone the repository and build the Docker containers for each section:
```bash
git clone git@github.com:jessdaubner/ml-exercise.git
cd ml-exercise

docker build -t python_debugging .
docker run --rm -ti python_debugging
```

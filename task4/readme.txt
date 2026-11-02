docker build -t food-ordering:1.0 .

docker run --name food-ordering-container -p 8000:8000 food-ordering:1.0


docker inspect food-ordering-container

docker image inspect food-ordering:1.0
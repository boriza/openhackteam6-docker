docker build . -t gear -f ./Dockerfile_local
docker run -p 5000:5000 -d gear

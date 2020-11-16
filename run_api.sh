docker build --no-cache -f ./Dockerfile -t exponea_task ./
docker run -d --name api -p 80:80 exponea_task

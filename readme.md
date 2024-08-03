docker-compose down

docker-compose up -d

docker-compose logs prometheus

docker-compose logs -f celery_beat

docker-compose logs -f celery_worker

docker-compose exec web python manage.py fetch_stock_data

docker-compose exec web python manage.py fetch_month_data

curl -X POST http://localhost:8000/api/login/ -H "Content-Type: application/json" -d '{"username": "your_username", "password": "your_password"}'

docker-compose exec web python manage.py makemigrations

docker-compose exec web python manage.py migrate

docker-compose exec db mysql -u sayali97 -p

snhy vpye xzvl dsth

minikube start

kubectl apply -f kubernetes-config.yaml

kubectl get pods

kubectl delete -f kubernetes-config.yaml

docker build -t sayalisa2li7/backend_techdemo:1.8 .

docker push sayalisa2li7/backend_techdemo:1.8
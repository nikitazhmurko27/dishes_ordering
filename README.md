# Description
A website for ordering ingredients according to recipes.
# Run the project
1. Before running the project add .env files: .backend.env and .database.env to the /config directory. The examples you can find in the same directory.
2. docker-compose up -d  --build
3. docker-compose exec web python manage.py migrate
4. docker-compose exec web python manage.py collectstatic
5. docker-compose exec web python manage.py createsuperuser
6. Then go to http://localhost/dishes-ordering/ or http://localhost/admin/ 
# Django REST
Use http://localhost/swagger/ link for testing API requests
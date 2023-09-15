dev-up:
	docker compose up -d --build
down:
	docker compose down

db:
	sudo -i -u postgres psql support_ticket_db
docker-db:
	docker compose exec db psql --user postgres car_rental_db
migrate:
	alembic revision --autogenerate -m $(m)
upgrade:
	alembic upgrade head

logs:
	docker logs --tail 50 --follow --timestamps $(service)

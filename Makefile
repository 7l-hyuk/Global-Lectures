############ container ############

.PHONY: db_container
db_container:
	docker exec -it global-lectures-db bash

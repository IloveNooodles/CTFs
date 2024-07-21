WORDPRESS_TOOLBOX=docker-compose run --rm wp_service_1_toolbox

start:  
	#@mkdir wordpress db_data
	docker-compose up -d --build

stop:  
	docker-compose stop

wordpress_install: start  
	$(WORDPRESS_TOOLBOX) install

wordpress_configure:  
	$(WORDPRESS_TOOLBOX) configure

wordpress_reinstall:
	docker-compose stop wp_service_1 wp_service_1_db
	docker-compose rm -f wp_service_1 wp_service_1_db
	@rm -rf wordpress db_data
	@mkdir wordpress db_data
	docker-compose up -d wp_service_1 wp_service_1_db
	$(WORDPRESS_TOOLBOX) configure

clean: stop  
	@echo "💥 Removing Wordpress..."
	@rm -rf wordpress db_data
	@echo "💥 Removing Docker containers..."
	docker-compose rm -f


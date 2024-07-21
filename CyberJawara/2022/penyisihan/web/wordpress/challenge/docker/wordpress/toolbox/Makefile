WP_CLI=wp-cli --allow-root

install: configure

configure:  
	@echo "⚙️ Configuring Wordpress database..."
	dockerize -wait tcp://wp_service_1_db:3306 -timeout 120s 2> /dev/null #2>&1
	@rm -f wp-config.php
	$(WP_CLI) core config \
		--dbhost=${WORDPRESS_DB_HOST} \
		--dbname=${WORDPRESS_DB_NAME} \
		--dbuser=${WORDPRESS_DB_USER} \
		--dbpass=${WORDPRESS_DB_PASSWORD} \
		--locale=${WORDPRESS_LOCALE}

	$(WP_CLI) core multisite-install \
		--url=${WORDPRESS_WEBSITE_URL_WITHOUT_HTTP} \
		--title="$(WORDPRESS_WEBSITE_TITLE)" \
		--admin_user=${WORDPRESS_ADMIN_USER} \
		--admin_password=${WORDPRESS_ADMIN_PASSWORD} \
		--admin_email=${WORDPRESS_ADMIN_EMAIL}

	$(WP_CLI) option update siteurl "${WORDPRESS_WEBSITE_URL}"
	$(WP_CLI) rewrite structure $(WORDPRESS_WEBSITE_POST_URL_STRUCTURE)
	$(WP_CLI) plugin install learnpress --activate
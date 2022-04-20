FROM php:fpm

RUN docker-php-ext-install pdo pdo_mysql
# RUN apt-get install -y libpq-dev \
#   && docker-php-ext-configure pgsql -with-pgsql=/usr/local/pgsql \
#   && docker-php-ext-install pdo pdo_pgsql pgsql    

RUN pecl install xdebug && docker-php-ext-enable xdebug

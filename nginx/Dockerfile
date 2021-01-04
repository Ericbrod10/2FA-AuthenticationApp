FROM nginx

# Remove the default nginx.conf
RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/nginx.conf


RUN apt-get update
RUN apt-get install -y python-certbot-nginx
RUN apt-get install nano
# RUN certbot --nginx -d proclubsnationauth1.3utilities.com -d www.proclubsnationauth1.3utilities.com
#RUN certbot certonly -d proclubsnationauth1.3utilities.com -n --standalone --agree-tos --email  ProclubsNation1@gmail.com
# Replace with our own nginx.conf


# COPY letsencrypt/ /etc/letsencrypt/

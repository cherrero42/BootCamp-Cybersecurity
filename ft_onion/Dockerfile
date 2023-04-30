FROM nginx
RUN mkdir -p /usr/share/nginx/html
RUN mkdir -p /etc/nginx/conf
RUN mkdir -p /etc/ssh
RUN mkdir -p /etc/tor
COPY ./ft_onion/nginx/html /usr/share/nginx/html
COPY ./ft_onion/nginx/conf /etc/nginx/conf
COPY ./ft_onion/nginx/ssh /etc/ssh
COPY ./ft_onion/nginx/tor /etc/tor
EXPOSE 80 4242
CMD ["nginx", "-g", "daemon off;"]

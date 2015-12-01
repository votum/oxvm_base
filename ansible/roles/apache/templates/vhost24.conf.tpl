# Default Apache virtualhost template

<VirtualHost *:80>
  ServerAdmin webmaster@localhost
  DocumentRoot {{ apache.docroot }}
  ServerName {{ apache.servername }}

  {% if mailhog.install %}
  ProxyPass "{{ mailhog.web_alias }}" "http://localhost:{{ mailhog.web_port }}/"
  ProxyPassReverse "{{ mailhog.web_alias }}" "http://localhost:{{ mailhog.web_port }}/"
  {% endif %}

  <Directory {{ apache.docroot }}>
    AllowOverride All
    Options -Indexes +FollowSymLinks
    Require all granted
  </Directory>
</VirtualHost>

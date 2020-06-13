# Wagtail Starter Template


## How it was bootstrapped

0. mkdir wagtail-starter-template && echo '3.8.3' > wagtail-starter-template/.python-version
1. cd wagtail-starter-template
2. pipenv shell
3. pipenv install wagtail
4. wagtail start website .
5. rm requirements.txt Dockerfile
6. python manage.py makemigrations
7. python manage.py migrate
8. python manage.py createsuperuser (user: admin; password: ab12cd34)
9. python manage.py runserver


## How to develop

1. python manage.py runserver (defaults to 8000)
2. gulp watch (proxy to 3000, build SASS & live reload)


## How to deploy

This guide assumes you're using Dokku (an open-source, Heroku-like PaaS) to deploy applications using S3-like object storage on a VPS.
Tested using default configuration to serve apps within subdomains (ex.: your-app.yourdomain.com).


### First deploy

You should create the app first:
- dokku apps:create your-app

After that, you should specify the buildpacks to be used (ordering matters):
1. dokku buildpacks:add your-app https://github.com/heroku/heroku-buildpack-nodejs#v171 (or another pinned version)
2. dokku buildpacks:add your-app https://github.com/heroku/heroku-buildpack-python#v169 (or another pinned version)

Now, you should set the required environment variables listed below with:
- dokku config your-app (get app's environment variables)
- dokku config:set your-app var=value (set app's environment variable)
- dokku config:unset your-app var (remove app's environment variable)

Finally, you should add all the domains where your app should be acessible:
- dokku domains:report your-app (get app's configured domains)
- dokku domains:add your-app domain1 domain2 ... (add app's new domains)

With everything set, you can use the following commands on your local machine to deploy:
1. git remote add dokku dokku@yourdomain.com:your-app
2. git push dokku master

To create the first user, you can use:
- dokku --rm run your-app python manage.py createsuperuser

Additionally, you may want to increase Nginx's default maximum file size for uploads:
- sudo mkdir /home/dokku/your-app/nginx.conf.d
- echo 'client_max_body_size 10m;' | sudo tee /home/dokku/your-app/nginx.conf.d/upload.conf >/dev/null
- sudo chown dokku:dokku /home/dokku/your-app/nginx.conf.d/
- sudo chown dokku:dokku /home/dokku/your-app/nginx.conf.d/upload.conf
- sudo service nginx reload

For addition and auto-renewal of SSL certificates, you can use the dokku-letsencrypt plugin:
- sudo dokku plugin:install https://github.com/dokku/dokku-letsencrypt.git
- dokku config:set --global DOKKU_LETSENCRYPT_EMAIL=your@email.tld
- dokku letsencrypt your-app
- dokku letsencrypt:cron-job --add

To redirect from root domain to www domain, you can use the dokku-redirect plugin:
- sudo dokku plugin:install https://github.com/dokku/dokku-redirect.git
- dokku redirect:set your-app your-domain.com www.your-domain.com

### Subsequent deploys

You just need to push your local branch to the dokku remote.
The app will build itself, install the required node and python packages, run all front-end build tasks and apply new migrations if needed.


### Environment variables

Storage:
- AWS_ACCESS_KEY_ID
- AWS_DEFAULT_ACL
- AWS_S3_ENDPOINT_URL
- AWS_S3_REGION_NAME
- AWS_SECRET_ACCESS_KEY
- AWS_STORAGE_BUCKET_NAME

Database:
- DATABASE_HOST
- DATABASE_NAME
- DATABASE_PASSWORD
- DATABASE_PORT
- DATABASE_USER

Django:
- DJANGO_ALLOWED_HOSTS (MUST be space-separated)
- DJANGO_SECRET_KEY (MUST be generated with using django.core.management.utils.get_random_secret_key)
- DJANGO_SETTINGS_MODULE (MUST be 'website.settings.production')

Email:
- EMAIL_HOST
- EMAIL_HOST_PASSWORD
- EMAIL_HOST_USER
- EMAIL_PORT
- EMAIL_USE_TLS


## Architecture

1. All app folders sit inside the project's folder (`website`)
2. All static files sit inside the project's static folder (`website/static`)
3. All source static files should be in `src` folder inside the project's static folder (`website/static/src`)
4. All production static files are built in `dist` folder inside the project's static folder (`website/static/dist`)
5. Only files from `dist` folder are deployed


## The `src` folder

1. Files inside `copy` will be copied 'as is' to `dist`
2. Files inside `scss` will be built and linted (errors appear in console)
3. Vendor files should be downloaded and put inside a `vendor`-like folder inside each language folder


## Notes

1. JS files should be in `website/static/src/copy/js` folder as currently we don't have a build step for JS files
2. Image files should be in `website/static/src/copy/img` folder as currently we don't have a build step for image files
3. Font files should be in `website/static/src/copy/fonts` folder as currently we don't have a build step for font files
4. You should issue "gulp watch" after "python manage.py runserver" spinned up the server successfully, else, BrowserSync won't proxy the connection and live reload won't work at all


## References

- http://dokku.viewdocs.io/dokku~v0.20.4/deployment/application-deployment/
- http://dokku.viewdocs.io/dokku~v0.20.4/configuration/environment-variables/
- http://dokku.viewdocs.io/dokku~v0.20.4/configuration/nginx/
- https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Deployment
- https://www.accordbox.com/blog/how-deploy-django-project-dokku/
- https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
- https://django-storages.readthedocs.io/en/latest/backends/digital-ocean-spaces.html
- https://devcenter.heroku.com/articles/node-with-grunt
- https://devcenter.heroku.com/articles/custom-domains
- https://github.com/dokku/dokku-letsencrypt
- https://michalzalecki.com/using-dokku-with-docker-let-s-encrypt-https-and-redirects/

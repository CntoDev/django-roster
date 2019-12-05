FROM python:3.5

COPY . /app
WORKDIR /app

# Add required env vars due to the app being built for openshift
ENV OPENSHIFT_DATA_DIR /app/data/
ENV OPENSHIFT_PYTHON_DIR /app/
ENV OPENSHIFT_REPO_DIR /app/
ENV DATA_DIR /app/data/
ENV DEBUG True

RUN \
# Install required python libs
pip install -r requirements.txt && \
# Generate Django secret key
python /app/libs/secrets.py > /app/data/secrets.json && \
# Run DB migrations
python /app/wsgi/cnto/manage.py migrate --noinput && \
# Create a default admin account with username "admin" and password "password"
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'password')" | python /app/wsgi/cnto/manage.py shell

# Run and expose to port 80
EXPOSE 80
CMD python /app/wsgi/cnto/manage.py runserver 0.0.0.0:80

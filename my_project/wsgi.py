import os
from django.core.wsgi import get_wsgi_application
from waitress import serve

# Set the default Django settings module for the 'application' object.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'shopkart.settings')

# Create the WSGI application.
application = get_wsgi_application()

# For development or local server running, use waitress to serve the app.
if __name__ == "__main__":
    serve(application, host='0.0.0.0', port=8080)

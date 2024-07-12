#The entry point to run flask application

from app import create_app

app = create_app()

if __name__ == "__main__":
    # Use SSL context with the generated certificates
    app.run(ssl_context=('cert.pem', 'key.pem'))

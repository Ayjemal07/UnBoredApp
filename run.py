# #The entry point to run flask application

# from app import create_app

# app = create_app()

# if __name__ == "__main__":
#     # Use SSL context with the generated certificates
#     app.run(ssl_context=('cert.pem', 'key.pem'))



from app import create_app
import os

app = create_app()

if __name__ == "__main__":
    # Use SSL context with the generated certificates (if needed)
    # app.run(ssl_context=('cert.pem', 'key.pem'))

    # Specify host and port for production deployment
    host = '0.0.0.0'  # Listen on all network interfaces
    port = int(os.environ.get('PORT', 5000))  # Use PORT environment variable or default to 5000
    app.run(host=host, port=port)
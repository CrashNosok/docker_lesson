# NewsParser
The application searches for new news on the site "https://www.benzinga.com/markets", sends them to the message queue
in RabbitMQ and saves to MongoDB

Made by <b>[Piggeeon](https://github.com/Piggeeon)</b>

Starting the application:
1) If necessary, change the environment variables in the .env file to your own
2) Go to project root and start application with `docker-compose up -d`

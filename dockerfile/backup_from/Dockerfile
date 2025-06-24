# Use the official RabbitMQ image with management plugin
FROM rabbitmq:3-management

# Install 'openssl' for certificate generation (optional, can be done outside the container)
# and 'ca-certificates' to trust CAs.
# The 'rm -rf /var/lib/apt/lists/*' command cleans up the package lists to reduce image size.
RUN apt-get update && apt-get install -y openssl ca-certificates --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Create directories for SSL certificates
RUN mkdir -p /etc/rabbitmq/ssl

# Copy SSL certificates into the container.
# Ensure these files exist in the 'certs' subdirectory relative to your Dockerfile.
COPY certs/ca_certificate.pem /etc/rabbitmq/ssl/ca_certificate.pem
COPY certs/server_certificate.pem /etc/rabbitmq/ssl/server_certificate.pem
COPY certs/server_key.pem /etc/rabbitmq/ssl/server_key.pem

# Copy RabbitMQ configuration files.
# These files will configure SSL, user/password, and other advanced settings.
COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
COPY advanced.config /etc/rabbitmq/advanced.config

# Expose default RabbitMQ ports:
# 5672: AMQP (plaintext)
# 5671: AMQP (SSL)
# 15672: Management UI (plaintext)
# 15671: Management UI (SSL)
EXPOSE 5671 5672 15671 15672

# Define environment variables for the default user and password.
# These variables will be used by RabbitMQ to create the initial user.
# ATTENTION: For production environments, consider using Docker Secrets or an orchestrator
# like Kubernetes to manage these credentials securely.
ENV RABBITMQ_DEFAULT_USER=myuser
ENV RABBITMQ_DEFAULT_PASS=mypassword

# The default command of the base image starts RabbitMQ.
CMD ["rabbitmq-server"]
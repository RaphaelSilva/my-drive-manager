# Use the official RabbitMQ image with management plugin
FROM rabbitmq:3-management

# Install 'openssl' for certificate generation (optional, can be done outside the container)
# and 'ca-certificates' to trust CAs.
# The 'rm -rf /var/lib/apt/lists/*' command cleans up the package lists to reduce image size.
RUN apt-get update && apt-get install -y openssl ca-certificates --no-install-recommends && rm -rf /var/lib/apt/lists/*

# Define build argument to enable/disable SSL
ARG USE_SSL=false

# Copy SSL certificates and configs only if USE_SSL is true
RUN mkdir -p /etc/rabbitmq/ssl
COPY certs/ca_certificate.pem /etc/rabbitmq/ssl/ca_certificate.pem
COPY certs/server_certificate.pem /etc/rabbitmq/ssl/server_certificate.pem
COPY certs/server_key.pem /etc/rabbitmq/ssl/server_key.pem
COPY rabbitmq.conf /etc/rabbitmq/rabbitmq.conf
COPY advanced.config /etc/rabbitmq/advanced.config
COPY rabbitmq.nossl.conf /etc/rabbitmq/rabbitmq.nossl.conf
COPY advanced.nossl.config /etc/rabbitmq/advanced.nossl.config

RUN if [ "$USE_SSL" = "false" ]; then \
        rm -rf /etc/rabbitmq/ssl && \
        rm -f /etc/rabbitmq/rabbitmq.conf && \
        rm -f /etc/rabbitmq/advanced.config && \
        mv /etc/rabbitmq/rabbitmq.nossl.conf /etc/rabbitmq/rabbitmq.conf && \
        mv /etc/rabbitmq/advanced.nossl.config /etc/rabbitmq/advanced.config ; \
    else \
        rm -f /etc/rabbitmq/rabbitmq.nossl.conf && \
        rm -f /etc/rabbitmq/advanced.nossl.config ; \
    fi


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
ENV RABBITMQ_DEFAULT_USER=admin
ENV RABBITMQ_DEFAULT_PASS=admin

# The default command of the base image starts RabbitMQ.
CMD ["rabbitmq-server"]
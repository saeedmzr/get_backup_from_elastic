FROM docker.elastic.co/logstash/logstash:7.15.0

USER root
COPY ./logstash/normalizer /usr/share/logstash/normalizer

# Install Python and pip
RUN yum update -y \
    && yum install -y python3 python3-pip \
    && yum clean all \
    && rm -rf /var/cache/yum

# Install Elasticsearch Python client
RUN pip3 install elasticsearch

USER logstash
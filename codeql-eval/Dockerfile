# Version-pinned CodeQL image for analyzing Python code.
# Pinned to linux/amd64, the only Linux CodeQL bundle GitHub publishes.
FROM --platform=linux/amd64 ubuntu:22.04

ARG CODEQL_VERSION=v2.25.4
ENV DEBIAN_FRONTEND=noninteractive

# python3: required by the CodeQL Python extractor to build the database.
RUN apt-get update \
 && apt-get install -y --no-install-recommends curl ca-certificates python3 \
 && rm -rf /var/lib/apt/lists/*

# Download + extract the pinned CodeQL bundle (ships codeql/python-queries).
RUN curl -fSL \
      "https://github.com/github/codeql-action/releases/download/codeql-bundle-${CODEQL_VERSION}/codeql-bundle-linux64.tar.gz" \
      -o /tmp/codeql.tar.gz \
 && mkdir -p /opt \
 && tar -xzf /tmp/codeql.tar.gz -C /opt \
 && rm /tmp/codeql.tar.gz

# Bundle extracts to /opt/codeql/ ; binary at /opt/codeql/codeql.
ENV PATH="/opt/codeql:${PATH}"

# Pre-create the working dirs we docker-cp into / out of.
RUN mkdir -p /work/src

# Sanity: fail the build if the python-queries pack isn't resolvable.
RUN codeql resolve qlpacks | grep -i python-queries

WORKDIR /work

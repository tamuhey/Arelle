FROM drydock-prod.workiva.net/workiva/smithy-runner-python:238563 as build

# Build Environment Vars
ARG BUILD_ID
ARG BUILD_NUMBER
ARG BUILD_URL
ARG GIT_COMMIT
ARG GIT_BRANCH
ARG GIT_TAG
ARG GIT_COMMIT_RANGE
ARG GIT_HEAD_URL
ARG GIT_MERGE_HEAD
ARG GIT_MERGE_BRANCH
ARG GIT_SSH_KEY
ARG KNOWN_HOSTS_CONTENT
WORKDIR /build/
ADD . /build/

RUN mkdir /root/.ssh && \
    echo "$KNOWN_HOSTS_CONTENT" > "/root/.ssh/known_hosts" && \
    chmod 700 /root/.ssh/ && \
    umask 0077 && echo "$GIT_SSH_KEY" >/root/.ssh/id_rsa && \
    eval "$(ssh-agent -s)" && ssh-add /root/.ssh/id_rsa
ENV PATH=/tmp/virtualenv/bin:$PATH
ENV PYTHONPATH=.
RUN echo "Starting the script section" && \
		./smithy_arelle.sh && \
		echo "script section completed"
ARG BUILD_ARTIFACTS_PYPI=/build/dist/w_versioned_arelle*.tar.gz

RUN mkdir /audit/
ARG BUILD_ARTIFACTS_AUDIT=/audit/*
RUN pip freeze > /audit/pip.lock
FROM scratch

FROM amazonlinux:2 as build

ARG GIT_TAG

WORKDIR /build/
ADD . /build/

RUN yum -y install python3-devel \
                   libxml2-devel \
                   libxslt-devel && \
    yum groupinstall -y "Development Tools" && \
    rm -rf /var/cache/yum

# pypi package creation
# The following command replaces the @VERSION@ string in setup.py with the tagged version number from GIT_TAG
RUN sed -i s/@VERSION@/$GIT_TAG/ ./setup.py
ARG BUILD_ARTIFACTS_PYPI=/build/dist/w_versioned_arelle*.tar.gz
RUN pip3 install build && \
    python3 -m build --sdist

RUN mkdir /audit/
ARG BUILD_ARTIFACTS_AUDIT=/audit/*
RUN pip3 freeze > /audit/pip.lock

FROM drydock-prod.workiva.net/workiva/wf_arelle:latest-release AS wf-arelle-test-consumption
USER root
ARG BUILD_ID
RUN yum update -y && \
    yum upgrade -y && \
    yum autoremove -y && \
    yum clean all && \
    rm -rf /var/cache/yum
COPY --from=build /build/dist/*.tar.gz /test.tar.gz
RUN pip3 install /test.tar.gz
USER nobody

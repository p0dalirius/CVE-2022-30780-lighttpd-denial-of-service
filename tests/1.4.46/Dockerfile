
FROM debian:buster

RUN apt-get -y -q update; \
    apt-get -y -q install git curl nano build-essential wget autoconf automake libtool m4 pkg-config libpcre2-dev libpcre++-dev zlib1g-dev bzip2 libbz2-dev

RUN mkdir -p /workspace/; mkdir -p /build/

WORKDIR /build/

ENV lighttpd_version 1.4.46

RUN wget https://github.com/lighttpd/lighttpd1.4/archive/refs/tags/lighttpd-${lighttpd_version}.tar.gz -O /build/lighttpd.tar.gz ;\
    tar xvf /build/lighttpd.tar.gz

RUN cd /build/lighttpd1.4-lighttpd-${lighttpd_version}/ ;\
    ./autogen.sh ;\
    ./configure ;\
    make && make install

WORKDIR /workspace/

EXPOSE 80

CMD ["/bin/bash"]
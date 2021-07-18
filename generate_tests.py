#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File name          : generate_tests.py
# Author             : Podalirius (@podalirius_)
# Date created       : 17 July 2021


import os
import requests
import jinja2
import time


def get_tags_from_github(username, repo, per_page=100):
    # https://docs.github.com/en/rest/reference/repos#releases
    print("[+] Loading %s/%s versions ... " % (username, repo))
    versions, page_number, running = {}, 1, True
    while running:
        r = requests.get(
            "https://api.github.com/repos/%s/%s/tags?per_page=%d&page=%d" % (username, repo, per_page, page_number),
            headers={"Accept": "application/vnd.github.v3+json"}
        )
        if type(r.json()) == dict:
            if "message" in r.json().keys():
                print(r.json()['message'])
                running = False
        else:
            for release in r.json():
                if release['name'].startswith('v'):
                    release['name'] = release['name'][1:]
                versions[release['name']] = release['zipball_url']
            if len(r.json()) < per_page:
                running = False
            page_number += 1
    print('[>] Loaded %d %s/%s versions.' % (len(versions.keys()), username, repo))
    return versions


dockerfile_template = """
FROM debian:buster

RUN apt-get -y -q update; \\
    apt-get -y -q install git curl nano build-essential wget autoconf automake libtool m4 pkg-config libpcre2-dev libpcre++-dev zlib1g-dev

RUN mkdir -p /workspace/; mkdir -p /build/

WORKDIR /build/

ENV lighttpd_version {{ lighttpd_version }}

RUN wget https://github.com/lighttpd/lighttpd1.4/archive/refs/tags/lighttpd-${lighttpd_version}.tar.gz -O /build/lighttpd.tar.gz ;\\
    tar xvf /build/lighttpd.tar.gz

RUN cd /build/lighttpd1.4-lighttpd-${lighttpd_version}/ ;\\
    ./autogen.sh ;\\
    ./configure ;\\
    make && make install

WORKDIR /workspace/

EXPOSE 80

CMD ["/bin/bash"]
"""

makefile_template = """
.PHONY: build img

IMGNAME := vulnresearch_lighttpd

all : build start

build:
	docker build -t $(IMGNAME):latest -f Dockerfile .

start:
	docker run --rm -it -v $(shell pwd)/workspace/:/workspace/ -p 10080:80 $(IMGNAME) "bash" "init.sh"

background:
	docker run --rm -d -v $(shell pwd)/workspace/:/workspace/ -p 10080:80 $(IMGNAME) "bash" "init.sh"


shell:
	docker exec -it $(shell docker ps | grep $(IMGNAME) | awk '{split($$0,a," "); print a[1]}') bash

stop:
	docker stop $(shell docker ps | grep $(IMGNAME) | awk '{split($$0,a," "); print a[1]}')
"""

IP = "192.168.1.27"

"""
generate = False
if generate == True:
    for version in get_tags_from_github("lighttpd", "lighttpd1.4"):

        version = version.split('lighttpd-')[1]
        if not os.path.exists("./tests/%s/" % version):
            os.makedirs("./tests/%s/" % version, exist_ok=True)

        f = open("./tests/%s/Makefile" % version, "w")
        f.write(jinja2.Template(makefile_template).render(lighttpd_version=version))
        f.close()

        f = open("./tests/%s/Dockerfile" % version, "w")
        f.write(jinja2.Template(dockerfile_template).render(lighttpd_version=version))
        f.close()
"""

versions = [v for v in get_tags_from_github("lighttpd", "lighttpd1.4")]
for version in versions:
    time.sleep(0.5)
    version = version.split('lighttpd-')[1]
    print("[>] Starting vulnerable environnement version %s" % version)
    result = os.popen("cd ./tests/%s/; make stop 2>/dev/null; make build 2>&1; make background; cd - >/dev/null" % version).read()
    if "returned a non-zero code" not in result:
        os.system("mkdir -p ./tests/%s/results/" % version)

        print("   [>] Starting fuzz_url_lent.py")
        os.system('../http-fuzzing-scripts/fuzz_url_lent.py -u http://%s:10080/ > ./tests/%s/results/url_length.fuzz' % (IP, version))

        print("   [>] Starting lighthttpd_crash.py")
        os.system('./CVE-2022-30780-lighttpd-denial-of-service.py -u http://%s:10080/ > ./tests/%s/results/dos_poc.txt' % (IP, version))

        # print("Starting Copying error.log")
        os.system('cp ./tests/%s/workspace/var/log/lighttpd/error.log ./tests/%s/results/error.log' % (version, version))
        os.system("cd ./tests/%s/; make stop 1>/dev/null; cd - >/dev/null" % version)

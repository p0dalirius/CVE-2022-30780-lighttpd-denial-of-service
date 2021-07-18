
.PHONY: build img

IMGNAME := vulnresearch_lighttpd

all : build start

build:
	@docker build -t $(IMGNAME):latest -f Dockerfile .

start:
	@docker run --rm -it -v $(shell pwd)/workspace/:/workspace/ -p 10080:80 $(IMGNAME) "bash" "init.sh"

background:
	@docker run --rm -d -v $(shell pwd)/workspace/:/workspace/ -p 10080:80 $(IMGNAME) "bash" "init.sh"


shell:
	@docker exec -it $(shell docker ps | grep $(IMGNAME) | awk '{split($$0,a," "); print a[1]}') bash

stop:
	@docker stop $(shell docker ps | grep $(IMGNAME) | awk '{split($$0,a," "); print a[1]}')
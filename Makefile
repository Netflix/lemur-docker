.DEFAULT_GOAL=all
.PHONY: clean all copy_env_files lemur_checkout build_containers restart_containers inspect_image_size

# Shell to use for running scripts
SHELL := $(shell which bash)
# Get docker path or an empty string
DOCKER := $(shell command -v docker)
# Get docker-compose path or an empty string
DOCKER_COMPOSE := $(shell command -v docker-compose)

# Test if the dependencies we need to run this Makefile are installed
deps:
ifndef DOCKER
	@echo "Docker is not available. Please install docker"
	@exit 1
endif
ifndef DOCKER_COMPOSE
	@echo "docker-compose is not available. Please install docker-compose"
	@exit 1
endif

# TODO: for future use, will tag docker build
COMMIT := $(shell git rev-list -1 HEAD)
BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
VERSION := $(shell git describe --tags --always)

LEMUR_GIT_DIR = lemur-build-docker/lemur

# TODO: check user permission im more elegant way instead of `some command || sudo some command`


clean: deps
	rm -rf $(LEMUR_GIT_DIR)
	docker-compose down -v || sudo docker-compose down -v

all: deps
	$(MAKE) copy_env_files
	$(MAKE) lemur_checkout
	$(MAKE) build_containers
	$(MAKE) restart_containers

copy_env_files:
	[ -f .lemur.env ] || cp .lemur.env.dist .lemur.env && echo ".lemur.env created from scratch"
	[ -f .pgsql.env ] || cp .pgsql.env.dist .pgsql.env && echo ".pgsql.env created from scratch"

lemur_checkout:
	[ -d $(LEMUR_GIT_DIR) ] || git clone --depth=1 https://github.com/Netflix/lemur.git $(LEMUR_GIT_DIR)
	cd $(LEMUR_GIT_DIR) && git pull

build_containers: deps
	docker-compose build || sudo docker-compose build || echo "failed to build containers"

restart_containers: deps
	docker-compose stop || sudo docker-compose stop || echo "failed to stop containers"
	docker-compose up -d || sudo docker-compose up -d || echo "failed to start containers"

# TODO: should run with sudo if you do not have access rights to docker
inspect_image_size: deps
	$(MAKE) lemur_checkout
	$(MAKE) build_containers
	# https://docs.docker.com/engine/reference/commandline/save/#save-an-image-to-a-targz-file-using-gzip
	docker save netlix-lemur:latest | gzip > netlix-lemur.latest.tar.gz
	ls -lh netlix-lemur.latest.tar.gz
	rm netlix-lemur.latest.tar.gz

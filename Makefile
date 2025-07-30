############ container ############
VERSION := 0.0.0
ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_REPOSITORY := 7lhyuku/global-lectures
DIR := $(ABSOLUTE_PATH)
TAG := dubbing_service

BASE_IMAGE_TAG := $(TAG)_base
BASE_DOCKERFILE := Dockerfile.base
BASE_IMAGE_NANE := $(DOCKER_REPOSITORY):$(BASE_IMAGE_TAG)_$(VERSION)

.PHONY: bulid_base_image
bulid_base_image:
	sudo docker buildx build \
		-t $(BASE_IMAGE_NANE) \
		-f $(BASE_DOCKERFILE) .

.PHONY: db_container
db_container:
	docker exec -it global-lectures-db bash

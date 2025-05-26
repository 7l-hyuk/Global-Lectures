VERSION := 0.0.0
ABSOLUTE_PATH := $(shell pwd)
DOCKERFILE := Dockerfile
DOCKER_REPOSITORY := 7lhyuku/global-lectures

DIR := $(ABSOLUTE_PATH)
TAG = dubbing_service



########## BACKEND ##########

BACKEND_DIR := $(DIR)/backend
DOCKERFILE_BACKEND = $(BACKEND_DIR)/$(DOCKERFILE)
DOCKER_BACKEND_TAG = $(TAG)_backend
DOCKER_BACKEND_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_BACKEND_TAG)_$(VERSION)

.PHONY: build_backend
build_backend:
	docker buildx build \
		-t $(DOCKER_BACKEND_IMAGE_NAME) \
		-f $(DOCKERFILE_BACKEND) \
		.

.PHONY: run_backend
run_backend: build_backend
	docker run \
		-it \
		-d \
		--name backend_test \
		-p 8000:8000 \
		-e COQUI_TOS_AGREED=1 \
		$(DOCKER_BACKEND_IMAGE_NAME)

.PHONY: rm_backend
rm_backend:
	docker rm -f backend_test


########## POC ##########

POC_DIR := $(DIR)/poc
DOCKERFILE_POC = $(POC_DIR)/$(DOCKERFILE)
DOCKER_POC_TAG = $(TAG)_poc
DOCKER_POC_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_POC_TAG)_$(VERSION)

.PHONY: build_poc
build_poc:
	docker buildx build \
		-t $(DOCKER_POC_IMAGE_NAME) \
		-f $(DOCKERFILE_POC) \
		.

.PHONY: run_poc
run_poc: build_poc
	docker run \
		-it \
		-d \
		--name poc_test \
		-p 8501:8501\
		$(DOCKER_POC_IMAGE_NAME)

.PHONY: rm_poc
rm_poc:
	docker rm -f poc_test


########## FRONTEND ##########

FRONTEND_DIR := $(DIR)/frontend
DOCKERFILE_FRONTEND = $(FRONTEND_DIR)/$(DOCKERFILE)
DOCKER_FRONTEND_TAG = $(TAG)_frontend
DOCKER_FRONTEND_IMAGE_NAME = $(DOCKER_REPOSITORY):$(DOCKER_FRONTEND_TAG)_$(VERSION)

.PHONY: build_frontend
build_frontend:
	docker buildx build \
		-t $(DOCKER_FRONTEND_IMAGE_NAME) \
		-f $(DOCKERFILE_FRONTEND) \
		.

.PHONY: run_frontend
run_frontend: build_frontend
	docker run \
		-it \
		-d \
		--name frontend_test \
		-p 3000:3000\
		$(DOCKER_FRONTEND_IMAGE_NAME)

.PHONY: rm_frontend
rm_frontend:
	docker rm -f frontend_test

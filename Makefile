
DOCKER_CMD = docker --config ./.docker
BUILD_CMD = $(DOCKER_CMD) buildx build --push --platform linux/arm64,linux/amd64
DOCKER_USER = expeca
IMG_REPO_CLIENT = $(DOCKER_USER)/demo_ew22_client
IMG_REPO_BACKEND = $(DOCKER_USER)/demo_ew22_backend

all: client backend
.PHONY: all

client: Dockerfile.client
	$(BUILD_CMD) -t $(IMG_REPO_CLIENT):latest -f $< .

backend: Dockerfile.backend
	$(BUILD_CMD) -t $(IMG_REPO_BACKEND):latest -f $< .

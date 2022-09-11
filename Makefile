
DOCKER_CMD = docker --config ./.docker
BUILD_CMD = $(DOCKER_CMD) buildx build --push --platform linux/arm64,linux/amd64
DOCKER_USER = expeca
IMG_REPO = $(DOCKER_USER)/simple-network-load

all: image
.PHONY: all clean

image: Dockerfile
	$(BUILD_CMD) -t $(IMG_REPO):latest -f $< .

clean:
	$(DOCKER_CMD) image rm $(IMG_REPO):latest
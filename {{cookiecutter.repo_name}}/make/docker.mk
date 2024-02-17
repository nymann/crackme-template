DOCKER_IMAGE = {{cookiecutter.project_slug}}
docker-build:
	@if ! docker inspect --type=image $(DOCKER_IMAGE) > /dev/null 2>&1; then \
		docker build -t $(DOCKER_IMAGE) -f docker/Dockerfile .; \
	fi

run: docker-build
	@ docker run -it $(DOCKER_IMAGE) $(command)

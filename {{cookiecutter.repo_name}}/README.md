# {{cookiecutter.project_name}}

## Run docker container

```sh
docker build -f docker/Dockerfile --tag={{cookiecutter.project_name}} .
docker run -it {{cookiecutter.project_name}} test
```

Where `test` is the argument given to the crackme program.

## Development

For help getting started developing check [DEVELOPMENT.md](DEVELOPMENT.md)

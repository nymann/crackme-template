install: ${VERSION}
	@pip install --break-system-packages .

install-all: ${VERSION}
	@pip install -e '.[all]'

install-dev: ${VERSION}
	@pip install -e '.[dev]'

install-tests: ${VERSION}
	@pip install -e '.[tests]'

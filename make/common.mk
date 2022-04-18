${VERSION}:
	@echo "__version__ = \"$(shell (git describe --tag --always || echo "0.0.0") | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')\"" > ${VERSION}

COMPONENT?=crackme_template
VERSION:=src/${COMPONENT}/version.py

include make/common.mk

include make/ci.mk
include make/clean.mk
include make/help.mk
include make/install.mk
include make/lint.mk
include make/test.mk

.DEFAULT:help

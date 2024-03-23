
MODULE		=	$(notdir $(patsubst %/,%,$(CURDIR)))

$(info --- Makefile dans $(MODULE), cible $(MAKECMDGOALS))

default: all

-include ./make/compiler.mk
-include ./make/module.mk

all:	$(BINS)

-include ./make/common.mk
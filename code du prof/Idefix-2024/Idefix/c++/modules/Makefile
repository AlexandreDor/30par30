
MODULE		=	$(notdir $(patsubst %/,%,$(CURDIR)))

$(info --- Makefile dans $(MODULE), cible $(MAKECMDGOALS))

TOPTARGETS := all clean

SUBDIRS := $(wildcard */.)

$(TOPTARGETS): $(SUBDIRS)

$(SUBDIRS):
	echo "Recurse in:" $@
	$(MAKE) -C $@ $(MAKECMDGOALS)

.PHONY: $(TOPTARGETS) $(SUBDIRS)

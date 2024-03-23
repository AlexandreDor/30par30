
TOOL		=	$(notdir $(patsubst %/,%,$(CURDIR)))

$(info --- Makefile dans $(TOOL), cible $(MAKECMDGOALS))

default: all

-include ../../make/compiler.mk
-include ../../make/tool.mk

INCLUDES += -I../../modules/encoding/include
LIBS += -L../../modules/encoding/lib  -lencoding

INCLUDES += -I../../modules/networking/include
LIBS += -L../../modules/networking/lib -lnetworking

INCLUDES += `pkg-config --cflags opencv4`
LIBS += `pkg-config --libs opencv4`

all:	$(BINS)

-include ../../make/common.mk
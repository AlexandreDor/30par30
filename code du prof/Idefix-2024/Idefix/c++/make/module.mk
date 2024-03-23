
$(info Inclusion module depuis $(MODULE))

LDFLAGS		+=	-shared

STMODULE	=	$(MODULE:%=lib%.a)
SHMODULE	=	$(MODULE:%=lib%.so)

TARGETS		=	$(STMODULE) $(SHMODULE)

BINS	:=	$(TARGETS:%=$(LDIR)/%)

$(LDIR)/$(STMODULE): $(OBJS)
	echo "linking static library:" $@
	ar rcs $@ $^
	ranlib $@

$(LDIR)/$(SHMODULE): $(OBJS)
	echo "linking shared library:" $@
	$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)

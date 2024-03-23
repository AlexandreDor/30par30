
$(info Inclusion tools depuis $(TOOL))

DESTEXEC	=	$(TOOL:%=%)

TARGETS		=	$(DESTEXEC)

BINS	:=	$(TARGETS:%=$(BDIR)/%)

$(BDIR)/$(DESTEXEC): $(OBJS)
	echo "linking executable:" $@
	$(LD) $(LDFLAGS) -o $@ $^ $(LIBS)

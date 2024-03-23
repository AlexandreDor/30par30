
$(info Inclusion common depuis $(MODULE))

# VERBOSE=	1

ifndef VERBOSE
.SILENT:
endif

NODEPS		=	clean all-clean

clean: FORCE 
	rm -f $(DEPS)
	rm -f $(OBJS)
	rm -f $(BINS)

#Don't create dependencies when we're cleaning, for instance
ifeq (0, $(words $(findstring $(MAKECMDGOALS), $(NODEPS))))
    #Chances are, these files don't exist.  GMake will create them and
    #clean up automatically afterwards
    -include $(DEPS)
endif

FORCE:

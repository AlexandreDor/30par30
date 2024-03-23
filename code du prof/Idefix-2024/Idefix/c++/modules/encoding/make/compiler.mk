
$(info Inclusion compiler depuis $(MODULE))

SDIR		=	srcs
HDIR		=	include
ODIR		=	objs
DDIR		=	deps
LDIR		=	lib
BDIR		=	bin
MDIR		=	modules

CXX			=	g++
CXXFLAGS	=	-ggdb -std=c++17 -fPIC
INCLUDES	=	-I$(HDIR)  

LD			=	g++
LDFLAGS		=	-std=c++17
LIBS		=

SRCS 	:=  $(wildcard $(SDIR)/*.cpp)
OBJS	:=	$(patsubst $(SDIR)/%.cpp,$(ODIR)/%.o,$(SRCS))
DEPS	:=	$(patsubst $(SDIR)/%.cpp,$(DDIR)/%.d,$(SRCS))

$(ODIR)/%.o:	$(SDIR)/%.cpp
	echo "Compiling file:" $<
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

$(DDIR)/%.d:	$(SDIR)/%.cpp
	echo "Generating deps file for:" $<
	$(CXX) $(CXXFLAGS) $(INCLUDES) -MM -MD -MT '$(patsubst $(SDIR)/%.cpp,$(ODIR)/%.o,$<)' $< -MF $@.tmp
	sed '/^ \/.* /d' < $@.tmp | sed 's/ \/.* / /g' > $@
	rm -f $@.tmp

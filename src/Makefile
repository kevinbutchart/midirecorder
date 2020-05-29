IDIR =.
CC=gcc
CFLAGS=-I$(IDIR) -O2 -pipe

ODIR=../obj
BINDIR=../bin

LIBS=-lm -lasound -ldl -lpthread

_DEPS = utils.h
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = arecordmidi.o utils.o 
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))


$(ODIR)/%.o: %.c $(DEPS)
		$(CC) -c -o $@ $< $(CFLAGS)

$(BINDIR)/arecsplitmidi: $(OBJ)
		$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
		rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~ 

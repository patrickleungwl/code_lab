CC = g++
CFLAGS = -c -std=c++14 -fmax-errors=3
SOURCES = test.cpp 
OBJECTS = $(SOURCES:.cpp=.o)
EXECUTABLE = test

all: $(OBJECTS) $(EXECUTABLE)

$(EXECUTABLE) : $(OBJECTS)
		$(CC) $(OBJECTS) -o $@  

.cpp.o: *.h
	$(CC) $(CFLAGS) $< -o $@

clean :
	-rm -f $(OBJECTS) $(EXECUTABLE)

.PHONY: all clean

CFLAGS=-g $(shell pkg-config --cflags json-c xmu)
LDFLAGS=-g $(shell pkg-config --libs json-c xmu)

all:
	$(CC) kintox11.c $(CFLAGS) $(LDFLAGS) -lm -lpthread -o kintox11

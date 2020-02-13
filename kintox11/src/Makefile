CFLAGS=-g $(pkg-config --libs --cflags json-c) $(pkg-config --libs --cflags xmu)

all:
	$(CC) kintox11.c -lXmu -lXt -lX11 -I/usr/include/json-c -ljson-c -o kintox11

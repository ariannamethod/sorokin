# sorokin — Literary Necromancy Engine
# Build: make          (standalone C, no sqlite)
#        make sqlite    (standalone C + SQLite bootstrap memory)
#        make go        (Go + CGO + nanollama)

CC = cc
CFLAGS = -O2 -Wall -Wextra -Wno-unused-parameter
LDFLAGS = -lm

.PHONY: all clean sqlite go test

all: sorokin

sorokin: sorokin.c
	$(CC) $(CFLAGS) -o $@ $< $(LDFLAGS)

sqlite: sorokin.c
	$(CC) $(CFLAGS) -DUSE_SQLITE -o sorokin $< $(LDFLAGS) -lsqlite3

go: main.go sorokin.c sorokin.h
	CGO_ENABLED=1 go build -o sorokin .

clean:
	rm -f sorokin sorokin.db

test: sorokin
	./sorokin "destroy the sentence"
	@echo ""
	./sorokin "bone becomes word and word becomes dust"

all:
	make compile
	make build

compile:
	g++ chall.c++ -o ./src/chall

build:
	docker build . -t pwn
	docker container run -p 9001:5000 --privileged pwn:latest
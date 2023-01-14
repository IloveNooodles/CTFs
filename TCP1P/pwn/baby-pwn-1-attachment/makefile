run:
	g++ chall.c++ -o ./src/chall -fno-stack-protector
	docker build . -t pwn
	docker container run -p 9001:5000 --privileged pwn:latest
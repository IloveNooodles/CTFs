ChallName=pp2rce
PORT=52271

all:
# make all goes here

compile:
# compile section goes here

run:
# run section goes here

rm-build:
	rm \
	.svelte-kit \
	build \
	node_modules \
	-r
	

stop:
	docker stop ${ChallName}
	docker rm ${ChallName}

debug:
	docker build -t ${ChallName} .
	docker run --restart always --name ${ChallName} -p ${PORT}:8080 -it ${ChallName}

build:
	docker build -t ${ChallName} .
	docker run --restart always --name ${ChallName} -p ${PORT}:8080 -itd ${ChallName}
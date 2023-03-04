ChallName=dom-clobbering
PORT=25982
D_PORT=1337

all:
# make all goes here

compile:
# compile section goes here

run:
# run section goes here

stop:
	docker stop ${ChallName}
	docker rm ${ChallName}

debug:
	docker build -t ${ChallName} .
	docker run --restart always --name ${ChallName} -p ${PORT}:${D_PORT} -it ${ChallName}

build:
	docker build -t ${ChallName} .
	docker run --restart always --name ${ChallName} -p ${PORT}:${D_PORT} -itd ${ChallName}
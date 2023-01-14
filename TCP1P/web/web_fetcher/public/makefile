ChallName=web-fetcher
PORT=47138

all:
# make all goes here

compile:
# compile section goes here

run:
	@deno cache main.ts
	@deno run --no-prompt \
	--allow-env \
	--allow-read \
	--allow-net \
	main.ts

stop:
	docker stop ${ChallName}
	docker rm ${ChallName}

debug:
	docker build -t ${ChallName} .
	docker run --restart always --name ${ChallName} -p ${PORT}:1337 -it ${ChallName}

build:
	docker build -t ${ChallName} .
	docker run --restart always --name ${ChallName} -p ${PORT}:1337 -itd ${ChallName}
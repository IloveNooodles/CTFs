FROM python:3-alpine

RUN mkdir -p /app

# Add application
WORKDIR /app
COPY challenge .
RUN mv flag.txt /flag_$(echo $RANDOM|md5sum|head -c 10; echo;).txt
RUN pip install -r requirements.txt

# Expose the port is reachable on
EXPOSE 80

# Start the application
CMD ["flask", "run", "-h", "0.0.0.0", "-p", "80"]

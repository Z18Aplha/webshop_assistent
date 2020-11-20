# webshop_assistent
Checks a given product in a webshop whether its available or not and sends a notification with Pushover when changing.

# Setup
1. create 'config.yaml' in the folder of 'main.py' according to 'config_example.yaml'.
2. start 'main.py' or run in docker
## Docker
To run the script in docker build the image with the Dockerfile and type
'''
docker build . webshop_assistent:latest
'''
and run it with
'''
docker run -v <path_to_repos>:/webshop_asisstent webshop_assistent_latest
'''

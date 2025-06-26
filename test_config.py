import configparser

config = configparser.ConfigParser()
config.read("config.properties")

print(config.sections())  # should print ['mysql']

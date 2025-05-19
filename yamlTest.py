import yaml
file = yaml.safe_load(open("config.yaml", "r"))

print(file)

print(type(file["dmeDevices"]))
print(type(file["dmeDevices"][0]))

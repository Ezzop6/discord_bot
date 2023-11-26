from micloud import MiCloud
XIA_USER = '1588384975'
XIA_PASS = 'asd09asd800as9d8'

cloud = MiCloud(XIA_USER, XIA_PASS)
cloud.login()
tokken = cloud.get_token()

print(cloud.get_devices())

print(tokken)

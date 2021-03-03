import time
Instruments = {"2b897": {"place": "on Shelf 3E", "name": "Aloma BB Shim Set", "status": "Equipment Room"}, "97908": {"place": "on Shelf 2D", "name": "Easy-Laser Alignment Kit 2", "status": "Aaron"}, "D": {"place": "", "name": "", "status": "Equipment Room"}, "fa0b6": {"place": "on Shelf 3E", "name": "4 in. Shim Set #2", "status": "Marco"}, "A": {"place": "", "name": "", "status": "Equipment Room"}, "81cfb": {"place": "on Shelf 3E", "name": "4 in. Shim Set #4", "status": "Equipment Room"}, "f3d3f": {"place": "on Shelf 3E", "name": "4 in. Shim Set #1", "status": "Tom"}, "891a1": {"place": "on Shelf 3E", "name": "3 in. Shim Set #1", "status": "Equipment Room"}, "C": {"place": "", "name": "", "status": "Equipment Room"}, "86695": {"place": "on Shelf 3E", "name": "2 in. Shim Set #1", "status": "Equipment Room"}, "150404": {"place": "on Shelf 2A", "name": "UE Ultraprobe 15000", "status": "Mayra"}, "ti32-09110024": {"place": "on Shelf 2C", "name": "Fluke Thermal Imager Ti32", "status": "Equipment Room"}, "78234": {"place": "on Shelf 2D", "name": "Easy-Laser Alignment Kit 2", "status": "Equipment Room"}, "B": {"place": "", "name": "", "status": "Equipment Room"}, "271e3": {"place": "on Shelf 3E", "name": "5 in. Shim Set #3", "status": "Equipment Room"}, "cf1a6": {"place": "on Shelf 3E", "name": "4 in. Shim Set #3", "status": "Marco"}, "E": {"place": "", "name": "", "status": "Equipment Room"}, "0003733": {"place": "on shelf 2A", "name": "Larson Davis Sound Expert LxT", "status": "Equipment Room"}, "7967c": {"place": "on Shelf 3E", "name": "3 in. Shim Set #3", "status": "Tom"}, "1961e": {"place": "on Shelf 3E", "name": "5 in. Shim Set #1", "status": "Equipment Room"}, "aacea": {"place": "on Shelf 3E", "name": "5 in. Shim Set #2", "status": "Equipment Room"}, "a1106": {"place": "on Shelf 3E", "name": "3 in. Shim Set #2", "status": "Equipment Room"}, "7b6c1": {"place": "on Shelf 3E", "name": "2 in. Shim Set #2", "status": "Equipment Room"}, "105542": {"place": "on shelf 2D", "name": "Easy-Laser Alignment Kit 1", "status": "Equipment Room"}}

values = list(Instruments.values())
time0 = time.time()
bigthing = []
for dict0 in values:
    output = [0,0,0]
    output[0]=dict0["name"]
    output[1]=dict0["status"]
    output[2]=time0
    bigthing.append(output)
print(bigthing)
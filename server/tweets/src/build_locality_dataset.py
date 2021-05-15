from tweets.src.functions import *

class BuildLocalityDataset:

    def __init__(self):
        locality_ds = readNeighborhoods()
        locality_ds = readStreets(locality_ds)
        with open('./tweets/dataset/locality_ds.json', 'w+') as f:
            f.write(json.dumps(locality_ds,indent=2))

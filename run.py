import os

import numpy as np
import json

data_dirpath = "./data"

def getDataDir():
    """
    {wsi_id: {
        "fraction": {
            "0.1": filepath,
            "0.2": filepath,
            },
        "label": filepath,
        },
    }
    """
    wsi_list = os.listdir(data_dirpath)
    out = {}
    for wsi_dirname in wsi_list:
        wsi_id = wsi_dirname.split("_")[1]
        wsi_dirpath = os.path.join(data_dirpath, wsi_dirname)
        out[wsi_id] = {"fraction": {}, "label": None}
        for fname in os.listdir(wsi_dirpath):
            if fname.startswith("pc_frac_"):
                fraction = int(fname.split(".")[0].split("_")[3]) / 10
                fraction_str = f"{fraction:.1f}"
                out[wsi_id]["fraction"][fraction_str] = os.path.join(
                        wsi_dirpath, fname)
            elif fname.startswith("label_"):
                out[wsi_id]["label"] = os.path.join(
                        wsi_dirpath, fname)
    return out

dataDir = getDataDir()

wsi_list_data = list(dataDir.keys())
with open("wsi_list.json", "w") as f:
    json.dump(wsi_list_data, f)

for wsi_id in dataDir:
    label_data = np.load(dataDir[wsi_id]["label"])
    for fraction in dataDir[wsi_id]["fraction"]:
        fraction_data = np.load(dataDir[wsi_id]["fraction"][fraction])
        data = [{
            "x": float(fraction_data[i, 0]),
            "y": float(fraction_data[i, 1]),
            "label": int(label_data[i]),
            } for i in range(label_data.shape[0])]
        with open(f"wsi_{wsi_id}_fraction_{fraction}.json", "w") as f:
            json.dump(data, f)

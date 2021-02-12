import os

from flask import Flask, render_template
from flask_restful import Resource, Api

import numpy as np

app = Flask(__name__)
api = Api(app=app, prefix="/api/v1")

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

class WSIData(Resource):
    def get(self, wsi_id: str, fraction: str):
        pc_fpath = dataDir[wsi_id]["fraction"][fraction]
        label_fpath = dataDir[wsi_id]["label"]
        pc, label = np.load(pc_fpath), np.load(label_fpath)
        out = [{
            "x": float(pc[i, 0]),
            "y": float(pc[i, 1]),
            "label": int(label[i]),
            }
            for i in range(pc.shape[0])]
        return out

class WSIList(Resource):
    def get(self):
        return sorted(list(dataDir.keys()))

class FractionList(Resource):
    def get(self, wsi_id: str):
        return sorted(list(dataDir.get(wsi_id)["fraction"].keys()))

api.add_resource(WSIList, "/wsi/list")
api.add_resource(FractionList, "/wsi/<string:wsi_id>/fraction/list")
api.add_resource(WSIData, "/wsi/<string:wsi_id>/fraction/<string:fraction>")

@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template
from flask_restful import Resource, Api

import numpy as np

app = Flask(__name__)
api = Api(app=app, prefix="/api/v1")

data = {"0.0": np.load("pc_frac0.0.npy"),
        "0.6": np.load("pc_frac0.6.npy"),
        }
label = np.load("label.npy").reshape((-1,1))

class Coord(Resource):
    def get(self, fraction: str):
        c = data.get(fraction)
        out = [{
            "x": float(c[i, 0]),
            "y": float(c[i, 1]),
            "label": int(label[i]),
            }
            for i in range(c.shape[0])]
        return out
#        out = np.concatenate([c, label], axis=1)
#        return out.tolist()

api.add_resource(Coord, "/coord/<string:fraction>")

@app.route("/index")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

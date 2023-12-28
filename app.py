from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
import os
import pathlib
from PIL import Image

app = Flask(__name__)

# init GoogleMaps extension
GoogleMaps(app, key=os.getenv("GMAPS_API_KEY"))
LAT_SEPPLISHOF = 48.34385
LNG_SEPPLISHOF = 8.352807


def get_thumbnail(im):
    new_height = 512
    new_width = 512

    width, height = im.size
    left = (width - new_width) / 2
    top = (height - new_height) / 2
    right = (width + new_width) / 2
    bottom = (height + new_height) / 2
    im = im.crop((left, top, right, bottom))
    return im


def init_images():
    imgs = []
    img_src = pathlib.Path("static/files/images")
    img_pths = sorted(img_src.iterdir())
    for pth in img_pths:
        if pth.name.startswith(".") or not pth.is_file():
            continue
        im = Image.open(pth)
        w, h = im.size
        thum_pth = img_src / "thumbnails" / (pth.stem + ".jpeg")
        if not thum_pth.exists():
            im = get_thumbnail(im)
            im.save(thum_pth, "jpeg")
        imgs.append((pth, thum_pth, w, h))

    return imgs


IMAGES = init_images()


@app.route("/", methods=["GET"])
def home():
    location_map = Map(
        lat=LAT_SEPPLISHOF,
        lng=LNG_SEPPLISHOF,
        markers=[(LAT_SEPPLISHOF, LNG_SEPPLISHOF)],
        maptype="HYBRID",
        zoom=15,
        language="de",
        region="DE",
        identifier="location-map",
        cls="location-map",
        style="width:70vw;height:50vh;margin:0 auto;"
    )
    return render_template("index.html", location_map=location_map, images=IMAGES)

@app.route("/impressum", methods=["GET"])
def impressum():
    return render_template("impressum.html", location_map=None, images=None)


@app.route("/agb", methods=["GET"])
def agb():
    return render_template("agb.html", location_map=None, images=None)

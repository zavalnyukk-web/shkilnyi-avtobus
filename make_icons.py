import glob, os, shutil
from PIL import Image, ImageDraw

src = Image.open("assets/icon.jpg").convert("RGB")
w, h = src.size
s = min(w, h)
left, top = (w - s) // 2, (h - s) // 2
src = src.crop((left, top, left + s, top + s))

res = "android/app/src/main/res"
for d in glob.glob(res + "/mipmap-anydpi*"):
    shutil.rmtree(d)

sizes = {"mdpi": 48, "hdpi": 72, "xhdpi": 96, "xxhdpi": 144, "xxxhdpi": 192}
for name, sz in sizes.items():
    d = f"{res}/mipmap-{name}"
    os.makedirs(d, exist_ok=True)
    im = src.resize((sz, sz), Image.LANCZOS)
    im.save(f"{d}/ic_launcher.png")
    mask = Image.new("L", (sz * 4, sz * 4), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, sz * 4 - 1, sz * 4 - 1), fill=255)
    mask = mask.resize((sz, sz), Image.LANCZOS)
    rnd = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
    rnd.paste(im.convert("RGBA"), (0, 0), mask)
    rnd.save(f"{d}/ic_launcher_round.png")
print("icons done")

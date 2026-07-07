"""Recolor the Figma factory illustration with the Daedalus logo gradient
(#FB923C -> #EC4899 -> #7C3AED, left to right), fade/blur the top so it
blends seamlessly into a white page background."""

import numpy as np
from PIL import Image, ImageFilter

SRC = "factory-raw1.png"   # 3450x1306 high-res source
OUT = "factory-brand.png"

img = Image.open(SRC).convert("RGB")
w, h = img.size

rgb = np.asarray(img).astype(np.float32) / 255.0

# Luminance (0 = dark, 1 = light)
lum = 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]
# Slight contrast lift so mids don't go muddy
lum = np.clip((lum - 0.5) * 1.05 + 0.55, 0.0, 1.0)

# Horizontal brand gradient (same stops as the logo: 0% orange, 47% pink, 100% violet)
stops = [(0.0, (0xFB, 0x92, 0x3C)), (0.4717, (0xEC, 0x48, 0x99)), (1.0, (0x7C, 0x3A, 0xED))]
x = np.linspace(0.0, 1.0, w)
grad = np.zeros((w, 3), dtype=np.float32)
for i in range(len(stops) - 1):
    p0, c0 = stops[i]
    p1, c1 = stops[i + 1]
    m = (x >= p0) & (x <= p1)
    t = np.zeros_like(x)
    t[m] = (x[m] - p0) / (p1 - p0)
    for ch in range(3):
        grad[m, ch] = (np.array(c0[ch]) + (c1[ch] - c0[ch]) * t[m]) / 255.0

grad_row = grad[None, :, :]                      # 1 x w x 3
lum3 = lum[..., None]                            # h x w x 1

# Duotone: dark pixels -> brand color, light pixels -> white.
out = grad_row + (1.0 - grad_row) * lum3

# Tritone: deep shadows go to black instead of full-saturation brand color.
# This preserves the original curved silhouettes (bushes / vignette) at the
# bottom of the illustration so the image ends organically into black.
shadow = np.clip(lum / 0.30, 0.0, 1.0) ** 1.4    # 0 for near-black source pixels
out *= shadow[..., None]
out = np.clip(out, 0.0, 1.0)

result = Image.fromarray((out * 255).astype(np.uint8), "RGB")

# Blur the top part progressively
blurred = result.filter(ImageFilter.GaussianBlur(radius=max(6, w // 240)))
yy = np.linspace(0.0, 1.0, h)[:, None]           # 0 top -> 1 bottom
blur_mask = np.clip(1.0 - yy / 0.45, 0.0, 1.0) ** 1.2   # full blur at top, none below 45%
blur_mask_img = Image.fromarray((blur_mask * 255).astype(np.uint8).repeat(w, axis=1), "L")
result = Image.composite(blurred, result, blur_mask_img)

# Fade the top into pure white for a seamless page blend
white = Image.new("RGB", (w, h), (255, 255, 255))
fade = np.clip(1.0 - yy / 0.38, 0.0, 1.0) ** 1.35        # white at row 0 -> transparent by ~38%
fade_img = Image.fromarray((fade * 255).astype(np.uint8).repeat(w, axis=1), "L")
result = Image.composite(white, result, fade_img)

# Gentle black assist at the very bottom only — the organic silhouettes from
# the source image (kept by the tritone) do most of the blending; this just
# guarantees the last rows are pure black where the footer bar begins.
black = Image.new("RGB", (w, h), (0, 0, 0))
bfade = np.clip((yy - 0.90) / 0.10, 0.0, 1.0) ** 1.5
bfade_img = Image.fromarray((bfade * 255).astype(np.uint8).repeat(w, axis=1), "L")
result = Image.composite(black, result, bfade_img)

result.save(OUT, optimize=True)
print("saved", OUT, result.size)

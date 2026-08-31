import struct, zlib, os, math

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(c1, c2, t):
    return tuple(int(round(lerp(c1[i], c2[i], t))) for i in range(3)) + (255,)

def dist_point_segment(px, py, x1, y1, x2, y2):
    dx, dy = x2 - x1, y2 - y1
    length_sq = dx * dx + dy * dy
    if length_sq == 0:
        return math.hypot(px - x1, py - y1)
    t = max(0, min(1, ((px - x1) * dx + (py - y1) * dy) / length_sq))
    proj_x, proj_y = x1 + t * dx, y1 + t * dy
    return math.hypot(px - proj_x, py - proj_y)

def make_png(path, size):
    sky_top = (20, 28, 56)      # deep indigo night sky
    sky_bottom = (52, 74, 112)  # soft dusk blue
    cloud = (206, 214, 227, 255)     # pale grey-blue cloud
    cloud_shadow = (168, 178, 198, 255)
    rain = (137, 196, 224, 255)      # calm light-blue rain streak

    cx = size / 2

    # cloud: union of overlapping circles forming a puffy silhouette
    cloud_cy = size * 0.36
    circles = [
        (cx - size * 0.17, cloud_cy + size * 0.03, size * 0.16),
        (cx + size * 0.02, cloud_cy - size * 0.06, size * 0.20),
        (cx + size * 0.22, cloud_cy + size * 0.02, size * 0.15),
        (cx - size * 0.01, cloud_cy + size * 0.08, size * 0.19),
    ]

    # rain streaks: slanted lines below the cloud
    slant = size * 0.09
    rain_len = size * 0.16
    rain_thick = size * 0.018
    xs = [size * f for f in (0.28, 0.42, 0.56, 0.70)]
    y0 = size * 0.58
    rains = []
    for i, x in enumerate(xs):
        off = (i % 2) * size * 0.07
        ry0 = y0 + off
        ry1 = ry0 + rain_len
        rains.append((x, ry0, x - slant, ry1))

    rows = []
    for y in range(size):
        t = y / size
        bg = lerp_color(sky_top, sky_bottom, t)
        row = bytearray()
        for x in range(size):
            px, py = x + 0.5, y + 0.5
            color = bg

            in_cloud = any((px - ccx) ** 2 + (py - ccy) ** 2 <= cr * cr for ccx, ccy, cr in circles)
            if in_cloud:
                near_edge = any(
                    cr * cr * 0.7 <= (px - ccx) ** 2 + (py - ccy) ** 2 <= cr * cr
                    for ccx, ccy, cr in circles
                )
                color = cloud_shadow if near_edge else cloud
            else:
                for x1, y1, x2, y2 in rains:
                    if dist_point_segment(px, py, x1, y1, x2, y2) <= rain_thick:
                        color = rain
                        break

            row.extend(color)
        rows.append(bytes(row))

    raw = b"".join(b"\x00" + r for r in rows)
    compressed = zlib.compress(raw, 9)

    def chunk(tag, data):
        return (struct.pack(">I", len(data)) + tag + data +
                struct.pack(">I", zlib.crc32(tag + data)))

    sig = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack(">IIBBBBB", size, size, 8, 6, 0, 0, 0)
    png = sig + chunk(b"IHDR", ihdr) + chunk(b"IDAT", compressed) + chunk(b"IEND", b"")

    with open(path, "wb") as f:
        f.write(png)

out_dir = os.path.dirname(os.path.abspath(__file__))
make_png(os.path.join(out_dir, "icon-192.png"), 192)
make_png(os.path.join(out_dir, "icon-512.png"), 512)
print("done")

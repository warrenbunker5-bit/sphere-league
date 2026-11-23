"""Cut a ChatGPT parts sheet (transparent PNG) into rig parts + rig.json for Sphere League's cut-out rig.
Usage: cut_form.py <sheet.png> <outdir> <spec.json>
spec: {"pieces": {name: {"i": index-in-sheet-order, "kind": "limb"|"plain", "prox": "top"|"left"|"bottom"|"right", "split": n (split a merged component into n parts left->right)}}, ...extra rig.json keys}
Pieces are numbered by row then x (same order as seg.py's contact sheet).
"""
import sys, json, os, math, numpy as np
from PIL import Image
from scipy import ndimage
src, out, specf = sys.argv[1:4]
spec = json.load(open(specf)); os.makedirs(out, exist_ok=True)
im = Image.open(src).convert('RGBA'); A = np.array(im); fg = A[..., 3] > 40
# ChatGPT's 'transparent' sheets fade light interior colours to partial alpha (colour-to-alpha).
# Rebuild: composite over white (how the art was drawn) and make the silhouette solid; keep soft alpha only on the rim.
al = A[..., 3:4].astype(float) / 255; rgb = A[..., :3] * al + 255 * (1 - al)
solid = ndimage.binary_fill_holes(fg); inner = ndimage.binary_erosion(solid, iterations=2)
alpha = np.where(inner, 255, np.where(solid, np.maximum(A[..., 3], 150), 0))
A = np.dstack([rgb, alpha]).clip(0, 255).astype(np.uint8)
lab, _ = ndimage.label(ndimage.binary_closing(fg, iterations=2))
P = []
for i, sl in enumerate(ndimage.find_objects(lab), 1):
    if (lab[sl] == i).sum() < 600: continue
    P.append((i, sl))
P.sort(key=lambda t: (round(t[1][0].start / 60), t[1][1].start))
SC = spec.get('upscale', 2)  # pilot sheets are low-res; upscale with Lanczos so the in-game downscale stays crisp

def crop(i, sl, keep=None):
    m = lab[sl] == i
    if keep is not None: m &= keep
    c = A[sl].copy(); c[..., 3] = np.where(m, c[..., 3], 0)
    ys, xs = np.nonzero(c[..., 3] > 0); c = c[ys.min():ys.max() + 1, xs.min():xs.max() + 1]
    c = np.pad(c, ((6, 6), (6, 6), (0, 0)))
    I = Image.fromarray(c); return I.resize((I.width * SC, I.height * SC), Image.LANCZOS)

def limb(I, prox, a_at=0.2, b_at=0.8):
    a = np.array(I)[..., 3] > 60; ys, xs = np.nonzero(a); pts = np.stack([xs, ys], 1).astype(float); c = pts.mean(0)
    u, s, vt = np.linalg.svd(pts - c, full_matrices=False); ax = vt[0]
    pr = (pts - c) @ ax; e1, e2 = c + ax * pr.min(), c + ax * pr.max()
    pick = {'top': lambda p, q: p[1] < q[1], 'bottom': lambda p, q: p[1] > q[1], 'left': lambda p, q: p[0] < q[0], 'right': lambda p, q: p[0] > q[0]}[prox]
    p0, p1 = (e1, e2) if pick(e1, e2) else (e2, e1)
    ang = math.degrees(math.atan2(p1[1] - p0[1], p1[0] - p0[0]))
    R = I.rotate(ang, resample=Image.BICUBIC, expand=True)  # PIL rotates CCW: brings p0->p1 to +x
    r = np.array(R)[..., 3] > 60; ys, xs = np.nonzero(r); R = R.crop((xs.min() - 2, ys.min() - 2, xs.max() + 3, ys.max() + 3))
    r = np.array(R)[..., 3] > 60; xs = np.nonzero(r.any(0))[0]; L = xs.max() - xs.min()
    def mid(x):
        col = np.nonzero(r[:, int(x)])[0]; return float((col.min() + col.max()) / 2) if len(col) else R.height / 2
    ax_, bx_ = xs.min() + L * a_at, xs.min() + L * b_at
    return R, [round(ax_), round(mid(ax_))], [round(bx_), round(mid(bx_))]

cfg = {k: v for k, v in spec.items() if k not in ('pieces', 'upscale', 'points')}; cfg['parts'] = {}
for name, q in spec['pieces'].items():
    i, sl = P[q['i']]
    if q.get('split'):
        m = lab[sl] == i; sub, n = ndimage.label(m & (A[sl][..., 3] > 40))
        comps = sorted([(ndimage.find_objects(sub)[k - 1][1].start, k) for k in range(1, n + 1) if (sub == k).sum() > 200])
        names = q['names']
        if len(comps) < len(names):  # segments touch: cut at the narrowest column in the middle of the piece
            cnt = m.sum(0); w = len(cnt); lo, hi = int(w * 0.3), int(w * 0.7); cx = lo + int(np.argmin(cnt[lo:hi]))
            sub = np.zeros_like(m, dtype=int); sub[:, :cx] = m[:, :cx] * 1; sub[:, cx:] = m[:, cx:] * 2; comps = [(0, 1), (cx, 2)]
        for (x0, k), nm in zip(comps, names):
            I = crop(i, sl, sub == k); R, a, b = limb(I, q.get('prox', 'left'), q.get('a', 0.15), q.get('b', 0.85))
            R.save(f'{out}/{nm}.png'); cfg['parts'][nm] = {'file': nm + '.png', 'a': a, 'b': b}
        continue
    I = crop(i, sl)
    if q['kind'] == 'limb':
        R, a, b = limb(I, q['prox'], q.get('a', 0.2), q.get('b', 0.8)); R.save(f'{out}/{name}.png'); cfg['parts'][name] = {'file': name + '.png', 'a': a, 'b': b}
    else:
        I.save(f'{out}/{name}.png'); e = {'file': name + '.png'}
        for k, (fx, fy) in q.get('pts', {}).items(): e[k] = [round(fx * I.width), round(fy * I.height)]
        cfg['parts'][name] = e
# forearm doubles as fist: these sheets draw the hand on the forearm piece
if 'forearm' in cfg['parts'] and 'fist' not in cfg['parts']: cfg['parts']['fist'] = dict(cfg['parts']['forearm'])
for ch in cfg.get('chains', []):
    if 'ptf' in ch:
        W_, H_ = Image.open(f"{out}/{ch['from']}.png").size; ch['pt'] = [round(ch['ptf'][0] * W_), round(ch['ptf'][1] * H_)]; del ch['ptf']
th = Image.open(f"{out}/torso.png").height; cfg['height'] = round(999 * th / 406)  # human torso is 406 px of a 999 px figure
json.dump(cfg, open(f'{out}/rig.json', 'w'), indent=1); print(out, sorted(cfg['parts']), 'height', cfg['height'])

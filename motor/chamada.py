"""Chamada animada de LIKE + INSCREVA-SE no estilo do Códex Obscuro (canto inferior direito)."""
import math, os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

DUR = 6.2  # segundos na tela

def _ease(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

def _pm(img):
    a = np.asarray(img).astype(np.float32) / 255.0
    a[..., :3] *= a[..., 3:4]
    return a

class Chamada:
    def __init__(self, W, H, S, fonte_fn, branco, destaque):
        self.W, self.H, self.S = W, H, S
        self.B, self.D = tuple(branco), tuple(destaque)
        self.f_bot = fonte_fn('titulo', 34 * S, 'Bold')
        self.f_txt = fonte_fn('italico', 30 * S, 'Medium')
        self.like_off = _pm(self._like(False)); self.like_on = _pm(self._like(True))
        self.bot_off = _pm(self._botao(False)); self.bot_on = _pm(self._botao(True))
        self.sino = self._sino()
        cw = int(26 * S) + int(84 * S) + int(22 * S) + self.bot_off.shape[1] + int(22 * S) + self.sino.width + int(30 * S)
        ch = int(120 * S)
        self.cw, self.ch = cw, ch
        self.x0 = W - cw - int(56 * S)
        self.y0 = H - ch - int(64 * S)
        self.card = _pm(self._card())
        self.mao = _pm(self._mao())

    # ---------- desenho das peças
    def _card(self):
        S = self.S
        im = Image.new('RGBA', (self.cw, self.ch), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        d.rounded_rectangle((0, 0, self.cw - 1, self.ch - 1), radius=int(22 * S), fill=(8, 7, 6, 225),
                            outline=self.B + (255,), width=max(2, int(2 * S)))
        return im

    def _like(self, on):
        S = self.S; s = int(84 * S); pad = int(18 * S)
        im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        cor = self.D if on else self.B
        w = max(2, int(3.2 * S))
        # punho
        d.rounded_rectangle((int(.08 * s), int(.45 * s), int(.28 * s), int(.90 * s)), radius=int(4 * S),
                            outline=cor + (255,), width=w, fill=(cor + (255,)) if on else None)
        # mão
        pts = [(.34, .47), (.50, .14), (.58, .12), (.62, .22), (.58, .40), (.84, .40), (.90, .48),
               (.86, .60), (.86, .70), (.82, .80), (.76, .90), (.34, .90)]
        pts = [(int(x * s), int(y * s)) for x, y in pts]
        d.polygon(pts, outline=cor + (255,), fill=(cor + (255,)) if on else None, width=w)
        if not on:
            for y in (.60, .70, .80):
                d.line((int(.70 * s), int(y * s), int(.86 * s), int(y * s)), fill=cor + (255,), width=w)
        big = Image.new('RGBA', (s + 2 * pad, s + 2 * pad), (0, 0, 0, 0)); big.paste(im, (pad, pad))
        if on:
            big = Image.alpha_composite(self._halo(big, cor, 9 * S), big)
        return big

    def _botao(self, on):
        S = self.S
        txt = 'INSCRITO  ✓' if on else 'INSCREVA-SE'
        txt = 'INSCRITO' if on else 'INSCREVA-SE'
        f = self.f_bot
        tw = f.getlength(txt)
        bw, bh = int(tw + 56 * S), int(64 * S)
        im = Image.new('RGBA', (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        if on:
            d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=bh // 2, fill=self.D + (255,))
            d.text((bw / 2, bh / 2), txt, font=f, anchor='mm', fill=(15, 12, 8, 255))
        else:
            d.rounded_rectangle((0, 0, bw - 1, bh - 1), radius=bh // 2, outline=self.B + (255,), width=max(2, int(3 * S)))
            d.text((bw / 2, bh / 2), txt, font=f, anchor='mm', fill=self.B + (255,))
        return im

    def _sino(self):
        S = self.S; s = int(56 * S)
        im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        w = max(2, int(3 * S)); c = self.B + (255,)
        d.arc((int(.18 * s), int(.10 * s), int(.82 * s), int(.80 * s)), 180, 360, fill=c, width=w)
        d.line((int(.18 * s), int(.45 * s), int(.14 * s), int(.74 * s)), fill=c, width=w)
        d.line((int(.82 * s), int(.45 * s), int(.86 * s), int(.74 * s)), fill=c, width=w)
        d.line((int(.08 * s), int(.76 * s), int(.92 * s), int(.76 * s)), fill=c, width=w)
        d.ellipse((int(.42 * s), int(.80 * s), int(.58 * s), int(.94 * s)), outline=c, width=w)
        d.line((int(.5 * s), int(.02 * s), int(.5 * s), int(.10 * s)), fill=c, width=w)
        return im

    def _mao(self):
        S = self.S; s = int(70 * S)
        im = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        # seta de cursor (ponta em 0,0)
        pts = [(0, 0), (0, .78), (.22, .60), (.38, .95), (.52, .89), (.36, .55), (.66, .55)]
        pts = [(int(x * s), int(y * s)) for x, y in pts]
        d.polygon(pts, fill=self.B + (255,), outline=(0, 0, 0, 255), width=max(2, int(2.5 * S)))
        return im

    def _halo(self, im, cor, r):
        a = im.split()[3].filter(ImageFilter.GaussianBlur(r)).point(lambda v: int(v * .9))
        h = Image.new('RGBA', im.size, cor + (0,)); h.putalpha(a)
        return h

    # ---------- desenho no quadro
    def desenhar(self, base, dt, compor):
        if dt < 0 or dt > DUR:
            return
        S = self.S
        op = _ease(dt / .5) * (1 - _ease((dt - (DUR - .6)) / .6))
        dy = int((1 - _ease(dt / .5)) * 40 * S)
        x0, y0 = self.x0, self.y0 + dy
        compor(base, self.card, x0, y0, op)
        # like
        clic_like, clic_bot = 1.7, 2.9
        lk = self.like_on if dt >= clic_like else self.like_off
        pop = 1.0
        if clic_like <= dt < clic_like + .35:
            pop = 1 + .25 * math.sin((dt - clic_like) / .35 * math.pi)
        pad = int(18 * S)
        lx, ly = x0 + int(26 * S) - pad, y0 + (self.ch - lk.shape[0]) // 2
        if pop != 1.0:
            import cv2
            nh, nw = int(lk.shape[0] * pop), int(lk.shape[1] * pop)
            lk2 = cv2.resize(lk, (nw, nh))
            compor(base, lk2, lx - (nw - lk.shape[1]) // 2, ly - (nh - lk.shape[0]) // 2, op)
        else:
            compor(base, lk, lx, ly, op)
        # botão
        bt = self.bot_on if dt >= clic_bot else self.bot_off
        bx = x0 + int(132 * S); by = y0 + (self.ch - bt.shape[0]) // 2
        compor(base, bt, bx, by, op)
        # sino (balança depois da inscrição)
        ang = 0.0
        if clic_bot + .1 <= dt < clic_bot + 1.1:
            ang = 22 * math.sin((dt - clic_bot) * 18) * (1 - (dt - clic_bot) / 1.1)
        sino = self.sino.rotate(ang, resample=Image.BICUBIC, center=(self.sino.width / 2, 4 * S)) if ang else self.sino
        sx = bx + bt.shape[1] + int(22 * S); sy = y0 + (self.ch - sino.height) // 2
        compor(base, _pm(sino), sx, sy, op)
        # cursor: entra, vai ao like, clica, vai ao botão, clica, sai
        alvo_like = (lx + pad + int(52 * S), ly + pad + int(48 * S))
        alvo_bot = (bx + int(bt.shape[1] * .6), by + int(40 * S))
        fora = (self.W - int(20 * S), self.H + int(40 * S))
        if dt < 1.0:
            p = None
        elif dt < clic_like:
            u = _ease((dt - 1.0) / (clic_like - 1.0)); p = (fora[0] + (alvo_like[0] - fora[0]) * u, fora[1] + (alvo_like[1] - fora[1]) * u)
        elif dt < clic_like + .4:
            p = alvo_like
        elif dt < clic_bot:
            u = _ease((dt - clic_like - .4) / (clic_bot - clic_like - .4)); p = (alvo_like[0] + (alvo_bot[0] - alvo_like[0]) * u, alvo_like[1] + (alvo_bot[1] - alvo_like[1]) * u)
        elif dt < clic_bot + .5:
            p = alvo_bot
        elif dt < clic_bot + 1.3:
            u = _ease((dt - clic_bot - .5) / .8); p = (alvo_bot[0] + (fora[0] - alvo_bot[0]) * u, alvo_bot[1] + (fora[1] - alvo_bot[1]) * u)
        else:
            p = None
        if p is not None:
            clique = (clic_like <= dt < clic_like + .12) or (clic_bot <= dt < clic_bot + .12)
            m = self.mao
            if clique:
                import cv2
                m = cv2.resize(m, (int(m.shape[1] * .85), int(m.shape[0] * .85)))
            compor(base, m, int(p[0]), int(p[1]), op)

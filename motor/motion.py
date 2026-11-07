#!/usr/bin/env python3
"""
MOTOR DE MOTION — motor de motion graphics do canal Canal Teste.

Pega o áudio do ElevenLabs + o texto usado para gerar o áudio + um storyboard
e monta o vídeo: fundo hachurado em movimento lento, imagens line-art entrando
no momento da fala, frases de impacto, contadores e cartões de título.

Comandos:
  python3 motion.py storyboard  --texto elevenlabs.md --parte 1 --saida storyboard-parte1.txt
  python3 motion.py render      --audio 1.mp3 --texto elevenlabs.md --parte 1 \
                                      --storyboard storyboard-parte1.txt --imagens pasta_imagens \
                                      --saida parte1.mp4 [--res 720] [--de 0 --ate 30]
  python3 motion.py quadros     (mesmos argumentos do render) --tempos 3,10,25 --saida pasta_png
  python3 motion.py juntar      --videos p1.mp4 p2.mp4 --audio 1.mp3 --saida final.mp4
"""
import argparse, json, math, os, re, subprocess, sys, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from alinhar import alinhar, trechos_do_texto  # noqa: E402

FONTES = os.path.join(AQUI, 'fontes')
FUNDO_PADRAO = os.path.join(AQUI, 'fundo.jpeg')

BRANCO = (236, 232, 222)          # branco levemente envelhecido
SANGUE = (190, 42, 36)            # vermelho de destaque
CINZA = (150, 146, 138)

# ----------------------------------------------------------------- utilidades

def ease_out(x):
    x = min(max(x, 0.0), 1.0)
    return 1 - (1 - x) ** 3

def ease_in_out(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)

def fonte(nome, tamanho, peso=None):
    arq = {
        'titulo': 'Cinzel[wght].ttf',
        'texto': 'CormorantGaramond[wght].ttf',
        'italico': 'CormorantGaramond-Italic[wght].ttf',
        'maquina': 'SpecialElite-Regular.ttf',
    }[nome]
    f = ImageFont.truetype(os.path.join(FONTES, arq), int(tamanho))
    if peso:
        try:
            f.set_variation_by_name(peso)
        except Exception:
            pass
    return f

def texto_da_parte(caminho, parte):
    t = open(caminho, encoding='utf-8').read()
    if parte is None:
        return t
    blocos = re.split(r'\n##\s+Parte\s+', t)
    for b in blocos[1:]:
        num = re.match(r'(\d+)', b)
        if num and int(num.group(1)) == int(parte):
            corpo = b.split('\n', 1)[1]
            return corpo.split('\n---')[0]
    raise SystemExit(f'Parte {parte} não encontrada em {caminho}')

# --------------------------------------------------------------- storyboard

def ler_storyboard(caminho):
    """Formato:
    [01] texto falado (só para leitura)
    imagem: arquivo.png
    video: videos/clipe.mp4   -> clipe line-art (fundo preto); se existir, substitui a imagem da cena
    efeito: zoom | desenhar | deslizar
    texto: frase com *destaque*
    falado            -> mostra o próprio trecho falado como texto cinético
    numero: 22% | legenda
    titulo: TÍTULO | subtítulo
    legenda: texto pequeno embaixo
    fonte: Ipsos-Ipec/MCCE, 2025
    print: captura.png
    documento: imagens/real.png   -> imagem real em cor (PNG com transparência: papel + sombra + selo), não vira line-art
    manter            -> continua a cena anterior
    preto             -> tela só com o fundo
    selo: 0.6         -> brilho (0 a 1) do selo fixo no canto (precisa de --selo imagem.png)
    transicao: corte | whip | zoom | flash | glitch   -> como esta cena ENTRA (padrão: fusão suave)
    + palavra         -> SUB-CENA: troca o visual no meio do trecho, quando "palavra" é falada
                         (as linhas seguintes valem para a sub-cena; "+" sozinho divide o tempo igualmente)
    """
    cenas = {}
    atual = None
    alvo = None
    for ln in open(caminho, encoding='utf-8'):
        ln = ln.rstrip('\n')
        if not ln.strip() or ln.lstrip().startswith('#'):
            continue
        m = re.match(r'\s*\[(\d+)\]', ln)
        if m:
            atual = int(m.group(1))
            cenas[atual] = {}
            alvo = cenas[atual]
            continue
        if atual is None:
            continue
        s = ln.strip()
        if s.startswith('+'):
            alvo = {}
            cenas[atual].setdefault('_subs', []).append((s[1:].strip(), alvo))
            continue
        if s in ('manter', 'falado', 'preto'):
            alvo[s] = True
            continue
        if ':' in s:
            k, v = s.split(':', 1)
            alvo[k.strip().lower()] = v.strip()
    return cenas

def gerar_storyboard(trechos, saida):
    with open(saida, 'w', encoding='utf-8') as f:
        f.write('# STORYBOARD — um bloco por trecho do áudio.\n')
        f.write('# Comandos: imagem / efeito / texto / falado / numero / titulo / legenda / fonte / print / manter / preto\n')
        f.write('# Use *asteriscos* para destacar palavras em vermelho.\n\n')
        for i, t in enumerate(trechos, 1):
            f.write(f'[{i:02d}] {t["texto"]}\n')
            f.write('falado\n\n' if i == 1 else 'manter\n\n')

# ------------------------------------------------------------------ camadas

class Camada:
    """Imagem RGBA float pré-multiplicada + posição."""
    def __init__(self, rgba, x=0, y=0):
        a = rgba.astype(np.float32) / 255.0
        a[..., :3] *= a[..., 3:4]
        self.px = a
        self.x, self.y = int(x), int(y)

def compor(base, cam_px, x, y, opac):
    """base: float32 HxWx3 (0..1). cam_px pré-multiplicado."""
    if opac <= 0.003:
        return
    H, W = base.shape[:2]
    h, w = cam_px.shape[:2]
    x0, y0 = max(x, 0), max(y, 0)
    x1, y1 = min(x + w, W), min(y + h, H)
    if x1 <= x0 or y1 <= y0:
        return
    src = cam_px[y0 - y:y1 - y, x0 - x:x1 - x]
    reg = base[y0:y1, x0:x1]
    inv = 1.0 - src[..., 3:4] * opac
    np.multiply(reg, inv, out=reg)
    if opac >= 0.999:
        reg += src[..., :3]
    else:
        reg += src[..., :3] * opac

def brilho(img_rgba, raio, forca, cor=BRANCO):
    """Adiciona brilho suave (glow) em volta do traço."""
    alfa = img_rgba.split()[3]
    g = alfa.filter(ImageFilter.GaussianBlur(raio)).point(lambda v: int(v * forca))
    halo = Image.new('RGBA', img_rgba.size, cor + (0,))
    halo.putalpha(g)
    return Image.alpha_composite(halo, img_rgba)

def carregar_lineart(caminho, W, H, escala_max=1.0):
    im = Image.open(caminho)
    if im.mode != 'RGBA':
        # JPG com fundo preto: a luminância vira transparência
        cinza = im.convert('L')
        im = Image.new('RGBA', im.size, BRANCO + (0,))
        im.putalpha(cinza)
    else:
        # garante traço claro
        r, g, b, a = im.split()
        lum = Image.merge('RGB', (r, g, b)).convert('L')
        a = Image.fromarray((np.asarray(a, np.float32) * np.clip(np.asarray(lum, np.float32) / 200, 0, 1)).astype(np.uint8))
        im = Image.new('RGBA', im.size, BRANCO + (0,))
        im.putalpha(a)
    f = min(W * escala_max / im.width, H * escala_max / im.height)
    im = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS)
    return im

def carregar_print(caminho, W, H):
    im = Image.open(caminho).convert('RGB')
    f = min(W * 0.62 / im.width, H * 0.66 / im.height)
    im = im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS)
    borda = max(6, W // 240)
    card = Image.new('RGBA', (im.width + 2 * borda, im.height + 2 * borda), BRANCO + (255,))
    card.paste(im, (borda, borda))
    sombra_pad = W // 40
    out = Image.new('RGBA', (card.width + 2 * sombra_pad, card.height + 2 * sombra_pad), (0, 0, 0, 0))
    sh = Image.new('RGBA', card.size, (0, 0, 0, 200))
    out.paste(sh, (sombra_pad + 8, sombra_pad + 12))
    out = out.filter(ImageFilter.GaussianBlur(sombra_pad / 2.5))
    out.alpha_composite(card, (sombra_pad, sombra_pad))
    return out.rotate(-1.2, resample=Image.BICUBIC, expand=True)

def achar_arquivo(caminho):
    """Acha a imagem mesmo se a extensão for outra (.png/.jpg/.jpeg/.webp)."""
    if os.path.exists(caminho):
        return caminho
    base = os.path.splitext(caminho)[0]
    for ext in ('.png', '.jpg', '.jpeg', '.webp', '.PNG', '.JPG', '.JPEG'):
        if os.path.exists(base + ext):
            return base + ext
    return None

# ------------------------------------------------------ texto cinético

def palavras_marcadas(frase):
    """'a *maioria* não' -> [(a,False),(maioria,True),(não,False)]"""
    out, destaque = [], False
    for tok in re.split(r'(\*)', frase):
        if tok == '*':
            destaque = not destaque
            continue
        for p in tok.split():
            if out and re.fullmatch(r'[.,;:!?…)"»]+', p):
                out[-1] = (out[-1][0] + p, out[-1][1])
            else:
                out.append((p, destaque))
    return out

def montar_texto(frase, W, H, S, tamanho=78, largura=0.78, y_centro=0.5, estilo='texto'):
    """Devolve lista de (Image palavra, x, y, indice) já posicionadas."""
    pal = palavras_marcadas(frase)
    f_norm = fonte(estilo, tamanho * S, 'Medium' if estilo == 'texto' else None)
    f_dest = fonte('texto', tamanho * S * 1.08, 'Bold')
    esp = f_norm.getlength(' ')
    maxw = W * largura
    linhas, linha, lw = [], [], 0
    for p, d in pal:
        f = f_dest if d else f_norm
        w = f.getlength(p)
        if linha and lw + esp + w > maxw:
            linhas.append((linha, lw)); linha, lw = [], 0
        linha.append((p, d, w)); lw += (esp if lw else 0) + w
    if linha:
        linhas.append((linha, lw))
    alt_linha = tamanho * S * 1.22
    total_h = alt_linha * len(linhas)
    y = H * y_centro - total_h / 2
    pad = int(30 * S)
    itens, idx = [], 0
    for linha, lw in linhas:
        x = (W - lw) / 2
        for p, d, w in linha:
            f = f_dest if d else f_norm
            cor = SANGUE if d else BRANCO
            asc, desc = f.getmetrics()
            img = Image.new('RGBA', (int(w) + 2 * pad, asc + desc + 2 * pad), (0, 0, 0, 0))
            dr = ImageDraw.Draw(img)
            dr.text((pad, pad), p, font=f, fill=cor + (255,))
            img = brilho(img, 9 * S, 0.40, BRANCO) if not d else brilho(img, 14 * S, 0.85, tuple(int(c * 0.6) for c in SANGUE))
            off_y = (tamanho * S * 1.08 - asc) if not d else (tamanho * S * 1.08 - asc)
            itens.append((img, x - pad, y - pad + off_y * 0.5, idx))
            x += w + esp
            idx += 1
        y += alt_linha
    return itens

# ---------------------------------------------------------- cenas

class Cena:
    def __init__(self, ini, fim, spec, trechos_txt, tempos_trechos):
        self.ini, self.fim, self.spec = ini, fim, spec
        self.trechos_txt = trechos_txt          # textos falados na cena
        self.tempos = tempos_trechos            # [(ini,fim)] de cada trecho

class Montador:
    def __init__(self, W, H, fps, pasta_imgs, fundo):
        self.W, self.H, self.fps = W, H, fps
        self.S = H / 1080.0
        self.pasta = pasta_imgs
        self.cache = {}
        self._fundo(fundo)

    # ---- fundo
    def _fundo(self, caminho):
        W, H = self.W, self.H
        bg = Image.open(caminho).convert('RGB')
        bw, bh = int(W * 1.12), int(H * 1.12)
        bg = bg.resize((bw, bh), Image.LANCZOS)
        self.bg = np.asarray(bg, np.float32) / 255.0 * 0.82
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)
        self.vinheta = np.clip(1.15 - 0.55 * d ** 1.6, 0.25, 1.0)[..., None]
        import cv2
        self.cv2 = cv2
        self.vinheta3 = np.repeat(self.vinheta, 3, axis=2).astype(np.float32)
        rng = np.random.default_rng(7)
        # textura de grão FIXA (grão animado deixa o arquivo gigante e o YouTube destrói de qualquer jeito)
        self.grao = cv2.resize(rng.standard_normal((H // 2, W // 2)).astype(np.float32) * 0.03, (W, H),
                               interpolation=cv2.INTER_LINEAR)[..., None]

    def tensao(self, t):
        tp = getattr(self, 'tensao_pts', None)
        if tp is None: return None
        return float(np.interp(t, tp[0], tp[1]))

    def _fase(self, t):
        """tempo 'deformado': o fundo anda mais rápido quando a tensão sobe (integra a velocidade)"""
        tp = getattr(self, 'tensao_pts', None)
        if tp is None: return t
        if not hasattr(self, '_fase_tab'):
            ts = np.arange(min(0.0, float(tp[0][0])) - 1, float(tp[0][-1]) + 1, 0.05, dtype=np.float64)
            vel = 0.5 + 6.5 * np.interp(ts, tp[0], tp[1]) ** 1.5
            self._fase_tab = (ts, np.cumsum(vel) * 0.05)
        return float(np.interp(t, *self._fase_tab))

    def fundo(self, t):
        cv2 = self.cv2
        W, H = self.W, self.H
        bh, bw = self.bg.shape[:2]
        k = self.tensao(t)
        if k is None:
            s = 1.0 + 0.025 * math.sin(t / 19.0)
            ang = 0.5 * math.sin(t / 27.0)
            dx = (bw - W) / 2 + 18 * self.S * math.sin(t / 23.0)
            dy = (bh - H) / 2 + 12 * self.S * math.cos(t / 29.0)
            M = cv2.getRotationMatrix2D((bw / 2, bh / 2), ang, s)
            M[0, 2] -= dx
            M[1, 2] -= dy
            return cv2.warpAffine(self.bg, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        f = self._fase(t)
        # camada 1: o hachurado de sempre, andando mais rápido e "respirando" com a tensão
        pulso = 0.012 * max(0.0, k - 0.5) * 2 * (0.5 + 0.5 * math.sin(f * 0.9))   # respiração suave, sem solavanco
        s = 1.0 + 0.03 * math.sin(f / 19.0) + 0.04 * k + pulso
        ang = (0.5 + 1.5 * k) * math.sin(f / 27.0)
        dx = (bw - W) / 2 + (18 + 40 * k) * self.S * math.sin(f / 23.0)
        dy = (bh - H) / 2 + (12 + 30 * k) * self.S * math.cos(f / 29.0)
        M = cv2.getRotationMatrix2D((bw / 2, bh / 2), ang, s); M[0, 2] -= dx; M[1, 2] -= dy
        base = cv2.warpAffine(self.bg, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        # camada 2: um segundo hachurado cruzado que desliza na diagonal (só aparece com tensão)
        if k > 0.05:
            M2 = cv2.getRotationMatrix2D((bw / 2, bh / 2), 90 + 8 * math.sin(f / 31.0), 1.15)
            # deslizamento contínuo (sem 'voltar ao começo'): ondas lentas e longas
            M2[0, 2] -= (bw - W) / 2 + 70 * self.S * math.sin(f / 13.0) + 30 * self.S * math.sin(f / 5.3)
            M2[1, 2] -= (bh - H) / 2 + 50 * self.S * math.cos(f / 17.0) + 20 * self.S * math.cos(f / 6.1)
            cam2 = cv2.warpAffine(self.bg, M2, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            base = np.maximum(base, cam2 * min(1.0, 1.1 * k))
        # brilho: calmo = mais escuro e suave; tenso = mais contraste e um calor âmbar nas bordas
        luz = 0.62 + 0.75 * k + 0.15 * pulso / 0.012 * k
        base = base * luz
        if k > 0.3:
            quente = (k - 0.3) / 0.7 * 0.32
            borda = (1.0 - self.vinheta) * quente
            base = base + borda * np.array([0.9, 0.45, 0.08], np.float32)
        return base

    def finalizar(self, quadro, t, fade=1.0):
        cv2 = self.cv2
        flick = 1.0 + 0.025 * math.sin(t * 13.1) * math.sin(t * 3.7)
        q = cv2.multiply(quadro, self.vinheta3, scale=flick)
        q += self.grao
        return cv2.convertScaleAbs(q, alpha=255.0 * fade)

    # ---- preparação de uma cena (pré-render dos elementos)
    def preparar(self, cena):
        W, H, S = self.W, self.H, self.S
        sp = cena.spec
        el = {}
        tem_visual = any(k in sp for k in ('imagem', 'print', 'video', 'documento'))
        tem_texto_baixo = 'legenda' in sp or (tem_visual and ('texto' in sp or 'falado' in sp))
        tem_video = 'video' in sp and os.path.exists(os.path.join(self.pasta, sp['video']))
        if 'imagem' in sp and not tem_video:   # se o clipe existir, ele substitui a imagem
            cam = achar_arquivo(os.path.join(self.pasta, sp['imagem']))
            if cam:
                esc = 0.74 if tem_texto_baixo else 0.9
                im = carregar_lineart(cam, W, H, esc)
                im = brilho(im, 6 * S, 0.35)
                self._guardar_img(el, im)
            else:
                el['faltando'] = sp['imagem']
        if 'video' in sp:
            cam = os.path.join(self.pasta, sp['video'])
            if os.path.exists(cam):
                cap = self.cv2.VideoCapture(cam)
                el['video'] = {'cap': cap, 'fps': cap.get(self.cv2.CAP_PROP_FPS) or 24,
                               'n': int(cap.get(self.cv2.CAP_PROP_FRAME_COUNT)), 'ult': -1, 'quadro': None,
                               'esc': 0.74 if tem_texto_baixo else 0.92}
            elif 'imagem' not in sp:
                el['faltando'] = sp['video']
        if 'documento' in sp:   # imagem real em cor (RGBA pronto: papel + sombra + selo), sem virar line-art
            cam = achar_arquivo(os.path.join(self.pasta, sp['documento']))
            if cam:
                im = Image.open(cam).convert('RGBA')
                f = min(W / im.width, H / im.height)
                im = im.resize((max(1, int(im.width * f)), max(1, int(im.height * f))), Image.LANCZOS)
                self._guardar_img(el, im)
            else:
                el['faltando'] = sp['documento']
        if 'print' in sp:
            cam = achar_arquivo(os.path.join(self.pasta, sp['print']))
            if cam:
                self._guardar_img(el, carregar_print(cam, W, H))
                el['eh_print'] = True
            else:
                el['faltando'] = sp['print']
        frase = sp.get('texto')
        sincroniza = False
        if not frase and sp.get('falado'):
            frase = ' '.join(cena.trechos_txt)
            sincroniza = True
        if frase:
            if tem_texto_baixo and ('img' in el or 'video' in el):
                itens = montar_texto(frase, W, H, S, tamanho=64, largura=0.8, y_centro=0.86)
            else:
                n = len(frase.split())
                tam = 112 if n <= 6 else (88 if n <= 18 else 68)
                itens = montar_texto(frase, W, H, S, tamanho=tam)
            el['palavras'] = [(Camada(np.asarray(im)), x, y, i) for im, x, y, i in itens]
            el['n_pal'] = len(itens)
            el['sincroniza'] = sincroniza
        if 'legenda' in sp:
            itens = montar_texto(sp['legenda'], W, H, S, tamanho=50, largura=0.8, y_centro=0.9, estilo='italico')
            el['legenda'] = [(Camada(np.asarray(im)), x, y) for im, x, y, i in itens]
        if 'numero' in sp:
            num, _, rot = sp['numero'].partition('|')
            m = re.match(r'\s*([^\d]*)([\d.,]+)(.*)', num.strip())
            if m:
                el['num'] = (m.group(1), float(m.group(2).replace('.', '').replace(',', '.')), m.group(3).rstrip(),
                             ',' in m.group(2))
            el['f_num'] = fonte('titulo', 250 * S, 'Bold')
            if rot.strip():
                itens = montar_texto(rot.strip(), W, H, S, tamanho=54, largura=0.7, y_centro=0.72)
                el['rot_num'] = [(Camada(np.asarray(im)), x, y) for im, x, y, i in itens]
        if 'titulo' in sp:
            tit, _, sub = sp['titulo'].partition('|')
            el['titulo'] = self._titulo(tit.strip(), sub.strip())
        if 'fonte' in sp:
            f = fonte('maquina', 32 * S)
            txt = 'FONTE: ' + sp['fonte']
            w = int(f.getlength(txt)) + 20
            im = Image.new('RGBA', (w, int(52 * S)), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((10, 6), txt, font=f, fill=(200, 196, 186, 255))
            # com legenda embaixo, o crédito sobe para o canto de cima
            y_f = int(36 * S) if 'legenda' in sp else int(H - 84 * S)
            el['fonte'] = Camada(np.asarray(im), int(56 * S), y_f)
        el['baixo'] = tem_texto_baixo
        el['seco'] = bool(sp.get('transicao'))
        cena.el = el

    def _guardar_img(self, el, im):
        bbox = im.split()[3].getbbox() or (0, 0, im.width, im.height)
        pad = int(4 * self.S)
        x0, y0 = max(0, bbox[0] - pad), max(0, bbox[1] - pad)
        x1, y1 = min(im.width, bbox[2] + pad), min(im.height, bbox[3] + pad)
        cr = np.asarray(im.crop((x0, y0, x1, y1))).astype(np.float32) / 255.0
        cr[..., :3] *= cr[..., 3:4]
        el['img'] = cr
        el['img_full'] = (im.width, im.height)
        el['img_off'] = (x0, y0)

    def _desenhar_video(self, base, el, dt, opac):
        """Clipe de vídeo line-art (fundo preto): o preto vira transparente, o traço fica branco."""
        cv2, W, H = self.cv2, self.W, self.H
        v = el['video']
        idx = min(max(0, int(dt * v['fps'])), max(0, v['n'] - 1))   # segura o último quadro
        if idx != v['ult']:
            if idx != v['ult'] + 1:
                v['cap'].set(cv2.CAP_PROP_POS_FRAMES, idx)
            ok, fr = v['cap'].read()
            if ok:
                f = min(W * v['esc'] / fr.shape[1], H * v['esc'] / fr.shape[0])
                fr = cv2.resize(fr, (int(fr.shape[1] * f), int(fr.shape[0] * f)), interpolation=cv2.INTER_AREA)
                rgb = cv2.cvtColor(fr, cv2.COLOR_BGR2RGB).astype(np.float32) / 255.0
                # fundo preto = transparente; mantém a cor original (ex.: janela acesa em âmbar)
                a = np.clip((rgb.max(axis=2) - 0.10) / 0.55, 0, 1)
                rgb = np.clip(rgb - 0.04, 0, 1) * (a[..., None] > 0)
                v['quadro'] = np.dstack([np.minimum(rgb, a[..., None]), a]).astype(np.float32)
            v['ult'] = idx
        if v['quadro'] is not None:
            cam = v['quadro']
            y_c = H * 0.42 if el.get('baixo') else H / 2
            compor(base, cam, int(W / 2 - cam.shape[1] / 2), int(y_c - cam.shape[0] / 2), opac * (1.0 if el.get('seco') else ease_out(dt / 0.6)))

    def _titulo(self, tit, sub):
        W, H, S = self.W, self.H, self.S
        f = fonte('titulo', 100 * S, 'Regular')
        letras = ' '.join(list(tit)) if len(tit) < 22 else tit
        tw = f.getlength(letras)
        im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        y = H * 0.44
        d.text(((W - tw) / 2, y), letras, font=f, fill=BRANCO + (255,))
        if sub:
            fs = fonte('italico', 60 * S, 'Medium')
            sw = fs.getlength(sub)
            d.text(((W - sw) / 2, y + 140 * S), sub, font=fs, fill=(185, 180, 170, 255))
        im = brilho(im, 12 * S, 0.5)
        linha_y = int(y + 128 * S)
        return Camada(np.asarray(im)), linha_y

    # ---- desenho de uma cena no instante t
    def desenhar(self, base, cena, t, opac_cena):
        W, H, S = self.W, self.H, self.S
        el, sp = cena.el, cena.spec
        dt = t - cena.ini
        dur = max(0.5, cena.fim - cena.ini)
        efeito = sp.get('efeito', 'zoom')
        if sp.get('transicao') and efeito == 'desenhar':
            efeito = 'zoom'      # transição seca: a imagem já entra inteira
        cv2 = self.cv2
        if 'img' in el:
            img = el['img']
            ch, cw = img.shape[:2]
            iw, ih = el['img_full']
            ox, oy = el['img_off']
            entra = ease_out(dt / 1.1)
            if efeito == 'zoom':
                esc = 1.07 - 0.07 * entra + 0.035 * (dt / dur)
            else:
                esc = 1.0 + 0.03 * (dt / dur)
            nw, nh = max(1, int(cw * esc)), max(1, int(ch * esc))
            cam = cv2.resize(img, (nw, nh), interpolation=cv2.INTER_LINEAR)
            alvo_y = H * 0.42 if el.get('baixo') else H / 2
            x = int(W / 2 - iw * esc / 2 + ox * esc)
            y = int(alvo_y - ih * esc / 2 + oy * esc)
            op = opac_cena * (ease_out(dt / 0.8) if efeito != 'desenhar' and not sp.get('transicao') else 1.0)
            if efeito == 'deslizar':
                x += int((1 - entra) * 120 * S)
            if efeito == 'desenhar':
                prog = ease_in_out(dt / 1.8)
                if prog < 1.0:
                    xs = np.arange(nw, dtype=np.float32)
                    borda = nw * 0.12
                    m = np.clip((prog * (nw + borda) - xs) / borda, 0, 1)[None, :, None]
                    cam = cam * m
            compor(base, cam, x, y, op)
        if 'video' in el:
            self._desenhar_video(base, el, dt, opac_cena)
        if 'faltando' in el:
            f = fonte('maquina', 34 * S)
            msg = f'[ IMAGEM FALTANDO: {el["faltando"]} ]'
            im = Image.new('RGBA', (int(f.getlength(msg)) + 20, int(60 * S)), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((10, 10), msg, font=f, fill=SANGUE + (255,))
            c = Camada(np.asarray(im))
            compor(base, c.px, int(W / 2 - im.width / 2), int(H * 0.2), opac_cena)
        if 'palavras' in el:
            n = el['n_pal']
            if el['sincroniza']:
                # distribui as palavras pelo tempo de fala de cada trecho
                tempos = []
                for (a, b), txt in zip(cena.tempos, cena.trechos_txt):
                    k = len(txt.split())
                    for j in range(k):
                        tempos.append(a + (b - a) * j / max(k, 1) - 0.08)
                tempos = (tempos + [tempos[-1]] * n)[:n] if tempos else [cena.ini] * n
            else:
                passo = min(0.28, (dur * 0.55) / max(n, 1))
                t0 = cena.ini + (0.35 if 'img' in el else 0.1)
                tempos = [t0 + i * passo for i in range(n)]
            for cam, x, y, i in el['palavras']:
                p = ease_out((t - tempos[i]) / 0.45)
                if p <= 0:
                    continue
                compor(base, cam.px, int(x), int(y + (1 - p) * 22 * S), p * opac_cena)
        if 'legenda' in el:
            p = ease_out((dt - 0.6) / 0.6)
            for cam, x, y in el['legenda']:
                compor(base, cam.px, int(x), int(y), p * opac_cena)
        if 'num' in el:
            pre, val, suf, virg = el['num']
            p = ease_out(dt / 1.6)
            v = val * p
            txt = f'{pre}{v:.1f}{suf}'.replace('.', ',') if virg else f'{pre}{int(round(v))}{suf}'
            f = el['f_num']
            w = f.getlength(txt)
            asc, desc = f.getmetrics()
            im = Image.new('RGBA', (int(w) + 80, asc + desc + 80), (0, 0, 0, 0))
            ImageDraw.Draw(im).text((40, 40), txt, font=f, fill=BRANCO + (255,))
            im = brilho(im, 18 * S, 0.6)
            c = Camada(np.asarray(im))
            compor(base, c.px, int(W / 2 - im.width / 2), int(H * 0.42 - im.height / 2), opac_cena * ease_out(dt / 0.5))
            if 'rot_num' in el:
                q = ease_out((dt - 1.0) / 0.7)
                for cam, x, y in el['rot_num']:
                    compor(base, cam.px, int(x), int(y + (1 - q) * 16 * S), q * opac_cena)
        if 'titulo' in el:
            cam, ly = el['titulo']
            p = ease_out(dt / 1.2)
            compor(base, cam.px, 0, int((1 - p) * 14 * S), p * opac_cena)
            # linha que se desenha
            lw = int(W * 0.42 * ease_in_out((dt - 0.3) / 1.4))
            if lw > 2:
                y = ly
                base[y:y + max(1, int(2 * S)), W // 2 - lw // 2:W // 2 + lw // 2] = \
                    base[y:y + max(1, int(2 * S)), W // 2 - lw // 2:W // 2 + lw // 2] * (1 - opac_cena) + np.array(BRANCO) / 255 * opac_cena
        if 'fonte' in el:
            c = el['fonte']
            compor(base, c.px, c.x, c.y, opac_cena * 0.85 * ease_out((dt - 0.8) / 0.6))

# ------------------------------------------------------------ montagem

def montar_cenas(trechos, story, duracao):
    cenas = []
    for i, tr in enumerate(trechos, 1):
        sp = dict(story.get(i, {'manter': True}))
        subs = sp.pop('_subs', [])
        if sp.get('manter') and cenas:
            c = cenas[-1]
            c.trechos_txt.append(tr['texto']); c.tempos.append((tr['inicio'], tr['fim']))
        else:
            ini = max(0.0, tr['inicio'] - 0.15)
            cenas.append(Cena(ini, None, sp, [tr['texto']], [(tr['inicio'], tr['fim'])]))
        # sub-cenas: o instante de cada troca é estimado pela posição da palavra no trecho
        txt, a, b = tr['texto'], tr['inicio'], tr['fim']
        for k, (ancora, ssp) in enumerate(subs, 1):
            pos = txt.lower().find(ancora.lower()) if ancora else -1
            frac = pos / max(1, len(txt)) if pos >= 0 else k / (len(subs) + 1)
            ts = a + (b - a) * frac
            cenas.append(Cena(max(0.0, ts - 0.15), None, dict(ssp), [txt], [(ts, b)]))
    cenas.sort(key=lambda c: c.ini)
    for a, b in zip(cenas, cenas[1:]):
        a.fim = b.ini
    if cenas:
        cenas[0].ini = 0.0
        cenas[-1].fim = duracao
    return cenas

TRANS = 0.45  # segundos de transição entre cenas

CHAMADAS = []   # tempos (s) em que a chamada de like/inscreva-se aparece
SELO = None     # {'img': array RGBA premultiplicado, 'niveis': [(t, nivel)]}

def nivel_selo(t):
    niv = SELO['niveis']
    atual = niv[0][1] if niv else 0.0
    ant, t_ant = atual, 0.0
    for tn, v in niv:
        if t < tn:
            break
        ant, atual, t_ant = atual, v, tn
    p = ease_in_out((t - t_ant) / 1.5)   # transição de 1,5 s
    return ant + (atual - ant) * p

def desenhar_selo(mont, base, t):
    nv = nivel_selo(t)
    if nv <= 0.01:
        return
    img = SELO['img']
    W, H, S = mont.W, mont.H, mont.S
    x = W - img.shape[1] - int(40 * S)
    y = int(36 * S)
    resp = 1.0 + 0.04 * math.sin(t * 1.7)          # leve pulsação
    compor(base, img, x, y, min(1.0, nv * resp))

TRANS_TIPOS = ('corte', 'whip', 'zoom', 'flash', 'glitch')

def efeito_transicao(base, t, cenas, W, H):
    """Efeitos de tela inteira em volta do instante de entrada das cenas com 'transicao:'."""
    cv2 = __import__('cv2')
    for c in cenas:
        tipo = c.spec.get('transicao')
        if tipo not in TRANS_TIPOS or tipo == 'corte':
            continue
        d = t - c.ini
        if tipo == 'whip' and -0.18 < d < 0.18:
            if d < 0:
                off = -W * 0.45 * ease_in_out((d + 0.18) / 0.18)
            else:
                off = W * 0.45 * (1 - ease_in_out(d / 0.18))
            k = int(90 * (1 - abs(d) / 0.18)) + 1
            M = np.float32([[1, 0, off], [0, 1, 0]])
            base[:] = cv2.warpAffine(base, M, (W, H), borderMode=cv2.BORDER_REFLECT)
            if k > 2:
                base[:] = cv2.blur(base, (k, 1))
        elif tipo == 'zoom' and 0 <= d < 0.35:
            sc = 1 + 0.14 * (1 - ease_out(d / 0.35))
            M = cv2.getRotationMatrix2D((W / 2, H / 2), 0, sc)
            base[:] = cv2.warpAffine(base, M, (W, H), borderMode=cv2.BORDER_REFLECT)
            if d < 0.08:
                base += 0.35 * (1 - d / 0.08)
        elif tipo == 'flash' and 0 <= d < 0.4:
            base += 0.9 * (1 - d / 0.4) ** 2
        elif tipo == 'glitch' and -0.08 < d < 0.28:
            rng = np.random.default_rng(int(t * 1000))
            k = int(rng.integers(8, 28))
            base[..., 0] = np.roll(base[..., 0], k, axis=1)
            base[..., 2] = np.roll(base[..., 2], -k, axis=1)
            for _ in range(6):
                y0 = int(rng.integers(0, H - 40)); hh = int(rng.integers(8, 60))
                base[y0:y0 + hh] = np.roll(base[y0:y0 + hh], int(rng.integers(-80, 80)), axis=1)

def quadro(mont, cenas, t, duracao, fade_final):
    base = mont.fundo(t)
    for i, c in enumerate(cenas):
        if t < c.ini - 0.01 or t > c.fim + TRANS:
            continue
        if c.spec.get('preto'):
            continue
        prox = cenas[i + 1] if i + 1 < len(cenas) else None
        seca = prox is not None and prox.spec.get('transicao') in TRANS_TIPOS
        if seca and t >= c.fim:
            continue          # transição seca: a cena anterior some na hora
        op = 1.0
        if t > c.fim:
            op = 1 - ease_in_out((t - c.fim) / TRANS)
        mont.desenhar(base, c, t, op)
    efeito_transicao(base, t, cenas, mont.W, mont.H)
    if SELO:
        desenhar_selo(mont, base, t)
    fade = 1.0
    if t < 0.6:
        fade = ease_out(t / 0.6)
    if fade_final and t > duracao - 1.5:
        fade = min(fade, max(0.0, (duracao - t) / 1.5))
    if CHAMADAS:
        if not hasattr(mont, 'chamada'):
            from chamada import Chamada
            mont.chamada = Chamada(mont.W, mont.H, mont.S, fonte, BRANCO, SANGUE)
        for tc in CHAMADAS:
            mont.chamada.desenhar(base, t - tc, compor)
    return mont.finalizar(base, t, fade)

CORES_DESTAQUE = {'vermelho': (190, 42, 36), 'ambar': (232, 160, 48), 'azul': (70, 140, 230)}

def preparar_tudo(a):
    global SANGUE, CHAMADAS, SELO
    CHAMADAS = [float(x) for x in (getattr(a, 'chamadas', '') or '').split(',') if x.strip()]
    d = getattr(a, 'destaque', None) or 'vermelho'
    if d in CORES_DESTAQUE:
        SANGUE = CORES_DESTAQUE[d]
    elif re.fullmatch(r'#?[0-9a-fA-F]{6}', d):
        h = d.lstrip('#'); SANGUE = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    texto = texto_da_parte(a.texto, a.parte)
    cache = os.path.splitext(a.audio)[0] + '.alinhamento.json'
    chave = hashlib.md5((texto + str(os.path.getsize(a.audio))).encode()).hexdigest()
    al = None
    if os.path.exists(cache):
        try:
            al = json.load(open(cache, encoding='utf-8'))
            if al.get('chave') != chave:
                al = None
        except Exception:
            al = None
    if al is None:
        print('Sincronizando texto com o áudio...')
        al = alinhar(a.audio, texto)
        al['chave'] = chave
        try:
            json.dump(al, open(cache, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        except OSError:
            pass
    story = ler_storyboard(a.storyboard)
    H = int(a.res)
    W = int(round(H * 16 / 9 / 2) * 2)
    mont = Montador(W, H, a.fps, a.imagens, a.fundo)
    if getattr(a, 'tensao', ''):
        pts = json.load(open(a.tensao, encoding='utf-8'))
        mont.tensao_pts = (np.array([p[0] for p in pts], np.float32) - a.tensao_offset, np.array([p[1] for p in pts], np.float32))
    cenas = montar_cenas(al['trechos'], story, al['duracao'])
    for c in cenas:
        mont.preparar(c)
    SELO = None
    if getattr(a, 'selo', None):
        cam = achar_arquivo(os.path.join(a.imagens, a.selo)) or achar_arquivo(a.selo)
        if cam:
            im = carregar_lineart(cam, W, H, 0.26)
            bb = im.split()[3].getbbox()
            if bb:
                im = im.crop(bb)
            # tinge com a cor de destaque e dá brilho
            arr = np.asarray(im).astype(np.float32) / 255.0
            cor = np.array(SANGUE, np.float32) / 255.0
            rgb = np.clip(arr[..., :3] * 0.6 + cor * 1.0, 0, 1)
            im = Image.fromarray((np.dstack([rgb, arr[..., 3:4]]) * 255).astype(np.uint8), 'RGBA')
            pad = int(30 * mont.S)
            tela = Image.new('RGBA', (im.width + 2 * pad, im.height + 2 * pad), (0, 0, 0, 0))
            tela.paste(im, (pad, pad))
            tela = brilho(tela, 14 * mont.S, 0.8, cor=tuple(SANGUE))
            px = np.asarray(tela).astype(np.float32) / 255.0
            px[..., :3] *= px[..., 3:4]
            niveis = sorted((c.ini, float(c.spec['selo'])) for c in cenas if 'selo' in c.spec)
            SELO = {'img': px, 'niveis': niveis or [(0.0, 1.0)]}
    return mont, cenas, al

def cmd_render(a):
    mont, cenas, al = preparar_tudo(a)
    dur = al['duracao']
    t0 = float(a.de or 0)
    t1 = float(a.ate) if a.ate else dur
    n = int((t1 - t0) * a.fps)
    print(f'{len(cenas)} cenas | {n} quadros | {mont.W}x{mont.H} @ {a.fps}fps')
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24',
           '-s', f'{mont.W}x{mont.H}', '-r', str(a.fps), '-i', '-']
    if not a.sem_audio:
        cmd += ['-ss', str(t0), '-t', str(t1 - t0), '-i', a.audio]
    cmd += ['-c:v', 'libx264', '-preset', a.preset, '-crf', '19', '-pix_fmt', 'yuv420p']
    if not a.sem_audio:
        cmd += ['-c:a', 'aac', '-b:a', '192k', '-shortest']
    cmd += ['-movflags', '+faststart', a.saida]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    import time
    ini = time.time()
    for k in range(n):
        t = t0 + k / a.fps
        p.stdin.write(quadro(mont, cenas, t, dur, a.fade_final).tobytes())
        if k % (a.fps * 10) == 0 and k:
            v = k / (time.time() - ini)
            print(f'  {t:7.1f}s / {t1:.0f}s  ({v:.1f} quadros/s, faltam ~{(n - k) / v / 60:.1f} min)', flush=True)
    p.stdin.close()
    p.wait()
    try:
        json.dump([{'t': round(c.ini, 3), 'tipo': c.spec['transicao']} for c in cenas if c.spec.get('transicao') in TRANS_TIPOS],
                  open(os.path.splitext(a.audio)[0] + '.transicoes.json', 'w', encoding='utf-8'))
    except OSError:
        pass
    print('Pronto:', a.saida)

def cmd_quadros(a):
    mont, cenas, al = preparar_tudo(a)
    os.makedirs(a.saida, exist_ok=True)
    for t in [float(x) for x in a.tempos.split(',')]:
        Image.fromarray(quadro(mont, cenas, t, al['duracao'], a.fade_final)).save(
            os.path.join(a.saida, f'quadro_{t:07.2f}.png'))
    print('Quadros salvos em', a.saida)

def cmd_juntar(a):
    """Junta pedaços de vídeo (sem áudio) e coloca o áudio inteiro por cima."""
    import tempfile
    lista = os.path.join(tempfile.gettempdir(), 'motion_lista.txt')
    with open(lista, 'w', encoding='utf-8') as f:
        for v in a.videos:
            f.write("file '" + os.path.abspath(v).replace("'", "'\\''") + "'\n")
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', lista]
    for au in a.audio:
        cmd += ['-i', au]
    n = len(a.audio)
    if n > 1:
        ent = ''.join(f'[{i + 1}:a]' for i in range(n))
        cmd += ['-filter_complex', f'{ent}concat=n={n}:v=0:a=1[a]', '-map', '0:v', '-map', '[a]']
    else:
        cmd += ['-map', '0:v', '-map', '1:a']
    cmd += ['-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', a.saida]
    subprocess.run(cmd, check=True)
    try:
        os.remove(lista)
    except OSError:
        pass
    print('Pronto:', a.saida)

def cmd_storyboard(a):
    texto = texto_da_parte(a.texto, a.parte)
    gerar_storyboard(trechos_do_texto(texto), a.saida)
    print('Storyboard criado:', a.saida)

def main():
    ap = argparse.ArgumentParser(description='Motor de Motion')
    sub = ap.add_subparsers(dest='cmd', required=True)
    s = sub.add_parser('storyboard')
    s.add_argument('--texto', required=True); s.add_argument('--parte', type=int)
    s.add_argument('--saida', required=True)
    for nome in ('render', 'quadros'):
        r = sub.add_parser(nome)
        r.add_argument('--audio', required=True)
        r.add_argument('--texto', required=True); r.add_argument('--parte', type=int)
        r.add_argument('--storyboard', required=True)
        r.add_argument('--imagens', default='.')
        r.add_argument('--fundo', default=FUNDO_PADRAO)
        r.add_argument('--saida', required=True)
        r.add_argument('--res', default=1080, type=int)
        r.add_argument('--fps', default=30, type=int)
        r.add_argument('--preset', default='veryfast')
        r.add_argument('--de'); r.add_argument('--ate')
        r.add_argument('--fade-final', action='store_true')
        r.add_argument('--sem-audio', action='store_true')
        r.add_argument('--destaque', default='vermelho', help='cor dos destaques: vermelho, ambar, azul ou #RRGGBB')
        r.add_argument('--chamadas', default='', help='segundos (nesta parte) em que entra o like/inscreva-se, ex.: 120,80')
        r.add_argument('--selo', default='', help='imagem fixa no canto superior direito (brilho controlado por "selo:" no storyboard)')
        r.add_argument('--tensao', default='', help='json com a curva de tensão [[t, 0..1], ...] (tempos do vídeo inteiro): o fundo se mexe de acordo')
        r.add_argument('--tensao-offset', type=float, default=0.0, help='onde esta parte começa no vídeo inteiro (s)')
        if nome == 'quadros':
            r.add_argument('--tempos', required=True)
    j = sub.add_parser('juntar')
    j.add_argument('--videos', nargs='+', required=True)
    j.add_argument('--audio', nargs='+', required=True)
    j.add_argument('--saida', required=True)
    a = ap.parse_args()
    {'storyboard': cmd_storyboard, 'render': cmd_render, 'quadros': cmd_quadros, 'juntar': cmd_juntar}[a.cmd](a)

if __name__ == '__main__':
    main()

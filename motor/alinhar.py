"""Alinha trechos do texto do ElevenLabs (separados por <break>) com o tempo no áudio.
Não usa modelo de transcrição: detecta pausas no áudio e escolhe, por programação
dinâmica, as pausas que melhor batem com o tamanho de cada trecho."""
import re, subprocess, json, sys

def trechos_do_texto(texto):
    """Divide o texto nos <break>. Devolve lista de dicts {texto, pausa}."""
    texto = re.sub(r'^#.*$', '', texto, flags=re.M)
    partes = re.split(r'<break time="([\d.]+)s"\s*/>', texto)
    out = []
    for i in range(0, len(partes), 2):
        t = ' '.join(partes[i].split())
        pausa = float(partes[i + 1]) if i + 1 < len(partes) else 0.0
        if t:
            out.append({'texto': t, 'pausa': pausa})
        elif out:
            out[-1]['pausa'] += pausa
    return out

def duracao(audio):
    r = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration',
                        '-of', 'csv=p=0', audio], capture_output=True, text=True)
    return float(r.stdout.strip())

def silencios(audio, db=-32, d=0.22):
    r = subprocess.run(['ffmpeg', '-hide_banner', '-i', audio, '-af',
                        f'silencedetect=noise={db}dB:d={d}', '-f', 'null', '-'],
                       capture_output=True, text=True)
    s, out = None, []
    for ln in r.stderr.splitlines():
        m = re.search(r'silence_start: ([\d.]+)', ln)
        if m: s = float(m.group(1))
        m = re.search(r'silence_end: ([\d.]+)', ln)
        if m and s is not None:
            out.append((s, float(m.group(1)))); s = None
    return out

def peso(t):
    # tempo de fala aproximado ~ letras + um pouco por pontuação
    return len(re.sub(r'[^\wÀ-ú]', '', t)) + 4 * len(re.findall(r'[.,:;?!…]', t))

def _proporcional(tr, pesos, ini, fim, dur):
    """Plano B: divide o tempo pelo tamanho de cada trecho (quando não há pausas suficientes)."""
    tot = sum(pesos) + 1e-9
    t = ini
    for x, p in zip(tr, pesos):
        d = (fim - ini) * p / tot
        x['inicio'], x['fim'] = round(t, 2), round(t + d, 2)
        t += d
    return {'audio': None, 'duracao': round(dur, 2), 'trechos': tr, 'aviso': 'alinhamento proporcional'}

def alinhar(audio, texto):
    tr = trechos_do_texto(texto)
    dur = duracao(audio)
    sil = silencios(audio)
    ini_fala = sil[0][1] if sil and sil[0][0] < 0.05 else 0.0
    fim_fala = sil[-1][0] if sil and sil[-1][1] > dur - 0.05 else dur
    if fim_fala - ini_fala < 1.0:  # áudio sem fala detectável: usa o arquivo todo
        ini_fala, fim_fala = 0.0, dur
    cands = [(a, b) for a, b in sil if a > ini_fala + 0.1 and b < fim_fala - 0.1]
    n = len(tr)
    pesos = [peso(x['texto']) for x in tr]
    # taxa: tempo de fala / peso total (descontando pausas previstas)
    pausas_prev = sum(x['pausa'] for x in tr[:-1])
    taxa = max(0.01, (fim_fala - ini_fala - pausas_prev) / sum(pesos))
    INF = float('inf')
    m = len(cands)
    # dp[k][j] = custo de ter o fim do trecho k na pausa j
    dp = [[INF] * m for _ in range(n)]
    pai = [[-1] * m for _ in range(n)]
    def custo_seg(t0, t1, k):
        prev = taxa * pesos[k]
        return (t1 - t0 - prev) ** 2 / (prev + 1.0)
    def bonus(j, k):
        a, b = cands[j]
        ln = b - a
        alvo = tr[k]['pausa'] or 0.6
        return -2.0 * min(ln, 1.5) + 0.6 * abs(ln - alvo)
    for j in range(m):
        dp[0][j] = custo_seg(ini_fala, cands[j][0], 0) + bonus(j, 0)
    for k in range(1, n - 1):
        best, bi = INF, -1
        for j in range(m):
            # varredura simples O(m^2) — m é pequeno
            for i in range(j):
                c = dp[k - 1][i]
                if c == INF: continue
                c += custo_seg(cands[i][1], cands[j][0], k) + bonus(j, k)
                if c < dp[k][j]:
                    dp[k][j] = c; pai[k][j] = i
    # último trecho termina no fim da fala
    if n > 1 and m < n - 1:
        return _proporcional(tr, pesos, ini_fala, fim_fala, dur)
    if n == 1:
        cortes = []
    else:
        melhor, bj = INF, -1
        for j in range(m):
            if dp[n - 2][j] == INF: continue
            c = dp[n - 2][j] + custo_seg(cands[j][1], fim_fala, n - 1)
            if c < melhor: melhor, bj = c, j
        if bj < 0:
            return _proporcional(tr, pesos, ini_fala, fim_fala, dur)
        cortes = [bj]
        for k in range(n - 2, 0, -1):
            cortes.append(pai[k][cortes[-1]])
        cortes.reverse()
    t0 = ini_fala
    for k in range(n):
        if k < n - 1:
            a, b = cands[cortes[k]]
            tr[k]['inicio'], tr[k]['fim'] = round(t0, 2), round(a, 2)
            t0 = b
        else:
            tr[k]['inicio'], tr[k]['fim'] = round(t0, 2), round(fim_fala, 2)
    return {'audio': audio, 'duracao': round(dur, 2), 'trechos': tr}


if __name__ == '__main__':
    audio, txt = sys.argv[1], sys.argv[2]
    res = alinhar(audio, open(txt, encoding='utf-8').read())
    print(json.dumps(res, ensure_ascii=False, indent=1))

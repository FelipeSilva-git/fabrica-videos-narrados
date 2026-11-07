"""Busca e baixa imagens REAIS do Wikimedia Commons, só com licença que permite uso em canal monetizado,
e escreve o CREDITOS.md (arquivo, original, licença, autor, tamanho, página).

Uso:
  python3 commons.py buscar <pasta_episodio> "termo 1" "termo 2" ...      -> <pasta>/commons.json
  (abra o commons.json, escolha as imagens e liste os títulos num arquivo selecao.txt, um por linha)
  python3 commons.py baixar <pasta_episodio> selecao.txt                  -> <pasta>/imagens-reais/ + CREDITOS.md

Licenças aceitas: domínio público, CC0, CC BY, CC BY-SA. Recusadas: qualquer NC (não comercial) ou ND (sem derivados).
O Commons limita acessos (erro 429): o script espera entre pedidos e usa tamanhos de miniatura padrão (1280 px).
"""
import json, sys, os, re, time, urllib.parse, urllib.request

UA = {'User-Agent': 'FabricaVideosNarrados/1.0 (pesquisa de imagens com licença livre)'}
API = 'https://commons.wikimedia.org/w/api.php'

def licenca_ok(lic):
    l = lic.lower()
    if 'nc' in re.split(r'[\s\-]+', l) or 'nd' in re.split(r'[\s\-]+', l) or 'noncommercial' in l or 'noderiv' in l:
        return False
    return any(x in l for x in ('public domain', 'cc0', 'cc by', 'pd', 'attribution'))

def get(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))

def buscar(pasta, termos):
    res = {}
    for q in termos:
        url = (API + '?action=query&generator=search&gsrnamespace=6&gsrlimit=30&format=json&prop=imageinfo'
               '&iiprop=extmetadata|size|url&iiurlwidth=1280&iiextmetadatafilter=LicenseShortName|Artist|ImageDescription'
               '&gsrsearch=' + urllib.parse.quote(q))
        try:
            d = get(url)
        except Exception as e:
            print('erro', q, e); time.sleep(10); continue
        for p in d.get('query', {}).get('pages', {}).values():
            ii = p['imageinfo'][0]; m = ii.get('extmetadata', {})
            limpa = lambda k: re.sub('<[^>]+>', '', m.get(k, {}).get('value', '')).strip()
            lic = limpa('LicenseShortName')
            if not licenca_ok(lic) or p['title'] in res:
                continue
            res[p['title']] = {'busca': q, 'licenca': lic, 'autor': limpa('Artist')[:80], 'descricao': limpa('ImageDescription')[:220],
                               'tam': f"{ii['width']}x{ii['height']}", 'url': ii.get('thumburl') or ii['url'], 'pagina': ii.get('descriptionurl', '')}
        time.sleep(2)
    json.dump(res, open(os.path.join(pasta, 'commons.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    for t, v in res.items():
        print(f"{v['licenca'][:12]:12} {v['tam']:>10}  {t[5:90]}  ||  {v['descricao'][:80]}")
    print(len(res), 'imagens com licença aceita ->', os.path.join(pasta, 'commons.json'))

def baixar(pasta, selecao):
    d = json.load(open(os.path.join(pasta, 'commons.json'), encoding='utf-8'))
    titulos = [l.strip() for l in open(selecao, encoding='utf-8') if l.strip()]
    os.makedirs(os.path.join(pasta, 'imagens-reais'), exist_ok=True)
    linhas = []
    for n, t in enumerate(titulos, 1):
        t = t if t.startswith('File:') else 'File:' + t
        v = d.get(t)
        if not v:
            print('não está no commons.json:', t); continue
        nome = f'r{n:02d}-' + re.sub(r'[^\w\-]+', '_', t[5:].rsplit('.', 1)[0])[:50] + '.jpg'
        for tent in range(3):
            try:
                dados = urllib.request.urlopen(urllib.request.Request(v['url'], headers=UA), timeout=60).read()
                open(os.path.join(pasta, 'imagens-reais', nome), 'wb').write(dados); break
            except Exception as e:
                print('tentando de novo', t, e); time.sleep(15 * (tent + 1))
        else:
            continue
        linhas.append(f"| `{nome}` | {t[5:]} | {v['licenca']} | {v['autor']} | {v['tam']} | {v['pagina']} |")
        time.sleep(3)
    open(os.path.join(pasta, 'imagens-reais', 'CREDITOS.md'), 'w', encoding='utf-8').write(
        '# Imagens reais: licenças e créditos\n\n| Arquivo | Original | Licença | Autor | Tamanho | Página |\n| --- | --- | --- | --- | --- | --- |\n'
        + '\n'.join(linhas) + '\n')
    print(len(linhas), 'baixadas')

if __name__ == '__main__':
    modo, pasta = sys.argv[1], sys.argv[2]
    buscar(pasta, sys.argv[3:]) if modo == 'buscar' else baixar(pasta, sys.argv[3])

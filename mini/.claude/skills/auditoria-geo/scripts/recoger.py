# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Recoge los datos GEO de una web y los guarda en datos/<dominio>.json.

Solo recoge hechos (robots.txt, llms.txt, sitemap, título, encabezados,
JSON-LD y párrafos). No puntúa nada: eso lo hacen los subagentes.

Uso: uv run recoger.py https://ejemplo.com
"""

import json
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlparse
from urllib.request import Request, urlopen

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"


def bajar(url: str) -> tuple[int, str]:
    """Devuelve (código HTTP, texto) de una URL; 0 si no hay conexión."""
    try:
        with urlopen(Request(url, headers={"User-Agent": UA}), timeout=20) as r:
            return r.status, r.read().decode("utf-8", "replace")
    except HTTPError as e:
        return e.code, ""
    except URLError:
        return 0, ""


class Pagina(HTMLParser):
    """Extrae título, meta descripción, h1/h2, JSON-LD y párrafos de un HTML."""

    def __init__(self):
        super().__init__()
        self.titulo, self.descripcion = "", ""
        self.h1, self.h2, self.jsonld, self.parrafos = [], [], [], []
        self._tag, self._buf, self._ld = None, "", False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta" and a.get("name", "").lower() == "description":
            self.descripcion = a.get("content", "")
        if tag == "script" and a.get("type") == "application/ld+json":
            self._ld, self._buf = True, ""
        if tag in ("title", "h1", "h2", "p"):
            self._tag, self._buf = tag, ""

    def handle_data(self, data):
        if self._ld or self._tag:
            self._buf += data

    def handle_endtag(self, tag):
        if tag == "script" and self._ld:
            self._ld = False
            try:
                self.jsonld.append(json.loads(self._buf))
            except json.JSONDecodeError:
                self.jsonld.append({"error": "JSON-LD mal formado"})
        elif tag == self._tag:
            texto = " ".join(self._buf.split())
            if tag == "title":
                self.titulo = texto
            elif tag == "p" and len(texto.split()) >= 25:
                self.parrafos.append(texto)
            elif tag in ("h1", "h2") and texto:
                getattr(self, tag).append(texto)
            self._tag = None


def main(url: str) -> None:
    raiz = f"{urlparse(url).scheme}://{urlparse(url).netloc}"
    estado, html = bajar(url)
    pagina = Pagina()
    pagina.feed(html)
    robots = bajar(f"{raiz}/robots.txt")
    llms = bajar(f"{raiz}/llms.txt")
    sitemap = bajar(f"{raiz}/sitemap.xml")

    datos = {
        "url": url,
        "estado_http": estado,
        "titulo": pagina.titulo,
        "meta_descripcion": pagina.descripcion,
        "h1": pagina.h1,
        "h2": pagina.h2[:20],
        "palabras_en_parrafos": sum(len(p.split()) for p in pagina.parrafos),
        "parrafos": pagina.parrafos[:15],
        "jsonld": pagina.jsonld,
        "robots_txt": {"estado": robots[0], "texto": robots[1][:4000]},
        "llms_txt": {"estado": llms[0], "inicio": llms[1][:1500]},
        "sitemap_xml": {"estado": sitemap[0], "urls": sitemap[1].count("<loc>")},
    }
    salida = Path("datos") / f"{urlparse(url).netloc}.json"
    salida.parent.mkdir(exist_ok=True)
    salida.write_text(json.dumps(datos, ensure_ascii=False, indent=2), encoding="utf-8")
    print(salida)


if __name__ == "__main__":
    main(sys.argv[1])

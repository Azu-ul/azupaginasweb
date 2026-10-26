#!/usr/bin/env python3
"""Genera el blog de Azu Páginas Web.

Uso:  python3 build.py
Lee los textos de content/*.html y crea:
  blog/index.html
  blog/<slug>/index.html   (uno por artículo)
  sitemap.xml
Para agregar un artículo nuevo: escribí content/<slug>.html, sumalo a POSTS y volvé a correr el script.
"""
import html
import json
import os

SITE = "https://azupaginasweb.com"
OG_IMAGE = SITE + "/assets/og-image.png"
LOGO_URL = SITE + "/assets/logo_cyan.png"
IG = "https://instagram.com/azupaginasweb"
# Las dos tipografías en un solo pedido (Gelasio y Comic Relief, peso 400)
FONTS_URL = "https://fonts.googleapis.com/css2?family=Comic+Relief&family=Gelasio&display=swap"
PUBLISHED = "2026-10-25"
MODIFIED = "2026-10-25"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio",
         "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

POSTS = [
    {
        "slug": "como-hacer-una-pagina-web",
        "short": "Cómo hacer una página web: guía paso a paso",
        "h1": "Cómo hacer una página web para tu emprendimiento: guía paso a paso",
        "desc": "Cómo hacer una página web para tu emprendimiento en 7 pasos: dominio, hosting, estructura, textos, diseño y publicación. Simple y sin tecnicismos.",
        "excerpt": "Los 7 pasos para tener tu web online, sin saber programar: objetivo, dominio, hosting, estructura, textos, diseño y publicación.",
        "tag": "GUÍA",
        "mins": 6,
        "faqs": [
            ("¿Necesito saber programar para hacer una página web?",
             "No. Podés usar un constructor con plantillas o contratar a alguien que la haga por vos. Programar te da más libertad, pero no es obligatorio para empezar."),
            ("¿Cuánto tarda en estar lista una página web?",
             "Depende de cuánto contenido tengas preparado y de lo compleja que sea. Con textos e imágenes listos, una landing page sencilla se resuelve mucho más rápido que un sitio con muchas funciones."),
            ("¿Puedo hacer mi página web gratis?",
             "Hay constructores con planes gratuitos, pero suelen tener límites y no te dejan usar un dominio propio. Para un negocio, conviene tener dominio propio y un hosting confiable."),
        ],
    },
    {
        "slug": "landing-page-que-es",
        "short": "Landing page: qué es y cuándo te conviene",
        "h1": "Landing page: qué es, para qué sirve y cuándo te conviene",
        "desc": "Qué es una landing page, en qué se diferencia de una web completa y cuándo conviene para tu emprendimiento. Elementos clave y errores comunes.",
        "excerpt": "Qué es una landing page, en qué se diferencia de una web completa y cuándo te conviene para tu emprendimiento.",
        "tag": "CONCEPTOS",
        "mins": 4,
        "faqs": [
            ("¿Una landing page y una página web son lo mismo?",
             "Una landing page es un tipo de página web: una sola página dividida en secciones. Una web completa suele tener varias páginas separadas."),
            ("¿Una landing page sirve para vender?",
             "Sí, sirve para llevar a la persona hacia una acción concreta, como escribirte por WhatsApp o pedir un presupuesto. Para una tienda con muchos productos y pagos online suele hacer falta una solución más completa."),
        ],
    },
    {
        "slug": "pagina-web-o-instagram",
        "short": "¿Página web o Instagram? Qué te conviene",
        "h1": "¿Página web o solo Instagram? Qué le conviene a un negocio en Mar del Plata",
        "desc": "¿Alcanza con Instagram o necesitás una página web? Ventajas de cada una y cómo combinarlas para tu negocio o emprendimiento en Mar del Plata.",
        "excerpt": "Instagram y una web propia no compiten: cumplen roles distintos. Cuándo conviene cada una y cómo combinarlas.",
        "tag": "NEGOCIOS",
        "mins": 4,
        "faqs": [
            ("¿Puedo tener solo Instagram para mi negocio?",
             "Podés empezar así, pero dependés de una plataforma que no controlás y tu información queda dispersa. Una web propia te da un lugar estable y ordenado."),
            ("¿Una página web reemplaza a Instagram?",
             "No, se complementan. Instagram sirve para mostrarte y mantener comunidad; la web, para ordenar la información y recibir consultas."),
        ],
    },
    {
        "slug": "cuanto-cuesta-una-pagina-web-mar-del-plata",
        "short": "Cuánto cuesta una página web en Mar del Plata",
        "h1": "Cuánto cuesta una página web en Mar del Plata (precios 2026)",
        "desc": "Precios de páginas web en Mar del Plata en 2026: qué incluye cada plan, cuánto se paga de dominio, hosting y mantenimiento, y qué preguntar antes de contratar.",
        "excerpt": "Precios de mis planes, qué se paga aparte (dominio, mantenimiento) y qué preguntar antes de contratar.",
        "tag": "PRECIOS",
        "mins": 4,
        "faqs": [
            ("¿El hosting está incluido en el precio de la página web?",
             "En mis planes, sí. En otros servicios puede ser un costo aparte y recurrente, por eso conviene preguntarlo antes de contratar."),
            ("¿El dominio está incluido?",
             "El dominio se abona aparte y queda siempre a tu nombre."),
            ("¿Cuánto cuesta el mantenimiento de la web?",
             "Un cambio puntual cuesta $7.000 ARS y el mantenimiento mensual $20.000 ARS, con hasta 3 cambios de textos o imágenes por mes, copias de seguridad y soporte por WhatsApp."),
        ],
    },
    {
        "slug": "desarrollador-web-mar-del-plata",
        "short": "Desarrollador web en Mar del Plata: cómo elegir",
        "h1": "Desarrollador web en Mar del Plata: cómo elegir a quién contratar",
        "desc": "Cómo elegir un desarrollador o desarrolladora web en Mar del Plata: freelance o agencia, qué preguntar, qué mirar en el portfolio y señales de alerta.",
        "excerpt": "Freelance, agencia o hacerlo vos: qué mirar antes de contratar, qué preguntar y qué señales de alerta evitar.",
        "tag": "CONTRATAR",
        "mins": 5,
        "faqs": [
            ("¿Es necesario que el desarrollador web sea de Mar del Plata?",
             "No es indispensable, porque el trabajo se puede hacer a distancia, pero ayuda a la comunicación y a conocer el mercado local."),
            ("¿A nombre de quién tiene que estar el dominio?",
             "A tu nombre. Así controlás tu web y podés cambiar de proveedor si lo necesitás."),
            ("¿Alguien puede garantizar el primer lugar en Google?",
             "No. Nadie puede asegurar una posición. Se puede optimizar tu web para mejorar sus chances, pero el resultado depende de muchos factores."),
        ],
    },
]

BLOG_TITLE = "Blog de páginas web para emprendimientos en Mar del Plata | Azu Páginas Web"
BLOG_DESC = "Guías simples para emprendedores: cómo hacer una página web, cuánto cuesta, qué es una landing page y cómo elegir a quién contratar en Mar del Plata."


def esc(s):
    return html.escape(s, quote=True)


def fecha_larga(iso):
    y, m, d = iso.split("-")
    return "%d de %s de %s" % (int(d), MESES[int(m) - 1], y)


def ld(data):
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=2) + "\n    </script>"


def head(title, desc, canonical, root, og_type, jsonld):
    return f"""<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{esc(title)}</title>
    <meta name="description" content="{esc(desc)}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="{canonical}">
    <meta property="og:type" content="{og_type}">
    <meta property="og:site_name" content="Azu Páginas Web">
    <meta property="og:locale" content="es_AR">
    <meta property="og:url" content="{canonical}">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(desc)}">
    <meta property="og:image" content="{OG_IMAGE}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{OG_IMAGE}">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link rel="stylesheet" href="{FONTS_URL}" media="print" onload="this.media='all'">
    <noscript><link rel="stylesheet" href="{FONTS_URL}"></noscript>
    <link rel="stylesheet" href="{root}styles.css">
    <link rel="stylesheet" href="{root}blog.css">
    <link rel="icon" type="image/x-icon" href="{root}assets/favicon.ico">
    {ld(jsonld)}
</head>
"""


def nav(root, blog):
    return f"""    <header class="nav">
        <div class="nav__inner">
            <a class="nav__brand" href="{root}" aria-label="Azu Páginas Web, inicio">
                <span class="logo-slot logo-slot--sm has-img"><img src="{root}assets/logo_crema.png" width="800" height="800" decoding="async" alt="Logo de Azu Páginas Web"></span>
                <span class="nav__name">Azu Páginas Web</span>
            </a>
            <button class="nav__toggle" type="button" aria-expanded="false" aria-controls="menu">Menú</button>
            <nav id="menu" class="nav__links">
                <a href="{root}#planes">Planes</a>
                <a href="{root}#sobre-mi">Sobre mí</a>
                <a href="{root}#proyectos">Proyectos</a>
                <a href="{blog}">Blog</a>
                <a href="{root}#contacto">Contacto</a>
                <a class="nav__ig" href="{IG}" target="_blank" rel="noopener">@azupaginasweb</a>
            </nav>
        </div>
    </header>
"""


def footer(root, blog):
    return f"""    <footer class="footer">
        <div class="container footer__inner">
            <span class="logo-slot logo-slot--footer has-img"><img src="{root}assets/logo_cyan.png" width="800" height="800" loading="lazy" decoding="async" alt="Logo de Azu Páginas Web"></span>
            <p>Azu Páginas Web · <a href="{IG}" target="_blank" rel="noopener">@azupaginasweb</a> · <a href="{blog}">Blog</a></p>
            <p>© <span id="year"></span> · Hecho con cariño en Mar del Plata ♡</p>
        </div>
    </footer>

    <script src="{root}blog.js" defer></script>
</body>

</html>
"""


def card(p, blog, tag="h2"):
    return f"""                <a class="post-card" href="{blog}{p['slug']}/">
                    <p class="post-card__tag">{esc(p['tag'])} · {p['mins']} MIN</p>
                    <{tag}>{esc(p['h1'])}</{tag}>
                    <p>{esc(p['excerpt'])}</p>
                    <span class="post-card__more">Leer artículo</span>
                </a>"""


def build_post(i, p):
    root, blog = "../../", "../"
    url = f"{SITE}/blog/{p['slug']}/"
    title = f"{p['short']} | Azu Páginas Web"
    with open(f"content/{p['slug']}.html", encoding="utf-8") as f:
        body = f.read().replace("{{ROOT}}", root).replace("{{BLOG}}", blog)

    faq_html = ""
    faq_ld = []
    for q, a in p["faqs"]:
        faq_html += f"            <h3>{esc(q)}</h3>\n            <p>{esc(a)}</p>\n"
        faq_ld.append({"@type": "Question", "name": q,
                       "acceptedAnswer": {"@type": "Answer", "text": a}})

    otros = [POSTS[(i + k) % len(POSTS)] for k in (1, 2)]
    related = "\n".join(card(o, blog, "h3") for o in otros)

    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "@id": url + "#articulo",
                "headline": p["h1"],
                "description": p["desc"],
                "inLanguage": "es-AR",
                "datePublished": PUBLISHED,
                "dateModified": MODIFIED,
                "image": OG_IMAGE,
                "mainEntityOfPage": url,
                "author": {"@type": "Person", "name": "Azu", "url": SITE + "/"},
                "publisher": {
                    "@type": "Organization",
                    "name": "Azu Páginas Web",
                    "url": SITE + "/",
                    "logo": {"@type": "ImageObject", "url": LOGO_URL},
                },
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE + "/blog/"},
                    {"@type": "ListItem", "position": 3, "name": p["h1"], "item": url},
                ],
            },
            {"@type": "FAQPage", "mainEntity": faq_ld},
        ],
    }

    out = head(title, p["desc"], url, root, "article", jsonld)
    out += f"""
<body data-root="{root}">

{nav(root, blog)}
    <main class="blog">
        <article>
            <header class="post-head">
                <div class="narrow">
                    <nav class="crumbs" aria-label="Migas de pan">
                        <a href="{root}">Inicio</a><span aria-hidden="true">/</span><a href="{blog}">Blog</a>
                    </nav>
                    <p class="eyebrow">{esc(p['tag'])}</p>
                    <h1>{esc(p['h1'])}</h1>
                    <p class="post-meta">Por Azu · <time datetime="{PUBLISHED}">{fecha_larga(PUBLISHED)}</time> · {p['mins']} min de lectura</p>
                </div>
            </header>

            <div class="narrow post-body">
{body}
                <section class="post-faq" aria-labelledby="faq-titulo">
                    <h2 id="faq-titulo">Preguntas frecuentes</h2>
{faq_html}                </section>

                <aside class="related" aria-labelledby="rel-titulo">
                    <h2 id="rel-titulo">Seguí leyendo</h2>
                    <div class="posts">
{related}
                    </div>
                </aside>
            </div>
        </article>
    </main>
    <div class="sea sea--up" aria-hidden="true"></div>

{footer(root, blog)}"""
    os.makedirs(f"blog/{p['slug']}", exist_ok=True)
    with open(f"blog/{p['slug']}/index.html", "w", encoding="utf-8") as f:
        f.write(out)
    return len(p["desc"]), len(title)


def build_index():
    root, blog = "../", "./"
    url = SITE + "/blog/"
    jsonld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Blog",
                "@id": url + "#blog",
                "url": url,
                "name": "Blog de Azu Páginas Web",
                "description": BLOG_DESC,
                "inLanguage": "es-AR",
                "publisher": {"@type": "Organization", "name": "Azu Páginas Web", "url": SITE + "/",
                              "logo": {"@type": "ImageObject", "url": LOGO_URL}},
                "blogPost": [{"@type": "BlogPosting", "headline": p["h1"],
                              "url": f"{SITE}/blog/{p['slug']}/", "datePublished": PUBLISHED}
                             for p in POSTS],
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Inicio", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "Blog", "item": url},
                ],
            },
        ],
    }
    cards = "\n".join(card(p, blog) for p in POSTS)
    out = head(BLOG_TITLE, BLOG_DESC, url, root, "website", jsonld)
    out += f"""
<body data-root="{root}">

{nav(root, blog)}
    <main class="blog">
        <section class="blog-hero">
            <div class="container">
                <nav class="crumbs" aria-label="Migas de pan">
                    <a href="{root}">Inicio</a><span aria-hidden="true">/</span>Blog
                </nav>
                <p class="eyebrow">Blog</p>
                <h1>Todo sobre páginas web para <em>emprendimientos</em> ♡</h1>
                <p class="lead">Guías simples y sin tecnicismos para que tu negocio de Mar del Plata tenga una web clara, linda y fácil de encontrar.</p>
            </div>
        </section>

        <section class="blog-list">
            <div class="container">
                <div class="posts">
{cards}
                </div>
            </div>
        </section>
    </main>
    <div class="sea sea--up" aria-hidden="true"></div>

{footer(root, blog)}"""
    os.makedirs("blog", exist_ok=True)
    with open("blog/index.html", "w", encoding="utf-8") as f:
        f.write(out)


def build_sitemap():
    urls = [(SITE + "/", MODIFIED), (SITE + "/blog/", MODIFIED)]
    urls += [(f"{SITE}/blog/{p['slug']}/", MODIFIED) for p in POSTS]
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, last in urls:
        lines.append(f"    <url>\n        <loc>{loc}</loc>\n        <lastmod>{last}</lastmod>\n    </url>")
    lines.append("</urlset>")
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    for i, p in enumerate(POSTS):
        d, t = build_post(i, p)
        aviso = "" if d <= 160 and t <= 70 else "  <-- revisar largo"
        print(f"{p['slug']}: description {d} car., title {t} car.{aviso}")
    build_index()
    build_sitemap()
    print("Listo: blog/ y sitemap.xml generados.")

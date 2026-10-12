#!/usr/bin/env python3
"""Genera el sitio estático del Instituto Abrevajams en la carpeta public/.

Uso (desde la carpeta generador/):  python3 construir.py
Todo el texto del sitio vive en este archivo; el menú, el pie y los datos de
contacto se escriben una sola vez y se repiten en todas las páginas.
"""
import json
import os
from datetime import date
from html import escape

RAIZ = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public")
DOMINIO = "https://www.abrevajams.edu.mx"
HOY = date.today().isoformat()
from datetime import datetime
VERSION = datetime.now().strftime("%Y%m%d%H%M")  # evita que el navegador muestre estilos viejos

# ------------------------------------------------------------------ Datos
ESCUELA = {
    "nombre": "Instituto Abrevajams",
    "direccion": "Independencia 126-B Poniente",
    "colonia": "Santa Ana Tlapaltitlán",
    "ciudad": "Toluca",
    "estado": "Estado de México",
    "direccion_completa": "Independencia 126-B Poniente, Santa Ana Tlapaltitlán, Toluca, Edo. de Méx.",
    "tel_atencion": "722 616 8205",
    "tel_atencion_int": "+527226168205",
    "tel_admin": "729 446 2874",
    "tel_admin_int": "+527294462874",
    "whatsapp": "527226168205",
    "correo": "administracion@abrevajams.edu.mx",
    "facebook": "https://www.facebook.com/abrevajams",
    "instagram": "https://www.instagram.com/instituto_abrevajams/",
    "fundacion": "2003",
}
MAPS_BUSQUEDA = "https://www.google.com/maps/search/?api=1&query=Instituto+Abrevajams+Independencia+126-B+Poniente+Santa+Ana+Tlapaltitl%C3%A1n+Toluca"
MAPS_EMBED = "https://www.google.com/maps?q=Instituto+Abrevajams,+Independencia+126-B+Poniente,+Santa+Ana+Tlapaltitl%C3%A1n,+Toluca&output=embed"


def wa(texto):
    from urllib.parse import quote
    return f"https://wa.me/{ESCUELA['whatsapp']}?text={quote(texto)}"


# ------------------------------------------------------------------ Íconos
ICONOS = {
    "wa": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 0C5.4 0 0 5.4 0 12c0 2.1.6 4.2 1.6 6L0 24l6.2-1.6c1.8 1 3.8 1.5 5.8 1.5 6.6 0 12-5.4 12-12S18.6 0 12 0zm5.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5.3-.5c.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.5s1.1 2.9 1.2 3.1c.1.2 2.1 3.2 5.1 4.5 2.5 1 3 .8 3.6.7.6-.1 1.7-.7 2-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3z"/></svg>',
    "fb": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M14 8h3V4h-3c-2.8 0-4 1.8-4 4.3V10H7v4h3v10h4V14h3l1-4h-4V8.6c0-.4.2-.6.6-.6z"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1" fill="currentColor"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 22s7-6.2 7-12a7 7 0 1 0-14 0c0 5.8 7 12 7 12z"/><circle cx="12" cy="10" r="2.5"/></svg>',
    "tel": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.9v3a2 2 0 0 1-2.2 2 19.8 19.8 0 0 1-8.6-3.1 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.1 4.2 2 2 0 0 1 4.1 2h3a2 2 0 0 1 2 1.7c.1.9.4 1.8.7 2.7a2 2 0 0 1-.5 2.1L8 9.8a16 16 0 0 0 6 6l1.3-1.3a2 2 0 0 1 2.1-.4c.9.3 1.8.6 2.7.7a2 2 0 0 1 1.7 2z"/></svg>',
    "correo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 6-10 7L2 6"/></svg>',
    "estrella": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l3 7h7l-5.5 4.5L18.5 21 12 16.5 5.5 21l2-7.5L2 9h7z"/></svg>',
    "red": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="6" cy="6" r="3"/><circle cx="18" cy="6" r="3"/><circle cx="12" cy="18" r="3"/><path d="M8.5 7.5l2.5 8M15.5 7.5l-2.5 8M9 6h6"/></svg>',
    "chat": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>',
    "bandera": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 21V4l8 4 8-4v17"/><path d="M12 8v13"/></svg>',
    "mundo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20M12 2a15 15 0 0 0 0 20"/></svg>',
    "reloj": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "libro": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20V3H6.5A2.5 2.5 0 0 0 4 5.5z"/><path d="M4 19.5A2.5 2.5 0 0 0 6.5 22H20v-5"/></svg>',
    "plato": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 11h18M5 11a7 7 0 0 1 14 0M4 15h16l-1.5 4h-13z"/></svg>',
    "medalla": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="8" r="5"/><path d="M8.5 12.5 7 22l5-3 5 3-1.5-9.5"/></svg>',
    "diana": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>',
    "ojo": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"/><circle cx="12" cy="12" r="3"/></svg>',
}

TONOS = {  # fondo claro / color del ícono
    "marino": ("#EEF0FF", "var(--marino)"),
    "cielo": ("#E6F6FC", "var(--cielo)"),
    "verde": ("#F2F8E3", "#6E8B1E"),
    "ambar": ("#FFF4D6", "#B07F00"),
    "coral": ("#FDE8EA", "var(--coral)"),
    "wa": ("#E7F9EE", "#1A9E4B"),
}


def icono(nombre, tono):
    fondo, color = TONOS[tono]
    return f'<div class="rasgo__icono" style="background:{fondo};color:{color}">{ICONOS[nombre]}</div>'


# ------------------------------------------------------------------ Plantilla
MENU = [
    ("inicio", "/", "Inicio"),
    ("nosotros", "/nosotros/", "Nosotros"),
    ("preescolar", "/preescolar/", "Preescolar"),
    ("primaria", "/primaria/", "Primaria"),
    ("secundaria", "/secundaria/", "Secundaria"),
    ("admisiones", "/admisiones/", "Admisiones"),
    ("contacto", "/contacto/", "Contacto"),
]


def cabecera(activo):
    items = []
    for clave, url, texto in MENU:
        extra = ' class="activo" aria-current="page"' if clave == activo else ""
        items.append(f'<li><a href="{url}"{extra}>{texto}</a></li>')
    items.append('<li><a class="btn btn--primario" href="/admisiones/#agenda">Agenda tu visita</a></li>')
    e = ESCUELA
    return f'''  <a class="salto" href="#contenido">Saltar al contenido</a>

  <div class="barra-info">
    <div class="contenedor">
      <span class="ocultar-movil">{e["direccion"]}, {e["colonia"]}, {e["ciudad"]}</span>
      <span><a href="tel:{e["tel_atencion_int"]}">{e["tel_atencion"]}</a> · <a href="mailto:{e["correo"]}">{e["correo"]}</a></span>
    </div>
  </div>

  <header class="cabecera">
    <div class="contenedor">
      <a class="logo" href="/" aria-label="Instituto Abrevajams, inicio">
        <img src="/img/logo-abrevajams.png" alt="Instituto Abrevajams" width="776" height="168">
      </a>
      <button class="boton-menu" aria-expanded="false" aria-controls="menu" aria-label="Abrir menú">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>
      </button>
      <nav aria-label="Principal">
        <ul class="menu" id="menu">
          {chr(10).join("          " + i for i in items).strip()}
        </ul>
      </nav>
    </div>
  </header>
'''


def pie():
    e = ESCUELA
    return f'''  <footer class="pie">
    <div class="pie__franja-eslogan">
      <img src="/img/slogan.png" alt="Unidos formamos niños felices" loading="lazy" width="230" height="184">
    </div>
    <div class="contenedor">
      <div class="pie__rejilla">
        <div>
          <img class="pie__logo" src="/img/logo-abrevajams-blanco.png" alt="Instituto Abrevajams" loading="lazy" width="776" height="168">
          <p>Preescolar, Primaria y Secundaria en Toluca desde {e["fundacion"]}.</p>
          <p>{e["direccion_completa"]}</p>
          <div class="redes">
            <a href="{e["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook">{ICONOS["fb"]}</a>
            <a href="{e["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram">{ICONOS["ig"]}</a>
            <a href="https://wa.me/{e["whatsapp"]}" target="_blank" rel="noopener" aria-label="WhatsApp">{ICONOS["wa"]}</a>
          </div>
        </div>
        <div>
          <h4>Niveles</h4>
          <ul>
            <li><a href="/preescolar/">Preescolar</a></li>
            <li><a href="/primaria/">Primaria</a></li>
            <li><a href="/secundaria/">Secundaria</a></li>
          </ul>
        </div>
        <div>
          <h4>Instituto</h4>
          <ul>
            <li><a href="/nosotros/">Nosotros</a></li>
            <li><a href="/admisiones/">Admisiones</a></li>
            <li><a href="/contacto/">Contacto</a></li>
            <li><a href="/aviso-de-privacidad/">Aviso de privacidad</a></li>
          </ul>
        </div>
        <div>
          <h4>Contacto</h4>
          <ul>
            <li><a href="tel:{e["tel_atencion_int"]}">{e["tel_atencion"]}</a> (atención)</li>
            <li><a href="tel:{e["tel_admin_int"]}">{e["tel_admin"]}</a> (administración)</li>
            <li><a href="mailto:{e["correo"]}">{e["correo"]}</a></li>
          </ul>
        </div>
      </div>
      <div class="pie__legal">
        <span>© {date.today().year} Instituto Abrevajams. Todos los derechos reservados.</span>
        <a href="/aviso-de-privacidad/">Aviso de privacidad</a>
      </div>
    </div>
  </footer>

  <a class="wa-flotante" href="{wa("Hola, me interesa información del Instituto Abrevajams")}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{ICONOS["wa"]}</a>
'''


SCRIPT = '''  <script>
    (function () {
      var boton = document.querySelector('.boton-menu');
      var menu = document.getElementById('menu');
      boton.addEventListener('click', function () {
        var abierto = menu.classList.toggle('abierto');
        boton.setAttribute('aria-expanded', abierto);
      });
      // Formularios: arman un mensaje de WhatsApp con los datos capturados
      document.querySelectorAll('form[data-whatsapp]').forEach(function (form) {
        form.addEventListener('submit', function (ev) {
          ev.preventDefault();
          if (!form.reportValidity()) return;
          var datos = new FormData(form);
          var lineas = [form.dataset.whatsapp];
          form.querySelectorAll('[data-etiqueta]').forEach(function (campo) {
            var valor = (datos.get(campo.name) || '').toString().trim();
            if (valor) lineas.push(campo.dataset.etiqueta + ': ' + valor);
          });
          var url = 'https://wa.me/''' + ESCUELA["whatsapp"] + '''?text=' + encodeURIComponent(lineas.join('\\n'));
          window.open(url, '_blank', 'noopener');
          var aviso = form.querySelector('.form-enviado');
          if (aviso) aviso.hidden = false;
        });
      });
    })();
  </script>
'''


def json_ld(obj):
    return '  <script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n  </script>\n"


ESCUELA_LD = {
    "@context": "https://schema.org",
    "@type": ["School", "EducationalOrganization"],
    "@id": DOMINIO + "/#escuela",
    "name": ESCUELA["nombre"],
    "slogan": "Unidos formamos niños felices",
    "url": DOMINIO + "/",
    "logo": DOMINIO + "/img/logo-abrevajams.png",
    "image": DOMINIO + "/img/edificio.webp",
    "foundingDate": ESCUELA["fundacion"],
    "description": "Colegio privado en Toluca, Estado de México, con Preescolar, Primaria y Secundaria. Educación integral con metodologías STEAM, basada en proyectos, en problemas y aprendizaje-servicio; inglés con enfoque Better Learning de Cambridge y certificación Cambridge; grupos reducidos; horario extendido hasta las 6:30 p.m., taller de tareas y comedor.",
    "email": ESCUELA["correo"],
    "telephone": "+52-722-616-8205",
    "address": {
        "@type": "PostalAddress",
        "streetAddress": "Independencia 126-B Poniente, " + ESCUELA["colonia"],
        "addressLocality": ESCUELA["ciudad"],
        "addressRegion": ESCUELA["estado"],
        "addressCountry": "MX",
    },
    "contactPoint": [
        {"@type": "ContactPoint", "contactType": "admissions", "telephone": "+52-722-616-8205", "availableLanguage": ["es"]},
        {"@type": "ContactPoint", "contactType": "billing", "telephone": "+52-729-446-2874", "availableLanguage": ["es"]},
    ],
    "sameAs": [ESCUELA["facebook"], ESCUELA["instagram"]],
}


def relativizar(html, profundidad):
    """Convierte rutas /algo en rutas relativas según la carpeta de la página,
    para que el sitio funcione igual en el dominio y en usuario.github.io/repositorio/."""
    import re
    prefijo = "../" * profundidad
    def cambiar(m):
        attr, ruta = m.group(1), m.group(2)
        if ruta.startswith("//"):
            return m.group(0)
        nueva = prefijo + ruta[1:]
        if nueva == "":
            nueva = "./"
        elif nueva.startswith("#"):
            nueva = "./" + nueva
        return f'{attr}="{nueva}'
    return re.sub(r'(href|src|poster|content)="(/[^"]*)', cambiar, html)


def pagina(ruta, activo, titulo, descripcion, cuerpo, extra_ld=(), imagen="/img/edificio.webp", css_extra=""):
    """Escribe sitio/<ruta>/index.html (o el archivo indicado)."""
    url = DOMINIO + ("/" + ruta.strip("/") + "/" if ruta.strip("/") else "/")
    if ruta.endswith(".html"):
        url = DOMINIO + "/" + ruta
    ld = json_ld(ESCUELA_LD) + "".join(json_ld(x) for x in extra_ld)
    html = f'''<!doctype html>
<html lang="es-MX">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(titulo)}</title>
  <meta name="description" content="{escape(descripcion)}">
  <link rel="canonical" href="{url}">
  <meta name="theme-color" content="#2E3192">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_MX">
  <meta property="og:site_name" content="Instituto Abrevajams">
  <meta property="og:title" content="{escape(titulo)}">
  <meta property="og:description" content="{escape(descripcion)}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{DOMINIO}{imagen}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" sizes="64x64" href="/img/favicon.png">
  <link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="/css/estilos.css?v={VERSION}">
{css_extra}{ld}</head>
<body>
{cabecera(activo)}
  <main id="contenido">
{cuerpo}
  </main>

{pie()}
{SCRIPT}</body>
</html>
'''
    destino = os.path.join(RAIZ, ruta) if ruta.endswith(".html") else os.path.join(RAIZ, ruta.strip("/"), "index.html")
    profundidad = 0 if ruta.endswith(".html") or not ruta.strip("/") else ruta.strip("/").count("/") + 1
    html = relativizar(html, profundidad)
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)
    return url


def migas(*pares):
    partes = ['<a href="/">Inicio</a>']
    for texto, enlace in pares:
        partes.append("<span aria-hidden=\"true\">/</span>")
        partes.append(f'<a href="{enlace}">{texto}</a>' if enlace else f"<span>{texto}</span>")
    return '<nav class="migas" aria-label="Ruta de navegación">' + "".join(partes) + "</nav>"


def migas_ld(*pares):
    elementos = [{"@type": "ListItem", "position": 1, "name": "Inicio", "item": DOMINIO + "/"}]
    for i, (texto, enlace) in enumerate(pares, start=2):
        elementos.append({"@type": "ListItem", "position": i, "name": texto, "item": DOMINIO + enlace})
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": elementos}


def faq_html(preguntas):
    bloques = "\n".join(
        f'          <details>\n            <summary>{escape(p)}</summary>\n            <p>{r}</p>\n          </details>'
        for p, r in preguntas
    )
    return f'''        <div class="faq">
{bloques}
        </div>'''


def faq_ld(preguntas):
    import re
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": p, "acceptedAnswer": {"@type": "Answer", "text": re.sub("<[^>]+>", "", r)}}
            for p, r in preguntas
        ],
    }


def franja_cta(titulo="Conoce la escuela en persona", texto="Agenda un recorrido por nuestras instalaciones, conoce a nuestro equipo y resuelve todas tus dudas sobre el proceso de inscripción.", mensaje="Hola, me interesa información de admisiones del Instituto Abrevajams"):
    return f'''    <section class="seccion">
      <div class="contenedor">
        <div class="franja">
          <div>
            <span class="etiqueta" style="color:var(--amarillo)">Admisiones abiertas</span>
            <h2>{titulo}</h2>
            <p>{texto}</p>
            <div class="franja__botones">
              <a class="btn btn--primario" href="/admisiones/#agenda">Agenda tu visita</a>
              <a class="btn btn--whatsapp" href="{wa(mensaje)}" target="_blank" rel="noopener">{ICONOS["wa"]} Escríbenos por WhatsApp</a>
            </div>
          </div>
          <ul>
            <li>Grupos reducidos y atención personalizada</li>
            <li>Horario extendido hasta las 6:30 p.m.</li>
            <li>Comedor y taller de tareas</li>
            <li>Inglés con enfoque Cambridge</li>
            <li>Instalaciones renovadas y seguras</li>
          </ul>
        </div>
      </div>
    </section>
'''


# ------------------------------------------------------------------ Contenido compartido
VALORES = [
    ("F", "verde", "Fraternidad", "Creamos un ambiente donde los niños y sus padres se sienten parte de una gran familia, apoyándose y cuidándose mutuamente."),
    ("H", "cielo", "Honestidad", "Enseñamos a los niños a ser sinceros y transparentes en sus acciones y palabras, construyendo relaciones de confianza."),
    ("C", "coral", "Compromiso", "Motivamos a los niños a dedicarse a sus estudios y actividades con responsabilidad y esfuerzo."),
]

MISION = "El Instituto Abrevajams es un Centro Educativo que tiene el compromiso de brindar una educación integral de calidad que atienda la diversidad y necesidades de todos los estudiantes que forman parte de nuestra comunidad."
VISION = "Formar seres humanos autónomos, éticos, respetuosos, honestos y responsables, asegurando el bienestar integral de nuestros alumnos a través de la convivencia armónica y una sólida formación en valores."
VISION_PENDIENTE = True  # cambiar a False cuando el cliente confirme el texto de la Visión


def mision_vision():
    pendiente = '<span class="pendiente">TEXTO PENDIENTE DE CONFIRMAR</span>' if VISION_PENDIENTE else ""
    valores = "\n".join(
        f'''          <div class="valor">
            <span class="valor__punto" style="background:var(--{tono})">{letra}</span>
            <div><h3 style="font-size:1.2rem;margin-bottom:4px">{nombre}</h3><p>{texto}</p></div>
          </div>''' for letra, tono, nombre, texto in VALORES)
    return f'''        <div class="mv">
          <article class="mv__tarjeta mv__tarjeta--mision">
            <div class="mv__icono" style="color:var(--amarillo)">{ICONOS["diana"]}</div>
            <h3>Misión</h3>
            <p>{MISION}</p>
          </article>
          <article class="mv__tarjeta mv__tarjeta--vision">
            <div class="mv__icono" style="color:var(--marino)">{ICONOS["ojo"]}</div>
            {pendiente}
            <h3>Visión</h3>
            <p>{VISION}</p>
          </article>
        </div>
        <div class="valores">
{valores}
        </div>'''


DISTINGUE = [
    ("estrella", "marino", "Sistema educativo de vanguardia", "Metodologías actualizadas desde temprana edad y un equipo docente en capacitación constante, buscando la innovación en su práctica."),
    ("red", "cielo", "Proyectos interdisciplinarios", "Los alumnos conectan los campos formativos y se vuelven agentes activos de su aprendizaje al resolver problemas reales con sus compañeros."),
    ("chat", "verde", "Comunicación abierta y eficiente", "Cercanía con madres, padres y tutores a través de diversos canales, con acompañamiento de docentes, personal administrativo y directivos."),
    ("bandera", "ambar", "Fomento de la identidad cultural", "Programas de historia, geografía y danza folclórica que desarrollan en los estudiantes un sentido de identidad y pertenencia."),
    ("mundo", "coral", "Experiencias que retan", "Visitas escolares, campamentos, viajes internacionales y concursos académicos que desafían a nuestros alumnos."),
    ("reloj", "marino", "Servicios vespertinos", "Servicios que se adaptan a las necesidades familiares, en un ambiente seguro donde tus hijos siguen aprendiendo después de clases."),
]


def distingue():
    tarjetas = "\n".join(
        f'''          <article class="rasgo">
            {icono(ic, tono)}
            <h3>{t}</h3>
            <p>{d}</p>
          </article>''' for ic, tono, t, d in DISTINGUE)
    return f'''        <div class="distingue">
{tarjetas}
        </div>'''


SERVICIOS = [
    ("reloj", "ambar", "Horario extendido", "De 2:30 a 6:30 p.m., con actividades lúdicas y formativas en un ambiente seguro y estimulante."),
    ("libro", "verde", "Taller de tareas", "Acompañamiento docente en un espacio guiado y tranquilo para terminar los deberes con comprensión."),
    ("plato", "coral", "Comedor", "Servicio de comedor flexible, adaptado a las necesidades de cada familia."),
    ("medalla", "cielo", "Actividades vespertinas", "Actividades que complementan el desarrollo físico, artístico y emocional de los alumnos."),
]


def servicios(clase="servicios"):
    tarjetas = "\n".join(
        f'''          <div class="servicio">
            {icono(ic, tono)}
            <h3>{t}</h3><p>{d}</p>
          </div>''' for ic, tono, t, d in SERVICIOS)
    return f'''        <div class="{clase}">
{tarjetas}
        </div>'''


METODOS = {
    "proyectos": ("Basada en proyectos", "Permite a los alumnos aprender de manera activa, significativa y colaborativa, desarrollando habilidades para la vida real."),
    "steam": ("Con enfoque STEAM", "Integra ciencia, tecnología, ingeniería, arte y matemáticas para fomentar el pensamiento crítico, la creatividad y la resolución de problemas en contextos reales."),
    "servicio": ("Aprendizaje-servicio", "Vincula el trabajo académico con la participación en proyectos comunitarios, fortaleciendo el compromiso social y el aprendizaje significativo."),
    "problemas": ("Basada en problemas", "El alumno resuelve un problema auténtico a partir de la investigación, el análisis y la toma de decisiones, desarrollando indagación, argumentación y autonomía."),
}


def metodos(claves):
    tarjetas = "\n".join(
        f'''          <article class="metodo">
            <small>Metodología</small>
            <h3>{METODOS[k][0]}</h3>
            <p>{METODOS[k][1]}</p>
          </article>''' for k in claves)
    return f'''        <div class="metodos">
{tarjetas}
        </div>'''


TESTIMONIOS = [
    ("M", "verde", "Marisol Hernández", "Excelente calidad humana de todo el personal y alto nivel académico."),
    ("D", "cielo", "Diana M.", "¡La calidad humana de los docentes, siempre apoyando a las mamás que trabajan!"),
    ("O", "ambar", "Olga Reylo", "Feliz con el trato, pero sobre todo con el método de aprendizaje que llevan."),
    ("A", "coral", "Alejandra García Escalante", "Excelente escuela, sin duda muy recomendable. El trato para los alumnos es excelente."),
]


def testimonios():
    tarjetas = "\n".join(
        f'''          <figure class="testimonio">
            <span class="estrellas" aria-label="5 de 5 estrellas">★★★★★</span>
            <blockquote>“{texto}”</blockquote>
            <figcaption><span class="avatar" style="background:var(--{tono})">{letra}</span>{nombre}</figcaption>
          </figure>''' for letra, tono, nombre, texto in TESTIMONIOS)
    return f'''        <div class="testimonios">
{tarjetas}
        </div>'''


def encabezado_seccion(etiqueta, titulo, texto=""):
    p = f"\n          <p>{texto}</p>" if texto else ""
    return f'''        <div class="encabezado-seccion">
          <span class="etiqueta">{etiqueta}</span>
          <h2>{titulo}</h2>{p}
        </div>'''


def portada_pagina(clase, foto, alt, migas_html, h1, texto, botones=True, posicion="center"):
    b = ""
    if botones:
        b = '''
        <div class="hero2__botones">
          <a class="btn btn--primario" href="/admisiones/#agenda">Agenda tu visita</a>
          <a class="btn btn--contorno" href="#contenido-pagina">Conoce más</a>
        </div>'''
    return f'''    <section class="portada-pag {clase}">
      <img class="portada-pag__foto" src="{foto}" alt="{alt}" style="object-position:{posicion}">
      <div class="portada-pag__capa"></div>
      <div class="contenedor">
        {migas_html}
        <h1>{h1}</h1>
        <p>{texto}</p>{b}
      </div>
    </section>
'''


def bloque_contacto(titulo="Estamos muy cerca de ti", h="h2"):
    e = ESCUELA
    return f'''        <div class="contacto">
          <div class="contacto__datos">
            <span class="etiqueta">Contacto</span>
            <{h}>{titulo}</{h}>
            <ul class="contacto__lista">
              <li>{icono("pin", "ambar")}<div><strong>Dirección</strong>{e["direccion_completa"]}<br><a href="{MAPS_BUSQUEDA}" target="_blank" rel="noopener">Cómo llegar en Google Maps</a></div></li>
              <li>{icono("tel", "wa")}<div><strong>Atención a clientes / WhatsApp</strong><a href="tel:{e["tel_atencion_int"]}">{e["tel_atencion"]}</a></div></li>
              <li>{icono("tel", "wa")}<div><strong>Administración / WhatsApp</strong><a href="tel:{e["tel_admin_int"]}">{e["tel_admin"]}</a></div></li>
              <li>{icono("correo", "marino")}<div><strong>Correo</strong><a href="mailto:{e["correo"]}">{e["correo"]}</a></div></li>
            </ul>
            <a class="btn btn--primario" href="/admisiones/#agenda">Agenda tu visita</a>
          </div>
          <div class="mapa">
            <iframe title="Mapa de ubicación del Instituto Abrevajams" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="{MAPS_EMBED}"></iframe>
          </div>
        </div>'''


def formulario(id_form, encabezado_msg, nivel_predef=""):
    opciones = "".join(
        f'<option{" selected" if n == nivel_predef else ""}>{n}</option>'
        for n in ["Preescolar (Kinder I, II o III)", "Primaria", "Secundaria"]
    )
    return f'''          <form class="formulario" id="{id_form}" data-whatsapp="{escape(encabezado_msg)}" novalidate>
            <div class="fila">
              <label for="{id_form}-nombre">Nombre de la madre, padre o tutor
                <input id="{id_form}-nombre" name="nombre" data-etiqueta="Nombre" autocomplete="name" required>
              </label>
              <label for="{id_form}-tel">Teléfono (WhatsApp)
                <input id="{id_form}-tel" name="telefono" data-etiqueta="Teléfono" type="tel" autocomplete="tel" inputmode="tel" required>
              </label>
            </div>
            <div class="fila">
              <label for="{id_form}-nivel">Nivel de interés
                <select id="{id_form}-nivel" name="nivel" data-etiqueta="Nivel de interés" required>
                  <option value="">Selecciona un nivel</option>{opciones}
                </select>
              </label>
              <label for="{id_form}-grado">Grado que cursará
                <input id="{id_form}-grado" name="grado" data-etiqueta="Grado" placeholder="Ej. 2° de primaria">
              </label>
            </div>
            <label for="{id_form}-mensaje">Mensaje o día preferido para la visita
              <textarea id="{id_form}-mensaje" name="mensaje" data-etiqueta="Mensaje"></textarea>
            </label>
            <label class="consentimiento" for="{id_form}-acepto">
              <input id="{id_form}-acepto" name="acepto" type="checkbox" required>
              <span>Acepto el <a href="/aviso-de-privacidad/">aviso de privacidad</a> y que me contacten por WhatsApp o teléfono.</span>
            </label>
            <button class="btn btn--primario" type="submit">Enviar por WhatsApp</button>
            <p class="nota">Al enviar se abre WhatsApp con tu mensaje listo; sólo presiona enviar.</p>
            <p class="nota form-enviado" hidden><strong>Listo.</strong> Si WhatsApp no se abrió, escríbenos al {ESCUELA["tel_atencion"]}.</p>
          </form>'''


# ------------------------------------------------------------------ Niveles
NIVELES = {
    "preescolar": {
        "nombre": "Preescolar",
        "clase": "portada-pag--pre",
        "color": "amarillo",
        "foto": "/img/preescolar-salon-morado.webp",
        "grados": "Kinder I, II y III",
        "titulo": "Preescolar en Toluca | Instituto Abrevajams",
        "descripcion": "Preescolar (Kinder I, II y III) en Santa Ana Tlapaltitlán, Toluca. Inglés Better Learning de Cambridge, método Singapur, STEAM, grupos de 14 a 16 alumnos y horario extendido.",
        "h1": "Preescolar: <span>el feliz inicio</span> del aprendizaje",
        "sub": "Kinder I, II y III en un ambiente cálido y seguro, donde los niños aprenden jugando, se expresan y descubren el mundo.",
        "ficha": [("Kinder I, II y III", "Grados"), ("8:00 a.m. – 2:30 p.m.", "Kinder II y III (Kinder I 8:30 – 2:00)"), ("14 a 16 alumnos", "Grupos reducidos"), ("Hasta 6:30 p.m.", "Horario extendido")],
        "intro_titulo": "Aprender jugando, con bases sólidas",
        "intro": [
            "En Preescolar sentamos las bases del aprendizaje con experiencias centradas en cada niño. Reconocemos que cada alumno aprende de manera única, por eso diseñamos actividades que promueven la participación activa, la exploración y el desarrollo de habilidades a través del juego.",
            "La alfabetización comienza desde Kinder I y se consolida en Kinder III; el inglés se introduce con juegos, canciones y cuentos; y las matemáticas se construyen manipulando, contando y descubriendo patrones.",
        ],
        "intro_foto": ("/img/preescolar-salon-2.webp", "Alumnos de preescolar en su salón temático"),
        "mapa": "/img/mapa-curricular-preescolar.webp",
        "campos": [
            ("Lenguajes", "coral", [
                ("Español y lectoescritura", "Alfabetización temprana que inicia en Kinder I y se consolida en Kinder III, promoviendo un aprendizaje gradual y significativo.",
                 ["Estrategias enfocadas en el desarrollo del lenguaje y la conciencia fonológica", "Apropiación progresiva del sistema de escritura", "Al concluir Kinder III, dominio funcional de la lectura y escritura acorde a su desarrollo"]),
                ("Inglés", "Metodología Better Learning de Cambridge, con contenidos diseñados para el desarrollo de habilidades lingüísticas, sociales, emocionales y cognitivas, respetando el ritmo natural de cada niño.",
                 ["Introducción al inglés a través del juego, canciones y cuentos", "Vocabulario, comprensión auditiva y expresión oral desde edades tempranas"]),
                ("Artes", "El arte es una herramienta para expresar emociones, desarrollar la creatividad y fortalecer habilidades esenciales.",
                 ["Artes plásticas: colores, formas y texturas", "Danza: ritmo, coordinación y expresión corporal", "Teatro: imaginación, lenguaje y juego de roles"]),
            ]),
            ("Saberes y pensamiento científico", "cielo", [
                ("Matemáticas", "Aprendizaje de las matemáticas con enfoque STEAM, que integra la manipulación, el juego y la creatividad para desarrollar habilidades lógico-matemáticas.",
                 ["Números y conteo en situaciones cotidianas", "Formas, patrones y medidas en actividades lúdicas", "Método Singapur para resolver problemas con actividades visuales y prácticas"]),
                ("Ciencias", "Pensamiento científico con metodología STEAM, estimulando la curiosidad y la investigación activa en el entorno natural y social.",
                 ["Observación y experimentación en el Taller de Ciencias", "Construcción de identidad personal y social", "Conexión con la naturaleza y cuidado del medio ambiente"]),
            ]),
            ("De lo humano y lo comunitario", "ambar", [
                ("Cantos y juegos", "Cantos y juegos que favorecen el desarrollo integral mediante la diversión, la expresión y la socialización.",
                 ["Estimulan el lenguaje, la memoria y la coordinación motriz", "Fomentan la interacción social y el trabajo en equipo", "Desarrollan la creatividad y el sentido rítmico"]),
                ("Regulación de emociones", "Acompañamos a los niños a reconocer y manejar sus emociones, favoreciendo un desarrollo afectivo saludable.",
                 ["Identifican y nombran emociones propias y de los demás", "Aprenden estrategias sencillas para autorregularse", "Fortalecen la empatía, la autoestima y la convivencia armónica"]),
                ("Ritmo en movimiento", "A través del ritmo y el movimiento desarrollan coordinación, expresión corporal y sensibilidad musical.",
                 ["Mejoran su motricidad gruesa y control corporal", "Reconocen patrones rítmicos que estimulan el pensamiento lógico y la memoria"]),
            ]),
            ("Ética, naturaleza y sociedades", "verde", [
                ("Convivencia y vida en comunidad", "Bases para una convivencia armónica: respetar turnos, seguir acuerdos, expresar ideas y resolver conflictos de manera pacífica.",
                 ["Reconocimiento de emociones propias y de los demás", "Autoestima, autonomía y seguridad", "Valoración de la diversidad y respeto por las diferencias"]),
                ("Tiempo histórico y cultura", "Los niños reconocen el paso del tiempo a través de rutinas, celebraciones y relatos, y se acercan a las manifestaciones culturales de su entorno.",
                 ["Acercamiento a tradiciones, costumbres, oficios y festividades", "Apreciación de la riqueza cultural propia y de otros grupos"]),
                ("Responsabilidad ética y social", "Reflexión sobre lo que está bien o mal, respeto a los derechos de los demás y toma de decisiones responsables.",
                 ["Sentido de justicia y equidad", "Respeto por los derechos propios y ajenos", "Impacto de nuestras acciones en los demás y en el planeta"]),
            ]),
        ],
        "metodos": ["proyectos", "steam", "servicio", "problemas"],
        "horario": [("Kinder I", "8:30 a.m. – 2:00 p.m."), ("Kinder II y Kinder III", "8:00 a.m. – 2:30 p.m."), ("Horario extendido", "2:30 p.m. – 6:30 p.m."), ("Grupos", "14 a 16 alumnos")],
        "fotos": [("/img/nivel-preescolar.webp", "Alumna de preescolar con su manualidad"), ("/img/fachada.webp", "Edificio del Instituto Abrevajams"), ("/img/patio.webp", "Patio de la escuela")],
        "faq": [
            ("¿Qué grados de preescolar ofrecen?", "Kinder I, Kinder II y Kinder III."),
            ("¿Cuál es el horario de preescolar?", "Kinder I de 8:30 a.m. a 2:00 p.m.; Kinder II y Kinder III de 8:00 a.m. a 2:30 p.m. Contamos con horario extendido de 2:30 a 6:30 p.m."),
            ("¿Cuántos alumnos hay por grupo en preescolar?", "Trabajamos con grupos reducidos de 14 a 16 alumnos."),
            ("¿Enseñan inglés en preescolar?", "Sí, con la metodología Better Learning de Cambridge, que introduce el inglés a través del juego, canciones y cuentos."),
            ("¿Los niños salen leyendo y escribiendo?", "La alfabetización inicia en Kinder I y se consolida en Kinder III; al concluir, los alumnos alcanzan un dominio funcional de la lectura y escritura acorde a su desarrollo."),
        ],
    },
    "primaria": {
        "nombre": "Primaria",
        "clase": "portada-pag--pri",
        "color": "verde",
        "foto": "/img/primaria-participacion.webp",
        "grados": "1° a 6° grado",
        "titulo": "Primaria en Toluca | Instituto Abrevajams",
        "descripcion": "Primaria de 1° a 6° en Santa Ana Tlapaltitlán, Toluca. Inglés Better Learning con certificaciones Cambridge A2 y B1, método Singapur, proyectos STEAM, tecnología y horario extendido.",
        "h1": "Primaria: <span>bases sólidas</span> para toda la vida",
        "sub": "De 1° a 6° grado, con proyectos que conectan con la vida real, inglés con certificación Cambridge y una formación en valores que acompaña cada etapa.",
        "ficha": [("1° a 6° grado", "Primaria baja y alta"), ("7:30 a.m. – 2:30 / 3:00 p.m.", "Horario escolar"), ("17 a 23 alumnos", "Grupos reducidos"), ("Hasta 6:30 p.m.", "Horario extendido")],
        "intro_titulo": "Aprender a pensar, comunicar y convivir",
        "intro": [
            "En Primaria acompañamos a nuestros alumnos en el desarrollo de competencias lingüísticas, matemáticas y científicas sólidas, con metodologías centradas en el estudiante que atienden sus distintos estilos y ritmos de aprendizaje.",
            "Trabajamos con el método Singapur, talleres de ciencias y retos matemáticos, proyectos integradores STEAM, tecnología y un programa socioemocional que fortalece la convivencia y la cultura de paz.",
        ],
        "intro_foto": ("/img/primaria-clase.webp", "Alumna de primaria escribiendo en su cuaderno"),
        "mapa": "/img/mapa-curricular-primaria.webp",
        "campos": [
            ("Lenguajes", "coral", [
                ("Español y lectoescritura", "Competencias lingüísticas sólidas para comunicarse con claridad, comprender textos y disfrutar el poder de la palabra.",
                 ["Estrategias activas para la comprensión lectora", "Escritura creativa con intención comunicativa", "Pensamiento crítico y autonomía del aprendizaje"]),
                ("Inglés", "Enfoque Better Learning con experiencias de aprendizaje dinámicas y efectivas, alineadas con estándares internacionales.",
                 ["Enfoque integral en listening, speaking, reading y writing", "Certificaciones Cambridge niveles A2 y B1 del CEFR", "Asesorías de nivelación para el avance individual", "Viajes internacionales que enriquecen la experiencia lingüística y cultural"]),
                ("Artes", "Expresión creativa, pensamiento simbólico y sensibilidad estética a través de experiencias artísticas significativas.",
                 ["Imaginación mediante diversas técnicas y materiales", "El arte como medio de expresión y comunicación", "Autoconfianza y trabajo colaborativo"]),
            ]),
            ("Saberes y pensamiento científico", "cielo", [
                ("Matemáticas", "Pensamiento lógico y resolución de problemas con una metodología activa, visual y contextualizada, alineada con el enfoque STEAM.",
                 ["Método Singapur: manipulación concreta, representación visual y razonamiento abstracto", "Taller de Retos y Desafíos Matemáticos", "Proyectos integradores STEAM"]),
                ("Ciencias", "Curiosidad y pensamiento científico para entender y transformar el mundo que nos rodea.",
                 ["Taller de Ciencias: experimentación práctica, observación y análisis", "Capacidad de cuestionar, investigar y resolver problemas", "Proyectos STEAM que integran ciencia, tecnología, ingeniería, arte y matemáticas"]),
            ]),
            ("De lo humano y lo comunitario", "ambar", [
                ("Educación socioemocional", "Habilidades para gestionar emociones, fortalecer la autoestima y construir relaciones saludables, con talleres y conferencias de CONVIVE y la CDHEM.",
                 ["Autoconocimiento y manejo emocional con resiliencia", "Empatía y habilidades sociales para una convivencia armoniosa", "Prevención de la violencia y cultura de paz"]),
                ("Tecnología", "Habilidades tecnológicas básicas y responsables para el mundo digital desde temprana edad.",
                 ["Uso seguro y responsable de las TIC", "Paquetería Office y aplicaciones educativas", "Introducción a la programación y el pensamiento computacional"]),
                ("Educación física y danza", "Desarrollo físico y artístico, hábitos saludables, expresión corporal y trabajo en equipo.",
                 ["Coordinación, motricidad y condición física", "Creatividad y expresión mediante el movimiento", "Disciplina, cooperación y respeto en actividades grupales"]),
            ]),
            ("Ética, naturaleza y sociedades", "verde", [
                ("Tiempo histórico y cultura", "Comprensión del pasado y valoración de la diversidad cultural como base de una identidad con sentido ético y social.",
                 ["Hechos, procesos y personajes clave de la historia", "Patrimonio cultural y tradiciones propias y de otros pueblos", "Identidad, pertenencia y memoria colectiva"]),
                ("Geografía", "Comprender la relación entre el entorno natural, la sociedad y nuestras propias decisiones.",
                 ["Elementos físicos y humanos del espacio geográfico", "Impacto de las actividades humanas en el medio ambiente", "Conciencia territorial, ambiental y social"]),
                ("Responsabilidad ética y social", "Formación ética mediante el análisis crítico de las propias acciones y una conciencia orientada al bien común.",
                 ["Juicio moral a partir del respeto a los derechos humanos", "Justicia, equidad y responsabilidad colectiva", "Impacto social y ambiental de nuestras acciones"]),
            ]),
        ],
        "metodos": ["proyectos", "steam", "servicio"],
        "horario": [("Primaria baja (1°, 2° y 3°)", "7:30 a.m. – 2:30 p.m."), ("Primaria alta (4°, 5° y 6°)", "7:30 a.m. – 3:00 p.m."), ("Horario extendido", "2:30 p.m. – 6:30 p.m."), ("Grupos", "17 a 23 alumnos")],
        "fotos": [("/img/nivel-primaria.webp", "Alumno de primaria escribiendo"), ("/img/primaria-pasillo.webp", "Alumnos de primaria caminando por el pasillo"), ("/img/primaria-participacion.webp", "Alumnos de primaria participando en clase")],
        "faq": [
            ("¿Cuál es el horario de primaria?", "Primaria baja (1° a 3°) de 7:30 a.m. a 2:30 p.m.; primaria alta (4° a 6°) de 7:30 a.m. a 3:00 p.m. Horario extendido de 2:30 a 6:30 p.m."),
            ("¿Cuántos alumnos hay por grupo en primaria?", "Los grupos de primaria son de 17 a 23 alumnos."),
            ("¿Qué nivel de inglés alcanzan en primaria?", "Trabajamos con el enfoque Better Learning y preparamos a los alumnos para las certificaciones Cambridge A2 y B1 del Marco Común Europeo (CEFR)."),
            ("¿Qué es el método Singapur?", "Una metodología para aprender matemáticas que avanza de la manipulación concreta a la representación visual y al razonamiento abstracto."),
            ("¿Tienen taller de tareas?", "Sí, dentro del horario extendido ofrecemos taller de tareas con acompañamiento docente, además de comedor y actividades vespertinas."),
        ],
    },
    "secundaria": {
        "nombre": "Secundaria",
        "clase": "portada-pag--sec",
        "color": "cielo",
        "foto": "/img/nivel-secundaria.webp",
        "grados": "1° a 3° grado",
        "titulo": "Secundaria en Toluca | Instituto Abrevajams",
        "descripcion": "Secundaria de 1° a 3° en Santa Ana Tlapaltitlán, Toluca. Inglés con certificación Cambridge B1–B2, francés, programa AutonoTech de programación y robótica, grupos de 14 a 16 alumnos.",
        "h1": "Secundaria: <span>listos</span> para el siguiente paso",
        "sub": "Adolescentes críticos, responsables y con herramientas para el mundo digital: inglés certificado, francés, robótica y una sólida formación ética.",
        "ficha": [("1° a 3° grado", "Secundaria"), ("Cambridge B1–B2", "Certificación de inglés"), ("14 a 16 alumnos", "Grupos reducidos"), ("Hasta 6:30 p.m.", "Horario extendido")],
        "intro_titulo": "Pensamiento crítico y visión global",
        "intro": [
            "En Secundaria nuestros alumnos profundizan en el uso del lenguaje, las matemáticas y las ciencias con un enfoque STEAM y proyectos interdisciplinarios, mientras desarrollan su identidad, su autonomía y su capacidad de argumentar.",
            "Además de inglés con certificación Cambridge, ofrecemos francés, el programa AutonoTech de computación y robótica, y experiencias como viajes internacionales y concursos académicos.",
        ],
        "intro_foto": ("/img/secundaria.webp", "Alumnos de secundaria con uniforme"),
        "mapa": "/img/mapa-curricular-secundaria.webp",
        "campos": [
            ("Lenguajes", "coral", [
                ("Español", "Uso y conocimiento de las convenciones, estructuras y recursos del lenguaje para la comunicación, la investigación, la argumentación y la creatividad.",
                 ["Expresión en distintas situaciones", "Uso de plataformas digitales"]),
                ("Inglés", "Competencias comunicativas con contenidos auténticos y globales que conectan con el mundo real.",
                 ["Enfoque integral en comprensión auditiva, expresión oral, lectura y escritura", "Certificación Cambridge nivel B1–B2 (MCER)", "Asesorías de nivelación personalizadas", "Viajes internacionales"]),
                ("Francés", "Formación inicial en lengua francesa que amplía el horizonte cultural y la competencia plurilingüe.",
                 ["Comprensión, expresión oral y escrita", "Contenidos francófonos y experiencias vivenciales", "Asesorías de nivelación"]),
                ("Artes", "Sensibilidad estética, expresión creativa y apreciación del arte como parte del desarrollo integral.",
                 ["Formas de expresión visuales, escénicas y sonoras", "El arte como medio de identidad y transformación social", "Proyectos colaborativos con sentido crítico"]),
            ]),
            ("Saberes y pensamiento científico", "cielo", [
                ("Matemáticas", "Pensamiento matemático con enfoque STEAM, con énfasis en la aplicación práctica y la resolución de problemas.",
                 ["Álgebra y funciones", "Geometría y cálculo de medidas en contextos reales", "Estadística, aritmética y probabilidad", "Proyectos interdisciplinarios"]),
                ("Ciencias", "Pensamiento científico con enfoque STEAM que promueve la investigación y la solución de problemas.",
                 ["Biología: seres vivos y ecosistemas", "Química: propiedades y cambios de la materia", "Física: energía, fuerza y movimiento", "Ciencias de la Tierra y talleres prácticos"]),
            ]),
            ("De lo humano y lo comunitario", "ambar", [
                ("Educación socioemocional", "Autoconocimiento, manejo emocional y resiliencia para los retos propios de la adolescencia.",
                 ["Empatía, comunicación asertiva y resolución pacífica de conflictos", "Talleres y conferencias con CONVIVE y la CDHEM", "Prevención de la violencia y promoción del respeto"]),
                ("AutonoTech", "Nuestro programa de computación y robótica para adquirir habilidades tecnológicas de forma práctica, creativa y responsable.",
                 ["Pensamiento computacional", "Robótica educativa", "Solución de problemas reales y retos del mundo digital"]),
                ("Educación física y danza", "Construcción de la corporeidad, conciencia motriz y expresión artística en una formación disciplinada y saludable.",
                 ["Capacidades físicas y habilidades motrices", "Expresión corporal, técnicas de danza y repertorios culturales"]),
            ]),
            ("Ética, naturaleza y sociedades", "verde", [
                ("Historia", "Análisis crítico de los procesos históricos para comprender la transformación de las sociedades.",
                 ["Hechos y contextos a nivel local, nacional y mundial", "Causas y consecuencias en la sociedad actual", "Investigar, argumentar y comunicar ideas con rigor"]),
                ("Geografía", "Comprensión del espacio geográfico y la interacción entre las sociedades y su entorno natural.",
                 ["Componentes físicos y humanos del territorio", "Impacto ambiental de las actividades humanas", "Interpretación de mapas, gráficos y SIG"]),
                ("Responsabilidad ética y social", "Ciudadanos críticos y comprometidos, capaces de reflexionar éticamente y asumir responsabilidades.",
                 ["Juicio moral basado en justicia, equidad y derechos humanos", "Corresponsabilidad social y ambiental", "Proyectos por el bien común y la sustentabilidad"]),
            ]),
        ],
        "metodos": ["proyectos", "steam", "servicio"],
        "horario": [("Horario académico", '<span class="por-confirmar">Por confirmar</span>'), ("Horario extendido", "2:30 p.m. – 6:30 p.m."), ("Grupos", "14 a 16 alumnos")],
        "fotos": [("/img/secundaria.webp", "Alumnos de secundaria en el patio"), ("/img/edificio.webp", "Edificio del Instituto Abrevajams"), ("/img/patio.webp", "Patio de la escuela")],
        "faq": [
            ("¿Qué idiomas estudian en secundaria?", "Inglés, con certificación Cambridge nivel B1–B2 (MCER), y francés como segunda lengua extranjera."),
            ("¿Qué es AutonoTech?", "Es nuestro programa de computación y robótica: pensamiento computacional y robótica educativa para resolver problemas reales."),
            ("¿Cuántos alumnos hay por grupo en secundaria?", "Trabajamos con grupos reducidos de 14 a 16 alumnos."),
            ("¿Tienen horario extendido en secundaria?", "Sí, de 2:30 a 6:30 p.m., con taller de tareas, comedor y actividades vespertinas."),
        ],
    },
}


def pagina_nivel(clave):
    n = NIVELES[clave]
    ruta = f"/{clave}/"
    ficha = "\n".join(f"          <div><strong>{a}</strong><span>{b}</span></div>" for a, b in n["ficha"])
    intro = "\n".join(f"            <p>{p}</p>" for p in n["intro"])
    campos_lista = "\n".join(
        f'              <li><i style="background:var(--{tono})"></i><div><strong>{nombre}</strong><span>{", ".join(m[0] for m in materias)}</span></div></li>'
        for nombre, tono, materias in n["campos"])
    campos = []
    for nombre, tono, materias in n["campos"]:
        tarjetas = "\n".join(
            f'''            <article class="materia">
              <h4>{t}</h4>
              <p>{d}</p>
              <ul>{"".join(f"<li>{x}</li>" for x in lista)}</ul>
            </article>''' for t, d, lista in materias)
        campos.append(f'''        <div class="campo">
          <div class="campo__titulo"><i style="background:var(--{tono})"></i><h3><small>Campo formativo</small>{nombre}</h3></div>
          <div class="materias">
{tarjetas}
          </div>
        </div>''')
    horario = "\n".join(f"            <tr><th scope=\"row\">{a}</th><td>{b}</td></tr>" for a, b in n["horario"])
    fotos = "\n".join(f'          <img src="{s}" alt="{a}" loading="lazy" width="1200" height="900">' for s, a in n["fotos"])
    cuerpo = f'''{portada_pagina(n["clase"], n["foto"], "", migas(("Niveles", "/#niveles"), (n["nombre"], None)), n["h1"], n["sub"])}
    <div class="ficha" id="contenido-pagina">
      <div class="contenedor">
{ficha}
      </div>
    </div>

    <section class="seccion">
      <div class="contenedor intro">
        <div>
          <span class="etiqueta">{n["nombre"]} · {n["grados"]}</span>
          <h2>{n["intro_titulo"]}</h2>
{intro}
        </div>
        <img src="{n["intro_foto"][0]}" alt="{n["intro_foto"][1]}" loading="lazy" width="1400" height="934">
      </div>
    </section>

    <section class="seccion seccion--suave" id="mapa-curricular">
      <div class="contenedor mapa-curricular">
        <figure>
          <img src="{n["mapa"]}" alt="Mapa curricular de {n["nombre"]}: campos formativos y asignaturas" width="999" height="1000" loading="lazy">
          <figcaption>Mapa curricular de {n["nombre"]}</figcaption>
        </figure>
        <div>
          <span class="etiqueta">Mapa curricular</span>
          <h2>Cuatro campos formativos</h2>
          <p>Nuestro plan de estudios se organiza en los campos formativos de la Nueva Escuela Mexicana, enriquecidos con los programas propios del Instituto.</p>
          <ul class="campos-lista">
{campos_lista}
          </ul>
        </div>
      </div>
    </section>

    <section class="seccion" id="campos">
      <div class="contenedor">
{encabezado_seccion("Qué aprenden", "Así trabajamos cada campo formativo")}
{chr(10).join(campos)}
      </div>
    </section>

    <section class="seccion seccion--suave" id="metodologias">
      <div class="contenedor">
{encabezado_seccion("Metodologías", "Aprendizaje centrado en el estudiante", "Diseñamos experiencias que atienden los distintos estilos y ritmos de aprendizaje, para que cada alumno alcance su máximo potencial.")}
{metodos(n["metodos"])}
      </div>
    </section>

    <section class="seccion" id="horarios">
      <div class="contenedor horarios">
        <table class="tabla-horario">
          <caption>Horarios de {n["nombre"]}</caption>
          <tbody>
{horario}
          </tbody>
        </table>
        <div>
          <span class="etiqueta">Servicios vespertinos</span>
          <h2>Pensado para familias que trabajan</h2>
{servicios("servicios servicios--2")}
        </div>
      </div>
    </section>

    <section class="seccion seccion--suave" id="vida-escolar">
      <div class="contenedor">
{encabezado_seccion("Promoción cultural", "Aprender también fuera del salón", "Visitas escolares, eventos culturales y clases abiertas que acercan a los alumnos al arte, la historia, las tradiciones y la comunidad.")}
        <div class="fotos">
{fotos}
        </div>
      </div>
    </section>

    <section class="seccion" id="preguntas">
      <div class="contenedor">
{encabezado_seccion("Preguntas frecuentes", f"Dudas sobre {n['nombre']}")}
{faq_html(n["faq"])}
      </div>
    </section>

{franja_cta(f"Inscripciones abiertas en {n['nombre']}", "Agenda un recorrido, conoce los salones y resuelve tus dudas con nuestro equipo.", f"Hola, me interesa información de {n['nombre']} en el Instituto Abrevajams")}'''
    programa = {
        "@context": "https://schema.org",
        "@type": "EducationalOccupationalProgram",
        "name": f"{n['nombre']} ({n['grados']})",
        "description": n["descripcion"],
        "url": DOMINIO + ruta,
        "provider": {"@id": DOMINIO + "/#escuela"},
        "educationalLevel": n["nombre"],
        "inLanguage": "es-MX",
    }
    return pagina(ruta, clave, n["titulo"], n["descripcion"], cuerpo,
                  extra_ld=[migas_ld((n["nombre"], ruta)), programa, faq_ld(n["faq"])], imagen=n["foto"])


# ------------------------------------------------------------------ Inicio
FAQ_INICIO = [
    ("¿Dónde se encuentra el Instituto Abrevajams?", f"Estamos en {ESCUELA['direccion_completa']}"),
    ("¿Qué niveles educativos ofrecen?", 'Preescolar (Kinder I, II y III), Primaria (1° a 6°) y Secundaria (1° a 3°). Conoce cada uno en <a href="/preescolar/">Preescolar</a>, <a href="/primaria/">Primaria</a> y <a href="/secundaria/">Secundaria</a>.'),
    ("¿Cuántos alumnos hay por grupo?", "Trabajamos con grupos reducidos: de 14 a 16 alumnos en Preescolar y Secundaria, y de 17 a 23 alumnos en Primaria."),
    ("¿Tienen horario extendido?", "Sí. El horario extendido es de 2:30 a 6:30 p.m. e incluye taller de tareas y actividades vespertinas. También contamos con comedor."),
    ("¿Cómo enseñan inglés?", "Con el enfoque Better Learning de Cambridge desde Preescolar. En Primaria preparamos certificaciones Cambridge A2 y B1, y en Secundaria B1–B2. En Secundaria también se estudia francés."),
    ("¿Cómo agendo una visita?", f'Llena el formulario de <a href="/admisiones/#agenda">Admisiones</a> o escríbenos por WhatsApp al <a href="https://wa.me/{ESCUELA["whatsapp"]}">{ESCUELA["tel_atencion"]}</a>.'),
]


def pagina_inicio():
    niveles = []
    for clave, edad, texto, puntos in [
        ("preescolar", "Kinder I, II y III", "El feliz inicio del aprendizaje: juego, lenguaje, emociones y descubrimiento.", ["Inglés Better Learning de Cambridge", "Matemáticas con método Singapur y STEAM", "Artes, danza y teatro"]),
        ("primaria", "1° a 6° grado", "Bases académicas sólidas y formación en valores con proyectos que conectan con la vida real.", ["Certificaciones Cambridge A2 y B1", "Taller de ciencias y retos matemáticos", "Tecnología y educación socioemocional"]),
        ("secundaria", "1° a 3° grado", "Adolescentes críticos, responsables y listos para el siguiente paso académico.", ["Inglés Cambridge B1–B2 y francés", "AutonoTech: programación y robótica", "Viajes internacionales y concursos académicos"]),
    ]:
        mod = {"preescolar": "pre", "primaria": "pri", "secundaria": "sec"}[clave]
        alt = {"preescolar": "Alumna de preescolar mostrando su manualidad", "primaria": "Alumno de primaria escribiendo en su salón", "secundaria": "Alumnos de secundaria con uniforme en el patio"}[clave]
        niveles.append(f'''          <article class="nivel nivel--{mod}">
            <img src="/img/nivel-{clave}.webp" alt="{alt}" loading="lazy" width="1200" height="900">
            <div class="nivel__cuerpo">
              <span class="nivel__edad">{edad}</span>
              <h3>{NIVELES[clave]["nombre"]}</h3>
              <p>{texto}</p>
              <ul>{"".join(f"<li>{p}</li>" for p in puntos)}</ul>
              <a class="enlace" href="/{clave}/">Conoce {NIVELES[clave]["nombre"]}</a>
            </div>
          </article>''')
    cuerpo = f'''    <section class="hero2">
      <video class="hero2__video" autoplay muted loop playsinline poster="/video/hero-poster.jpg" aria-hidden="true">
        <source src="/video/hero-movil.mp4" type="video/mp4" media="(max-width: 760px)">
        <source src="/video/hero.webm" type="video/webm">
        <source src="/video/hero.mp4" type="video/mp4">
      </video>
      <div class="hero2__capa"></div>
      <div class="contenedor hero2__contenido">
        <h1 class="hero2__titulo">Instituto Abrevajams: Preescolar, Primaria y Secundaria en Toluca</h1>
        <div class="hero2__botones">
          <a class="btn btn--primario" href="/admisiones/#agenda">Agenda tu visita</a>
          <a class="btn btn--contorno" href="#niveles">Conoce los niveles</a>
        </div>
        <p>Más de 20 años formando alumnos autónomos, éticos y responsables, con inglés Cambridge, grupos reducidos y horario extendido para tu familia.</p>
      </div>
      <div class="hero2__datos">
        <div class="contenedor">
          <div class="dato2"><strong>2003</strong><span>Año de fundación</span></div>
          <div class="dato2"><strong>3</strong><span>Niveles educativos</span></div>
          <div class="dato2"><strong>Cambridge</strong><span>Inglés certificado</span></div>
          <div class="dato2"><strong>6:30 p.m.</strong><span>Horario extendido</span></div>
        </div>
      </div>
    </section>

    <section class="seccion" id="niveles">
      <div class="contenedor">
{encabezado_seccion("Niveles educativos", "Acompañamos cada etapa de su crecimiento", "Un mismo proyecto educativo desde Kinder I hasta 3° de Secundaria, con programas pensados para cada edad.")}
        <div class="niveles">
{chr(10).join(niveles)}
        </div>
      </div>
    </section>

    <section class="seccion seccion--suave" id="mision">
      <div class="contenedor">
{encabezado_seccion("Quiénes somos", "Nuestra misión y visión")}
{mision_vision()}
      </div>
    </section>

    <section class="seccion" id="distingue">
      <div class="contenedor">
{encabezado_seccion("¿Por qué Abrevajams?", "Lo que nos distingue", "Metodologías actuales, cercanía con las familias y una comunidad que se siente como en casa.")}
{distingue()}
      </div>
    </section>

{franja_cta()}
    <section class="seccion seccion--suave" id="espacios">
      <div class="contenedor">
{encabezado_seccion("Nuestras instalaciones", "Espacios pensados para aprender y convivir")}
        <div class="galeria">
          <figure class="g-ancha g-alta"><img src="/img/edificio.webp" alt="Edificio principal del Instituto Abrevajams" loading="lazy"><figcaption>Edificio</figcaption></figure>
          <figure><img src="/img/nivel-preescolar.webp" alt="Alumna de preescolar mostrando su manualidad" loading="lazy"><figcaption>Preescolar</figcaption></figure>
          <figure class="g-alta"><img src="/img/pasillo.webp" alt="Alumnos caminando por el pasillo de la escuela" loading="lazy"><figcaption>Pasillos</figcaption></figure>
          <figure><img src="/img/primaria-participacion.webp" alt="Alumnos de primaria levantando la mano en clase" loading="lazy"><figcaption>Primaria</figcaption></figure>
          <figure class="g-ancha"><img src="/img/patio.webp" alt="Patio de la escuela" loading="lazy"><figcaption>Patio</figcaption></figure>
          <figure class="g-ancha"><img src="/img/preescolar-salon-morado.webp" alt="Salón temático de preescolar" loading="lazy"><figcaption>Salones temáticos</figcaption></figure>
        </div>
      </div>
    </section>

    <section class="seccion" id="servicios">
      <div class="contenedor">
{encabezado_seccion("Pensado para familias que trabajan", "Servicios vespertinos")}
{servicios()}
      </div>
    </section>

    <section class="seccion seccion--suave" id="testimonios">
      <div class="contenedor">
{encabezado_seccion("Opiniones de familias", "Nuestra comunidad nos recomienda")}
{testimonios()}
      </div>
    </section>

    <section class="seccion" id="preguntas">
      <div class="contenedor">
{encabezado_seccion("Resolvemos tus dudas", "Preguntas frecuentes")}
{faq_html(FAQ_INICIO)}
      </div>
    </section>

    <section class="seccion seccion--suave" id="contacto">
      <div class="contenedor">
{bloque_contacto()}
      </div>
    </section>
'''
    catalogo = {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "name": "Niveles educativos del Instituto Abrevajams",
        "itemListElement": [
            {"@type": "ListItem", "position": i, "url": DOMINIO + f"/{c}/", "name": NIVELES[c]["nombre"]}
            for i, c in enumerate(["preescolar", "primaria", "secundaria"], start=1)
        ],
    }
    return pagina("/", "inicio", "Instituto Abrevajams | Preescolar, Primaria y Secundaria en Toluca",
                  "Colegio en Santa Ana Tlapaltitlán, Toluca, con Preescolar, Primaria y Secundaria desde 2003. Inglés Cambridge, metodología STEAM, grupos reducidos y horario extendido hasta 6:30 p.m.",
                  cuerpo, extra_ld=[catalogo, faq_ld(FAQ_INICIO)])


# ------------------------------------------------------------------ Nosotros
def pagina_nosotros():
    cuerpo = f'''{portada_pagina("portada-pag--gen", "/img/edificio.webp", "", migas(("Nosotros", None)), "Una comunidad que <span>educa como familia</span>", "Desde 2003 acompañamos a las familias de Toluca con educación de alto nivel académico, formación en valores y servicios que se adaptan a su día a día.")}
    <section class="seccion" id="contenido-pagina">
      <div class="contenedor intro">
        <div>
          <span class="etiqueta">¿Quiénes somos?</span>
          <h2>Educación integral con calidad humana</h2>
          <p>{MISION}</p>
          <p>Nuestro compromiso es brindar a nuestros estudiantes una educación de calidad que contribuya a su desarrollo como seres humanos autónomos, éticos, respetuosos, honestos y responsables. En nuestra comunidad escolar buscamos asegurar el bienestar integral de nuestros alumnos fomentando la convivencia armónica y una sólida formación en valores.</p>
          <p>Nos une el deseo de responder a las necesidades familiares y laborales, garantizando bienestar y seguridad para sus hijos a través de nuestros servicios.</p>
        </div>
        <img src="/img/pasillo.webp" alt="Alumnos del Instituto Abrevajams en el pasillo" loading="lazy" width="800" height="1200" style="aspect-ratio:4/5">
      </div>
    </section>

    <section class="seccion seccion--suave">
      <div class="contenedor">
{encabezado_seccion("Misión, visión y valores", "Lo que nos guía")}
{mision_vision()}
      </div>
    </section>

    <section class="seccion">
      <div class="contenedor">
{encabezado_seccion("¿Qué nos distingue?", "Una escuela a la medida de cada familia")}
{distingue()}
      </div>
    </section>

    <section class="seccion seccion--suave">
      <div class="contenedor">
{encabezado_seccion("Metodologías", "Aprendizaje centrado en el estudiante", "Reconocemos que cada alumno aprende de manera única, por eso diseñamos experiencias que promueven la participación activa, la exploración significativa y el desarrollo de habilidades.")}
{metodos(["proyectos", "steam", "servicio", "problemas"])}
      </div>
    </section>

    <section class="seccion">
      <div class="contenedor intro">
        <img src="/img/primaria-participacion.webp" alt="Alumnos participando en clase" loading="lazy" width="1400" height="934">
        <div>
          <span class="etiqueta">Convivencia escolar</span>
          <h2>Una cultura escolar empática y pacífica</h2>
          <p>Cuidamos la personalidad e individualidad de cada alumno: validamos sus emociones y brindamos un ambiente seguro para expresarse.</p>
          <p>Trabajamos con plataformas y programas como CONVIVE y la Comisión de Derechos Humanos del Estado de México (CDHEM) para establecer una cultura escolar empática, pacífica, inclusiva y armoniosa.</p>
          <p>El acompañamiento es cercano: docentes, personal administrativo y directivos dan seguimiento a cada alumno y mantienen comunicación constante con las familias.</p>
        </div>
      </div>
    </section>

    <section class="seccion seccion--suave" id="instalaciones">
      <div class="contenedor">
{encabezado_seccion("Instalaciones", "Espacios renovados, seguros y llenos de color")}
        <div class="galeria">
          <figure class="g-ancha g-alta"><img src="/img/fachada.webp" alt="Fachada del edificio" loading="lazy"><figcaption>Edificio</figcaption></figure>
          <figure><img src="/img/preescolar-salon-2.webp" alt="Salón temático de preescolar" loading="lazy"><figcaption>Salones</figcaption></figure>
          <figure class="g-alta"><img src="/img/pasillo.webp" alt="Pasillo exterior" loading="lazy"><figcaption>Pasillos</figcaption></figure>
          <figure><img src="/img/primaria-clase.webp" alt="Salón de primaria" loading="lazy"><figcaption>Primaria</figcaption></figure>
          <figure class="g-ancha"><img src="/img/patio.webp" alt="Patio" loading="lazy"><figcaption>Patio</figcaption></figure>
          <figure class="g-ancha"><img src="/img/preescolar-salon-morado.webp" alt="Salón temático de preescolar" loading="lazy"><figcaption>Preescolar</figcaption></figure>
        </div>
      </div>
    </section>

    <section class="seccion">
      <div class="contenedor">
{encabezado_seccion("Opiniones de familias", "Nuestra comunidad nos recomienda")}
{testimonios()}
      </div>
    </section>

{franja_cta()}'''
    return pagina("/nosotros/", "nosotros", "Nosotros | Instituto Abrevajams, Toluca",
                  "Conoce al Instituto Abrevajams: misión, visión, valores, metodologías e instalaciones. Una comunidad escolar en Toluca que educa como familia desde 2003.",
                  cuerpo, extra_ld=[migas_ld(("Nosotros", "/nosotros/"))], imagen="/img/fachada.webp")


# ------------------------------------------------------------------ Admisiones
DOCUMENTOS = [
    ("Expediente académico", ["Ficha de inscripción", "Copia del acta de nacimiento del menor", "CURP (formato actualizado)", "Copia del reporte de evaluación de los ciclos escolares anteriores", "Expediente clínico para alumnos con necesidades especiales (NE) o necesidades educativas especiales (NEE)", "Certificado médico (institución pública o privada) con peso y talla del menor", "Comprobante de domicilio"]),
    ("Padres, tutores y personas autorizadas", ["Copia del INE de la madre (ampliada al 200%, ambos lados)", "Copia de la CURP de la madre", "Copia del INE del padre (ampliada al 200%, ambos lados)", "Copia de la CURP del padre", "Copia del INE del tutor legal (ampliada al 200%, ambos lados)", "Copia de la sentencia donde se nombra al tutor legal o del acta de tutela", "Copia del INE de las personas autorizadas a recoger al menor (ampliada al 200%, ambos lados)"]),
    ("Expediente administrativo", ["Constancia de situación fiscal", "Constancia de no adeudo (si aplica)", "Acuerdo de Convivencia Escolar", "Contrato de prestación de servicios"]),
]

FAQ_ADMISIONES = [
    ("¿Cuándo puedo inscribir a mi hijo?", "Las inscripciones están abiertas. Escríbenos para conocer la disponibilidad de lugares en el grado que te interesa."),
    ("¿Puedo conocer la escuela antes de inscribir?", 'Sí. Agenda una visita con el <a href="#agenda">formulario</a> o por WhatsApp y te mostramos las instalaciones.'),
    ("¿Dónde consulto colegiaturas y cuotas?", f'Te compartimos cuotas, esquemas de pago y descuentos vigentes por WhatsApp al <a href="https://wa.me/{ESCUELA["whatsapp"]}">{ESCUELA["tel_atencion"]}</a> o durante tu visita.'),
    ("¿Qué documentos necesito?", "Consulta la lista completa en esta página: expediente académico, documentos de padres o tutores y expediente administrativo."),
]


def pagina_admisiones():
    docs = "\n".join(
        f'''          <section>
            <h3>{t}</h3>
            <ul>{"".join(f"<li>{x}</li>" for x in lista)}</ul>
          </section>''' for t, lista in DOCUMENTOS)
    cuerpo = f'''{portada_pagina("portada-pag--gen", "/img/primaria-pasillo.webp", "", migas(("Admisiones", None)), "Admisiones <span>abiertas</span>", "Te acompañamos en cada paso para que tu familia forme parte de la comunidad Abrevajams.", botones=False)}
    <section class="seccion" id="contenido-pagina">
      <div class="contenedor">
{encabezado_seccion("Proceso de admisión", "Cuatro pasos para inscribirte")}
        <ol class="pasos">
          <li><h3>Contáctanos</h3><p>Escríbenos por WhatsApp o llena el formulario para recibir información del nivel que te interesa.</p></li>
          <li><h3>Visita la escuela</h3><p>Agenda un recorrido por las instalaciones y resuelve tus dudas con nuestro equipo.</p></li>
          <li><h3>Entrega de documentos</h3><p>Reúne el expediente académico, los documentos de padres o tutores y el expediente administrativo.</p></li>
          <li><h3>Inscripción</h3><p>Firma el contrato de prestación de servicios y realiza el pago de inscripción para asegurar el lugar.</p></li>
        </ol>
      </div>
    </section>

    <section class="seccion seccion--suave" id="agenda">
      <div class="contenedor agenda">
        <div>
          <span class="etiqueta">Agenda tu visita</span>
          <h2>Conoce Abrevajams en persona</h2>
          <p>Déjanos tus datos y te contactamos por WhatsApp para confirmar el día y la hora de tu recorrido.</p>
          <ul class="contacto__lista">
            <li>{icono("tel", "wa")}<div><strong>Atención a clientes / WhatsApp</strong><a href="tel:{ESCUELA["tel_atencion_int"]}">{ESCUELA["tel_atencion"]}</a></div></li>
            <li>{icono("pin", "ambar")}<div><strong>Dirección</strong>{ESCUELA["direccion_completa"]}</div></li>
          </ul>
        </div>
{formulario("form-visita", "Hola, quiero agendar una visita al Instituto Abrevajams.")}
      </div>
    </section>

    <section class="seccion" id="documentos">
      <div class="contenedor">
{encabezado_seccion("Documentos", "Documentos para la inscripción", "Te recomendamos tenerlos listos antes de tu cita de inscripción.")}
        <div class="documentos">
{docs}
        </div>
      </div>
    </section>

    <section class="seccion seccion--suave">
      <div class="contenedor">
{encabezado_seccion("Servicios", "Todo lo que tu familia necesita")}
{servicios()}
      </div>
    </section>

    <section class="seccion" id="preguntas">
      <div class="contenedor">
{encabezado_seccion("Preguntas frecuentes", "Dudas sobre admisiones")}
{faq_html(FAQ_ADMISIONES)}
      </div>
    </section>
'''
    return pagina("/admisiones/", "admisiones", "Admisiones | Instituto Abrevajams, Toluca",
                  "Proceso de admisión, documentos para la inscripción y formulario para agendar tu visita al Instituto Abrevajams en Toluca: Preescolar, Primaria y Secundaria.",
                  cuerpo, extra_ld=[migas_ld(("Admisiones", "/admisiones/")), faq_ld(FAQ_ADMISIONES)], imagen="/img/primaria-pasillo.webp")


# ------------------------------------------------------------------ Contacto
def pagina_contacto():
    cuerpo = f'''{portada_pagina("portada-pag--gen", "/img/fachada.webp", "", migas(("Contacto", None)), "Contáctanos", "Estamos en Santa Ana Tlapaltitlán, Toluca. Escríbenos por WhatsApp, llámanos o visítanos.", botones=False)}
    <section class="seccion" id="contenido-pagina">
      <div class="contenedor">
{bloque_contacto("Estamos muy cerca de ti")}
      </div>
    </section>

    <section class="seccion seccion--suave">
      <div class="contenedor agenda">
        <div>
          <span class="etiqueta">Escríbenos</span>
          <h2>¿Tienes una pregunta?</h2>
          <p>Cuéntanos qué necesitas y te respondemos por WhatsApp a la brevedad.</p>
          <div class="redes" style="margin-top:8px">
            <a href="{ESCUELA["facebook"]}" target="_blank" rel="noopener" aria-label="Facebook" style="background:var(--marino);color:#fff">{ICONOS["fb"]}</a>
            <a href="{ESCUELA["instagram"]}" target="_blank" rel="noopener" aria-label="Instagram" style="background:var(--marino);color:#fff">{ICONOS["ig"]}</a>
          </div>
        </div>
{formulario("form-contacto", "Hola, tengo una pregunta para el Instituto Abrevajams.")}
      </div>
    </section>
'''
    return pagina("/contacto/", "contacto", "Contacto | Instituto Abrevajams, Toluca",
                  f"Dirección, teléfonos, WhatsApp y correo del Instituto Abrevajams: {ESCUELA['direccion_completa']} Tel. {ESCUELA['tel_atencion']}.",
                  cuerpo, extra_ld=[migas_ld(("Contacto", "/contacto/"))], imagen="/img/fachada.webp")


# ------------------------------------------------------------------ Aviso de privacidad
def pagina_aviso():
    cuerpo = f'''    <section class="portada-pag portada-pag--gen">
      <div class="contenedor">
        {migas(("Aviso de privacidad", None))}
        <h1>Aviso de privacidad</h1>
      </div>
    </section>
    <section class="seccion">
      <div class="contenedor legal">
        <p>Con fundamento en los artículos 15 y 16 de la Ley Federal de Protección de Datos Personales en Posesión de Particulares, Art. 23 del Reglamento y Lineamientos de aviso de privacidad publicados en el Diario Oficial de la Federación, le damos a conocer el aviso de privacidad respecto al tratamiento de los datos.</p>
        <p>El presente aviso tiene como objetivo delimitar los alcances y condiciones generales del tratamiento de datos que usted nos proporciona, con el compromiso de nuestra parte de utilizarlos solamente con fines académicos y en cumplimiento a la legislación aplicable. Por lo anterior le hacemos saber:</p>

        <h2>I. Identidad y domicilio del responsable que trata los datos personales</h2>
        <p>Lic. Vanesa Bello Aguirre, Directora del Instituto Abrevajams, con domicilio en Bahía de Todos los Santos 321, Santa Ana Tlapaltitlán, Toluca, Estado de México.</p>

        <h2>II. Datos personales que serán sometidos a tratamiento</h2>
        <ol type="a">
          <li>Nombre del alumno</li>
          <li>Nombre de los padres o tutores</li>
          <li>Identificaciones</li>
          <li>Fotografías de identidad</li>
          <li>Teléfono fijo y/o celular</li>
          <li>Correo electrónico</li>
          <li>Dirección</li>
          <li>Datos para alguna emergencia, como tipo de sangre o alergias</li>
        </ol>

        <h2>III. Datos personales sensibles</h2>
        <p>En este caso será sólo información confidencial que, en su caso, nos proporcione y que deberá constar por escrito, previo acuse de recibo.</p>

        <h2>IV. Finalidades del tratamiento</h2>
        <p>Los datos serán utilizados únicamente para las siguientes finalidades:</p>
        <ol type="a">
          <li>Fines académicos.</li>
          <li>Información que se proporciona a la Secretaría de Educación Pública, sólo para fines académicos y en las formas oficiales autorizadas por dicha institución.</li>
          <li>Control escolar de los alumnos.</li>
          <li>Proporcionarle información importante del desempeño escolar del alumno.</li>
          <li>Evaluar la calidad del servicio que brindamos.</li>
          <li>En general, dar cumplimiento a las obligaciones que hemos contraído con usted.</li>
        </ol>
        <p>Los datos que nos comparta mediante los formularios de este sitio web (nombre, teléfono, nivel de interés y mensaje) se utilizan únicamente para responder su solicitud de información o de visita.</p>

        <h2>V. Mecanismos para ejercer sus derechos</h2>
        <ol type="a">
          <li>Usted tiene derecho al acceso, rectificación y cancelación de sus datos personales, a oponerse al tratamiento de los mismos o a revocar el consentimiento que para dicho fin nos haya otorgado.</li>
          <li>Para ello, es necesario que envíe la solicitud en los términos que marca la Ley a nuestro responsable de Protección de Datos Personales, mediante un escrito dirigido a la Lic. Vanesa Bello Aguirre, directora del Instituto Abrevajams, con domicilio en Bahía de Todos los Santos 321, Santa Ana Tlapaltitlán, Toluca, Estado de México.</li>
          <li>En caso de que no desee recibir mensajes de nuestra parte, puede enviarnos su solicitud de la misma manera.</li>
        </ol>

        <h2>VI. Publicaciones</h2>
        <p>Para el caso de que el Instituto se vea en la necesidad de realizar alguna publicación gráfica o de datos, deberá contar con el consentimiento previo y por escrito del padre o tutor para dichos fines.</p>

        <p>Quedamos a su disposición para cualquier duda o aclaración.</p>
        <p><strong>Lic. Vanesa Bello Aguirre</strong><br>Directora del Instituto Abrevajams</p>
      </div>
    </section>
'''
    return pagina("/aviso-de-privacidad/", "", "Aviso de privacidad | Instituto Abrevajams",
                  "Aviso de privacidad del Instituto Abrevajams sobre el tratamiento de datos personales de alumnos, madres, padres y tutores.",
                  cuerpo, extra_ld=[migas_ld(("Aviso de privacidad", "/aviso-de-privacidad/"))])


def pagina_404():
    cuerpo = '''    <section class="seccion error-404">
      <div class="contenedor">
        <strong>404</strong>
        <h1>No encontramos esta página</h1>
        <p>Es posible que la dirección haya cambiado con el nuevo sitio.</p>
        <div class="hero2__botones" style="justify-content:center">
          <a class="btn btn--primario" href="/">Ir al inicio</a>
          <a class="btn btn--secundario" href="/contacto/">Contacto</a>
        </div>
      </div>
    </section>
'''
    pagina("404.html", "", "Página no encontrada | Instituto Abrevajams", "La página que buscas no existe.", cuerpo,
           css_extra='  <meta name="robots" content="noindex">\n')


# ------------------------------------------------------------------ Archivos para buscadores e IAs
def archivos_buscadores(urls):
    prioridad = {"/": "1.0", "/admisiones/": "0.9", "/preescolar/": "0.9", "/primaria/": "0.9", "/secundaria/": "0.9", "/nosotros/": "0.7", "/contacto/": "0.7", "/aviso-de-privacidad/": "0.2"}
    items = []
    for u in urls:
        ruta = u.replace(DOMINIO, "")
        items.append(f"  <url>\n    <loc>{u}</loc>\n    <lastmod>{HOY}</lastmod>\n    <priority>{prioridad.get(ruta, '0.5')}</priority>\n  </url>")
    with open(os.path.join(RAIZ, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "\n".join(items) + "\n</urlset>\n")

    with open(os.path.join(RAIZ, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(f"""# Instituto Abrevajams
# Todos los buscadores y asistentes de IA pueden leer el sitio.
User-agent: *
Allow: /

# Asistentes de IA (permitidos de forma explícita)
User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Claude-User
Allow: /

User-agent: Claude-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: Applebot-Extended
Allow: /

Sitemap: {DOMINIO}/sitemap.xml
""")

    e = ESCUELA
    faq_txt = "\n".join(f"- **{p}** " + __import__("re").sub("<[^>]+>", "", r) for p, r in FAQ_INICIO)
    niveles_txt = []
    for c in ["preescolar", "primaria", "secundaria"]:
        n = NIVELES[c]
        horario = "; ".join(f"{a}: {__import__('re').sub('<[^>]+>', '', b)}" for a, b in n["horario"])
        campos = "; ".join(f"{nombre}: " + ", ".join(m[0] for m in materias) for nombre, _, materias in n["campos"])
        niveles_txt.append(f"""### {n['nombre']} ({n['grados']})
{n['descripcion']}
- Horarios: {horario}
- Campos formativos: {campos}
- Página: {DOMINIO}/{c}/""")
    with open(os.path.join(RAIZ, "llms.txt"), "w", encoding="utf-8") as f:
        f.write(f"""# Instituto Abrevajams

> Colegio privado en Santa Ana Tlapaltitlán, Toluca, Estado de México, fundado en {e['fundacion']}. Ofrece Preescolar (Kinder I, II y III), Primaria (1° a 6°) y Secundaria (1° a 3°) con educación integral, inglés con enfoque Cambridge, metodologías STEAM, grupos reducidos y horario extendido hasta las 6:30 p.m. Lema: "Unidos formamos niños felices".

## Datos de contacto
- Dirección: {e['direccion_completa']}
- Atención a clientes y WhatsApp: {e['tel_atencion']}
- Administración y WhatsApp: {e['tel_admin']}
- Correo: {e['correo']}
- Facebook: {e['facebook']}
- Instagram: {e['instagram']}
- Sitio web: {DOMINIO}/

## Qué distingue al Instituto
""" + "\n".join(f"- {t}: {d}" for _, _, t, d in DISTINGUE) + """

## Metodologías
""" + "\n".join(f"- {v[0]}: {v[1]}" for v in METODOS.values()) + """

## Niveles educativos
""" + "\n\n".join(niveles_txt) + """

## Servicios
""" + "\n".join(f"- {t}: {d}" for _, _, t, d in SERVICIOS) + f"""

## Misión
{MISION}

## Valores
""" + "\n".join(f"- {n}: {t}" for _, _, n, t in VALORES) + f"""

## Preguntas frecuentes
{faq_txt}

## Páginas
- [Inicio]({DOMINIO}/): presentación general del Instituto
- [Nosotros]({DOMINIO}/nosotros/): misión, visión, valores, metodologías e instalaciones
- [Preescolar]({DOMINIO}/preescolar/): Kinder I, II y III, mapa curricular, horarios
- [Primaria]({DOMINIO}/primaria/): 1° a 6°, mapa curricular, horarios
- [Secundaria]({DOMINIO}/secundaria/): 1° a 3°, mapa curricular, horarios
- [Admisiones]({DOMINIO}/admisiones/): proceso, documentos y formulario para agendar visita
- [Contacto]({DOMINIO}/contacto/): dirección, teléfonos y mapa
""")



# ------------------------------------------------------------------ Redirecciones del sitio anterior (WordPress)
REDIRECCIONES = {
    "sobre-nosotros-instituto-abrevajams-toluca": "/nosotros/",
    "niveles-escolares": "/#niveles",
    "niveles-escolares/preescolar": "/preescolar/",
    "niveles-escolares/primaria": "/primaria/",
    "niveles-escolares/secundaria": "/secundaria/",
    "niveles/preescolar": "/preescolar/",
    "niveles/primaria": "/primaria/",
    "niveles/secundaria": "/secundaria/",
    "aviso-de-privacidad-instituto-abrevajams": "/aviso-de-privacidad/",
}


def redirecciones():
    for viejo, nuevo in REDIRECCIONES.items():
        destino = os.path.join(RAIZ, viejo, "index.html")
        os.makedirs(os.path.dirname(destino), exist_ok=True)
        prof = viejo.count("/") + 1
        nuevo_rel = relativizar(f'href="{nuevo}"', prof)[6:-1]
        with open(destino, "w", encoding="utf-8") as f:
            f.write(f"""<!doctype html>
<html lang="es-MX">
<head>
  <meta charset="utf-8">
  <title>Instituto Abrevajams</title>
  <link rel="canonical" href="{DOMINIO}{nuevo}">
  <meta name="robots" content="noindex">
  <meta http-equiv="refresh" content="0; url={nuevo_rel}">
</head>
<body>
  <p>Esta página cambió de dirección: <a href="{nuevo_rel}">continuar</a>.</p>
</body>
</html>
""")


if __name__ == "__main__":
    urls = [pagina_inicio(), pagina_nosotros()]
    urls += [pagina_nivel(c) for c in ["preescolar", "primaria", "secundaria"]]
    urls += [pagina_admisiones(), pagina_contacto(), pagina_aviso()]
    pagina_404()
    redirecciones()
    archivos_buscadores(urls)
    print("Sitio generado en", RAIZ)
    for u in urls:
        print(" ", u)

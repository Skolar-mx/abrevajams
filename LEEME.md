# Instituto Abrevajams — sitio web estático

Sustituye por completo la instalación de WordPress de abrevajams.edu.mx.
No necesita base de datos, ni PHP, ni plugins, ni actualizaciones de seguridad.

## Qué hay en este repositorio

```
public/        ← el sitio. Esto es lo que se publica en public_html.
generador/     ← construir.py, que genera todas las páginas de public/
.cpanel.yml    ← instrucciones para que cPanel copie public/ a public_html
.gitignore
LEEME.md       ← este archivo
```

## Cómo se publica

GitHub (Skolar-mx/abrevajams) → cPanel → Git™ Version Control →
**Update from Remote** → **Deploy HEAD Commit**.

Nada se publica hasta pulsar **Deploy HEAD Commit** en cPanel.
La guía paso a paso está en `guia-github-cpanel.html` (se entrega aparte).

Antes del primer despliegue hay que poner el usuario real de cPanel en
`.cpanel.yml` (sustituir `USUARIO_CPANEL`).

## Archivos ocultos

`.cpanel.yml`, `.gitignore` y `public/.htaccess` empiezan con punto y el
Finder no los muestra. En Mac: **Cmd + Shift + .** para verlos antes de
arrastrarlos a GitHub.

`public/.htaccess`:
- fuerza HTTPS y `www`;
- redirige las direcciones viejas de WordPress (`/niveles-escolares/…`,
  `/sobre-nosotros-instituto-abrevajams-toluca/`, `/wp-admin/`, etc.);
- activa compresión y caché;
- muestra la página 404 propia.

## Cómo cambiar cosas

**Una frase o una errata en una sola página:** edita el `.html` en GitHub
(lápiz → Commit changes) y despliega desde cPanel.

**Datos que se repiten en todas las páginas** (teléfonos, dirección, correo,
redes, horarios, textos de niveles, preguntas frecuentes): se cambian en
`generador/construir.py` y se ejecuta:

```bash
cd generador
python3 construir.py
```

Ojo: el generador vuelve a escribir todas las páginas de `public/`. Si
editaste un `.html` a mano en GitHub, pide que ese cambio se pase también a
`construir.py`, o se perderá la próxima vez que se genere el sitio.

**Fotos y video:** se optimizan antes de subirlas (WebP para fotos; MP4 y WebM
comprimidos para el video). El video de la portada está en
`public/video/hero.mp4`, `hero.webm` y `hero-movil.mp4`.

## Formularios

Los formularios de Admisiones y Contacto no usan servidor: arman el mensaje y
abren WhatsApp al 722 616 8205 con todo escrito. La persona sólo pulsa enviar.

## Para buscadores e IAs

- `public/sitemap.xml` — enviarlo en Google Search Console y Bing Webmaster Tools.
- `public/robots.txt` — permite buscadores y asistentes de IA.
- `public/llms.txt` — resumen del Instituto para IAs.
- Cada página lleva datos estructurados schema.org (escuela, niveles, preguntas frecuentes).

## Pendientes con el cliente

- Texto de la **Visión** (aparece marcado como pendiente). Al confirmarlo, cambiar
  `VISION` y poner `VISION_PENDIENTE = False` en `construir.py`.
- **Horario académico de Secundaria** (en la carta dice "2:30 a.m."; en el sitio dice "Por confirmar").
- **Aviso de privacidad:** dirección del responsable (Bahía de Todos los Santos 321) y
  revisión legal por la ley de datos personales de 2025.
- Correo `.edu.mx` vs `.com.mx` en las cartas de presentación.
- Más fotos de Secundaria y de Preescolar.

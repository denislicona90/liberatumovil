#!/usr/bin/env python3
"""
Libera Tu Móvil — v2 (solo queda la Comunidad). Modifica: comunidad, servicio,
clases-en-directo y las 3 páginas legales. (index.html se reemplaza por el nuevo.)
Uso: deja este archivo, site.js y los .html en la misma carpeta y ejecuta:
     python aplicar_cambios.py
Las copias originales quedan en ./respaldo y siempre se parte de ellas (se puede repetir).
"""
import re, shutil
from pathlib import Path

TEL = "50432741511"  # Gustavo Limas
MISS = []

def rep(t, old, new, f):
    if old not in t:
        MISS.append((f, old[:80])); return t
    return t.replace(old, new)

def rx(t, pat, new, f):
    t2, n = re.subn(pat, new, t, flags=re.S)
    if n == 0: MISS.append((f, pat[:80]))
    return t2

MAP = {"formaciones": "comunidad.html#planes", "clases": "comunidad.html",
       "curso-de-software": "comunidad.html"}

def fix_links(t):
    return re.sub(r'href="https://liberatumovil(?:\.net)?/(?:liberatumovil/)?([a-z0-9-]+)\.html',
                  lambda m: 'href="' + MAP.get(m.group(1), m.group(1) + ".html"), t)

def strip_target(t):
    def f(mo):
        tag = mo.group(0)
        h = re.search(r'href="([^"]*)"', tag)
        if h and not re.match(r"(https?:|mailto:|tel:)", h.group(1).strip()):
            tag = re.sub(r'\s+target="_blank"', "", tag)
            tag = re.sub(r'\s+rel="noopener"', "", tag)
        return tag
    return re.sub(r"<a\b[^>]*>", f, t)

LEGIT = ("Contenido educativo para uso legítimo: solo sobre dispositivos propios o con "
         "autorización expresa del propietario. No se garantizan resultados ni ingresos. "
         "Contacto: info@liberatumovil.net")

def det(summary, items):
    return ('<details class="accordion-item"><summary>%s</summary><div class="accordion-content"><ul>%s</ul></div></details>\n'
            % (summary, "".join("<li>%s</li>" % i for i in items)))

NEW_TEMARIO = (
    det("Manuales y primeros pasos", ["Plan de incorporación", "Preparación de la PC e instalación de controladores"]) +
    det("Fundamentos", ["Hardware, componentes y términos del sector"]) +
    det("Flasheo y reparación de software", ["Reinstalación de sistema en Samsung, Motorola, Xiaomi y Huawei"]) +
    det("Clases en vivo", ["Clases periódicas sobre nuevos modelos y métodos de reparación de software, grabadas para repasar"]) +
    det("Trabajo remoto", ["Servicio remoto con TeamViewer, FlexiHub y USB Redirector"]))

def comunidad(t, f):
    t = rx(t, r'<title>.*?</title>', '<title>Comunidad Libera Tu Móvil | Clases en vivo y soporte para técnicos de celulares</title>', f)
    t = rx(t, r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="Clases en vivo, recursos actualizados y soporte entre colegas para técnicos de celulares. Planes desde $20 USD/mes. Garantía de 7 días según Hotmart.">', f)
    t = rep(t, "Herramientas profesionales, clases en vivo y soporte real para técnicos de desbloqueo. Mantente actualizado y trabaja con confianza.",
            "Clases en vivo, recursos actualizados y soporte entre colegas para técnicos de celulares.", f)
    t = rep(t, '<span class="stat-pill">📡 Box\'s y dongles remotos</span>', '<span class="stat-pill">📚 Manuales y recursos</span>', f)
    t = rep(t, '<span class="stat-pill">🗃️ Licencias compartidas</span>', "", f)
    t = rep(t, "Ya tienes experiencia en desbloqueo o tomaste alguno de nuestros cursos", "Ya tienes experiencia en reparación de celulares", f)
    t = rep(t, "Necesitas acceso a herramientas profesionales sin comprarlas todas", "Quieres aprender con colegas y expertos", f)
    t = rx(t, r'<div class="for-card no">.*?</a>\s*</div>', "", f)
    t = t.replace("</style>", ".for-who{grid-template-columns:1fr!important}</style>", 1)
    for title in ["Box's y dongles", "Licencias compartidas", "Archivos y Firmwares"]:
        t = rx(t, r'<div class="benefit-card">(?:(?!<div class="benefit-card">).)*?<h3>' + re.escape(title) + r'</h3>.*?</div></div>\s*</div>', "", f)
    t = rx(t, r'<div class="free-box"[^>]*>.*?Ver clases gratis →</a>\s*</div>\s*</div>', "", f)
    t = rx(t, r'<details class="accordion-item">.*(?=\s*</div>\s*</div>\s*</section>\s*<hr class="divider">\s*<!-- ===== INSTRUCTORES)',
           lambda m: NEW_TEMARIO, f)
    t = rx(t, r'<details class="accordion-item faq-item">\s*<summary>¿Necesito haber tomado el Curso de Software primero\?</summary>.*?</details>', "", f)
    t = rep(t, "el acceso remoto a las box's, las licencias compartidas, el soporte en grupos y los recursos actualizados",
            "el soporte en grupos y los recursos actualizados", f)
    t = t.replace("las herramientas y servicios", "los contenidos y servicios")
    t = rep(t, "Productor / Instructor — Experto en liberación de dispositivos móviles",
            "Productor / Instructor — Más de 10 años de experiencia en reparación de software Android", f)
    t = rep(t, "Sin preguntas, sin problemas", "según las condiciones de Hotmart", f)
    t = rep(t, "te devolvemos el dinero sin preguntas.", "puedes solicitar el reembolso según las condiciones de Hotmart.", f)
    t = rep(t, "Servicios gestionados a través de Hotmart. La cancelación es libre en cualquier momento.",
            "Servicios gestionados a través de Hotmart. La cancelación es libre en cualquier momento. " + LEGIT, f)
    t = rx(t, r'<div class="instructor-card">(?:(?!<div class="instructor-card">).)*?alt="Denis Licona".*?</p>\s*</div>', "", f)
    return t

def servicio(t, f):
    t = rx(t, r'<title>.*?</title>', '<title>Servicio técnico de software para celulares | Libera Tu Móvil</title>', f)
    t = rx(t, r'<meta name="description" content="[^"]*"\s*/?>',
           '<meta name="description" content="Servicio técnico remoto de software para celulares: flasheo y diagnóstico. Rellena el formulario y recibe tu cotización por WhatsApp.">', f)
    t = rep(t, "Desbloqueo de<br><span>celulares</span> a distancia", "Servicio técnico de<br><span>software</span> a distancia", f)
    t = rep(t, "¿Tu celular tiene un bloqueo que no puedes quitar? Cuéntanos el problema", "¿Tu celular tiene fallas de software? Cuéntanos el problema", f)
    for ti in ["FRP — Cuenta Google", "MDM y KG — Bloqueo empresarial y mora", "Reparación de IMEI"]:
        t = rx(t, r'<div class="service-item">(?:(?!<div class="service-item">).)*?' + re.escape(ti) + r'.*?</p>\s*</div>\s*</div>', "", f)
    for o in ['<option value="FRP">FRP — Cuenta Google</option>',
              '<option value="MDM o KG">MDM o KG — Bloqueo empresarial / mora</option>',
              '<option value="Reparar IMEI">Reparar IMEI</option>']:
        t = rep(t, o, "", f)
    t = rep(t, "<li>Desbloqueos de KG o MDM motivados por negativa a pagar una deuda vigente con la operadora o empresa financiera</li>", "", f)
    t = rep(t, "Ofrecemos exclusivamente servicios de desbloqueo legítimos.", "Ofrecemos exclusivamente servicios legítimos.", f)
    t = rep(t, "con software dañado o bloqueado", "con software dañado", f)
    t = rep(t, "Marca, modelo, tipo de bloqueo y descripción del problema.", "Marca, modelo, tipo de servicio y descripción del problema.", f)
    t = rep(t, "*Solicitud de Desbloqueo — Libera Tu Móvil*", "*Solicitud de servicio — Libera Tu Móvil*", f)
    return t

def clases(t, f):
    t = rx(t, r'<meta property="og:url"[^>]*>\s*', "", f)
    t = rep(t, "Ver formaciones →", "Ver la Comunidad →", f)
    t = rep(t, "conoce nuestras formaciones aquí", "conoce la Comunidad aquí", f)
    return t

def privacidad(t, f):
    b = ("<h2>Publicidad y servicios de terceros</h2>"
      "<p>Podemos usar herramientas de terceros como Google Analytics, Google Ads y Meta (Facebook/Instagram) para medir visitas y mostrar publicidad. "
      "Estos servicios pueden usar cookies o píxeles y recibir datos de navegación (por ejemplo tu IP y las páginas visitadas). "
      "También usamos WhatsApp, Zoom y Hotmart para contacto, clases y pagos, y un servicio de geolocalización por IP (ipinfo.io) para sugerir el código de país en el formulario. "
      "Cada proveedor trata tus datos según su propia política. Puedes gestionar tus preferencias de anuncios en los ajustes de tu cuenta de Google y de Meta.</p>"
      "<p>Los datos que envías por el formulario de servicio técnico se transmiten por WhatsApp únicamente para cotizarte; no los publicamos.</p>")
    return rep(t, "<h2>5. Cookies</h2>", b + "<h2>5. Cookies</h2>", f)

def cookies(t, f):
    return rep(t, "<li>Ofrecer contenidos personalizados y relevantes.</li>",
      "<li>Medir y mostrar publicidad (Google Ads, Meta), solo si aceptas las cookies en el aviso del sitio.</li>"
      "<li>Puedes cambiar tu decisión borrando los datos del sitio en tu navegador.</li>", f)

def terminos(t, f):
    t = rep(t, "Libera Tu Móvil proporciona servicios de desbloqueo de móviles, recursos educativos, herramientas y contenidos informativos.",
            "Libera Tu Móvil proporciona clases, recursos educativos, servicios técnicos de software para celulares y contenidos informativos.", f)
    b = ("<h2>Uso legítimo de los servicios</h2>"
      "<p>Los contenidos y servicios se ofrecen para uso legítimo. Solo se debe trabajar sobre dispositivos propios o con autorización expresa del propietario. "
      "No atendemos dispositivos robados o extraviados, ni procesos para evadir obligaciones legales o contractuales, y podemos rechazar cualquier solicitud dudosa. "
      "No garantizamos resultados ni ingresos. Los reembolsos se rigen por las condiciones de Hotmart.</p>")
    return rep(t, "<h2>2. Registro y acceso</h2>", b + "<h2>2. Registro y acceso</h2>", f)

PAGES = {"comunidad.html": comunidad, "servicio-de-desbloqueo.html": servicio,
         "clases-en-directo.html": clases, "politica-de-privacidad.html": privacidad,
         "terminos-y-condiciones.html": terminos, "politica-de-cookies.html": cookies}

RISK = re.compile(r"\b(FRP|MDM|KG|IMEI|iCloud|bypass|box'?s?|dongles?|firmwares?|Binance|testpoint|root|knox|"
                  r"lista negra|licencias? compartidas?|desbloque\w*|liberaci\w+|liberar|formaciones|curso\w*)\b", re.I)

def main():
    base = Path(__file__).parent
    bk = base / "respaldo"; bk.mkdir(exist_ok=True)
    for name, fn in PAGES.items():
        p = base / name
        if not (p.exists() or (bk / name).exists()):
            print("⚠ No encontrado:", name); continue
        if not (bk / name).exists():
            shutil.copy(p, bk / name)
        t = (bk / name).read_text(encoding="utf-8")
        t = fn(t, name)
        t = t.replace("50487987314", TEL)
        t = fix_links(t); t = strip_target(t)
        if 'src="site.js"' not in t:
            t = t.replace("</body>", '<script src="site.js" defer></script>\n</body>')
        p.write_text(t, encoding="utf-8")
        print("✔", name)
        for w in ("Denis", "8798", "7314"):
            if w in t: print("  ⚠ Aún aparece '%s'" % w)
        vistos = sorted({m.group(0).lower() for m in RISK.finditer(re.sub(r"<[^>]+>", " ", t))})
        if vistos: print("  ⚠ Palabras de riesgo que quedan (revisa):", ", ".join(vistos))
    if MISS:
        print("\nNo se encontró este texto (revísalo a mano):")
        for f, s in MISS: print(" -", f, "→", s)

if __name__ == "__main__":
    main()

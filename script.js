/* ====== CONFIGURACIÓN: lo único que tenés que editar acá ====== */
const CONFIG = {
    whatsapp: "5492233445238", // tu número con código de país, sin + ni espacios (ej: 5492231234567)
    logo: "assets/logo_crema.png",                  // ruta de tu logo, por ejemplo "img/logo.png"
    logoCrema: "assets/logo_cyan.png",
    foto: "assets/azu.png"                   // ruta de tu foto, por ejemplo "img/azu.jpg"
};

/* Logo y foto */
function ponerLogo(selector, src) {
    if (!src) return;
    document.querySelectorAll(selector).forEach(function (el) {
        el.classList.add("has-img");
        el.innerHTML = '<img src="' + src + '" alt="Logo de Azu Páginas Web">';
    });
}
ponerLogo("[data-logo]", CONFIG.logo);
ponerLogo("[data-logo-light]", CONFIG.logoCrema);
document.querySelectorAll("[data-photo]").forEach(function (el) {
    if (!CONFIG.foto) return;
    el.innerHTML = '<img src="' + CONFIG.foto + '" alt="Azu, diseñadora de páginas web">';
});

/* Menú en celular */
const toggle = document.querySelector(".nav__toggle");
const menu = document.getElementById("menu");
toggle.addEventListener("click", function () {
    const open = menu.classList.toggle("is-open");
    toggle.setAttribute("aria-expanded", open);
});
menu.querySelectorAll("a").forEach(function (a) {
    a.addEventListener("click", function () {
        menu.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
    });
});

/* Los botones de cada plan eligen ese plan en el formulario */
document.querySelectorAll("[data-plan]").forEach(function (btn) {
    btn.addEventListener("click", function () {
        document.getElementById("plan").value = btn.dataset.plan;
    });
});

/* Formulario: arma el mensaje y abre WhatsApp */
const form = document.getElementById("contact-form");
const status = document.getElementById("form-status");
form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!form.checkValidity()) {
        form.reportValidity();
        return;
    }
    if (CONFIG.whatsapp.indexOf("X") !== -1) {
        status.textContent = "Falta cargar tu número de WhatsApp en script.js";
        return;
    }
    const data = new FormData(form);
    const lineas = [
        "Hola Azu, te escribo desde tu web ♡",
        "",
        "Nombre: " + data.get("nombre"),
        "Emprendimiento: " + (data.get("emprendimiento") || "-"),
        "Plan que me interesa: " + data.get("plan"),
        "",
        "Mi idea: " + data.get("idea")
    ];
    const url = "https://wa.me/" + CONFIG.whatsapp + "?text=" + encodeURIComponent(lineas.join("\n"));
    window.open(url, "_blank", "noopener");
    status.textContent = "Listo, se abrió WhatsApp con tu mensaje ♡";
    form.reset();
});

/* Año del footer */
document.getElementById("year").textContent = new Date().getFullYear();

/* Aparición suave al hacer scroll */
const items = document.querySelectorAll(".reveal");
if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                io.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12 });
    items.forEach(function (el) { io.observe(el); });
} else {
    items.forEach(function (el) { el.classList.add("is-visible"); });
}

/* Preguntas frecuentes con desplegable fluido */
document.querySelectorAll(".faq details").forEach(function (details) {
    const summary = details.querySelector("summary");
    const texto = details.querySelector("p");
    const reducido = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    let anim = null;
    let abierto = details.open;

    details.classList.toggle("is-open", abierto);

    summary.addEventListener("click", function (e) {
        e.preventDefault();
        abierto = !abierto;
        details.classList.toggle("is-open", abierto);

        if (reducido) { details.open = abierto; return; }

        const cs = getComputedStyle(texto);
        const desde = details.open
            ? { height: cs.height, opacity: cs.opacity, marginTop: cs.marginTop }
            : { height: "0px", opacity: "0", marginTop: "0px" };
        if (anim) anim.cancel();

        let hasta;
        if (abierto) {
            details.open = true;
            hasta = { height: texto.scrollHeight + "px", opacity: "1", marginTop: getComputedStyle(texto).marginTop };
        } else {
            hasta = { height: "0px", opacity: "0", marginTop: "0px" };
        }

        texto.style.overflow = "hidden";
        anim = texto.animate([desde, hasta], {
            duration: 450,
            easing: "cubic-bezier(.4, 0, .2, 1)",
            fill: "forwards"
        });
        anim.onfinish = function () {
            details.open = abierto;
            anim.cancel();
            anim = null;
            texto.style.overflow = "";
        };
    });
});
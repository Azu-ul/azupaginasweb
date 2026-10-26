/* Script del blog: logo, menú del celular y año del footer.
   Las rutas de las imágenes se calculan con data-root del <body>
   (en /blog/ es "../" y en /blog/articulo/ es "../../"). */
const ROOT = document.body.dataset.root || "";
const CONFIG = {
    logo: ROOT + "assets/logo_crema.png",
    logoCrema: ROOT + "assets/logo_cyan.png"
};

/* Logo */
function ponerLogo(selector, src) {
    document.querySelectorAll(selector).forEach(function (el) {
        el.classList.add("has-img");
        el.innerHTML = '<img src="' + src + '" alt="Logo de Azu Páginas Web">';
    });
}
ponerLogo("[data-logo]", CONFIG.logo);
ponerLogo("[data-logo-light]", CONFIG.logoCrema);

/* Menú en celular */
const toggle = document.querySelector(".nav__toggle");
const menu = document.getElementById("menu");
if (toggle && menu) {
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
}

/* Año del footer */
const year = document.getElementById("year");
if (year) year.textContent = new Date().getFullYear();

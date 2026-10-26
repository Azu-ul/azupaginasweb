/* Script del blog: menú del celular y año del footer.
   Los logos ya vienen escritos en el HTML (con ancho y alto) para que carguen enseguida. */

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

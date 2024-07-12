const show = document.querySelector('.hamburger');
const mobMenu = document.querySelector('.mobile-menu');
const exit = document.querySelector('.mobile-memu-hide');

// show.addEventListener('click', showNav)

function showNav() {
    mobMenu.classList.toggle('show');
    show.classList.toggle('rot');
}

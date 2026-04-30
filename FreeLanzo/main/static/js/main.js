const categoryToggle = document.getElementById("categoryToggle");
const categoryMenu = document.getElementById("categoryMenu");

categoryToggle.addEventListener("click", function (e) {
    e.preventDefault();
    categoryMenu.classList.toggle("show");
});

document.addEventListener("click", function (e) {
    if (!categoryToggle.contains(e.target) && !categoryMenu.contains(e.target)) {
        categoryMenu.classList.remove("show");
    }
});

const themeToggle = document.getElementById("themeToggle");

themeToggle.addEventListener("click", function () {
    document.body.classList.toggle("dark-mode");

    if (document.body.classList.contains("dark-mode")) {
        themeToggle.textContent = "🌙";
    } else {
        themeToggle.textContent = "☀️";
    }
});

const menuToggle = document.getElementById("menuToggle");
const navCenter = document.querySelector(".nav-center");

menuToggle.addEventListener("click", function () {
    navCenter.classList.toggle("show");
});
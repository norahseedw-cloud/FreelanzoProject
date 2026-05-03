const categoryToggle = document.getElementById("categoryToggle");
const categoryMenu = document.getElementById("categoryMenu");

if (categoryToggle && categoryMenu) {
    categoryToggle.addEventListener("click", function (e) {
        e.preventDefault();
        categoryMenu.classList.toggle("show");
    });

    document.addEventListener("click", function (e) {
        if (!categoryToggle.contains(e.target) && !categoryMenu.contains(e.target)) {
            categoryMenu.classList.remove("show");
        }
    });
}

const themeToggle = document.getElementById("themeToggle");

if (themeToggle) {
    themeToggle.addEventListener("click", function () {
        document.body.classList.toggle("dark-mode");
        themeToggle.textContent = document.body.classList.contains("dark-mode") ? "🌙" : "☀️";
    });
}

const menuToggle = document.getElementById("menuToggle");
const navCenter = document.querySelector(".nav-center");

if (menuToggle && navCenter) {
    menuToggle.addEventListener("click", function () {
        navCenter.classList.toggle("show");
    });
}

const revealElements = document.querySelectorAll(".reveal");

function revealOnScroll() {
    revealElements.forEach((element) => {
        if (element.getBoundingClientRect().top < window.innerHeight - 100) {
            element.classList.add("show");
        }
    });
}

window.addEventListener("scroll", revealOnScroll);
window.addEventListener("load", revealOnScroll);

const programTrack = document.getElementById("programTrack");

if (programTrack) {
    const items = Array.from(programTrack.children);
    items.forEach(item => {
        programTrack.appendChild(item.cloneNode(true));
    });
}

const saveBtn = document.querySelector(".btn-save");

if (saveBtn) {
    saveBtn.addEventListener("click", function () {
        const icon = this.querySelector("i");

        if (!icon) return;

        if (icon.classList.contains("bi-heart")) {
            icon.classList.replace("bi-heart", "bi-heart-fill");
            this.style.color = "var(--btn-color)";
            this.style.borderColor = "var(--btn-color)";
        } else {
            icon.classList.replace("bi-heart-fill", "bi-heart");
            this.style.color = "";
            this.style.borderColor = "";
        }
    });
}

const faqButtons = document.querySelectorAll(".faq-question");

faqButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        const faqItem = button.closest(".faq-item");
        faqItem.classList.toggle("active");
    });
});

const menuBtn = document.querySelector('.menu-btn');
const container = document.getElementById('chatContainer');
const overlay = document.querySelector('.overlay');

if (menuBtn && container && overlay) {
    menuBtn.addEventListener('click', () => {
        container.classList.toggle('active');
    });

    overlay.addEventListener('click', () => {
        container.classList.remove('active');
    });
}


document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("roleModal");
    const roleInput = document.getElementById("roleInput");
    const form = document.getElementById("signupForm");

    
    if (modal && roleInput && form) {

        
        modal.style.display = "flex";

        
        window.selectRole = function(role) {
            roleInput.value = role;
            modal.style.display = "none";
        };

        
        form.addEventListener("submit", function(e) {
            if (!roleInput.value) {
                e.preventDefault();
                alert("Please choose a role first");
            }
        });
    }

});

function skipProfile(){
    document.getElementById("completeProfileModal").style.display = "none";
}


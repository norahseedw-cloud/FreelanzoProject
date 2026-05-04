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

const faqButtons = document.querySelectorAll(".faq-question");

faqButtons.forEach(function (button) {
    button.addEventListener("click", function () {
        const faqItem = button.closest(".faq-item");
        faqItem.classList.toggle("active");
    });
});


document.addEventListener("DOMContentLoaded", function () {

    const modal = document.getElementById("roleModal");
    const roleInput = document.getElementById("roleInput");
    const form = document.getElementById("signupForm");

    if (!modal || !roleInput || !form) return;

    const selectedRole = localStorage.getItem("selectedRole");

    if (!selectedRole) {
        modal.style.display = "flex";
    } else {
        roleInput.value = selectedRole;
    }

    window.selectRole = function(role) {
        roleInput.value = role;
        localStorage.setItem("selectedRole", role);
        modal.style.display = "none";
    };

    form.addEventListener("submit", function(e) {
        if (!roleInput.value) {
            e.preventDefault();
            modal.style.display = "flex";
        }
    });

});

function skipProfile(){
    document.getElementById("completeProfileModal").style.display = "none";
}

document.addEventListener("DOMContentLoaded", function () {
    const deleteModal = document.getElementById("deleteModal");
    const deleteForm = document.getElementById("deleteForm");

    if (deleteModal && deleteForm) {
        deleteModal.addEventListener("show.bs.modal", function (event) {
            const button = event.relatedTarget;
            const reviewId = button.getAttribute("data-review-id");

            deleteForm.action = `/reviews/delete/${reviewId}/`;
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {

    const togglePassword = document.getElementById("togglePassword");
    const passwordInput = document.getElementById("passwordInput");

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener("click", function () {
            const isPassword = passwordInput.type === "password";
            passwordInput.type = isPassword ? "text" : "password";

            this.innerHTML = isPassword
                ? '<i class="bi bi-eye-slash"></i>'
                : '<i class="bi bi-eye"></i>';
        });
    }

});
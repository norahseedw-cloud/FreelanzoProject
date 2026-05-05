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

const programTrack = document.querySelector(".program-track");

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

    modal.style.display = "flex";

    window.selectRole = function(role) {
        roleInput.value = role;
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

document.addEventListener("DOMContentLoaded", function () {
    const revealElements = document.querySelectorAll(".reveal");

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("show");
            }
        });
    }, {
        threshold: 0.15
    });

    revealElements.forEach((element) => {
        observer.observe(element);
    });
});
document.addEventListener("DOMContentLoaded", function () {
    const chatContainer = document.getElementById("chatContainer");
    const btn = document.getElementById("chatToggleBtn");
    const overlay = document.querySelector(".overlay");
    const backBtn = document.querySelector(".back-btn");

    function closeChatSidebar() {
        chatContainer.classList.remove("active");

        if (btn) {
            btn.innerHTML = '<i class="bi bi-list"></i>';
        }
    }

    if (chatContainer && btn) {
        btn.addEventListener("click", function () {
            chatContainer.classList.toggle("active");

            if (chatContainer.classList.contains("active")) {
                btn.innerHTML = '<i class="bi bi-x-lg"></i>';
            } else {
                btn.innerHTML = '<i class="bi bi-list"></i>';
            }
        });
    }

    if (overlay && chatContainer) {
        overlay.addEventListener("click", closeChatSidebar);
    }

    if (backBtn && chatContainer) {
        backBtn.addEventListener("click", closeChatSidebar);
    }
});

document.addEventListener('DOMContentLoaded', function () {

    const deleteModal = document.getElementById('deleteModal');
    const deleteForm = document.getElementById('deleteForm');

    deleteModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const conversationId = button.getAttribute('data-id');

        deleteForm.action = `/chat/${conversationId}/delete/`;
    });

});

document.addEventListener("DOMContentLoaded", function () {

    const input = document.getElementById("avatarInput");
    const box = document.getElementById("avatarPreviewBox");

    if (!input || !box) return;

    input.addEventListener("change", function () {
        const file = this.files[0];

        if (file) {
            const url = URL.createObjectURL(file);
            box.innerHTML = "";
            const img = document.createElement("img");
            img.src = url;
            img.className = "profile-avatar";
            const overlay = document.createElement("div");
            overlay.className = "avatar-overlay";
            overlay.innerText = "Change Your Avatar";
            box.appendChild(img);
            box.appendChild(overlay);
        }
    });

});
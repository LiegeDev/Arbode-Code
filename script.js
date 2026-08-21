const mobileButton = document.querySelector(".mobile-menu-button");
const mobileMenu = document.querySelector(".mobile-menu");

mobileButton.addEventListener("click", () => {
    mobileMenu.classList.toggle("open");
});


document.querySelectorAll(".mobile-menu a").forEach(link => {
    link.addEventListener("click", () => {
        mobileMenu.classList.remove("open");
    });
});


document.querySelectorAll("button").forEach(button => {

    button.addEventListener("click", () => {

        const text = button.textContent.trim();

        if (
            text.includes("Start Learning") ||
            text.includes("Get Started")
        ) {
            alert("Arbode Code is currently in development.");
        }

        if (text.includes("Run Code")) {
            alert("Code execution will be connected to the Arbode Code API.");
        }

    });

});


const observer = new IntersectionObserver(
    entries => {

        entries.forEach(entry => {

            if (entry.isIntersecting) {

                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";

            }

        });

    },
    {
        threshold: 0.12
    }
);


document
    .querySelectorAll(
        ".feature-card, .path-card, .mini-editor, .progress-dashboard, .leaderboard, .studio-window"
    )
    .forEach(element => {

        element.style.opacity = "0";
        element.style.transform = "translateY(25px)";
        element.style.transition = "opacity 0.7s ease, transform 0.7s ease";

        observer.observe(element);

    });

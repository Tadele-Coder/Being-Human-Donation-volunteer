document.addEventListener("DOMContentLoaded", function () {

    console.log("DONSVOL JS LOADED");


    /* =========================================================
       LOGIN DROPDOWN
    ========================================================= */

    const loginButton =
        document.getElementById("loginDropdownButton");

    const loginMenu =
        document.getElementById("loginDropdownMenu");

    const loginContainer =
        document.querySelector(".donsvol-login");


    if (loginButton && loginMenu && loginContainer) {

        loginButton.addEventListener("click", function (event) {

            event.preventDefault();
            event.stopPropagation();

            loginMenu.classList.toggle("show");
            loginContainer.classList.toggle("open");

        });


        document.addEventListener("click", function (event) {

            if (!loginContainer.contains(event.target)) {

                loginMenu.classList.remove("show");
                loginContainer.classList.remove("open");

            }

        });

    }


    /* =========================================================
       PASSWORD SHOW / HIDE
    ========================================================= */

    const passwordToggles =
        document.querySelectorAll(".password-toggle");


    passwordToggles.forEach(function (toggle) {

        toggle.addEventListener("click", function (event) {

            event.preventDefault();


            const targetId =
                toggle.getAttribute("data-password-target");


            let passwordInput;


            if (targetId) {

                passwordInput =
                    document.getElementById(targetId);

            } else {

                passwordInput =
                    document.getElementById("id_password");

            }


            if (!passwordInput) {
                return;
            }


            const icon =
                toggle.querySelector("i");


            if (passwordInput.type === "password") {

                passwordInput.type = "text";


                if (icon) {

                    icon.classList.remove("fa-eye");
                    icon.classList.add("fa-eye-slash");

                }


                toggle.setAttribute(
                    "title",
                    "Hide password"
                );

                toggle.setAttribute(
                    "aria-label",
                    "Hide password"
                );

                toggle.classList.add("active");

            } else {

                passwordInput.type = "password";


                if (icon) {

                    icon.classList.remove("fa-eye-slash");
                    icon.classList.add("fa-eye");

                }


                toggle.setAttribute(
                    "title",
                    "Show password"
                );

                toggle.setAttribute(
                    "aria-label",
                    "Show password"
                );

                toggle.classList.remove("active");

            }

        });

    });


    /* =========================================================
       DONSVOL ADMIN SIDEBAR
    ========================================================= */

    const sidebar =
        document.getElementById("adminSidebar");

    const btnSidebar =
        document.getElementById("btn-sidebar");


    console.log("Sidebar:", sidebar);
    console.log("Sidebar Button:", btnSidebar);


    if (!sidebar) {

        console.error(
            "DONSVOL ERROR: #adminSidebar not found"
        );

        return;

    }


    if (!btnSidebar) {

        console.error(
            "DONSVOL ERROR: #btn-sidebar not found"
        );

        return;

    }


    /* =========================================================
       SIDEBAR TOGGLE
    ========================================================= */

    btnSidebar.addEventListener("click", function (event) {

        event.preventDefault();
        event.stopPropagation();


        sidebar.classList.toggle("active");


        console.log(
            "Sidebar active:",
            sidebar.classList.contains("active")
        );

    });


    /* =========================================================
       MOBILE OUTSIDE CLICK
    ========================================================= */

    document.addEventListener("click", function (event) {

        if (window.innerWidth > 768) {
            return;
        }


        if (!sidebar.classList.contains("active")) {
            return;
        }


        if (sidebar.contains(event.target)) {
            return;
        }


        sidebar.classList.remove("active");

    });

});


/* =========================================================
   DONOR SIDEBAR
   ========================================================= */

const donorSidebar = document.getElementById("donorSidebar");
const donorSidebarButton = document.getElementById("btn-donor-sidebar");

if (donorSidebar && donorSidebarButton) {

    donorSidebarButton.addEventListener("click", function (event) {

        event.preventDefault();
        event.stopPropagation();

        donorSidebar.classList.toggle("active");

        console.log(
            "Donor sidebar:",
            donorSidebar.classList.contains("active")
                ? "OPEN"
                : "CLOSED"
        );
    });


    /* Close donor sidebar when clicking outside on mobile */

    document.addEventListener("click", function (event) {

        if (window.innerWidth > 768) {
            return;
        }

        if (!donorSidebar.classList.contains("active")) {
            return;
        }

        if (
            donorSidebar.contains(event.target) ||
            donorSidebarButton.contains(event.target)
        ) {
            return;
        }

        donorSidebar.classList.remove("active");
    });
}



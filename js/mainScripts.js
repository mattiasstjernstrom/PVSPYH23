window.onscroll = function () {
  progressBar();
};

function progressBar() {
  var winScroll = document.body.scrollTop || document.documentElement.scrollTop;
  var height =
    document.documentElement.scrollHeight -
    document.documentElement.clientHeight;
  var scrolled = (winScroll / height) * 100;
  document.getElementById("progress-bar").style.width = scrolled + "%";
}

function smoothscroll() {
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// const toggleSwitch = document.querySelector(
//   '.theme-switch input[type="checkbox"]'
// );
// const currentTheme = localStorage.getItem("theme");

// if (currentTheme) {
//   document.documentElement.setAttribute("data-theme", currentTheme);

//   if (currentTheme === "dark") {
//     toggleSwitch.checked = true;
//   }
// }

// function switchTheme(event) {
//   if (event.target.checked) {
//     document.documentElement.setAttribute("data-theme", "dark");
//     localStorage.setItem("theme", "dark");
//   } else {
//     document.documentElement.setAttribute("data-theme", "light");
//     localStorage.setItem("theme", "light");
//   }
// }

// toggleSwitch.addEventListener("change", switchTheme, false);

/* load theme from local storage and set */

window.addEventListener("load", function () {
  const theme = localStorage.getItem("theme");
  if (theme) {
    document.documentElement.setAttribute("data-theme", theme);
  }

  toggleTheme();
});

const themeSwitch = document.querySelector(".toggle-container");

themeSwitch.addEventListener("click", function () {
  const theme = document.documentElement.getAttribute("data-theme");
  const newTheme = theme === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);

  toggleTheme();
});

function toggleTheme() {
  const storedTheme = localStorage.getItem("theme");

  if (storedTheme === "dark") {
    themeSwitch.innerHTML = `<img src="/assets/sun.svg" alt="Light Mode" />`;
  } else {
    themeSwitch.innerHTML = `<img src="/assets/moon.svg" alt="Dark Mode" />`;
  }
}

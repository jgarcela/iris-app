document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("analyzer-form");
  const loadingModal = document.getElementById("loading-modal");

  form.addEventListener("submit", function () {
    loadingModal.style.display = "flex";

    const steps = [1, 2, 3];
    const delays = [2000, 2000, 5000]; // más tiempo en el paso 3

    steps.forEach((step, i) => {
      setTimeout(() => {
        const prev = document.getElementById(`step-${step - 1}`);
        const current = document.getElementById(`step-${step}`);

        if (prev) prev.classList.remove("active");
        if (prev) prev.classList.add("completed");
        if (current) current.classList.add("active");
      }, delays.slice(0, i).reduce((a, b) => a + b, 0));
    });
  });
});

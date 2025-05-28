document.addEventListener("DOMContentLoaded", function () {
  const headers = document.querySelectorAll('.accordion-header');

  headers.forEach(header => {
    const icon = header.querySelector('.accordion-icon');
    const body = header.nextElementSibling;

    header.addEventListener('click', function () {
      body.classList.toggle('open');
      icon.textContent = body.classList.contains('open') ? '−' : '+';
    });
  });
});
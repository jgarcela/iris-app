document.addEventListener('DOMContentLoaded', function() {
    const btnUrl    = document.getElementById('use-url');
    const fieldsTxt = document.getElementById('fields-text');
    const fieldsUrl = document.getElementById('fields-url');
  
    btnUrl.addEventListener('click', () => {
      // Ocultar campos de texto
      fieldsTxt.style.display = 'none';
      // Mostrar campo de URL
      fieldsUrl.style.display = 'block';
  
      // Ajustar validaciones: quitar required de textarea, añadir a URL
      document.getElementById('input-text').required = false;
      document.getElementById('url').required       = true;
    });

    const btnBack = document.getElementById('back-to-text');
    btnBack.addEventListener('click', () => {
      fieldsUrl.style.display = 'none';
      fieldsTxt.style.display = 'block';
      document.getElementById('url').required       = false;
      document.getElementById('input-text').required = true;
    });
  });
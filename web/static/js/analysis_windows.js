document.addEventListener('DOMContentLoaded', function() {
  const btnUrl      = document.getElementById('use-url');
  const btnBack     = document.getElementById('back-to-text');
  const fieldsTxt   = document.getElementById('fields-text');
  const fieldsUrl   = document.getElementById('fields-url');
  const textarea    = document.getElementById('input-text');
  const urlInput    = document.getElementById('url');
  const loadExample = document.getElementById('load-example');

  // Mostrar campo URL y ocultar textarea
  btnUrl.addEventListener('click', () => {
    fieldsTxt.style.display = 'none';
    fieldsUrl.style.display = 'block';

    textarea.required = false;
    urlInput.required  = true;
  });

  // Volver al textarea y ocultar URL
  btnBack.addEventListener('click', () => {
    fieldsUrl.style.display = 'none';
    fieldsTxt.style.display = 'block';

    urlInput.required  = false;
    textarea.required = true;
  });

  // Cargar un ejemplo de texto
  loadExample.addEventListener('click', () => {
    const ejemplo = `"En un lugar de la Mancha, de cuyo nombre no quiero acordarme..."`;
    // Asegúrate de usar el campo que esté visible
    if (!fieldsUrl.classList.contains('d-none') && fieldsUrl.style.display !== 'none') {
      urlInput.value = ejemplo;
      urlInput.required = true;
      textarea.required = false;
      fieldsTxt.style.display  = 'none';
    } else {
      textarea.value = ejemplo;
      textarea.required = true;
    }
  });
});
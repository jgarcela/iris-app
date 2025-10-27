// File: static/js/table_noticias.js

  $(function () {
  // 1) Inicializar Bootstrap Table con configuración mejorada
  $("#tabla-noticias").bootstrapTable({
    search: false,
    showColumns: true,
    showExport: false,
    pagination: true,
    pageSize: 10,
    pageList: [5, 10, 25, 50, 100],
    locale: 'es-ES',
    filterControl: true,
    filterShowClear: true,
    clickToSelect: true,
    sortName: 'IdNoticia',
    sortOrder: 'asc',
    // No searchText/placeholder because search is disabled
    showToggle: true,
    showRefresh: true,
    showFullscreen: true,
    toolbar: '#toolbar',
    onSearch: function (text) {},
    onRefresh: function () {}
  });

  // 2) Función para generar y descargar CSV de filas (selected o all)
  function exportarCSV() {
    const seleccionadas = $("#tabla-noticias").bootstrapTable("getSelections");
    const filas = seleccionadas.length > 0
      ? seleccionadas
      : $("#tabla-noticias").bootstrapTable("getData");

    if (!filas || filas.length === 0) {
      alert("No hay datos para exportar.");
      return;
    }

    const columnasVisible = [];
    $("#tabla-noticias").find("thead th[data-field]").each(function () {
      const field = $(this).attr("data-field");
      if (field && field !== "state") {
        columnasVisible.push(field);
      }
    });

    const csvRows = [];
    const encabezados = columnasVisible.map(col => `"${col.replace(/_/g, " ").toUpperCase()}"`);
    csvRows.push(encabezados.join(","));

    filas.forEach(row => {
      const valores = columnasVisible.map(col => {
        let val = row[col];
        if (val === null || val === undefined) val = "";
        return `"${String(val).replace(/"/g, '""')}"`;
      });
      csvRows.push(valores.join(","));
    });

    const csvContent = csvRows.join("\r\n");
    const blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
    const fileName = "noticias_exportadas.csv";

    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", fileName);
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // 3) Función para generar y descargar JSON de filas (selected o all)
  function exportarJSON() {
    const seleccionadas = $("#tabla-noticias").bootstrapTable("getSelections");
    const filas = seleccionadas.length > 0
      ? seleccionadas
      : $("#tabla-noticias").bootstrapTable("getData");

    if (!filas || filas.length === 0) {
      alert("No hay datos para exportar.");
      return;
    }

    const jsonString = JSON.stringify(filas, null, 2);
    const blob = new Blob([jsonString], { type: "application/json;charset=utf-8;" });
    const fileName = "noticias_exportadas.json";

    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.setAttribute("href", url);
    link.setAttribute("download", fileName);
    link.style.visibility = "hidden";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // 4) Función para generar y descargar PDF con jsPDF + AutoTable
  function exportarPDF() {
    const seleccionadas = $("#tabla-noticias").bootstrapTable("getSelections");
    const filas = seleccionadas.length > 0
      ? seleccionadas
      : $("#tabla-noticias").bootstrapTable("getData");

    if (!filas || filas.length === 0) {
      alert("No hay datos para exportar.");
      return;
    }

    const columnasVisible = [];
    $("#tabla-noticias").find("thead th[data-field]").each(function () {
      const field = $(this).attr("data-field");
      if (field && field !== "state") {
        columnasVisible.push(field);
      }
    });

    const columnasParaPdf = columnasVisible.map(col => ({
      header: col.replace(/_/g, " ").toUpperCase(),
      dataKey: col
    }));

    const datosParaPdf = filas.map(row => {
      const obj = {};
      columnasVisible.forEach(col => {
        obj[col] = row[col];
      });
      return obj;
    });

    const { jsPDF } = window.jspdf;
    const doc = new jsPDF({
      orientation: "landscape",
      unit: "pt",
      format: "a4"
    });

    doc.autoTable({
      head: [columnasParaPdf.map(c => c.header)],
      body: datosParaPdf.map(rowObj =>
        columnasParaPdf.map(col => rowObj[col.dataKey])
      ),
      startY: 40,
      styles: { fontSize: 8 },
      headStyles: { fillColor: [41, 128, 185] },
      margin: { top: 40 },
    });

    doc.save("noticias_exportadas.pdf");
  }

  // 5) Función para generar y descargar Excel (.xlsx) con SheetJS
  function exportarExcel() {
    const seleccionadas = $("#tabla-noticias").bootstrapTable("getSelections");
    const filas = seleccionadas.length > 0
      ? seleccionadas
      : $("#tabla-noticias").bootstrapTable("getData");

    if (!filas || filas.length === 0) {
      alert("No hay datos para exportar.");
      return;
    }

    const columnasVisible = [];
    $("#tabla-noticias").find("thead th[data-field]").each(function () {
      const field = $(this).attr("data-field");
      if (field && field !== "state") {
        columnasVisible.push(field);
      }
    });

    const ws_data = [];
    const encabezados = columnasVisible.map(col => col.replace(/_/g, " ").toUpperCase());
    ws_data.push(encabezados);

    filas.forEach(row => {
      const filaArr = columnasVisible.map(col => row[col]);
      ws_data.push(filaArr);
    });

    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(ws_data);
    XLSX.utils.book_append_sheet(wb, ws, "Noticias");

    const wbout = XLSX.write(wb, { bookType: "xlsx", type: "array" });
    const blob = new Blob([wbout], { type: "application/octet-stream" });

    const link = document.createElement("a");
    const url = URL.createObjectURL(blob);
    link.href = url;
    link.download = "noticias_exportadas.xlsx";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  }

  // 6) Función para limpiar filtros
  function limpiarFiltros() {
    $("#tabla-noticias").bootstrapTable('clearFilter');
    $("#tabla-noticias").bootstrapTable('resetSearch');
    
  }

  // 7) Vinculamos los botones de exportación a sus funciones
  $("#exportar-csv").on("click", exportarCSV);
  $("#exportar-excel").on("click", exportarExcel);
  $("#exportar-json").on("click", exportarJSON);
  $("#exportar-pdf").on("click", exportarPDF);
  $("#clear-filters").on("click", limpiarFiltros);

  // 8) Mejorar la funcionalidad de búsqueda
  // Removed custom search keyup handler because search toolbar is disabled

  // 9) Añadir indicador de carga
  $(document).on('load-success.bs.table', '#tabla-noticias', function() {});

  $(document).on('load-error.bs.table', '#tabla-noticias', function() {});
});

// static/js/dashboard_charts.js

document.addEventListener('DOMContentLoaded', () => {
  const chartData = window.CHART_DATA;

  function createChart(canvasId, cfg) {
    const ctx = document.getElementById(canvasId);
    new Chart(ctx, {
      type: cfg.type,
      data: {
        labels: cfg.labels,
        datasets: [{
          // dataset de barras: data = conteos
          // dataset de doughnut: data = porcentajes
          data: cfg.type === 'bar' ? cfg.data : cfg.percent,
          backgroundColor: cfg.type === 'doughnut' ? cfg.colors : cfg.color,
          // solo para doughnut mostramos % en la etiqueta
          label: cfg.type === 'doughnut' ? '%' : undefined
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: cfg.type === 'doughnut'
            ? { position: 'bottom', labels: { boxWidth: 10, padding: 8 } }
            : { display: false },
          tooltip: {
            callbacks: {
              label: context => {
                const v = context.dataset.data[context.dataIndex];
                return cfg.type === 'doughnut'
                  ? `${v}%`
                  : `${v}`;
              }
            }
          }
        },
        ...(cfg.type === 'bar' && {
          indexAxis: 'y',
          scales: {
            x: {
              beginAtZero: true,
              ticks: { font: { size: 10 } }
            },
            y: {
              ticks: { autoSkip: false, font: { size: 10 } }
            }
          }
        })
      }
    });
  }

  Object.entries(chartData).forEach(([key, cfg]) => {
    createChart(`${key}Chart`, cfg);
  });
});

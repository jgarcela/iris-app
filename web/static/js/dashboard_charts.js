// static/js/dashboard_charts.js
// Clay-themed Chart.js rendering with a validated categorical palette.

document.addEventListener('DOMContentLoaded', () => {
  const chartData = window.CHART_DATA;
  if (!chartData || typeof Chart === 'undefined') return;

  const isDark = document.documentElement.getAttribute('data-theme') === 'dark';

  // Validated categorical palette (dataviz skill; worst adjacent CVD ΔE 24.2)
  const CATEGORICAL = isDark
    ? ['#3987e5', '#199e70', '#c98500', '#008300', '#9085e9', '#e66767', '#d55181', '#d95926']
    : ['#2a78d6', '#1baf7a', '#eda100', '#008300', '#4a3aa7', '#e34948', '#e87ba4', '#eb6834'];

  const BAR_HUE = isDark ? '#3987e5' : '#2a78d6';
  const SURFACE = isDark ? '#241c15' : '#ffffff';   // gap color between segments
  const TEXT    = isDark ? '#cfc7bb' : '#55534e';
  const GRID    = isDark ? 'rgba(255,255,255,0.08)' : 'rgba(0,0,0,0.06)';

  // Global Chart.js defaults
  Chart.defaults.font.family = "'Space Grotesk', 'Roobert', Arial, sans-serif";
  Chart.defaults.font.size = 11;
  Chart.defaults.color = TEXT;

  // Assign categorical hues in fixed order (never cycled beyond the palette)
  const paletteFor = (n) => Array.from({ length: n }, (_, i) => CATEGORICAL[i % CATEGORICAL.length]);

  function createChart(canvasId, cfg) {
    const ctx = document.getElementById(canvasId);
    if (!ctx) return;

    const isDoughnut = cfg.type === 'doughnut';
    const values = isDoughnut ? cfg.percent : cfg.data;
    const colors = isDoughnut ? paletteFor(cfg.labels.length) : BAR_HUE;

    new Chart(ctx, {
      type: cfg.type,
      data: {
        labels: cfg.labels,
        datasets: [{
          data: values,
          backgroundColor: colors,
          // 2px surface gap between doughnut segments / rounded bar ends
          borderColor: isDoughnut ? SURFACE : 'transparent',
          borderWidth: isDoughnut ? 2 : 0,
          borderRadius: isDoughnut ? 0 : 4,
          hoverOffset: isDoughnut ? 6 : 0,
          maxBarThickness: 26,
          label: isDoughnut ? '%' : undefined
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        cutout: isDoughnut ? '58%' : undefined,
        layout: { padding: isDoughnut ? 4 : 2 },
        plugins: {
          legend: isDoughnut
            ? {
                position: 'bottom',
                labels: {
                  boxWidth: 10,
                  boxHeight: 10,
                  usePointStyle: true,
                  pointStyle: 'circle',
                  padding: 10,
                  color: TEXT
                }
              }
            : { display: false },
          tooltip: {
            backgroundColor: isDark ? '#1a140f' : '#000000',
            titleColor: '#fff',
            bodyColor: '#fff',
            padding: 10,
            cornerRadius: 8,
            displayColors: true,
            usePointStyle: true,
            callbacks: {
              label: (context) => {
                const v = context.dataset.data[context.dataIndex];
                return isDoughnut ? ` ${v}%` : ` ${v}`;
              }
            }
          }
        },
        ...(cfg.type === 'bar' && {
          indexAxis: 'y',
          scales: {
            x: {
              beginAtZero: true,
              grid: { color: GRID, drawBorder: false },
              ticks: { font: { size: 10 }, color: TEXT }
            },
            y: {
              grid: { display: false, drawBorder: false },
              ticks: { autoSkip: false, font: { size: 10 }, color: TEXT }
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

let groupedDataGlobal = {};
let chart2Instance = null;

async function uploadFile() {
  const fileInput = document.getElementById('csvFile');
  const file = fileInput.files[0];
  if (!file) return alert("Please select a CSV file!");

  const formData = new FormData();
  formData.append('file', file);

  try {
    const response = await fetch('http://127.0.0.1:5000/predict-file', {
      method: 'POST',
      body: formData
    });

    const data = await response.json();
    if (data.error) return alert("❌ " + data.error);

    document.getElementById("accuracy").innerText = `✅ Model Accuracy: ${data.accuracy}%`;

    // Chart 1
    const actualLabels = data.actual_sales.map(d => d.label);
    const actualValues = data.actual_sales.map(d => d.Quantity_Sold);
    const predictedLabels = data.forecast.map(f => f.month);
    const predictedValues = data.forecast.map(f => f.predicted_total);

    new Chart(document.getElementById('chart1'), {
      type: 'line',
      data: {
        labels: [...actualLabels, ...predictedLabels],
        datasets: [
          {
            label: 'Actual Sales',
            data: [...actualValues, null, null, null],
            borderColor: 'green',
            backgroundColor: 'lightgreen',
            fill: false,
            tension: 0.3
          },
          {
            label: 'Predicted Sales',
            data: [...Array(actualValues.length).fill(null), ...predictedValues],
            borderColor: 'blue',
            backgroundColor: 'lightblue',
            borderDash: [5, 5],
            fill: false,
            tension: 0.3
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          title: { display: true, text: 'Overall Sales Trend' }
        },
        scales: {
          y: {
            beginAtZero: true,
            title: { display: true, text: 'Units Sold' }
          },
          x: {
            title: { display: true, text: 'Month' }
          }
        }
      }
    });

    // Chart 2 Setup
    groupedDataGlobal = data.grouped;
    updateGroupedChart();

    // Chart 3
    const catLabels = data.category_change.map(c => c.category);
    const catChanges = data.category_change.map(c => c.change);
    const colors = catChanges.map(v => v >= 0 ? 'green' : 'red');

    new Chart(document.getElementById('chart3'), {
      type: 'bar',
      data: {
        labels: catLabels,
        datasets: [{
          label: 'Change (%)',
          data: catChanges,
          backgroundColor: colors
        }]
      },
      options: {
        indexAxis: 'y',
        plugins: {
          title: { display: true, text: 'Category-wise % Sales Change' }
        },
        scales: {
          x: {
            beginAtZero: true,
            title: { display: true, text: 'Percentage' },
            ticks: {
              callback: value => `${value}%`
            }
          },
          y: {
            title: { display: true, text: 'Category' }
          }
        }
      }
    });

    // Forecast Table
    let tableHTML = "<table border='1' style='margin:auto'><tr><th>Month</th><th>Predicted Sales</th></tr>";
    data.forecast.forEach(f => {
      tableHTML += `<tr><td>${f.month}</td><td>${f.predicted_total}</td></tr>`;
    });
    tableHTML += "</table>";
    document.getElementById("forecastTable").innerHTML = tableHTML;

  } catch (err) {
    alert("❌ Server Error: " + err.message);
  }
}

function updateGroupedChart() {
  const filterType = document.getElementById('filterType').value;
  const data = groupedDataGlobal;
  const labelsSet = new Set();
  const datasetsMap = {};
  const colors = [
    'rgba(75,192,192,0.8)', 'rgba(255,99,132,0.8)',
    'rgba(255,206,86,0.8)', 'rgba(54,162,235,0.8)'
  ];

  for (let key in data) {
    const [cat, gen, reg] = key.split('_');

    let xLabel, groupLabel;
    if (filterType === "category") {
      xLabel = cat;
      groupLabel = `${gen}-${reg}`;
    } else if (filterType === "gender") {
      xLabel = gen;
      groupLabel = `${cat}-${reg}`;
    } else {
      xLabel = reg;
      groupLabel = `${cat}-${gen}`;
    }

    labelsSet.add(xLabel);
    if (!datasetsMap[groupLabel]) datasetsMap[groupLabel] = {};
    datasetsMap[groupLabel][xLabel] = data[key];
  }

  const labels = Array.from(labelsSet); // 👈 Actual readable labels
  const datasets = [];

  let i = 0;
  for (const [group, values] of Object.entries(datasetsMap)) {
    datasets.push({
      label: group,
      data: labels.map(label => values[label] || 0),
      backgroundColor: colors[i % colors.length]
    });
    i++;
  }

  if (chart2Instance) chart2Instance.destroy();

  chart2Instance = new Chart(document.getElementById('chart2'), {
    type: 'bar',
    data: {
      labels: labels,
      datasets: datasets
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        title: {
          display: true,
          text: `Grouped Forecast by ${filterType.toUpperCase()}`
        },
        tooltip: {
          callbacks: {
            label: ctx => `${ctx.dataset.label}: ${ctx.parsed.y} units`
          }
        },
        datalabels: {
          anchor: 'end',
          align: 'top',
          color: 'black',
          formatter: val => val
        }
      },
      scales: {
        x: {
          title: {
            display: true,
            text: filterType.charAt(0).toUpperCase() + filterType.slice(1)
          },
          ticks: {
            autoSkip: false,
            callback: (val, i) => labels[i]
          }
        },
        y: {
          beginAtZero: true,
          title: { display: true, text: 'Units Sold' }
        }
      }
    },
   
  });
}

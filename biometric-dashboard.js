/* AGING?F***THAT! - Standardised Biometric Dashboard chart renderer
   Used by: biomarkers.html (Lee's Data), bio-age-calculator.html (illustration),
   Age_Reversal_Client_Pack (per-client test history).
   Requires Chart.js to already be loaded on the page.

   history: array of { date:'YYYY-MM-DD', chronoAge:Number, bioAge:Number }, any order.
   Chronological Age line: blue.
   Biological Age line: green on any segment ending at or below chrono age that date,
                         red on any segment ending above chrono age that date.
*/
function renderBiometricChart(canvasId, history) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === 'undefined' || !history || !history.length) return null;

  const sorted = [...history].sort((a, b) => new Date(a.date) - new Date(b.date));
  const labels = sorted.map(h => h.date);
  const chronoVals = sorted.map(h => Number(h.chronoAge));
  const bioVals = sorted.map(h => Number(h.bioAge));

  const ctx = canvas.getContext('2d');
  if (canvas._chartInstance) canvas._chartInstance.destroy();

  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Chronological Age',
          data: chronoVals,
          borderColor: '#173f6d',
          backgroundColor: '#173f6d',
          borderWidth: 2,
          pointRadius: 4,
          pointBackgroundColor: '#173f6d',
          fill: false,
          tension: 0
        },
        {
          label: 'Biological Age',
          data: bioVals,
          borderWidth: 3,
          pointRadius: 4,
          fill: false,
          tension: 0,
          segment: {
            borderColor: c => (bioVals[c.p1DataIndex] <= chronoVals[c.p1DataIndex]) ? '#2E7D32' : '#B3261E'
          },
          pointBackgroundColor: c => (bioVals[c.dataIndex] <= chronoVals[c.dataIndex]) ? '#2E7D32' : '#B3261E'
        }
      ]
    },
    options: {
      responsive: true,
      animation: false,
      scales: {
        x: { title: { display: true, text: 'Date of Analysis' } },
        y: { title: { display: true, text: 'Age (years)' } }
      },
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 14, font: { size: 11 } } },
        tooltip: {
          callbacks: {
            label: c => `${c.dataset.label}: ${Number(c.parsed.y).toFixed(1)} yrs`
          }
        }
      }
    }
  });
  canvas._chartInstance = chart;
  return chart;
}

/* Shared scoring core, so Lee's Data, the Calculator, and the Client Pack
   all convert biomarkers to a Biological Age the same way. */
function scoreBiomarker(field, val) {
  const v = parseFloat(val);
  if (isNaN(v)) return null;
  const [oMin, oMax] = field.optimal;
  if (field.dir === 'lower_better') {
    if (v <= oMax) return 100;
    const [, gMax] = field.good; if (v <= gMax) return 75;
    const [, wMax] = field.warn; if (v <= wMax) return 40;
    return 10;
  } else if (field.dir === 'higher_better') {
    if (v >= oMin) return 100;
    const [gMin] = field.good; if (v >= gMin) return 75;
    const [wMin] = field.warn; if (v >= wMin) return 40;
    return 10;
  } else {
    if (v >= oMin && v <= oMax) return 100;
    const dist = Math.min(Math.abs(v - oMin), Math.abs(v - oMax));
    const range = oMax - oMin;
    if (dist <= range * 0.3) return 75;
    if (dist <= range * 0.8) return 40;
    return 10;
  }
}

function computeBioAge(fields, values, chronAge) {
  let totalWeight = 0, totalScore = 0;
  for (const [id, field] of Object.entries(fields)) {
    const score = scoreBiomarker(field, values[id]);
    if (score !== null) {
      totalWeight += field.weight;
      totalScore += score * field.weight;
    }
  }
  if (totalWeight === 0) return null;
  const avgScore = totalScore / totalWeight;
  return Math.round(chronAge - ((avgScore - 50) / 50) * 17);
}

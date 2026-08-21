/* AGING?F***THAT! - Standardised Biometric Dashboard chart renderer
   Used by: biomarkers.html (Lee's Data), bio-age-calculator.html (illustration),
   Age_Reversal_Client_Pack (per-client test history).
   Requires Chart.js to already be loaded on the page.
*/

const _glowPlugin = {
  id: 'bioGlow',
  beforeDatasetDraw(chart, args) {
    if (!chart.data.datasets[args.index]._glow) return;
    chart.ctx.save();
    chart.ctx.shadowBlur = 10;
    chart.ctx.shadowColor = chart.data.datasets[args.index]._glowColor || 'rgba(0,0,0,0.4)';
  },
  afterDatasetDraw(chart) {
    chart.ctx.restore();
  }
};

const _endLabelPlugin = {
  id: 'bioEndLabels',
  afterDatasetsDraw(chart) {
    const { ctx } = chart;
    chart.data.datasets.forEach((ds, i) => {
      if (!ds._endLabel) return;
      const meta = chart.getDatasetMeta(i);
      const last = meta.data[meta.data.length - 1];
      if (!last) return;
      ctx.save();
      ctx.font = '600 11px Rajdhani, sans-serif';
      ctx.fillStyle = ds._endLabelColor || ds.borderColor;
      ctx.textAlign = 'left';
      ctx.fillText(ds._endLabel, last.x + 8, last.y + (ds._endLabelOffset || 0));
      ctx.restore();
    });
  }
};

const _pointValuePlugin = {
  id: 'bioPointValues',
  afterDatasetsDraw(chart) {
    const { ctx } = chart;
    chart.data.datasets.forEach((ds, dsIndex) => {
      if (!ds._showPointValues) return;
      const meta = chart.getDatasetMeta(dsIndex);
      meta.data.forEach((point, i) => {
        const val = ds.data[i];
        if (val === null || val === undefined) return;
        ctx.save();
        ctx.font = '500 9px "Share Tech Mono", monospace';
        ctx.fillStyle = '#8A7666';
        ctx.textAlign = 'center';
        ctx.fillText(Math.round(val * 10) / 10, point.x, point.y + 20);
        ctx.restore();
      });
    });
  }
};

if (typeof Chart !== 'undefined') {
  Chart.register(_glowPlugin, _endLabelPlugin, _pointValuePlugin);
}

function renderBiometricChart(canvasId, history, opts) {
  const canvas = document.getElementById(canvasId);
  if (!canvas || typeof Chart === 'undefined' || !history || !history.length) return null;
  opts = opts || {};

  const sorted = [...history].sort((a, b) => new Date(a.sortDate || a.date) - new Date(b.sortDate || b.date));
  const labels = sorted.map(h => h.date);
  const chronoVals = sorted.map(h => Number(h.chronoAge));
  const bioVals = sorted.map(h => Number(h.bioAge));
  const endGood = bioVals[bioVals.length - 1] <= chronoVals[chronoVals.length - 1];

  const ctx = canvas.getContext('2d');
  if (canvas._chartInstance) canvas._chartInstance.destroy();

  const chart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: labels,
      datasets: [
        {
          label: 'Chronological age',
          data: chronoVals,
          borderColor: '#173f6d',
          backgroundColor: '#173f6d',
          borderWidth: 2.5,
          pointRadius: 4,
          pointBackgroundColor: '#173f6d',
          fill: false,
          tension: 0,
          _glow: true,
          _glowColor: 'rgba(23,63,109,0.45)',
          _endLabel: 'Chrono',
          _endLabelColor: '#185FA5',
          _endLabelOffset: -8
        },
        {
          label: 'Biological age',
          data: bioVals,
          borderWidth: 3,
          pointRadius: 4,
          fill: false,
          tension: 0,
          _glow: true,
          _glowColor: endGood ? 'rgba(99,153,34,0.55)' : 'rgba(226,75,74,0.55)',
          _showPointValues: true,
          _endLabel: 'Bio',
          _endLabelColor: endGood ? '#27500A' : '#791F1F',
          _endLabelOffset: 16,
          segment: {
            borderColor: c => (bioVals[c.p1DataIndex] <= chronoVals[c.p1DataIndex]) ? '#639922' : '#E24B4A'
          },
          pointBackgroundColor: c => (bioVals[c.dataIndex] <= chronoVals[c.dataIndex]) ? '#639922' : '#E24B4A'
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: false,
      layout: { padding: { top: 10, right: 44, bottom: 4 } },
      plugins: {
        title: {
          display: true,
          text: opts.title || 'Age gap: chrono vs bio age',
          font: { family: 'Rajdhani', size: 16, weight: '700' },
          color: '#3E1C01',
          align: 'start',
          padding: { bottom: 14 }
        },
        legend: { display: false },
        tooltip: {
          callbacks: { label: c => `${c.dataset.label}: ${Number(c.parsed.y).toFixed(1)} yrs` }
        }
      },
      scales: {
        x: { title: { display: false }, grid: { display: false } },
        y: { title: { display: true, text: 'Age (years)' } }
      }
    },
    plugins: [_glowPlugin, _endLabelPlugin, _pointValuePlugin]
  });

  canvas._chartInstance = chart;
  return chart;
}

/* Dash-panel: legend + dynamic "X years biologically younger/older" tile,
   rendered as HTML into a container placed right after the canvas.
   Legend indent (44px) lines the first dot up under the chart's y-axis. */
function renderBiometricPanel(panelId, history) {
  const el = document.getElementById(panelId);
  if (!el || !history || !history.length) { if (el) el.innerHTML = ''; return; }
  const sorted = [...history].sort((a, b) => new Date(a.sortDate || a.date) - new Date(b.sortDate || b.date));
  const latest = sorted[sorted.length - 1];
  const delta = Math.round((latest.bioAge - latest.chronoAge) * 10) / 10;
  const isYounger = delta <= 0;
  const tileText = (isYounger ? '\u2212' : '+') + Math.abs(delta) + ' yrs';
  const tileCaption = isYounger ? 'biologically younger' : 'biologically older';
  const tileBg = isYounger ? '#EAF3DE' : '#FCEBEB';
  const tileNum = isYounger ? '#173404' : '#501313';
  const tileCap = isYounger ? '#27500A' : '#791F1F';
  const bioColor = isYounger ? '#639922' : '#E24B4A';

  el.innerHTML =
    '<div style="border:1px solid #DCE8F1;border-radius:10px;padding:14px 16px 16px 44px;margin-top:6px;">' +
      '<div style="display:flex;gap:22px;flex-wrap:wrap;margin-bottom:12px;">' +
        '<span style="display:flex;align-items:center;gap:6px;font-size:12px;color:#8A7666;">' +
          '<span style="width:10px;height:10px;border-radius:50%;background:#173f6d;display:inline-block;"></span>Chronological age</span>' +
        '<span style="display:flex;align-items:center;gap:6px;font-size:12px;color:#8A7666;">' +
          '<span style="width:10px;height:10px;border-radius:50%;background:' + bioColor + ';display:inline-block;"></span>Biological age</span>' +
      '</div>' +
      '<div style="background:' + tileBg + ';border-radius:8px;padding:8px 14px;display:inline-block;">' +
        '<div style="font-family:\'Rajdhani\',sans-serif;font-weight:700;font-size:15px;color:' + tileNum + ';">' + tileText + '</div>' +
        '<div style="font-size:10px;color:' + tileCap + ';">' + tileCaption + '</div>' +
      '</div>' +
    '</div>';
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

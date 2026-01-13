let chartType = "line";
let enabled = new Set();
let selected = [];

function yyyy_mm_dd(d) {
  return d.toISOString().slice(0,10);
}

function setDefaults() {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 1);
  document.querySelector("#from").value = yyyy_mm_dd(start);
  document.querySelector("#to").value = yyyy_mm_dd(now);
}

async function loadSelected() {
  const res = await fetch("/api/selected-tickers");
  selected = await res.json();
  enabled = new Set(selected.map(r => r.ticker)); // default: all on
}

function renderToggles() {
  const div = document.querySelector("#ticker-toggles");
  div.innerHTML = "";
  selected.forEach(r => {
    const b = document.createElement("button");
    const on = enabled.has(r.ticker);
    b.textContent = `${on ? "ON " : "OFF "} ${r.ticker}`;
    b.addEventListener("click", async () => {
      if (enabled.has(r.ticker)) enabled.delete(r.ticker);
      else enabled.add(r.ticker);
      renderToggles();
      await renderChart();
    });
    div.appendChild(b);
  });
}

async function fetchBars(ticker) {
  const from = document.querySelector("#from").value;
  const to = document.querySelector("#to").value;
  const tf = document.querySelector("#tf").value;

  const res = await fetch(`/api/aggregates?ticker=${encodeURIComponent(ticker)}&from=${from}T00:00:00Z&to=${to}T23:59:59Z&tf=${encodeURIComponent(tf)}`);
  const data = await res.json();
  return data.bars;
}

async function renderChart() {
  const tickers = selected.map(r => r.ticker).filter(t => enabled.has(t));
  const traces = [];

  for (const t of tickers) {
    const bars = await fetchBars(t);
    const x = bars.map(b => b.ts);
    if (chartType === "line") {
      traces.push({
        type: "scatter",
        mode: "lines",
        name: t,
        x,
        y: bars.map(b => b.close),
      });
    } else {
      traces.push({
        type: "candlestick",
        name: t,
        x,
        open: bars.map(b => b.open),
        high: bars.map(b => b.high),
        low: bars.map(b => b.low),
        close: bars.map(b => b.close),
      });
    }
  }

  Plotly.newPlot("chart", traces, {margin:{t:30}, xaxis:{title:"Time"}, yaxis:{title:"Price"}});
}

document.querySelector("#line").addEventListener("click", async () => { chartType="line"; await renderChart(); });
document.querySelector("#candle").addEventListener("click", async () => { chartType="candle"; await renderChart(); });
document.querySelector("#from").addEventListener("change", renderChart);
document.querySelector("#to").addEventListener("change", renderChart);
document.querySelector("#tf").addEventListener("change", renderChart);

(async function init(){
  setDefaults();
  await loadSelected();
  renderToggles();
  await renderChart();
})();

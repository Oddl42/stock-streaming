async function loadSelected() {
  const res = await fetch("/api/selected-tickers");
  const rows = await res.json();
  const sel = document.querySelector("#ticker");
  sel.innerHTML = "";
  rows.forEach(r => {
    const opt = document.createElement("option");
    opt.value = r.ticker;
    opt.textContent = r.ticker;
    sel.appendChild(opt);
  });
}

async function refresh() {
  const t = document.querySelector("#ticker").value;
  if (!t) return;

  const latestRes = await fetch(`/api/streaming/latest?ticker=${encodeURIComponent(t)}`);
  const latest = await latestRes.json();
  document.querySelector("#latest").textContent = JSON.stringify(latest, null, 2);

  const barsRes = await fetch(`/api/streaming/bars?ticker=${encodeURIComponent(t)}&limit=5000`);
  const bars = (await barsRes.json()).bars;

  const x = bars.map(b => b.ts).reverse();
  const trace = {
    type: "candlestick",
    name: t,
    x,
    open: bars.map(b => b.open).reverse(),
    high: bars.map(b => b.high).reverse(),
    low: bars.map(b => b.low).reverse(),
    close: bars.map(b => b.close).reverse(),
  };
  Plotly.newPlot("stream-chart", [trace], {margin:{t:30}});
}

document.querySelector("#refresh").addEventListener("click", refresh);

// Start/Stop: Stub (wird in Teil C durch SparkOperator ersetzt)
document.querySelector("#start").addEventListener("click", async () => {
  await fetch("/api/streaming/start", {method:"POST"});
});
document.querySelector("#stop").addEventListener("click", async () => {
  await fetch("/api/streaming/stop", {method:"POST"});
});

(async function init(){
  await loadSelected();
  setInterval(refresh, 2000); // Polling
})();

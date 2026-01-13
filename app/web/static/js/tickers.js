let allTickers = [];
let selectedSet = new Set();

async function loadSelected() {
  const res = await fetch("/api/selected-tickers");
  const rows = await res.json();
  selectedSet = new Set(rows.map(r => r.ticker));
}

function renderTable(filterText = "") {
  const tbody = document.querySelector("#tickers tbody");
  tbody.innerHTML = "";

  const ft = filterText.trim().toUpperCase();

  allTickers
    .filter(r => !ft || (r.ticker || "").toUpperCase().includes(ft) || (r.name || "").toUpperCase().includes(ft))
    .forEach(r => {
      const tr = document.createElement("tr");
      const checked = selectedSet.has(r.ticker);

      tr.innerHTML = `
        <td><input type="checkbox" data-ticker="${r.ticker}" ${checked ? "checked" : ""}></td>
        <td>${r.name ?? ""}</td>
        <td>${r.ticker ?? ""}</td>
        <td>${r.market ?? ""}</td>
        <td>${r.primary_exchange ?? ""}</td>
        <td>${r.locale ?? ""}</td>
      `;
      tbody.appendChild(tr);
    });

  tbody.querySelectorAll("input[type=checkbox]").forEach(cb => {
    cb.addEventListener("change", (e) => {
      const t = e.target.dataset.ticker;
      if (e.target.checked) selectedSet.add(t);
      else selectedSet.delete(t);
    });
  });
}

async function reload() {
  await loadSelected();
  const res = await fetch("/api/tickers");
  allTickers = await res.json();
  renderTable(document.querySelector("#search").value);
}

async function save() {
  const rows = allTickers
    .filter(r => selectedSet.has(r.ticker))
    .map(r => ({
      ticker: r.ticker,
      name: r.name,
      market: r.market,
      primary_exchange: r.primary_exchange,
      locale: r.locale
    }));

  await fetch("/api/selected-tickers", {
    method: "POST",
    headers: {"Content-Type":"application/json"},
    body: JSON.stringify({rows})
  });
  alert("Saved");
}

document.querySelector("#reload").addEventListener("click", reload);
document.querySelector("#save").addEventListener("click", save);
document.querySelector("#search").addEventListener("input", (e) => renderTable(e.target.value));

reload();

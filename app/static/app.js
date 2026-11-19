document.addEventListener("DOMContentLoaded", () => {
  const queryForm = document.getElementById("query-form");
  const questionInput = document.getElementById("question-input");
  const companySelect = document.getElementById("company-select");
  const yearSelect = document.getElementById("year-select");
  const submitBtn = document.getElementById("submit-btn");
  const errorBox = document.getElementById("error-box");
  const resultsBox = document.getElementById("results-box");
  const metaModel = document.getElementById("meta-model");
  const metaLatency = document.getElementById("meta-latency");
  const metaTokens = document.getElementById("meta-tokens");
  const answerText = document.getElementById("answer-text");
  const citationsTitle = document.getElementById("citations-title");
  const citationsList = document.getElementById("citations-list");

  let corpusData = {};

  // 1. Fetch available companies & years from backend
  async function loadCorpus() {
    try {
      const res = await fetch("/corpus");
      if (!res.ok) return;
      corpusData = await res.json();
      populateDropdowns();
    } catch (err) {
      console.warn("Failed to load corpus metadata:", err);
    }
  }

  function populateDropdowns() {
    // Populate Companies
    const companies = Object.keys(corpusData).sort();
    companySelect.innerHTML = '<option value="">All Companies</option>';
    companies.forEach((comp) => {
      const opt = document.createElement("option");
      opt.value = comp;
      opt.textContent = comp;
      companySelect.appendChild(opt);
    });

    updateYears();
  }

  function updateYears() {
    const selectedCompany = companySelect.value;
    let years = [];

    if (selectedCompany && corpusData[selectedCompany]) {
      years = [...corpusData[selectedCompany]].sort((a, b) => b - a);
    } else {
      const yearSet = new Set();
      Object.values(corpusData).forEach((list) => {
        list.forEach((y) => yearSet.add(y));
      });
      years = Array.from(yearSet).sort((a, b) => b - a);
    }

    const currentYear = yearSelect.value;
    yearSelect.innerHTML = '<option value="">All Years</option>';
    years.forEach((y) => {
      const opt = document.createElement("option");
      opt.value = y.toString();
      opt.textContent = y;
      yearSelect.appendChild(opt);
    });

    if (currentYear && years.includes(parseInt(currentYear, 10))) {
      yearSelect.value = currentYear;
    } else {
      yearSelect.value = "";
    }
  }

  companySelect.addEventListener("change", updateYears);

  // 2. Handle Query Submission
  queryForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = questionInput.value.trim();
    if (!question) return;

    errorBox.classList.add("hidden");
    resultsBox.classList.add("hidden");
    submitBtn.disabled = true;
    submitBtn.textContent = "Retrieving & Generating...";

    const payload = { question };
    if (companySelect.value) {
      payload.tickers = [companySelect.value];
    }
    if (yearSelect.value) {
      payload.year = parseInt(yearSelect.value, 10);
    }

    try {
      const res = await fetch("/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!res.ok) {
        const errorData = await res.json().catch(() => ({}));
        const msg = errorData.detail || `Query failed with status ${res.status}`;
        throw new Error(msg);
      }

      const data = await res.json();
      displayResults(data);
    } catch (err) {
      errorBox.textContent = err.message || "An error occurred while querying.";
      errorBox.classList.remove("hidden");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Ask";
    }
  });

  function displayResults(data) {
    metaModel.textContent = data.model || "-";
    metaLatency.textContent = (data.latency_ms || 0) + "ms";
    metaTokens.textContent = data.tokens || 0;
    answerText.textContent = data.answer || "";

    const citations = data.citations || [];
    citationsTitle.textContent = `Citations (${citations.length})`;
    citationsList.innerHTML = "";

    citations.forEach((c) => {
      const item = document.createElement("div");
      item.className = "citation-item";

      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "citation-header";
      btn.innerHTML = `
        <div class="citation-meta">
          <span class="citation-index">[${c.n}]</span>
          <span><strong>${c.company}</strong> - ${c.doc} (FY${c.year})</span>
          <span class="citation-page-badge">Page ${c.page}</span>
        </div>
        <span class="citation-chevron">▼</span>
      `;

      const body = document.createElement("div");
      body.className = "citation-body hidden";
      body.textContent = c.text;

      btn.addEventListener("click", () => {
        const isHidden = body.classList.contains("hidden");
        body.classList.toggle("hidden", !isHidden);
        btn.querySelector(".citation-chevron").textContent = isHidden ? "▲" : "▼";
      });

      item.appendChild(btn);
      item.appendChild(body);
      citationsList.appendChild(item);
    });

    resultsBox.classList.remove("hidden");
  }

  loadCorpus();
});

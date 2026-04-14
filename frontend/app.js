const analysisForm = document.getElementById("analysisForm");
const textInput = document.getElementById("textInput");
const fileInput = document.getElementById("fileInput");
const fileLabel = document.getElementById("fileLabel");
const analyzeButton = document.getElementById("analyzeButton");
const emptyState = document.getElementById("emptyState");
const loadingState = document.getElementById("loadingState");
const results = document.getElementById("results");
const correctedText = document.getElementById("correctedText");
const summaryGrid = document.getElementById("summaryGrid");
const pipelineGrid = document.getElementById("pipelineGrid");
const spellingList = document.getElementById("spellingList");
const grammarList = document.getElementById("grammarList");
const tokenList = document.getElementById("tokenList");
const systemStatus = document.getElementById("systemStatus");
const metricWords = document.getElementById("metricWords");
const metricMisspellings = document.getElementById("metricMisspellings");

function setLoadingState(isLoading) {
  analyzeButton.disabled = isLoading;
  analyzeButton.classList.toggle("is-loading", isLoading);
  if (isLoading) systemStatus.textContent = "Processing";
  emptyState.classList.toggle("hidden", isLoading || !results.classList.contains("hidden"));
  loadingState.classList.toggle("hidden", !isLoading);
}

function renderSummary(summary) {
  const cards = [
    ["Words", summary.wordCount],
    ["Sentences", summary.sentenceCount],
    ["Misspellings", summary.misspellingCount],
    ["Grammar issues", summary.grammarIssueCount]
  ];

  summaryGrid.innerHTML = cards
    .map(
      ([label, value]) => `
        <article class="summary-card">
          <span class="summary-value">${value}</span>
          <span class="summary-label">${label}</span>
        </article>
      `
    )
    .join("");
}

function renderPipeline(phases) {
  pipelineGrid.innerHTML = phases
    .map(
      (phase) => `
        <article class="pipeline-card">
          <h4>${phase.phase}</h4>
          <p>${phase.description}</p>
          <code>${JSON.stringify(phase.result)}</code>
        </article>
      `
    )
    .join("");
}

function renderIssues(container, items, type) {
  if (!items.length) {
    container.innerHTML =
      `<div class="issue-item"><div class="issue-copy"><strong>No ${type} issues</strong>` +
      `<span class="issue-copy">The system did not flag any ${type} problems in this pass.</span></div></div>`;
    return;
  }

  container.innerHTML = items
    .map((item) => {
      const title = item.word || item.type || "Issue";
      const message = item.message || `Suggested correction for "${item.word}".`;
      const suggestion = item.suggestion ? `Suggestion: ${item.suggestion}` : "No suggestion available";

      return `
        <article class="issue-item">
          <div class="issue-copy">
            <strong>${title}</strong>
            <div>${message}</div>
          </div>
          <div class="issue-suggestion">${suggestion}</div>
        </article>
      `;
    })
    .join("");
}

function renderTokens(tokens) {
  tokenList.innerHTML = tokens
    .map(
      (token) => `
        <article class="token-chip">
          <span class="token-type">${token.type}</span>
          <strong>${token.value.replace(/</g, "&lt;").replace(/>/g, "&gt;")}</strong>
          <span class="token-position">#${token.position}</span>
        </article>
      `
    )
    .join("");
}

function renderResults(payload) {
  correctedText.textContent = payload.correctedText;
  renderSummary(payload.summary);
  renderPipeline(payload.compilerPipeline);
  renderIssues(spellingList, payload.spellingIssues, "spelling");
  renderIssues(grammarList, payload.grammarIssues, "grammar");
  renderTokens(payload.tokens);
  metricWords.textContent = payload.summary.wordCount;
  metricMisspellings.textContent = payload.summary.misspellingCount;
  emptyState.classList.add("hidden");
  loadingState.classList.add("hidden");
  results.classList.remove("hidden");
}

function renderError(message) {
  emptyState.classList.remove("hidden");
  loadingState.classList.add("hidden");
  results.classList.add("hidden");
  systemStatus.textContent = "Error";
  emptyState.innerHTML = `<h3>Analysis failed</h3><p>${message}</p>`;
}

analysisForm.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!textInput.value.trim()) {
    systemStatus.textContent = "Add text";
    textInput.focus();
    return;
  }

  setLoadingState(true);

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: textInput.value })
    });

    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Analysis failed.");

    renderResults(payload);
    systemStatus.textContent = "Report ready";
  } catch (error) {
    renderError(error.message);
  } finally {
    setLoadingState(false);
  }
});

fileInput.addEventListener("change", async (event) => {
  const [file] = event.target.files;
  if (!file) {
    fileLabel.textContent = "No file selected";
    return;
  }

  fileLabel.textContent = file.name;
  textInput.value = await file.text();
  systemStatus.textContent = "File loaded";
});

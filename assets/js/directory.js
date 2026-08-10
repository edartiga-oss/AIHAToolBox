/* Tool directory: search, faceted filtering, and shareable URLs.
   Rows are rendered at build time, so the full list works without JavaScript;
   this script only hides and shows what is already there. */
(function () {
  "use strict";

  var table = document.getElementById("tools-table");
  if (!table) return;

  var rows = Array.prototype.slice.call(document.querySelectorAll("#tools-body tr"));
  var input = document.getElementById("search-input");
  var clearBtn = document.getElementById("search-clear");
  var resetBtn = document.getElementById("reset-filters");
  var countEl = document.getElementById("results-count");
  var emptyEl = document.getElementById("empty-state");
  var chips = Array.prototype.slice.call(document.querySelectorAll(".chip"));

  var FACETS = ["type", "hazard", "route", "category"];
  var state = { q: "" };
  FACETS.forEach(function (name) { state[name] = ""; });

  function matches(row) {
    if (state.q && row.dataset.search.indexOf(state.q) === -1) return false;
    for (var i = 0; i < FACETS.length; i++) {
      var name = FACETS[i];
      var wanted = state[name];
      if (!wanted) continue;
      var values = (row.dataset[name] || "").split("|");
      if (values.indexOf(wanted) === -1) return false;
    }
    return true;
  }

  function describe(shown) {
    if (shown === rows.length && !state.q) return "Showing all " + rows.length + " tools";
    var text = "Showing " + shown + " of " + rows.length + " tools";
    if (state.q) text += ' for "' + state.q + '"';
    return text;
  }

  function isFiltered() {
    return Boolean(state.q) || FACETS.some(function (name) { return state[name]; });
  }

  function syncUrl() {
    var params = new URLSearchParams();
    if (state.q) params.set("q", state.q);
    FACETS.forEach(function (name) {
      if (state[name]) params.set(name, state[name]);
    });
    var query = params.toString();
    var url = window.location.pathname + (query ? "?" + query : "") + window.location.hash;
    window.history.replaceState(null, "", url);
  }

  function apply(updateUrl) {
    var shown = 0;
    rows.forEach(function (row) {
      var ok = matches(row);
      row.hidden = !ok;
      if (ok) shown++;
    });
    countEl.textContent = describe(shown);
    emptyEl.hidden = shown !== 0;
    table.parentNode.hidden = shown === 0;
    resetBtn.hidden = !isFiltered();
    clearBtn.classList.toggle("is-visible", Boolean(input.value));
    if (updateUrl !== false) syncUrl();
  }

  function setChipState() {
    chips.forEach(function (chip) {
      var active = state[chip.dataset.filter] === chip.dataset.value;
      chip.setAttribute("aria-pressed", active ? "true" : "false");
    });
  }

  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      state[chip.dataset.filter] = chip.dataset.value;
      setChipState();
      apply();
    });
  });

  input.addEventListener("input", function () {
    state.q = input.value.trim().toLowerCase();
    apply();
  });

  clearBtn.addEventListener("click", function () {
    input.value = "";
    state.q = "";
    apply();
    input.focus();
  });

  resetBtn.addEventListener("click", function () {
    input.value = "";
    state.q = "";
    FACETS.forEach(function (name) { state[name] = ""; });
    setChipState();
    apply();
    input.focus();
  });

  // Restore state from the query string so filtered views can be linked to.
  (function restore() {
    var params = new URLSearchParams(window.location.search);
    var q = params.get("q");
    if (q) {
      state.q = q.trim().toLowerCase();
      input.value = q;
    }
    FACETS.forEach(function (name) {
      var value = (params.get(name) || "").toLowerCase();
      if (!value) return;
      var known = chips.some(function (chip) {
        return chip.dataset.filter === name && chip.dataset.value === value;
      });
      if (known) state[name] = value;
    });
    setChipState();
    apply(false);
  })();
})();

/* Tool directory: search, faceted filtering, and shareable URLs.
   Rows are rendered at build time, so the full list works without JavaScript;
   this script only hides and shows what is already there.

   Every filter control — the chip rows and the Category column dropdown — is a
   [data-filter][data-value] element, so one click handler drives them all. Values
   are lowercase to match the lowercased data-* attributes on each row. */
(function () {
  "use strict";

  var table = document.getElementById("tools-table");
  if (!table) return;

  var rows = Array.prototype.slice.call(document.querySelectorAll("#tools-body tr"));
  var controls = Array.prototype.slice.call(document.querySelectorAll("[data-filter][data-value]"));
  var input = document.getElementById("search-input");
  var clearBtn = document.getElementById("search-clear");
  var resetBtn = document.getElementById("reset-filters");
  var countEl = document.getElementById("results-count");
  var emptyEl = document.getElementById("empty-state");

  var dropdown = document.getElementById("category-dropdown");
  var dropdownBtn = document.getElementById("category-filter-btn");
  var dropdownLabel = document.getElementById("category-filter-label");

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

  function labelFor(value) {
    // Human text of a category option, for the dropdown button.
    var opt = document.querySelector('.filter-option[data-value="' + value + '"] span');
    return opt ? opt.textContent : value;
  }

  function syncControls() {
    controls.forEach(function (control) {
      var active = state[control.dataset.filter] === control.dataset.value;
      control.setAttribute("aria-pressed", active ? "true" : "false");
    });
    if (dropdownBtn) {
      var chosen = state.category;
      dropdownBtn.classList.toggle("is-active", Boolean(chosen));
      if (dropdownLabel) dropdownLabel.textContent = chosen ? labelFor(chosen) : "Filter";
    }
  }

  function syncUrl() {
    var params = new URLSearchParams();
    if (state.q) params.set("q", state.q);
    FACETS.forEach(function (name) {
      if (state[name]) params.set(name, state[name]);
    });
    var query = params.toString();
    window.history.replaceState(null, "", window.location.pathname + (query ? "?" + query : "") + window.location.hash);
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
    if (clearBtn) clearBtn.classList.toggle("is-visible", Boolean(input.value));
    syncControls();
    if (updateUrl !== false) syncUrl();
  }

  // One handler for every chip and dropdown option.
  controls.forEach(function (control) {
    control.addEventListener("click", function () {
      state[control.dataset.filter] = control.dataset.value;
      closeDropdown();
      apply();
    });
  });

  // Category dropdown open/close.
  function openDropdown() {
    if (!dropdown) return;
    dropdown.classList.add("is-open");
    dropdownBtn.setAttribute("aria-expanded", "true");
  }
  function closeDropdown() {
    if (!dropdown || !dropdown.classList.contains("is-open")) return;
    dropdown.classList.remove("is-open");
    dropdownBtn.setAttribute("aria-expanded", "false");
  }
  if (dropdownBtn) {
    dropdownBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      if (dropdown.classList.contains("is-open")) closeDropdown();
      else openDropdown();
    });
    document.addEventListener("click", function (e) {
      if (!e.target.closest(".column-filter")) closeDropdown();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeDropdown();
    });
  }

  if (input) {
    input.addEventListener("input", function () {
      state.q = input.value.trim().toLowerCase();
      apply();
    });
  }
  if (clearBtn) {
    clearBtn.addEventListener("click", function () {
      input.value = "";
      state.q = "";
      apply();
      input.focus();
    });
  }

  resetBtn.addEventListener("click", function () {
    if (input) input.value = "";
    state.q = "";
    FACETS.forEach(function (name) { state[name] = ""; });
    apply();
    if (input) input.focus();
  });

  // Restore state from the query string so filtered views can be linked to.
  (function restore() {
    var params = new URLSearchParams(window.location.search);
    var q = params.get("q");
    if (q && input) {
      state.q = q.trim().toLowerCase();
      input.value = q;
    }
    FACETS.forEach(function (name) {
      var value = (params.get(name) || "").toLowerCase();
      if (!value) return;
      var known = controls.some(function (c) {
        return c.dataset.filter === name && c.dataset.value === value;
      });
      if (known) state[name] = value;
    });
    apply(false);
  })();
})();

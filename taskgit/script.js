function generateColor(type) {
  const hash = Array.from(type).reduce((acc, char) => acc + char.charCodeAt(0), 0);
  const hue = hash % 360;
  const saturation = 80;
  const lightness = 50;
  return `hsl(${hue}, ${saturation}%, ${lightness}%)`;
}
// Give each label a unique color.
const labels = Array.from(document.querySelectorAll('.label')).sort((a, b) => a.textContent.localeCompare(b.textContent));
for (const label of labels) {
  label.style.backgroundColor = generateColor(label.textContent);
}

// Observe changes to the DOM and apply generateColor to newly added labels
const observer = new MutationObserver((mutations) => {
  mutations.forEach((mutation) => {
    if (mutation.type === 'childList') {
      const newLabels = Array.from(mutation.addedNodes).filter(node => node.classList?.contains('label'));
      for (const label of newLabels) {
        label.style.backgroundColor = generateColor(label.textContent);
      }
    }
  });
});

const observerOptions = {
  childList: true,
  subtree: true
};

observer.observe(document.documentElement, observerOptions);


document.addEventListener('DOMContentLoaded', function() {
  document.body.addEventListener("click", function (event) {
    if (event.target.matches(".meta-item")) {
      const itemKey = event.target.classList[1];
      itemValue = event.target.textContent
      if (itemValue.includes(":")) {
        itemValue = itemValue.split(": ")[1];
      }
      if (itemKey && itemValue) {
        updateFilter(itemKey, itemValue);
      }
    }
  });

  var clearFilterButton = document.getElementById("clear-filter");
    clearFilterButton.addEventListener("click", function () {
      clearFilter();
    });
});

filterState = {};

function updateFilter(key, value) {
  if (filterState[key] === value) {
    delete filterState[key];
  } else {
    filterState[key] = value;
  }
  applyFilter();
}

function applyFilter() {
  const clearFilterButton = document.getElementById("clear-filter");
  clearFilterButton.style.display = "block";

  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    let shouldDisplay = true;

    for (const [key, value] of Object.entries(filterState)) {
      const cardMetaItem = card.querySelector(`.meta-item.${key}`);
      const cardMetaItemValue = cardMetaItem?.textContent
      if (!cardMetaItem || cardMetaItemValue !== value) {
        shouldDisplay = false;
        break;
      }
    }

    card.style.display = shouldDisplay ? "block" : "none";
  });

  const currentFilters = document.getElementById("current-filters");
  currentFilters.textContent = "";
  Object.entries(filterState).forEach(([key, value]) => {
    const div = document.createElement("div");
    div.classList.add("meta-item", key);
    div.textContent = value;
    currentFilters.appendChild(div);
  });
}


function clearFilter() {
  console.log('clearFilter', filterState);
  filterState = {}; // Add this line to reset the filterState

  const cards = document.querySelectorAll(".card");
  cards.forEach((card) => {
    console.log('clearFilter');
    card.style.display = "block";
  });

  const clearFilterButton = document.getElementById("clear-filter");
  clearFilterButton.style.display = "none";
  
  const currentFilters = document.getElementById("current-filters");
  currentFilters.textContent = "";
}

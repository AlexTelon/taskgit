document.addEventListener('DOMContentLoaded', function() {
  var labels = document.querySelectorAll('.label');
  labels.forEach(function(label) {
    label.addEventListener('click', function(event) {
      filterTasksByLabel(event.target.textContent);
    });
  });

  var clearFilterButton = document.getElementById("clear-filter");
  clearFilterButton.addEventListener("click", function () {
    var cards = document.querySelectorAll(".card");
    cards.forEach(function (card) {
      card.style.display = "block";
    });
    clearFilterButton.style.display = "none";
  });
});

function filterTasksByLabel(labelText) {
  var cards = document.querySelectorAll(".card");
  var clearFilterButton = document.getElementById("clear-filter");
  clearFilterButton.style.display = "block";
  var cards = document.querySelectorAll('.card');
  cards.forEach(function(card) {
    var cardLabels = card.querySelectorAll('.label');
    var hasLabel = false;
    cardLabels.forEach(function(cardLabel) {
      if (cardLabel.textContent === labelText) {
        hasLabel = true;
      }
    });
    if (hasLabel) {
      card.style.display = 'block';
    } else {
      card.style.display = 'none';
    }
  });
}
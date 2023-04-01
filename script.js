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


document.addEventListener('DOMContentLoaded', function() {
    var labels = document.querySelectorAll('.label');
    labels.forEach(function(label) {
      label.addEventListener('click', function(event) {
        filterTasksByLabel(event.target.textContent);
      });
    });
  
    var assignees = document.querySelectorAll('.assignee');
    assignees.forEach(function(assignee) {
      assignee.addEventListener('click', function(event) {
        filterTasksByAssignee(event.target.textContent.replace('Assignee: ', ''));
      });
    });
  
    var clearFilterButton = document.getElementById("clear-filter");
    clearFilterButton.addEventListener("click", function () {
      clearFilter();
    });
  });
  
  function filterTasksByLabel(labelText) {
    var cards = document.querySelectorAll(".card");
    var clearFilterButton = document.getElementById("clear-filter");
    clearFilterButton.style.display = "block";
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

function filterTasksByAssignee(assigneeText) {
    var cards = document.querySelectorAll(".card");
    var clearFilterButton = document.getElementById("clear-filter");
    clearFilterButton.style.display = "block";
    cards.forEach(function(card) {
        var cardAssignee = card.querySelector('.assignee');
        if (cardAssignee.textContent.replace('Assignee: ', '') === assigneeText) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function clearFilter() {
    var cards = document.querySelectorAll(".card");
    cards.forEach(function (card) {
        card.style.display = "block";
    });

    var clearFilterButton = document.getElementById("clear-filter");
    clearFilterButton.style.display = "none";
}
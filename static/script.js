const urlParams = new URLSearchParams(window.location.search);

var hideClosedFilterCheckbox = document.getElementById('hide-closed-filter');
hideClosedFilterCheckbox.checked = localStorage.getItem('hideClosedChecked');

var sortSelectionBox = document.getElementById('sort-select-box');
sortSelectionBox.value = localStorage.getItem('sortSelection');

function updateSort() {
    var sortSelection = sortSelectionBox.value;
    urlParams.set('sort', sortSelection);
    localStorage.setItem('sortSelection', sortSelection)
    window.location.search = urlParams;
}

function handleHideClosedTickets(checkbox) {
    if (checkbox.checked){
        localStorage.setItem('hideClosedChecked', true);
        urlParams.set('filters', 'hideClosed')
        window.location.search = urlParams;
    } else {
        urlParams.delete('filters')
        localStorage.removeItem('hideClosedChecked')
        window.location.search = urlParams;
    }
}
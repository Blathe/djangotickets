const urlParams = new URLSearchParams(window.location.search);

var hideClosedFilterCheckbox = document.getElementById('hide-closed-filter');
var sortSelectionBox = document.getElementById('sort-select-box');

setupSessions()

function setupSessions() {
    if (urlParams.has('filters')) {
        hideClosedFilterCheckbox.checked = sessionStorage.getItem('hideClosedChecked');
    } else {
        sessionStorage.removeItem('hideClosedChecked');
    }
    if (urlParams.has('sort')) {
        sortSelectionBox.value = sessionStorage.getItem('sortSelection');
    } else {
        sessionStorage.removeItem('sortSelection');
    }
    if (urlParams.has('search')) {
        document.getElementById('clear-search-results-btn').style.visibility = "visible";
    } else {
        document.getElementById('clear-search-results-btn').style.visibility = "hidden";
    }
}

function updateSort() {
    var sortSelection = sortSelectionBox.value;
    urlParams.set('sort', sortSelection);
    sessionStorage.setItem('sortSelection', sortSelection)
    window.location.search = urlParams;
}

function handleHideClosedTickets(checkbox) {
    if (checkbox.checked) {
        sessionStorage.setItem('hideClosedChecked', true);
        urlParams.set('filters', 'hideClosed')
        window.location.search = urlParams;
    } else {
        urlParams.delete('filters')
        sessionStorage.removeItem('hideClosedChecked')
        window.location.search = urlParams;
    }
}

function handleSearch() {
    console.log('handle search');
    var query = document.getElementById('search-box').value;
    if (query != "") {
        urlParams.set('search', query)
        window.location.search = urlParams;
    }
}
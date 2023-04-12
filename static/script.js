const urlParams = new URLSearchParams(window.location.search);

var hideClosedFilterCheckbox = document.getElementById('hide-closed-filter');
var sortSelectionBox = document.getElementById('sort-select-box');

setupSessions()

//Set up our session storage information for filters and sorting (checkboxes, drop downs, etc.) so they persist through refreshes.
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

    //only show our "clear search results" button if we've actually searched anything
    //TODO: Make this so it only appears if we actually get some results... rather than being based on if we have done a search
    if (urlParams.has('search')) {
        document.getElementById('clear-search-results-btn').style.visibility = "visible";
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
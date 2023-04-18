const urlParams = new URLSearchParams(window.location.search);

var hideClosedFilterCheckbox = document.getElementById('hide-closed-filter');
var sortSelectionBox = document.getElementById('sort-select-box');
var resultsPerPageSelect = document.getElementById('results-per-page-select');


setupSessions()

//Set up our session storage information for filters and sorting (checkboxes, drop downs, etc.) so they persist through refreshes.
function setupSessions() {
    //hideClosedFilterCheckbox.checked = sessionStorage.getItem('hideClosedChecked');
    //sortSelectionBox.value = sessionStorage.getItem('sortSelection');
    if (localStorage.getItem('results-per-page') != null )
    {
        resultsPerPageSelect.value = localStorage.getItem('results-per-page');
    }
    /*if (urlParams.has('filters')) {
        hideClosedFilterCheckbox.checked = sessionStorage.getItem('hideClosedChecked');
    }
    if (urlParams.has('sort')) {
        sortSelectionBox.value = sessionStorage.getItem('sortSelection');
    }
    if (urlParams.has('per_page')){
        resultsPerPageSelect.value = sessionStorage.getItem('results-per-page');
    }*/
}

function updateResults() {
    var results = resultsPerPageSelect.value;
    urlParams.set('per_page', results);
    localStorage.setItem('results-per-page', results);
    window.location.search = urlParams;
}

function updateSort() {
    var sortSelection = sortSelectionBox.value;
    urlParams.set('sort', sortSelection);
    localStorage.setItem('sortSelection', sortSelection)
    window.location.search = urlParams;
}

function handleHideClosedTickets(checkbox) {
    if (checkbox.checked) {
        localStorage.setItem('hideClosedChecked', true);
        urlParams.set('filters', 'hideClosed')
        window.location.search = urlParams;
    } else {
        urlParams.delete('filters')
        localStorage.removeItem('hideClosedChecked')
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

//Code thanks to PotatoParser
//https://stackoverflow.com/questions/63515279/how-to-initialize-toasts-with-javascript-in-bootstrap-5
//TODO: Customize this a bit more so that we can use toasts for other things, right now they are only use for alerts
window.onload = (event) => {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'))
    var toastList = toastElList.map(function(toastEl) {
        // Creates an array of initialized Toats
        return new bootstrap.Toast(toastEl)
    });
    toastList.forEach(toast => toast.show()); // show the toast

}
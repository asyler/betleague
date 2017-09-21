$(document).ready(function () {
    $('table#results_table').floatThead({
        position: 'fixed',
        top: $('nav').height(),
        floatTableClass: 'results_table_float'
    })
});
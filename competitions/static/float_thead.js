$(document).ready(function () {
    $('table#results_table').floatThead({
        position: 'fixed',
        top: $('nav').height()+2,
        floatTableClass: 'results_table_float'
    })
});
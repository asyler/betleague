$(document).ready(function () {
    $('table#results_table').floatThead({
        position: 'fixed',
        top: $('nav').height()+2,
        floatTableClass: 'results_table_float'
    });

    $('#bet_points_switcher').change(function() {
        $('.bet_with_result').toggleClass('hidden');
        $('.bet_result').toggleClass('hidden');
    });
});
$(document).ready(function () {
    $('#save_bets').click(function () {
        $('form').submit();
    });
    $('.saved_alert').fadeOut(1000);
});
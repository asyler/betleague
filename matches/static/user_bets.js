$(document).ready(function () {
    $('#save_bets').click(function () {
        $('form').submit();
    });
    $('.saved_alert').fadeOut(1000);

    $('input.shootout_winner_radio').change(function () {
        let match_row = $(this).parents('tr');
        $(match_row).find('.reset_link').removeClass('hidden');
    });

    $('.reset_link').click(function () {
        let match_row = $(this).parents('tr');
        $(match_row).find('input.shootout_winner_radio').prop(
            'checked', false
        );
    });
});
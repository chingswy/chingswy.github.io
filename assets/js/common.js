$(document).ready(function() {
    $('a.abstract').click(function() {
        $(this).parent().parent().find(".abstract.hidden").toggleClass('open');
    });
    $('a.qing').click(function() {
        $(this).parent().parent().find(".qing.hidden").toggleClass('open');
    });
    $('a.sida').click(function() {
        $(this).parent().parent().find(".sida.hidden").toggleClass('open');
    });
    $('a.bibtex').click(function() {
        $(this).parent().parent().find(".bibtex.hidden").toggleClass('open');
    });
    $('a').removeClass('waves-effect waves-light');
});

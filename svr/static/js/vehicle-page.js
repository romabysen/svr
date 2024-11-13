$(document).ready(function() {

    // Search
    $(".table-search").on("keyup", function() {
        var value = $(this).val().toLowerCase();
        $(".card span.searchable").filter(function() {
          $(this).closest('.column').toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $(".table-search").val("");

});

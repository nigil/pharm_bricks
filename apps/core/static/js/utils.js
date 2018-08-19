$(function(){
    $("select#id_country").change(function () {
        var country_id = $(this).val();
        var load_cities_url = $(this).attr('data-load_cities_url');

        $.ajax({
            url: load_cities_url,
            data: {
                'country': country_id
            },
            success: function (data) {
                $("#id_city").html(data);
            }
        });
    });
});

function get_basket_size() {
    $.get(
        '/api/basket/count/',
        {},
        function(data) {
            if (data.quantity > 0) {
                var basket_count = $('#basket_count');
                basket_count.text(data.quantity);
                basket_count.css('display', 'inline');
            }
        }
    )
}
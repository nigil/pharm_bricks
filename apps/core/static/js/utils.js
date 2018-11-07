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

function increase_basket_size(quantity) {
    if (!quantity) {
        quantity = 1;
    }

    var basket_count = $('#basket_count');
    basket_count.text(parseInt(basket_count.text()) + parseInt(quantity))
        .css('display', 'inline');
}

function decrease_basket_size(quantity) {
    if (!quantity) {
        quantity = 1;
    }

    var basket_count = $('#basket_count');
    var new_quantity = parseInt(basket_count.text()) - parseInt(quantity);
    if (new_quantity < 0) {
        new_quantity = 0;
    }

    basket_count.text(new_quantity);
    if (new_quantity == 0) {
        basket_count.hide()
    }
}
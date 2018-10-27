function put_to_basket(product_id, quantity, csrf_token) {
    $.post(
        '/api/basket/',
        {
            'csrfmiddlewaretoken': csrf_token,
            variant_id: product_id,
            quantity: quantity
        },
        function(data, status) {
            if (status == 'success') {
                var basket_count = $('#basket_count');
                basket_count.text(parseInt(basket_count.text()) + parseInt(quantity))
                    .css('display', 'inline');

                alert('You have just add product to basket. ' +
                    'You can check to basket or continue to shopping')
            }
            else {
                alert('Something is wrong. Please check errors and try again.')
            }
        }
    );
}

function calc_basket_total() {
    var sum = 0;

    $('.basket_product').each(function(){
        var quantity = $(this).find('.item_quantity').val();
        var price = $(this).find('.product_type').find('option:selected').attr('data-price');

        sum += quantity * price;
    });

    $('#total_price').text(sum);
}

$(function(){
    var csrf_token = $("[name=csrfmiddlewaretoken]").val();
    var prise_size_error = $('#prise_size_none_error');

    $(document).on('click', '#add_to_basket', function(){
        var variant_id = $("input[name='pricensize']:checked").val();
        var quantity = $('#el_count').val();
        if (variant_id && quantity) {
            put_to_basket(variant_id, quantity, csrf_token);
        }
        else if (!variant_id) {
            prise_size_error.show();
        }

        return false;
    });
});
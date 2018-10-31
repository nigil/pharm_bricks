function put_to_basket(product_id, quantity, csrf_token, target) {
    if (!target) {
        target = null;
    }
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

                if (target) {
                    target.prop('disabled', true);
                    var button_text = target.find('span');
                    var target_original_text = button_text.text();
                    var new_text = 'added';

                    button_text.text(new_text);
                    setTimeout(function() {
                        button_text.text(target_original_text);
                        target.prop('disabled', false);
                    }, 3000);
                }

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
            put_to_basket(variant_id, quantity, csrf_token, $(this));
        }
        else if (!variant_id) {
            prise_size_error.show();
        }

        return false;
    });
});
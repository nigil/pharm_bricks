function calc_basket_total() {
    var sum = 0;

    $('.basket_product').each(function(){
        var quantity = $(this).find('.item_quantity').val();
        var price = $(this).find('.product_type').find('option:selected').attr('data-price');

        sum += quantity * price;
    });

    $('#total_price').text(sum);
}
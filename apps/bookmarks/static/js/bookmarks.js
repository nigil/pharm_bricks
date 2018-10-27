function add_product_to_bookmarks(product_id, csrf_token) {
    $.post(
        '/bookmarks/add-product-to-bookmarks/',
        {
            'csrfmiddlewaretoken': csrf_token,
            product_id: product_id
        },
        function(data) {
            if (data.success) {
                alert('You have just add product to library. ' +
                    'Open My Libraries in Profile to see all bookmarks')
            }
            else {
                alert(data.error)
            }
        }
    );
}

$(function(){
    var csrf_token = $("[name=csrfmiddlewaretoken]").val();
    var prise_size_error = $('#prise_size_none_error');

    $(document).on('click', '#add_to_library', function(){
        var variant_id = $("input[name='pricensize']:checked").val();
        if (variant_id) {
            add_product_to_bookmarks(variant_id, csrf_token);
        }
        else if (!variant_id) {
            prise_size_error.show()
        }

        return false;
    });
});
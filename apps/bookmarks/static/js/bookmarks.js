function add_product_to_bookmarks(product_id, csrf_token, target) {
    if (!target) {
        target = null;
    }

    $.post(
        '/bookmarks/add-product-to-bookmarks/',
        {
            'csrfmiddlewaretoken': csrf_token,
            product_id: product_id
        },
        function(data) {
            if (data.success) {
                if (target) {
                    target.prop('disabled', true);
                    var button_text = target.find('span');
                    var target_original_text = button_text.text();
                    var new_text = 'added';

                    button_text.text(new_text);
                    setTimeout(function(){
                        button_text.text(target_original_text);
                        target.prop('disabled', false);
                    }, 3000);
                }
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
            add_product_to_bookmarks(variant_id, csrf_token, $(this));
        }
        else if (!variant_id) {
            prise_size_error.show()
        }

        return false;
    });
});
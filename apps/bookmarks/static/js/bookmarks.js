function add_product_to_bookmarks(product_id, csrf_token) {
    $.post(
        '/bookmarks/add_product_to_bookmarks/',
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
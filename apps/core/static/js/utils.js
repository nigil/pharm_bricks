$(function(){
    $("select#id_country").change(function () {
        console.log('select is changed!');
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
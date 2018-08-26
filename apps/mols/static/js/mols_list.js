function load_molecules(page_num, reset) {
    if (page_num === null) {
        page_num = 1
    }
    if (reset === null) {
        reset = false
    }

    var mols_container = $('#mols_list_container');
    var page_size = $('#catalogue_page_size').val();
    var section_slug = mols_container.attr('data-section');
    var sub_section_slug = mols_container.attr('data-sub_section');
    var search_query = mols_container.attr('data-search_query');
    var show_more_button = $('#show_more_button');

    $('#no_data_result').hide();

    $.ajax({
        url: mols_container.attr('data-mols_list_url'),
        data: {
            size: page_size,
            page: page_num,
            section: section_slug,
            sub_section: sub_section_slug,
            q: search_query
        },
        success: function(data) {
            if ($.trim(data.mols)) {
                if (reset) {
                    mols_container.html(data.mols);
                }
                else {
                    mols_container.append(data.mols);
                }

                if (data.page_num < data.pages_cnt) {
                    show_more_button.show();
                    cur_page_num = show_more_button.attr('data-page_num');
                    show_more_button.attr('data-page_num', ++cur_page_num);
                }
                else {
                    show_more_button.hide();
                }
            }
            else {
                $('#no_data_result').show();
            }
        },
        error: function() {
            mols_container.text('There was Error when getting data. Please try later.')
        }
    })
}
$(function(){
    $(document).on('click', '#show_more_button', function() {
        load_molecules($('#show_more_button').attr('data-page_num'));
    });

    $(document).on('change', '#catalogue_page_size', function() {
        $('#show_more_button').attr('data-page_num', 1);
        load_molecules(1, true);
    });
});
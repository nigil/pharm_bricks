(function ($) {
    var menuTimer;
    var menuTwoTimer;
    var menuMainTimer;
    var menuCheckEvent;
    var menuCheckelement;

    $(document).on("click", ".topmenu > li", function (e) {
        topMenuItemHideShow($(this), e);
    });
    $(document).on("mouseenter", ".topmenu > li", function (e) {

        clearTimeout(menuMainTimer);
        menuMainTimer = null;
        clearTimeout(menuTimer);
        menuTimer = null;
        clearTimeout(menuTwoTimer);
        menuTwoTimer = null;

        menuCheckEvent = e;
        menuCheckelement = $(this);

        menuMainTimer = setTimeout(function () {
            topMenuItemHideShow(menuCheckelement, menuCheckEvent);
        }, 300);

    });
    $(document).on("mouseleave", ".navbar.navbar-expand-lg", function () {

        clearTimeout(menuMainTimer);
        menuMainTimer = null;
        clearTimeout(menuTimer);
        menuTimer = null;
        clearTimeout(menuTwoTimer);
        menuTwoTimer = null;

        menuTimer = setTimeout(function () {
            topMenuBlockHide();
        }, 3000);
    });

    $(document).on("mouseenter", ".menu_two", function (e) {
        clearTimeout(menuMainTimer);
        clearTimeout(menuTimer);
        clearTimeout(menuTwoTimer);
    });
    $(document).on("mouseleave", ".menu_two", function () {
        menuTwoTimer = setTimeout(function () {
            topMenuBlockHide();
        }, 3000);
    });

    $(document).on("click", ".topmenu_left > li", function (e) {
        e.stopPropagation();
        if ($(this).hasClass("active")) {
            $(".img-right_min").removeClass("active");
            $(".submenu_left").removeClass("active");
            $(".img-right").removeClass("active");
            $(this).removeClass("active");
        } else {
            $(".submenu_left").addClass("active");
            $(".topmenu li").removeClass("active");

            $(".img-right_min").addClass("active");
            $(".topmenu li").removeClass("active");

            $(".img-right").addClass("active");
            $(".topmenu li").removeClass("active");
            $(this).addClass("active");
        }
    });

    $(document).on("click", ".topmenu .submenu>li", function (e) {
        e.stopPropagation();
        if ($(e.target).find('.disabled').length > 0 || $(e.target).has('.disabled') || $(this).find('.disabled').length > 0 || $(this).has('.disabled')) {
            return false;
        }

        if ($(this).hasClass('isactive')) {
            $(this).removeClass("isactive");
            $(this).removeClass("active");
        } else {
            $(".topmenu li ul li ").removeClass("active");
            $(".topmenu li ul li ").removeClass("isactive");
            $(this).addClass("isactive");
            $(this).addClass("active");
        }
    });

    $(document).on("mouseenter", ".topmenu .submenu>li", function (e) {
        e.stopPropagation();
        clearTimeout(menuMainTimer);
        clearTimeout(menuTimer);
        clearTimeout(menuTwoTimer);
        if ($('.navbar-toggler').is(":visible") || $(this).closest('ul').hasClass('submenu_last')) {
            return false;
        }
        $(".topmenu li ul li ").removeClass("active");
        $(this).addClass("active");
    });

    $(document).on("mouseleave", ".topmenu .submenu>li", function () {
        if ($('.navbar-toggler').is(":visible") || $(this).closest('ul').hasClass('submenu_last')) {
            return false;
        }
        $(".topmenu li ul li ").removeClass("active");
    });

    $(document).on("click", ".topmenu .submenu .submenu>li", function () {
        $(".topmenu li").removeClass("active");
        $(".menu_two").slideUp();
    });

    $(window).click(function () {
        topMenuBlockHide();
    });

    function topMenuBlockHide() {
        //$(".menu_two").removeClass("active");
        $(".menu_two").slideUp(function () {
            $('.container-fluid.band'
            ).removeClass("no-disabled");
        });
        $(".topmenu li").removeClass("active");
    }

    function topMenuItemHideShow(curentTopItem, event) {
        if ($(event.target).find('.disabled').length > 0 || $(curentTopItem).find('.disabled').length > 0) {
            return false;
        }
        if (curentTopItem.find('ul').hasClass('submenu')) {
            event.stopPropagation();
            //$(".menu_two").addClass("active");
            $(".menu_two").slideDown();
            $(".topmenu li").removeClass("active");
            curentTopItem.addClass("active");
            $('.container-fluid.band').addClass("no-disabled");
        } else {
            topMenuBlockHide();
        }
    }

    /*News Events*/
    $(document).on("click", ".all-news-block .active1", function () {
        $('#active_news').slideUp(400, function() {
            $('#active_news').html($(this).next('.content_news').html());
            $('#active_news').slideDown(400)
        })
        $('#active_news').html($(this).next('.content_news').html());
        $('.all-news-block .active1').removeClass('show_news');
        $(this).addClass('show_news');
        $('html, body').stop().animate({
            'scrollTop': $('#top_news').offset().top
        }, 500, 'swing', function () {

        });
    });

    $(document).on("click", ".read_more", function () {
        $('#active_news').find('.more_content').removeClass('hidden');
        $('#active_news').find('.read_more').addClass('hidden');
        $('#active_news').append('<span class="text_bold a_green read_less">Read less</span>');
    });

    $(document).on("click", ".read_less", function () {
        $('#active_news').find('.more_content').addClass('hidden');
        $('#active_news').find('.read_more').removeClass('hidden');
        $(this).remove();
    });


})(jQuery);


function toggle_show(id) {
    document.getElementById(id).style.display = document.getElementById(id).style.display == 'none' ? 'block' : 'none';
}


$(document).ready(function () {
    if ($('div').is('#slider_container')) {
        $("#slider_container").owlCarousel({
            singleItem: true,
            autoPlay: true,
            afterMove: function() {
                var owl = $(".owl-carousel").data('owlCarousel');
                if (owl.maximumItem == owl.currentItem) {
                    owl.stop()
                }
            }
        });
    }

    $(".harmonic h3:first").addClass("active1");
    $(".harmonic p:not(:first)").hide();

    $(".harmonic h3").click(function () {

        $(this).next("p").slideToggle("fast").siblings("p:visible").slideUp("fast");
        $(this).toggleClass("active1");
        $(this).siblings("h3").removeClass("active1");
    });
    $('#minus_el').click(function (e) {
        e.preventDefault()
        var v = parseInt($('#el_count').val()) - 1;
        if (v < 1) v = 1
        $('#el_count').val(v);
        return false;
    });
    $('#plus_el').click(function (e) {
        e.preventDefault()
        var v = parseInt($('#el_count').val()) + 1;
        $('#el_count').val(v);
        return false;
    });

    $('.checkbox_disabled').on('click', function(e) {
        e.preventDefault()
        return false
    })


    // $('#toggle_editor').on('click', function(e) {
    //     e.preventDefault();
    //     $('#editor_container').toggle()
    //     $(this).toggleClass('active')
    //     render_editor("editor_container")
    // })
    //
    // if ($('#redactor_generation').length > 0) {
    //     console.log('render editor')
    //     render_editor("redactor_generation")
    // }

    $('#generation_step_1_radios input[name="radio_el"]').on('change', function() {
        $('.generation_step_1').hide()
        $('#generation_step_2_radios > div').hide()
        $('.generation_step_2, .generation_step_2_hide').show()
        var val = $('#generation_step_1_radios input[name="radio_el"]:checked').val()
        $('#generation_step_2_radios > .generation_step_2_radios_' + val).show()
        $('#generation_step_2_radios input:checked').click()
        $('#generation_step_2_btn').addClass('disabled').removeClass('blue_butt')
        $('#generation_step_3_btn').removeClass('disabled').addClass('blue_butt').text('save to my libraries')
    })
    $('#generation_step_2_radios').on('click', function(e) {
        if ($(e.target).is('input[name="step2_el"]') && $('#generation_step_2_radios input[name="step2_el"]:checked').length > 0) {
            $('#generation_step_2_btn').removeClass('disabled').addClass('blue_butt')
        } else {
            $('.generation_step_1').hide()
            $('.generation_step_2, .generation_step_2_hide').show()
            $('#generation_step_2_btn').addClass('disabled').removeClass('blue_butt')
            $('.generation_step_3').hide()
            $('#generation_step_3_btn').removeClass('disabled').addClass('blue_butt').text('save to my libraries')
        }
    })

    $('#basket_checkout').on('click', function() {
        $('.basket_step_1').hide()
        $('.basket_step_2').show()
    })

    $('#generation_step_2_btn').on('click', function(e) {
        e.preventDefault()
        if ($(this).hasClass('blue_butt')) {
            $('.generation_step_2_hide').hide()
            $('.generation_step_3').show()
        }
    })
    $('#generation_step_3_btn').on('click', function(e) {
        e.preventDefault()
        // call to save to libraries
        $(this).addClass('disabled').removeClass('blue_butt').text('saved')
    });

    $('#my_libraries_repeat .checkbox').on('change', function() {
        // TODO: make call to server to repeat order from MyLibraries page
    })

    $('textarea').autogrow({vertical: true, horizontal: false});
});





function toggle_show(id) {
    document.getElementById(id).style.display = document.getElementById(id).style.display == 'none' ? 'block' : 'none';
}

// function render_editor(container_name) {
//     // if (jsmeApplet === null && typeof JSApplet != 'undefined') {
//     //     jsmeApplet = new JSApplet.JSME(container_name);
//     //     jsmeApplet.deferredRepaint();
//     //     document.JME = jsmeApplet;
//     // } else {
//     //     setTimeout(function() {
//     //         render_editor(container_name)
//     //     }, 300)
//     // }
//
//
// 	function getSmiles() {
// 		var data = document.JME.smiles();
// 		console.log(data);
// 	}
// }



/*
 * Sticky navigation
 * Fatih Erikli
 * fatiherikli at gmail dot com
 * */

!function ($) {

    var POSITION_THRESHOLD = 100;

    $(window).ready(function () {

        var navigation = $("nav");
        var content = $("section#main");
        var class_name = "sticky-navigation";

        $(this).scroll(function () {
            var scroll_position = $(this).scrollTop();
            var content_position = content.offset().top;

            if (scroll_position > content_position - POSITION_THRESHOLD) {
                !navigation.hasClass(class_name) && navigation.addClass(class_name)
            }
            else {
                navigation.removeClass(class_name);
            }

        });

    });

}(window.jQuery);
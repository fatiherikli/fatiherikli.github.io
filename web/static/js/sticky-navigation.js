/*
 * Sticky navigation
 * Fatih Erikli
 * fatiherikli at gmail dot com
 * */

!function ($) {

    var CONTENT_POSITION_THRESHOLD = 100;
    var STICKY_CLASS_NAME = "sticky-navigation";

    $(window).ready(function () {

        var navigation = $("nav");
        var content = $("section#main");

        $(this).scroll(function () {
            var scroll_position = $(this).scrollTop();
            var content_position = content.offset().top;

            if (scroll_position > content_position - CONTENT_POSITION_THRESHOLD) {
                !navigation.hasClass(STICKY_CLASS_NAME) && navigation.addClass(STICKY_CLASS_NAME)
            }
            else {
                navigation.removeClass(STICKY_CLASS_NAME);
            }

        });

    });

}(window.jQuery);
!function ($){

    /*
     * Actual-heights for columns.
     * */
//    var highestCol = Math.max($('#projects').height(), $('#open-source').height());
//    $('#open-source, #projects').css("min-height", highestCol);


    /*
     * Google prettify settings
     * */
    $("pre").addClass("prettyprint");
    prettyPrint();



//    var post_offsets = [];
//    $(".post").each(function (index, element) {
//       post_offsets.push($(element).offset().top)
//    })
    $(window).scroll(function () {

//        var index = -1;
//        for (var offset in post_offsets) {
//            if ($(window).scrollTop() > post_offsets[offset]) {
//                index = post_offsets.indexOf(post_offsets[offset])
//            }
//        }
//
//        if (index > -1)  {
//            console.log(index)
//            $("section.info, .post h3").css("position", "relative")
//            $("section.info").eq(index).css("position", "fixed")
//            $(".post").eq(index).css({
////                "padding-top": "80px"
//            })
//            $(".post h3").eq(index).css({
//                "position": "fixed"
//            })
//        } else {
//            $("section.info, .post h3").css("position", "relative")
//            $(".post").css({
//                "padding-top": "0px"
//            })
//        }

    });


}(window.jQuery);




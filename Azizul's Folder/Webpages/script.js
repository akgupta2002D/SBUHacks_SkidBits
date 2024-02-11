(function() {
    var file     = ["https:\/\/academics.skidmore.edu\/blogs\/skidmorecodes\/wp-content\/et-cache\/1\/2298\/206\/et-divi-dynamic-206-late.css"];
    var handle   = document.getElementById('divi-style-inline-inline-css');
    var location = handle.parentNode;

    if (0===document.querySelectorAll('link[href="' + file + '"]').length) {
        var link  = document.createElement('link');
        link.rel  = 'stylesheet';
        link.id   = 'et-dynamic-late-css';
        link.href = file;

        location.insertBefore(link, handle.nextSibling);
    }
})();
    var et_animation_data = [{"class":"et_pb_button_0","style":"zoom","repeat":"once","duration":"1000ms","delay":"0ms","intensity":"6%","starting_opacity":"0%","speed_curve":"ease-in-out"}];
var DIVI = {"item_count":"%d Item","items_count":"%d Items"};
var et_builder_utils_params = {"condition":{"diviTheme":true,"extraTheme":false},"scrollLocations":["app","top"],"builderScrollLocations":{"desktop":"app","tablet":"app","phone":"app"},"onloadScrollLocation":"app","builderType":"fe"};
var et_frontend_scripts = {"builderCssContainerPrefix":"#et-boc","builderCssLayoutPrefix":"#et-boc .et-l"};
var et_pb_custom = {"ajaxurl":"https:\/\/academics.skidmore.edu\/blogs\/skidmorecodes\/wp-admin\/admin-ajax.php","images_uri":"https:\/\/academics.skidmore.edu\/blogs\/skidmorecodes\/wp-content\/themes\/Divi\/images","builder_images_uri":"https:\/\/academics.skidmore.edu\/blogs\/skidmorecodes\/wp-content\/themes\/Divi\/includes\/builder\/images","et_frontend_nonce":"cdcd559076","subscription_failed":"Please, check the fields below to make sure you entered the correct information.","et_ab_log_nonce":"81f5f05bff","fill_message":"Please, fill in the following fields:","contact_error_message":"Please, fix the following errors:","invalid":"Invalid email","captcha":"Captcha","prev":"Prev","previous":"Previous","next":"Next","wrong_captcha":"You entered the wrong number in captcha.","wrong_checkbox":"Checkbox","ignore_waypoints":"no","is_divi_theme_used":"1","widget_search_selector":".widget_search","ab_tests":[],"is_ab_testing_active":"","page_id":"206","unique_test_id":"","ab_bounce_rate":"5","is_cache_plugin_active":"no","is_shortcode_tracking":"","tinymce_uri":"https:\/\/academics.skidmore.edu\/blogs\/skidmorecodes\/wp-content\/themes\/Divi\/includes\/builder\/frontend-builder\/assets\/vendors","accent_color":"#e02b20","waypoints_options":[]};
var et_pb_box_shadow_elements = [];
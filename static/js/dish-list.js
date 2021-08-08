jQuery(document).ready(function ($) {
    if (window.location.search.indexOf('order_by') > -1) {
        $('.filter_container').show();
        $('.filter_container').addClass('filter-active');
        $('#filter_btn').text('Hide Filter');
    } else {
        $('.filter_container').hide();
        $('.filter_container').removeClass('filter-active');
        $('#filter_btn').text('Show Filter');
    }
    $('#filter_btn').click(function(){
        $('.filter_container').slideToggle();
        if (!$('.filter_container').hasClass('filter-active')) {
            $('.filter_container').addClass('filter-active');
            $('#filter_btn').text('Hide Filter');
        }else{
            $('.filter_container').removeClass('filter-active');
            $('#filter_btn').text('Show Filter');
        }
    });
});
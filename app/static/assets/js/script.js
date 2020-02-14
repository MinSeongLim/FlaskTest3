$(document).ready(function(){

    function dropdownMenu(a){
        $(a).click(function(e){
            e.preventDefault();
            $(this).next('.slidedown-menu').stop().slideToggle();
        }); 
    }
    dropdownMenu('.user-link');  

    $('.close-btn').click(function(){
        $('.join').hide();
    });
    $('.nav-btn').click(function(){
        $('nav').slideToggle();
    });

   

});













$.tinysort.defaults.order = 'desc';

jQuery.fn.ajaxifyForm = function(done, fail) {
    var forms = $(this);
    forms.submit(function(event) {
        event.preventDefault();
        form = $(this);
        var method = form.attr('method');
        var action = form.attr('action');
        $.ajax({
            type: method,
            url: action,
            data: form.serialize()
        }).done(function(data, textStatus, jqXHR){
            done(form, data, textStatus, jqXHR);
        }).fail(function(jqXHR, textStatus, errorThrown){
            fail(form, jqXHR, textStatus, errorThrown);
        });
    });
}

$(function(){
    $('.votes form').ajaxifyForm(
        function(form, data, textStatus, jqXHR){
            form.children('button').prop('disabled', true);
            form.siblings('form').children('button').prop('disabled', false);
            voteCount = parseInt(form.siblings('.count').text());

            if(form.children('input[name=action]').attr('value') == 'increment'){
                form.siblings('.count').text(voteCount + 1);
            } else if(form.children('input[name=action]').attr('value') == 'decrement'){
                form.siblings('.count').text(voteCount - 1);
            }
            sortAlbums();
        },
        function(form, jqXHR, textStatus, errorThrown){
            console.log(jqXHR);
            toast(jqXHR.responseJSON.message);
        }
    );
});

function sortAlbums() {
    var albumsContainer = $('.albums');
    albumsContainer.css({
        position: 'relative',
        height: albumsContainer.height(),
        display: 'block'
    });
    var albumPositionMultiplier;
    var albums = $('.albums > li');
    albums.each(function(i, album){
        var top = $(album).position().top;
        $.data(album, 'top', top);
        if (i===1) albumPositionMultiplier = top;
    });
    albums.tsort(
        '.votes .count', '.card .artist', '.card .year', '.card h3'
    ).each(function(i, album){
        var $album = $(album);
        var from = $.data(album, 'top');
        var to = i * albumPositionMultiplier;
        $album.css({position:'absolute',top:from}).animate({top:to},500);
    });
}

function toast(message) {
    message = message == undefined ? 'Unable to perform action' : message;
    var toastDiv = $('#toast');
    console.log(message);

    toastDiv.text(message);
    if(toastDiv.hasClass('active')){
        clearTimeout(this.timeout);
    } else {
        toastDiv.addClass('active');
    }
    this.timeout = setTimeout(function(){
        toastDiv.removeClass('active');
    }, 2500);
}
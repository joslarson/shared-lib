$.tinysort.defaults.order = 'desc';

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

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
    var search_results = null;

    $('body > header a[href="#add"]').click(function(event){
        event.preventDefault();
        $('#album_finder ul.results').html('');
        $('#album_finder .search-box input[name=album]').val('');
        $('#album_finder').addClass('active');
        $('#album_finder .search-box input[name=album]').focus();
        $('body').addClass('lock-scroll');
    });

    $('#album_finder .close').click(function(event){
        $('#album_finder').removeClass('active');
        $('body').removeClass('lock-scroll');
    });

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
            // sortAlbums();
        },
        function(form, jqXHR, textStatus, errorThrown){
            console.log(jqXHR);
            toast(jqXHR.responseJSON.message);
        }
    );
    $('#album_finder .search-box').ajaxifyForm(
        function(form, data, textStatus, jqXHR){
            search_results = data;
            var results = [];
            results_ul = $('#album_finder ul.results');
            for(var key in data) {
                result =  '<li class="card" style="background-image: url(' + data[key].image_url + ');">'; 
                result +=     '<h3 title="' + data[key].title + '">' + data[key].title + '</h3>';
                result +=     '<span title="' + data[key].artist + '" class="artist">' + data[key].artist + '</span>';
                result +=     '<span class="year">' + data[key].year + '</span>';
                if(data[key].is_explicit){
                    result += '<span class="explicit">Explicit</span>';
                }
                result +=     '<div class="actions">';
                result +=         '<a href="#share" data-id="' + key + '">+ Share this Album</a>';
                result +=         '<a href="' + data[key].listen_url + '" target="_blank">Listen →</a>';
                result +=     '</div>';
                result += '</li>';
                results.push(result);
            }
            results_ul.html(results.join(''));
            $('#album_finder .card a[href="#share"]').click(function(event){
                event.preventDefault();
                var spotify_id = $(this).attr('data-id');
                $.post("/api/album.json", {
                    "artist": search_results[spotify_id]['artist'],
                    "title": search_results[spotify_id]['title'],
                    "year": search_results[spotify_id]['year'],
                    "is_explicit": search_results[spotify_id]['is_explicit'],
                    "external_link": search_results[spotify_id]['listen_url'],
                    "image_url": search_results[spotify_id]['image_url']
                }).done(function(data, textStatus, jqXHR){
                    document.location.reload(true);
                }).fail(function(jqXHR, textStatus, errorThrown){
                    toast('fail!');
                });
            });
        },
        function(form, jqXHR, textStatus, errorThrown){
            toast('No albums found.');
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
        '.votes .count', '.card .artist', {order:'asc'}, '.card .year', '.card h3'
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
def parse_cast(cast):
    names = ""
    i = 0

    for actress in cast:
        i += 1
        names += '<a href="' + actress.url + '" rel="nofollow">' + actress.name.strip(
        ) + '</a>'
        if (i + 1) <= len(cast):
            names += ", "

    return names


def parse_image(movie_id, cast, number):
    url = "https://www.zenra.net/imgcache/blog-text/photos/Writers/vienna/"
    url += movie_id + '/' + movie_id + '-JAV-'

    if len(cast) == 1:
        for actress in cast:
            url += actress.name.replace(" ", "-")
        url += "-"

    if number == 0:
        url += "Header.jpg"
    else:
        url += '0' + str(number) + '.jpg'

    return url


def parse_html(movie):

    # header : movie_id, title

    content = '<p style="text-align: center"><strong><span style="font-size:22px;"><a href="' + movie.get_url(
    ) + '" rel="nofollow">' + movie.get_movie_id(
    ) + '</a></span></strong><br />'
    content += '<span style="font-size:26px;">'

    # header : cast

    if len(movie.get_cast()) != 0:
        content += parse_cast(movie.get_cast())
        content += '&nbsp;&minus;&nbsp;'

    # header : title

    content += '<strong><a href="' + movie.get_url(
    ) + '">&quot;' + movie.get_title() + '&quot;</a></strong></span><br>'

    # header : header image

    content += '<a href="' + movie.get_url() + '"/><img src="' + parse_image(
        movie.get_movie_id(), movie.get_cast(), 0) + '" /></a></p>'

    # table

    content += '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width:400px"><tbody>'

    # table : movie_id

    content += '<tr><td><strong>Movie</strong></td> <td><a href="' + movie.get_url(
    ) + '" rel="nofollow">' + movie.get_movie_id() + '</a></td></tr>'

    # table : studio

    content += '<tr><td><strong>Studio</strong></td><td><a href="' + movie.get_studio(
    ).get_url() + '" rel="nofollow">' + movie.get_studio().get_name(
    ) + '</a></td></tr>'

    # table : cast

    content += '<tr><td><strong>Cast</strong></td><td>'

    if len(movie.get_cast()) != 0:
        content += parse_cast(movie.get_cast())
    else:
        content += "--"

    content += '</td></tr>'

    # table : release_date

    content += '<tr><td><strong>Release Date</strong></td><td>' + movie.get_release_date(
    ) + '</td></tr>'
    content += '</tbody></table><br>'

    # trailer

    if (movie.get_trailer() is not None):
        trailer_link = 'https://www.zenra.net/storage/photos/Writers/vienna/' + movie.get_movie_id(
        ) + '/' + movie.get_trailer()

        content += '<br><br><span style="font-size:16px;">Check out the trailer of the movie here:</span><br>'
        content += '<video controls="controls" height="404" preload="metadata" src="' + trailer_link + '" width="720">&nbsp;</video></span></p>'

    # first 2 images

    content += '<p style="text-align: center">'
    content += '<a href="' + movie.get_url(
    ) + '"><img style="height: 275px !important" src="' + parse_image(
        movie.get_movie_id(), movie.get_cast(), 1) + '" /></a>'
    content += '<a href="' + movie.get_url(
    ) + '"><img style="height: 275px !important" src="' + parse_image(
        movie.get_movie_id(), movie.get_cast(), 2) + '" /></a>'
    content += '</p>'

    # text

    content += '<p style="font-size:16px">Text</p>'

    # last 3 images

    content += '<p style="text-align: center">'
    content += '<a href="' + movie.get_url(
    ) + '"><img style="height: 275px !important" src="' + parse_image(
        movie.get_movie_id(), movie.get_cast(), 3) + '" /></a>'
    content += '<a href="' + movie.get_url(
    ) + '"><img style="height: 275px !important" src="' + parse_image(
        movie.get_movie_id(), movie.get_cast(), 4) + '" /></a>'
    content += '<a href="' + movie.get_url(
    ) + '"><img style="height: 275px !important" src="' + parse_image(
        movie.get_movie_id(), movie.get_cast(), 5) + '" /></a>'

    content += '<br>'

    return content
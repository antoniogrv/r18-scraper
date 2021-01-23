def parse_cast(cast):
    names = ""
    i = 0

    for actress in cast:
        i += 1
        names += '<a href="' + actress.url + '" rel="nofollow">' + actress.name + '</a>'
        if (i + 1) >= len(cast):
            names += " "
        else:
            names += ", "

    return names

def parse_image(movie_id, cast, number):
    url = "https://www.zenra.net/imgcache/blog-text/photos/Writers/vienna/"
    url += movie_id + '/' + movie_id + '-JAV-'

    if len(cast) != 0:
        for actress in cast:
            url += actress.name.replace(" ", "-")
        url += "-"

    if number == 0:
        url += "Header.jpg"
    else:
        url += '0' + str(number) + '.jpg'

    return url

def parse_html(title, release_date, studio, cast, url, movie_id):

    # header : movie_id, title

    content  = '<p style="text-align: center"><strong><span style="font-size:22px;"><a href="' + url + '" rel="nofollow">' + movie_id + '</a></span></strong><br />'
    content += '<span style="font-size:26px;">'

    # header : cast

    if len(cast) != 0:
        content += parse_cast(cast)
        content += '&minus;&nbsp;'

    # header : title

    content += '<strong><a href="' + url + '">&quot;' + title + '&quot;</a></strong></span><br>'

    # header : header image

    content += '<a href="' + url + '"/><img src="' + parse_image(movie_id, cast, 0) + '" /></a></p>'

    # table

    content += '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width:400px"><tbody>'

    # table : movie_id

    content += '<tr><td><strong>Movie</strong></td> <td><a href="' + url + '" rel="nofollow">' + movie_id + '</a></td></tr>'

    # table : studio

    content += '<tr><td><strong>Studio</strong></td><td><a href="' + studio.get_url() + '" rel="nofollow">' + studio.get_name() + '</a></td></tr>'
    
    # table : cast
    
    content += '<tr><td><strong>Cast</strong></td><td>'

    if len(cast) != 0:
        content += parse_cast(cast)
    else:
        content += "--"

    content += '</td></tr>'

    # table : release_date

    content += '<tr><td><strong>Release Date</strong></td><td>' + release_date + '</td></tr>'
    content += '</tbody></table><br>'

    # first 2 images

    content += '<p style="text-align: center">'
    content += '<a href="' + url + '"><img src="' + parse_image(movie_id, cast, 1) + '" /></a>'
    content += '<a href="' + url + '"><img src="' + parse_image(movie_id, cast, 2) + '" /></a>'
    content += '</p>'

    # text

    content += '<br><p>Text</p><br>'

    # last 3 images

    content += '<p style="text-align: center">'
    content += '<a href="' + url + '"><img src="' + parse_image(movie_id, cast, 3) + '" /></a>'
    content += '<a href="' + url + '"><img src="' + parse_image(movie_id, cast, 4) + '" /></a>'
    content += '<a href="' + url + '"><img src="' + parse_image(movie_id, cast, 5) + '" /></a>'
    content += '</p>'

    return content
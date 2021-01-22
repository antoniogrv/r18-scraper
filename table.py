def parse_html(title, release_date, studio, cast, url, movie_id):
    content  = '<p style="text-align: center;"><strong><span style="font-size:22px;"><a href="' + url + '" rel="nofollow">' + movie_id + '</a></span></strong><br />'
    content += '<span style="font-size:26px;">'

    if len(cast) != 0:
        i = 0

        for actress in cast:
            i += 1
            content += '<a href="' + actress.link + '" rel="nofollow">' + actress.name + '</a>'
            if (i + 1) >= len(cast):
                content += " "
            else:
                content += ", "

        content += '&minus;&nbsp;'

    content += '<a href="' + url + '">&quot;<strong>' + title.text + '</strong>&quot;</span><br />'
    content += '<a href="' + url + '"/><img src="IMAGE LINK" /></a></p>'

    # table

    content += '<table align="center" border="1" cellpadding="1" cellspacing="1" style="width:400px"><tbody>'
    content += '<tr><td><strong>Movie</strong></td> <td><a href="' + url + '" rel="nofollow">' + movie_id + '</a></td></tr>'
    content += '<tr><td><strong>Studio</strong></td><td><a href="' + studio["href"] + '" rel="nofollow">' + studio.text + '</a></td></tr>'
    content += '<tr><td><strong>Cast</strong></td><td>'

    if len(cast) != 0:
        i = 0

        for actress in cast:
            i += 1
            content += '<a href="' + actress.link + '" rel="nofollow">' + actress.name + '</a>'
            if (i + 1) >= len(cast):
                content += " "
            else:
                content += ", "
    else:
        content += "--"

    content += '</td></tr>'
    content += '<tr><td><strong>Release Date</strong></td><td>' + release_date.text + '</td></tr></tbody>'
    content += '<p>&nbsp;</p><p>Text</p>'

    return content
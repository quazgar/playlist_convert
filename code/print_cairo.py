"""Module to print to cairo output."""

import cairo
import rsvg

def print_tracks(tracks, format="svg"):
    """Prints the tracks to the given format."""

    svg = rsvg.Handle(file="templates/template.01.plain.svg")
    svg.set_dpi(72) # why do we have to specify this at all?

    # A4 in pixels:
    width, height = 744.09, 1052.36
    # A4 in points:
    width_pt, height_pt = 595.27, 841.89
    # from svg:
    width_svg, height_svg = svg.get_dimension_data()[2:4]

    out_svg = file("cover.pdf", 'w')
    surf = cairo.PDFSurface(out_svg, width_pt, height_pt)

    ctx = cairo.Context(surf)
    svg.render_cairo(ctx)

    ctx.set_source_rgb(0.0, 0.0, 0.0)
    ctx.select_font_face("Sans")
    ctx.set_font_size(10)
    ctx.move_to(140, 300)

    print_text(ctx, tracks)

    surf.finish()

def print_text(ctx, tracks):
    """Actually prints the text onto the context."""
    for track in tracks:
        print_track(ctx, track)


def print_track(ctx, track):
    short_track = shorten_track(track)
    line_start = ctx.get_current_point()

    height = ctx.text_extents("X")[3]
    width = ctx.text_extents("m")[2]

    col1 = line_start[0] + 3*width
    col2 = 420

    ctx.show_text(str(short_track[0]))
    ctx.move_to(col1, line_start[1])
    ctx.show_text(str(short_track[2]) + \
                  " (" + str(short_track[1]) + ")")
    ctx.move_to(col2, line_start[1])
    ctx.show_text(str(short_track[3]))

    ctx.move_to(line_start[0], line_start[1] + height * 1.5);

def shorten_track(track):
    short_track = list(track)
    for i in (1, 2):
        if len(track[i]) > 25:
            short_track[i] = track[i][0:25] + "..."
    return short_track

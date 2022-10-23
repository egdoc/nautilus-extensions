"""
Add a Nautilus property page to epub files to display book metadata.

Author: Egidio Docile
"""

from gi.repository import GObject, Gtk, Nautilus
from urllib.parse import urlparse, unquote

import epub_meta


class EpubMetadataPropertyPageProvider(GObject.GObject, Nautilus.PropertyPageProvider):

    def get_property_pages(self, files):
        if len(files) != 1:
            return

        file = files[0]
        if file.get_mime_type() != 'application/epub+zip':
            return ()

        metadata = epub_meta.get_epub_metadata(file.get_location().get_path())

        property_label = Gtk.Label('Epub Metadata')
        property_label.show()

        grid = Gtk.Grid()
        grid.props.margin_left = 50
        grid.props.margin_top = 20

        for row, key in enumerate(['authors', 'publisher', 'title']):
            val = ",".join(metadata[key]) if isinstance(metadata[key], list) else metadata[key]
            grid.attach(Gtk.Label(f'{key.capitalize()}: ', xalign=1), 0, row, 1, 1)
            grid.attach(Gtk.Label(val, xalign=0), 1, row, 1, 1)

        grid.show_all()

        page = Nautilus.PropertyPage(
                    name="epub_metadata",
                    label=property_label,
                    page=grid)

        return page,

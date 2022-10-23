"""
Add an action to the Nautilus context-menu to convert png and jpeg images
to the wepb format.

Author: Egidio Docile
"""

from gi.repository import GObject, Nautilus
from PIL import Image


class ConvertToWebpMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    VALID_MIMETYPES = ('image/png', 'image/jpeg')

    def convert(self, menu, files):
        for file in files:
            file_path = file.get_location().get_path()
            image = Image.open(file_path)
            image.save(f"{file_path}.webp", format="webp")

    def get_file_items(self, window, files):
        for file in files:
            if file.get_mime_type() not in self.VALID_MIMETYPES:
                return ()

        menu_item = Nautilus.MenuItem(
                        name="convert_to_webp",
                        label="Convert to wepb")

        menu_item.connect('activate', self.convert, files)

        return menu_item,

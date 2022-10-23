import os
from datetime import datetime

from gi.repository import GObject, Nautilus
from PIL import Image


DATETIME_ORIGINAL=36867


class PicsOrganizerNautilusMenuProvider(GObject.GObject, Nautilus.MenuProvider):
    def organize(self, menu, files):
        for file in files:
            path = file.get_location().get_path()
            filename = os.path.basename(path).replace(' ', '_').lower()
            dirname = os.path.dirname(path)

            try:
                exif_data = Image.open(path)._getexif()
            except OSError:
                continue

            try:
                date = datetime.strptime(exif_data[DATETIME_ORIGINAL], '%Y:%m:%d %H:%M:%S')
                directory = os.path.join(date.strftime('%Y'), date.strftime('%B').lower())
            except (KeyError, ValueError, TypeError):
                directory = "unsorted"

            destination = os.path.join(dirname, directory)
            os.makedirs(destination, exist_ok=True)
            os.rename(path, os.path.join(destination, filename))


    def get_file_items(self, window, files):
        for file in files:
            if not file.get_mime_type() in ('image/jpeg', 'image/png'):
                return ()

        menu_item = Nautilus.MenuItem(
                name='picsort',
                label='Organize by date')

        menu_item.connect('activate', self.organize, files)

        return (menu_item,)

"""
Add a column which displays file permissions in octal notation in Nautilus list
view.

Author: Egidio Docile
"""

import os

from gi.repository import GObject, Nautilus


class OctalPermissionsInfoProvider(GObject.GObject, Nautilus.ColumnProvider, Nautilus.InfoProvider):
    def get_columns(self):
        column = Nautilus.Column(
            name="file_permissions_octal",
            attribute="file_permissions_octal",
            label="Permissions (octal)",
            description="The octal file permissions"
        )

        return column,

    def update_file_info(self, file):
        file_path = file.get_location().get_path()
        octal_permissions = oct(os.stat(file_path).st_mode)[-3:]
        file.add_string_attribute('file_permissions_octal', octal_permissions)

import os
import shutil

from cheat.sheets import Sheets
from cheat.utils import Utils


class Sheet:


    def __init__(self,default_cheat_dir,cheatpath,editor_exec):
        self.sheets_instance = Sheets(default_cheat_dir,cheatpath)
        self.utils_instance = Utils(None,editor_exec)


    def copy(self,current_sheet_path, new_sheet_path):
        """ Copies a sheet to a new path """

        # attempt to copy the sheet to DEFAULT_CHEAT_DIR
        try:
            shutil.copy(current_sheet_path, new_sheet_path)

        # fail gracefully if the cheatsheet cannot be copied. This can happen if
        # DEFAULT_CHEAT_DIR does not exist
        except IOError:
            Utils.die('Could not copy cheatsheet for editing.')


    def create_or_edit(self,sheet):
        """ Creates or edits a cheatsheet """

        # if the cheatsheet does not exist
        if not self.exists(sheet):
            self.create(sheet)

        # if the cheatsheet exists but not in the default_path, copy it to the
        # default path before editing
        elif self.exists(sheet) and not self.exists_in_default_path(sheet):
            self.copy(self.path(sheet), os.path.join(self.sheets_instance.default_path(), sheet))
            self.edit(sheet)

        # if it exists and is in the default path, then just open it
        else:
            self.edit(sheet)


    def create(self,sheet):
        """ Creates a cheatsheet """
        new_sheet_path = os.path.join(self.sheets_instance.default_path(), sheet)
        self.utils_instance.open_with_editor(new_sheet_path)


    def edit(self,sheet):
        """ Opens a cheatsheet for editing """
        self.utils_instance.open_with_editor(self.path(sheet))


    def exists(self,sheet):
        """ Predicate that returns true if the sheet exists """
        return sheet in self.sheets_instance.get() and os.access(self.path(sheet), os.R_OK)


    def exists_in_default_path(self,sheet):
        """ Predicate that returns true if the sheet exists in default_path"""
        default_path_sheet = os.path.join(self.sheets_instance.default_path(), sheet)
        return sheet in self.sheets_instance.get() and os.access(default_path_sheet, os.R_OK)


    def is_writable(self,sheet):
        """ Predicate that returns true if the sheet is writeable """
        return sheet in self.sheets_instance.get() and os.access(self.path(sheet), os.W_OK)


    def path(self,sheet):
        """ Returns a sheet's filesystem path """
        return self.sheets_instance.get()[sheet]


    def read(self,sheet):
        """ Returns the contents of the cheatsheet as a String """
        if not self.exists(sheet):
            Utils.die('No cheatsheet found for ' + sheet)

        with open(self.path(sheet)) as cheatfile:
            return cheatfile.read()

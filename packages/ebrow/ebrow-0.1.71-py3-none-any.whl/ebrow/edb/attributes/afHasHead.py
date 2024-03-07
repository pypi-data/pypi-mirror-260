"""
******************************************************************************

    Echoes Data Browser (Ebrow) is a data navigation and report generation
    tool for Echoes.
    Echoes is a RF spectrograph for SDR devices designed for meteor scatter
    Both copyright (C) 2018-2023
    Giuseppe Massimo Bertani gm_bertani(a)yahoo.it

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, version 3 of the License.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, http://www.gnu.org/copyleft/gpl.html

*******************************************************************************

"""

from PyQt5.QtWidgets import QDialog
from edb.attributes.ui_afhashead import Ui_afHasHead
from edb.logprint import print
from edb.utilities import splitASCIIdumpFile, splitBinaryDumpFile


class HasHead(QDialog):
    """
    This filter detects the presence of a head echo.
    It cannot rely on Raise front data uniquely, they
    must be integrated with information taken
    from the related dump file, so this filter
    cannot work if dumps are disabled and evalFilter()
    will return always None in this case.
    """
    def __init__(self, parent, ui, settings):
        QDialog.__init__(self)
        self._parent = parent
        self._ui = Ui_afHasHead()
        self._ui.setupUi(self)
        self._ui.pbOk.setEnabled(True)
        self._ui.pbOk.clicked.connect(self.accept)
        self._settings = settings
        self._enabled = False
        self._load()
        print("HasHead loaded")

    def _load(self):
        """
        loads this filter's parameters
        from settings file
        """
        self._enabled = self._settings.readSettingAsBool('afHasHeadEnabled')

    def _save(self):
        """
        save ths filter's parameters
        to settings file
        """
        self._settings.writeSetting('afHasHeadEnabled', self._enabled)

    def evalFilter(self, evId: int) -> bool:
        """
        Calculates the frequency shift of the head echo from a DATB if present.
        The results must be stored by the caller.
        Returns a dictionary containing the positive and negative shifts
        centered on the carrier.
        A None value means that the calculation was impossible
        due to missing data
        """

        df = self._parent.datasource.getEventData(evId)
        datName, datData, dailyNr, utcDate = self._parent.dataSource.extractDumpData(evId)
        if datName is not None and datData is not None:
            if ".datb" in datName:
                dfMap, dfPower = splitBinaryDumpFile(datData)
            else:
                dfMap, dfPower = splitASCIIdumpFile(datData)

        # dfMap is a table time,freq,S

    def getParameters(self):
        """
        displays the parametrization dialog
        and gets the user's settings
        """
        print("HasHead.getParameters()")
        self._save()
        return None

    def isFilterEnabled(self) -> bool:
        return self._enabled

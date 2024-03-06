###############################################################################
# (c) Copyright 2023 CERN for the benefit of the LHCb Collaboration           #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from DIRAC import gLogger
from DIRAC.Core.Utilities.ReturnValues import S_OK, DReturnType


class NewOracleBookkeepingDB:
    def __init__(self, *, dbW, dbR):
        self.log = gLogger.getSubLogger("LegacyOracleBookkeepingDB")
        self.dbW_ = dbW
        self.dbR_ = dbR

    def getAvailableFileTypes(self) -> DReturnType[list[str]]:
        """Retrieve all available file types from the database."""
        return self.dbR_.executeStoredProcedure("BOOKKEEPINGORACLEDB.getAvailableFileTypes", [])

    def getAvailableSMOG2States(self) -> DReturnType[list[str]]:
        """Retrieve all available SMOG2 states."""
        retVal = self.dbR_.query("SELECT state FROM smog2")
        if not retVal["OK"]:
            return retVal
        return S_OK([i[0] for i in retVal["Value"]])

    def getRunsForSMOG2(self, state: str) -> DReturnType[list[int]]:
        """Retrieve all runs with specified SMOG2 state

        :param sr state: required state
        """
        retVal = self.dbR_.query(
            "SELECT runs.runnumber FROM smog2"
            " LEFT JOIN runs ON runs.smog2_id = smog2.id"
            f" WHERE smog2.state  = '{state}'"
        )
        if not retVal["OK"]:
            return retVal
        return S_OK([int(i[0]) for i in retVal["Value"]])

    def setSMOG2State(self, state: str, update: bool, runs: list[int]) -> DReturnType[None]:
        """Set SMOG2 state for runs.

        :param str state: state for given runs
        :param bool update: when True, updates existing state, when False throw an error in such case
        :param list[int] runs: runs list
        """
        return self.dbW_.executeStoredProcedure(
            "BOOKKEEPINGORACLEDB.setSMOG2", parameters=[state, update], output=False, array=runs
        )

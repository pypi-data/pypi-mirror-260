# This file is part of daf_butler.
#
# Developed for the LSST Data Management System.
# This product includes software developed by the LSST Project
# (http://www.lsst.org).
# See the COPYRIGHT file at the top-level directory of this distribution
# for details of code ownership.
#
# This software is dual licensed under the GNU General Public License and also
# under a 3-clause BSD license. Recipients may choose which of these licenses
# to use; please see the files gpl-3.0.txt and/or bsd_license.txt,
# respectively.  If you choose the GPL option then the following text applies
# (but note that there is still no warranty even if you opt for BSD instead):
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Specialized Butler exceptions."""
__all__ = ("DatasetTypeNotSupportedError", "EmptyQueryResultError", "ValidationError")


class DatasetTypeNotSupportedError(RuntimeError):
    """A `DatasetType` is not handled by this routine.

    This can happen in a `Datastore` when a particular `DatasetType`
    has no formatters associated with it.
    """

    pass


class ValidationError(RuntimeError):
    """Some sort of validation error has occurred."""

    pass


class EmptyQueryResultError(Exception):
    """Exception raised when query methods return an empty result and `explain`
    flag is set.

    Parameters
    ----------
    reasons : `list` [`str`]
        List of possible reasons for an empty query result.
    """

    def __init__(self, reasons: list[str]):
        self.reasons = reasons

    def __str__(self) -> str:
        # There may be multiple reasons, format them into multiple lines.
        return "Possible reasons for empty result:\n" + "\n".join(self.reasons)

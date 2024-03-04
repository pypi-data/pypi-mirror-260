# Copyright 2024 Patrick C. Tapping
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program.  If not, see <http://www.gnu.org/licenses/>.

__all__ = ["MFF101"]

from .aptdevice_motor import APTDevice_Motor
from ..enums import EndPoint


class MFF101(APTDevice_Motor):
    """
    A class specific to the ThorLabs MFF101 motion controller.

    Note that several advanced features are not yet implemented.

    As it is a single bay/channel controller, aliases of ``status = status_[0][0]``
    etc are created for convenience.

    :param serial_port: Serial port device the device is connected to.
    :param vid: Numerical USB vendor ID to match.
    :param pid: Numerical USB product ID to match.
    :param manufacturer: Regular expression to match to a device manufacturer string.
    :param product: Regular expression to match to a device product string.
    :param serial_number: Regular expression matching the serial number of device to search for.
    :param location: Regular expression to match to a device bus location.
    :param home: Perform a homing operation on initialisation.
    :param invert_direction_logic: Invert the meaning of "forward" and "reverse".
    :param swap_limit_switches: Swap the "forward" and "reverse" limit switch signals.
    """

    def __init__(self, serial_port=None, vid=None, pid=None, manufacturer=None, product=None, serial_number="37",
                 location=None, home=True, invert_direction_logic=False, swap_limit_switches=False):
        super().__init__(serial_port=serial_port, vid=vid, pid=pid, manufacturer=manufacturer, product=product,
                         serial_number=serial_number, location=location, home=home,
                         invert_direction_logic=invert_direction_logic, swap_limit_switches=swap_limit_switches,
                         status_updates="auto", controller=EndPoint.RACK, bays=(EndPoint.BAY0,), channels=(1,))

        self.status = self.status_[0][0]
        """Alias to first bay/channel of :data:`APTDevice_Motor.status_`."""

        self.velparams = self.velparams_[0][0]
        """Alias to first bay/channel of :data:`APTDevice_Motor.velparams_`"""

        self.genmoveparams = self.genmoveparams_[0][0]
        """Alias to first bay/channel of :data:`APTDevice_Motor.genmoveparams_`"""

        self.jogparams = self.jogparams_[0][0]
        """Alias to first bay/channel of :data:`APTDevice_Motor.jogparams_`"""

    def _process_message(self, m):
        super()._process_message(m)

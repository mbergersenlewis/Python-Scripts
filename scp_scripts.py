import jxmlease
from jnpr.junos import Device
from pprint import pprint
from lxml import etree
from jnpr.junos.utils.config import Config
import jnpr.junos.exception
from jnpr.junos.utils.scp import SCP


class Junos_op_scripts(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def PushOps(self, hostname):
        ## Shows interfaces in Smart Rack vlan ##
        self.hostname = hostname
        try:
            connect = Device(
                host=self.hostname, username=self.username, password=self.password).open()
            successful_message = "You have successfully loaded, iv-link.slax, mac-address-count.slax, show-bpdu-errors.slax and show-storm-errors.slax on to this device! "
            if connect.facts['model'] == ''
            with SCP(dev, progress=True) as scp:
                scp.put("iv-link.slax", remote_path="/var/db/scripts/op/")
                scp.put("mac-address-count.slax",
                        remote_path="/var/db/scripts/op/")
                scp.put("show-bpdu-errors.slax",
                        remote_path="/var/db/scripts/op/")
                scp.put("show-storm-errors.slax",
                        remote_path="/var/db/scripts/op/")
            connect.close()
            return {"result": successful_message}

        except jnpr.junos.exception.ConnectError as err:
            print(' Error: ' + repr(err))

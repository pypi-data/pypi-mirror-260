from extras.plugins import PluginConfig
# from dcim.models import Device
# from virtualization.models import VirtualMachine, Cluster
# from ipam.models import L2VPN, ASN, IPAddress, IPRange, Prefix, VLAN
# from extras.models import CustomField


class NetboxSubsystems(PluginConfig):
    name = 'netbox_subsystems'
    verbose_name = 'Системы и подсистемы'
    description = 'Manage subsystems in Netbox'
    version = '0.2.8'
    author = 'Ilya Zakharov'
    author_email = 'me@izakharov.ru'
    min_version = '3.2.0'
    base_url = 'subsystems'
    default_settings = {
        "enable_navigation_menu": True,
        "enable_subsystems": True,
        "subsystems_location": "left",
    }


config = NetboxSubsystems



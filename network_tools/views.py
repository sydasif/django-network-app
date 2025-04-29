import ipaddress

from django.http import JsonResponse
from django.shortcuts import render
from netutils.ip import (
    cidr_to_netmask,
    get_all_host,
    get_broadcast_address,
    get_first_usable,
    get_usable_range,  # ADDED
    is_ip,
    is_netmask,
    netmask_to_cidr,
)
from netutils.ping import tcp_ping

from . import forms


def home(request):
    """Renders the home page."""
    return render(request, "network_tools/home.html")


def ping(request):
    """
    Handles TCP ping requests.

    Retrieves 'ip' and 'port' from GET parameters, performs a TCP ping,
    and either returns a JSON response (for AJAX requests)
    or renders the ping results page.

    Context passed to template:
        test_result (str): A message indicating the ping success or failure,
                           or an error message if input is invalid.
    """
    test_result = {}
    ping_form = forms.PingForm(request.GET)

    ip_address = request.GET.get("ip")
    port_str = request.GET.get("port")

    if not ip_address:
        test_result["test_result"] = "Please enter an IP Address"
    elif not port_str:
        test_result["test_result"] = "Please enter a TCP Port"
    else:
        if is_ip(ip_address) is False:
            test_result["test_result"] = "Please enter a valid IP Address"
        else:
            try:
                port = int(port_str)
                if 0 <= port <= 65535:
                    host_ip = ip_address
                    host_port = port
                    ping_result = tcp_ping(host_ip, host_port)
                    if ping_result is True:
                        test_result["test_result"] = (
                            f"Success: Port {host_port} is Open on host {host_ip}"
                        )
                    else:
                        test_result["test_result"] = (
                            f"Failure: Cannot open connection to Port {host_port} on host {host_ip}"
                        )
                else:
                    test_result["test_result"] = (
                        "Please enter a valid TCP Port (0-65535)"
                    )
            except ValueError:
                test_result["test_result"] = "Please enter a valid TCP Port (0-65535)"

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(test_result)
    else:
        return render(
            request,
            "network_tools/ping.html",
            {"test_result": test_result, "ping_form": ping_form},
        )


def _handle_cidr_to_netmask(cidr_param):
    """Helper function to handle CIDR to Netmask conversion."""
    try:
        cidr = int(cidr_param)
        if 1 <= cidr <= 32:
            netmask_result = cidr_to_netmask(cidr)
            return {
                "netmask_result": f"Netmask for CIDR value {cidr} is {netmask_result}"
            }
        else:
            return {"netmask_result": "CIDR value must be between 1 and 32"}
    except ValueError:
        return {"netmask_result": "Invalid CIDR value"}


def _handle_netmask_to_cidr(netmask_param):
    """Helper function to handle Netmask to CIDR conversion."""
    if is_netmask(netmask_param) is False:
        return {"cidr_result": "Please enter a valid Netmask"}
    else:
        cidr_value = netmask_to_cidr(netmask_param)
        return {
            "cidr_result": f"CIDR Value for netmask {netmask_param} is {cidr_value}"
        }


def _handle_get_all_hosts(network_cidr_param):
    """Helper function to handle getting all hosts from a network CIDR."""
    try:
        ipaddress.ip_network(network_cidr_param, strict=False)
        host_list = list(get_all_host(network_cidr_param))
        return {"host_list": host_list}
    except ValueError as e:
        return {"host_list_error": str(e)}


def _handle_get_broadcast_address(broadcast_network_cidr_param):
    """Helper function to handle getting the broadcast address from a network CIDR."""
    try:
        broadcast_address = get_broadcast_address(broadcast_network_cidr_param)
        return {"broadcast_result": f"Broadcast address: {broadcast_address}"}
    except ValueError as e:
        return {"broadcast_result": str(e)}


def _handle_get_first_usable(first_usable_network_cidr_param):
    """Helper function to handle getting the first usable IP address from a network CIDR."""
    try:
        first_usable_address = get_first_usable(first_usable_network_cidr_param)
        return {"first_usable_result": f"First usable address: {first_usable_address}"}
    except ValueError as e:
        return {"first_usable_result": str(e)}


def _handle_get_usable_range(usable_range_network_cidr_param):  # ADDED
    """Helper function to handle getting the usable IP range from a network CIDR."""
    try:
        usable_range = get_usable_range(usable_range_network_cidr_param)
        return {"usable_range_result": f"Usable IP range: {usable_range}"}
    except ValueError as e:
        return {"usable_range_result": str(e)}


def ip_addr(request):
    """
    Handles various IP address and CIDR/Netmask conversions.

    Retrieves 'cidr', 'netmask', 'network_cidr', 'broadcast_network_cidr',
    'first_usable_network_cidr', or 'usable_range_network_cidr' from GET
    parameters, performs the requested conversion or calculation using netutils,
    and either returns a JSON response (for AJAX requests) or renders the IP
    address tools page.

    Context passed to template:
        netmask_result (str, optional): Result of CIDR to Netmask conversion.
        cidr_result (str, optional): Result of Netmask to CIDR conversion or error.
        host_list (list, optional): List of host IPs generated from network_cidr.
        host_list_error (str, optional): Error message if network_cidr is invalid.
        broadcast_result (str, optional): Result of getting broadcast address.
        first_usable_result (str, optional): Result of getting first usable address.
        usable_range_result (str, optional): Result of getting usable IP range.  # ADDED
    """
    test_result = {}
    cidr_to_netmask_form = forms.CidrToNetmaskForm(request.GET)
    netmask_to_cidr_form = forms.NetmaskToCidrForm(request.GET)
    get_all_hosts_form = forms.GetAllHostsForm(request.GET)
    get_broadcast_address_form = forms.GetBroadcastAddressForm(request.GET)
    get_first_usable_form = forms.GetFirstUsableForm(request.GET)
    get_usable_range_form = forms.GetUsableRangeForm(request.GET)  # ADDED

    if request.GET.get("cidr"):
        test_result.update(_handle_cidr_to_netmask(request.GET["cidr"]))
    elif request.GET.get("netmask"):
        test_result.update(_handle_netmask_to_cidr(request.GET["netmask"]))
    elif request.GET.get("network_cidr"):
        test_result.update(_handle_get_all_hosts(request.GET["network_cidr"]))
    elif request.GET.get("broadcast_network_cidr"):
        test_result.update(
            _handle_get_broadcast_address(request.GET["broadcast_network_cidr"])
        )
    elif request.GET.get("first_usable_network_cidr"):
        test_result.update(
            _handle_get_first_usable(request.GET["first_usable_network_cidr"])
        )
    elif request.GET.get("usable_range_network_cidr"):  # ADDED
        test_result.update(
            _handle_get_usable_range(request.GET["usable_range_network_cidr"])
        )

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse(test_result)
    else:
        return render(
            request,
            "network_tools/ip_addr.html",
            {
                "test_result": test_result,
                "cidr_to_netmask_form": cidr_to_netmask_form,
                "netmask_to_cidr_form": netmask_to_cidr_form,
                "get_all_hosts_form": get_all_hosts_form,
                "get_broadcast_address_form": get_broadcast_address_form,
                "get_first_usable_form": get_first_usable_form,
                "get_usable_range_form": get_usable_range_form,  # ADDED
            },
        )

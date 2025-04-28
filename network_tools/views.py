from django.shortcuts import render
from netutils.ping import tcp_ping
from netutils.ip import (
    is_ip,
    cidr_to_netmask,
    netmask_to_cidr,
    is_netmask,
    cidr_to_netmaskv6,
    get_all_host,
)


def home(request):
    """Renders the home page."""
    return render(request, "network_tools/home.html")


def ping(request):
    """
    Handles TCP ping requests.

    Retrieves 'ip' and 'port' from GET parameters, performs a TCP ping,
    and renders the ping results page.

    Context passed to template:
        test_result (str): A message indicating the ping success or failure,
                           or an error message if input is invalid.
    """
    test_result = {}

    if request.GET.get("ip") == "":
        test_result["test_result"] = f"Please enter an IP Address {request.GET}"
    elif "ip" in request.GET:
        if is_ip(request.GET["ip"]) is False:
            test_result["test_result"] = "Please enter a valid IP Address"
            return render(request, "network_tools/ping.html", test_result)
        host_ip = request.GET["ip"]
        host_port = request.GET["port"]
        ping_result = tcp_ping(host_ip, host_port)
        if ping_result is True:
            test_result["test_result"] = (
                f"Success: Port {host_port} is Open on host {host_ip}"
            )
        else:
            test_result["test_result"] = (
                f"Failure: Cannot open connection to Port {host_port} on host {host_ip}"
            )

    return render(request, "network_tools/ping.html", test_result)


def _handle_cidr_to_netmask(cidr_param):
    """Helper function to handle CIDR to Netmask conversion."""
    try:
        cidr = int(cidr_param)
        netmask_result = cidr_to_netmask(cidr)
        return {"netmask_result": f"Netmask for CIDR value {cidr} is {netmask_result}"}
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


def _handle_cidr_v6_to_netmask(cidr_v6_param):
    """Helper function to handle IPv6 CIDR to Netmask conversion."""
    try:
        cidr_v6 = int(cidr_v6_param)
        netmask_v6_result = cidr_to_netmaskv6(cidr_v6)
        return {
            "netmask_v6_result": f"Netmask for CIDR value {cidr_v6} is {netmask_v6_result}"
        }
    except ValueError:
        return {"netmask_v6_result": "Invalid CIDR value"}


def _handle_get_all_hosts(network_cidr_param):
    """Helper function to handle getting all hosts from a network CIDR."""
    try:
        host_list = list(get_all_host(network_cidr_param))
        return {"host_list": host_list}
    except ValueError as e:
        return {"host_list_error": str(e)}


def ip_addr(request):
    """
    Handles various IP address and CIDR/Netmask conversions.

    Retrieves 'cidr', 'netmask', 'cidr_v6', or 'network_cidr' from GET
    parameters, performs the requested conversion or calculation using
    netutils, and renders the IP address tools page.

    Context passed to template:
        netmask_result (str, optional): Result of CIDR to Netmask conversion.
        cidr_result (str, optional): Result of Netmask to CIDR conversion or error.
        netmask_v6_result (str, optional): Result of IPv6 CIDR to Netmask conversion.
        host_list (list, optional): List of host IPs generated from network_cidr.
        host_list_error (str, optional): Error message if network_cidr is invalid.
    """
    test_result = {}

    if request.GET.get("cidr"):
        test_result.update(_handle_cidr_to_netmask(request.GET["cidr"]))
    elif request.GET.get("netmask"):
        test_result.update(_handle_netmask_to_cidr(request.GET["netmask"]))
    elif request.GET.get("cidr_v6"):
        test_result.update(_handle_cidr_v6_to_netmask(request.GET["cidr_v6"]))
    elif request.GET.get("network_cidr"):
        test_result.update(_handle_get_all_hosts(request.GET["network_cidr"]))

    return render(request, "network_tools/ip_addr.html", test_result)

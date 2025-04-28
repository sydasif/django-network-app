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
        cidr = int(request.GET["cidr"])
        netmask_result = cidr_to_netmask(cidr)
        test_result["netmask_result"] = (
            f"Netmask for CIDR value {cidr} is {netmask_result}"
        )

    if request.GET.get("netmask"):
        netmask = request.GET["netmask"]
        if is_netmask(netmask) is False:
            test_result["cidr_result"] = "Please enter a valid Netmask"
        else:
            cidr_value = netmask_to_cidr(netmask)
            test_result["cidr_result"] = (
                f"CIDR Value for netmask {netmask} is {cidr_value}"
            )

    if request.GET.get("cidr_v6"):
        cidr_v6 = int(request.GET["cidr_v6"])
        netmask_v6_result = cidr_to_netmaskv6(cidr_v6)
        test_result["netmask_v6_result"] = (
            f"Netmask for CIDR value {cidr_v6} is {netmask_v6_result}"
        )

    if request.GET.get("network_cidr"):
        network_cidr = request.GET["network_cidr"]
        try:
            host_list = list(get_all_host(network_cidr))
            test_result["host_list"] = host_list
        except ValueError as e:
            test_result["host_list_error"] = str(e)

    return render(request, "network_tools/ip_addr.html", test_result)

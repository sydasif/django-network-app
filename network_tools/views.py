from django.shortcuts import render
from netutils.ping import tcp_ping
from netutils.ip import is_ip, cidr_to_netmask, netmask_to_cidr, is_netmask


def home(request):
    return render(request, "network_tools/home.html")


def ping(request):
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
    test_result = {}

    if request.GET.get("cidr") == "":
        test_result["test_result"] = "Please a valid CIDR value [1-24]"
    elif "cidr" in request.GET:
        cidr = int(request.GET["cidr"])
        netmask_result = cidr_to_netmask(cidr)
        test_result["netmask_result"] = (
            f"Netmask for CIDR value {cidr} is {netmask_result}"
        )
    elif "netmask" in request.GET:
        netmask = request.GET["netmask"]
        if is_netmask(netmask) is False:
            test_result["cidr_result"] = "Please enter a valid Netmask"
            return render(request, "network_tools/ip_addr.html", test_result)
        cidr_value = netmask_to_cidr(netmask)
        test_result["cidr_result"] = f"CIDR Value for netmask {netmask} is {cidr_value}"

    return render(request, "network_tools/ip_addr.html", test_result)

import subprocess
import click
import json


def get_interfaces_data():
    """Retrieve information about the network interfaces of the computer."""

    args = ["ip", "--json", "address"]
    result = subprocess.run(args, capture_output=True, text=True)

    if result.returncode != 0:
        click.echo(result.stderr, err=True)
        exit(-1)

    return json.loads(result.stdout)


def get_interface_ip(interface_name: str):
    """
    Retrieve the first IP address from a specified interface.
    If the specified interface is not found, fallback to the first non-loopback interface.
    """

    interfaces = get_interfaces_data()

    # Try to find the requested interface
    for i in interfaces:
        if i["ifname"] == interface_name:
            interface = i
            break

    # fallback to first non lookback interface
    else:
        for i in interfaces:
            if "LOOPBACK" not in i["flags"]:
                click.secho(f"WARN: {interface_name} not found, using {i['ifname']} interface", fg="black")
                interface = i
                break

    # If we did not find an interface, exit
    if interface is None or not any(interface["addr_info"]):
        click.echo("Could not find an interface to bind", err=True)
        exit(-1)

    return interface["addr_info"][0]["local"]

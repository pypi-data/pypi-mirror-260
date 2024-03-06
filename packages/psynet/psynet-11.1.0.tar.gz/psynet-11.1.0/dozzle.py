def setup_dozzle(ssh_host, ssh_user, dozzle_username, dozzle_password, ip_address):
    from dallinger.command_line.docker_ssh import Executor, get_dns_host, get_sftp
    from io import BytesIO

    executor = Executor(ssh_host, user=ssh_user)
    executor.run('mkdir -p ~/dallinger')
    executor.run('mkdir -p ~/dallinger/dozzle')
    # compose_file = f"""
    # version: "3"
    # services:
    #   dozzle:
    #     container_name: dozzle
    #     image: amir20/dozzle:latest
    #     volumes:
    #       - /var/run/docker.sock:/var/run/docker.sock
    #       - /home/{ssh_user}/dallinger/dozzle:/data
    #     ports:
    #       - 9999:8080
    #     networks:
    #       - dallinger
    #     environment:
    #       DOZZLE_AUTH_PROVIDER: simple
    # networks:
    #   dallinger:
    #     name: dallinger
    # """
    # executor.run(f'echo \'{compose_file}\' > ~/dallinger/dozzle/docker-compose.yml')

    # password_hash = sha256(dozzle_password.encode('utf-8')).hexdigest()
    # users_file = f"""
    # users:
    #   {dozzle_username}:
    #     name: "Admin"
    #     password: "{password_hash}"
    # """
    # executor.run(f'echo \'{users_file}\' > ~/dallinger/dozzle/users.yml')

    executor.run('cd ~/dallinger/dozzle && sudo docker compose up -d')
    nipio = f'dozzle.{ip_address}.nip.io'
    caddyfile = f"""
    {nipio} {{
        reverse_proxy dozzle:8080
    }}"""

    executor.run("mkdir -p ~/dallinger/caddy.d")

    dns_host = get_dns_host(ssh_host)
    tls = "tls internal"

    sftp = get_sftp(ssh_host, user=ssh_user)
    sftp.putfo(BytesIO(DOCKER_COMPOSE_SERVER), "dallinger/docker-compose.yml")

    sftp.putfo(
        BytesIO(CADDYFILE.format(host=dns_host, tls=tls).encode()),
        "dallinger/Caddyfile",
    )
    executor.run(f'echo "{caddyfile}" > ~/dallinger/caddy.d/dozzle')
    executor.run("sudo docker compose -f ~/dallinger/docker-compose.yml up -d")
    print(
        f'Dozzle available at https://{nipio}. Takes a few minutes to start up. '
        f'You can log in with username {dozzle_username} and password {dozzle_password}.'
    )

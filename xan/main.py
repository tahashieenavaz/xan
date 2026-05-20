import fire


def xan_command(name: str):
    print(f"Hello {name}!")


def main():
    fire.Fire(xan_command)

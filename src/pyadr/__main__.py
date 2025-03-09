from pyadr import cli

def main() -> int:
    cliargs = cli.parse_args()
    return cliargs.entrypoint(cliargs)


if __name__ == "__main__":
    exit(main())

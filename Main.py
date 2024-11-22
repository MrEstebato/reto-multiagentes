import argparse, datetime, volume_calculation, simulation


def main():
    parser = argparse.ArgumentParser("Reto Multiagentes")
    subparsers = parser.add_subparsers()
    parser.set_defaults(func=None)

    subparser = subparsers.add_parser("Simulacion", description="Corre simulacion")
    subparser.add_argument(
        "--lifters", required=False, type=int, help="Numero de montacargas", default =1
    )

    subparser.add_argument(
        "--Delta",
        required=False,
        type=float,
        default=0.05,
        help="Velocidad de simulacion",
    )
    subparser.add_argument("--theta", required=False, type=float, default=0, help="")
    subparser.add_argument("--radious", required=False, type=float, default=30, help="")
    subparser.set_defaults(func=simulation.Simulacion)

    subparser = subparsers.add_parser(
        "BinPacking", description="Resolver el problema del bin packing"
    )
    subparser.add_argument("--ListaCSV", required=True, type=str)
    subparser.add_argument("--Confianza", required=True, type=float)
    subparser.add_argument("--VRackC", required=True, type=str)
    subparser.add_argument("--VRackR", required=True, type=str)
    subparser.add_argument("--VRackS", required=True, type=str)
    subparser.add_argument("--salidaCSV", required=True, type=str)
    subparser.set_defaults(func=volume_calculation.calculate_volume)

    subparser.set_defaults()
    Options = parser.parse_args()

    Options.func(Options)


if __name__ == "__main__":
    print(
        "\n"
        + "\033[0;32m"
        + "[start] "
        + str(datetime.datetime.now())
        + "\033[0m"
        + "\n"
    )
    main()
    print(
        "\n" + "\033[0;32m" + "[end] " + str(datetime.datetime.now()) + "\033[0m" + "\n"
    )

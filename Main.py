import argparse, datetime, volume_calculation

def main():
	parser = argparse.ArgumentParser("Reto Multiagentes");
	subparsers = parser.add_subparsers();

	subparser = subparsers.add_parser("BinPacking", description="Resolver el problema del bin packing")
	subparser.add_argument("--ListaCSV", required = True, type = str)
	subparser.add_argument("--Confianza", required = True, type = float)
	subparser.add_argument("--VRackC", required = True, type = str)
	subparser.add_argument("--VRackR", required = True, type = str)
	subparser.add_argument("--VRackS", required = True, type = str)
	subparser.add_argument("--salidaCSV", required = True, type = str)
	subparser.set_defaults(func = volume_calculation.VolCalc)

	subparser.set_defaults()
	Options = parser.parse_args();
	
	print(str(Options) + "\n");

	Options.func(Options);


if __name__ == "__main__":
	print("\n" + "\033[0;32m" + "[start] " + str(datetime.datetime.now()) + "\033[0m" + "\n");
	main();
	print("\n" + "\033[0;32m" + "[end] "+ str(datetime.datetime.now()) + "\033[0m" + "\n");




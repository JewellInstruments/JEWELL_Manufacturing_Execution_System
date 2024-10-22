import json

with open("RUBY_PN_CONSTANTS.json") as RUBY_json:
    preDefinedParts = json.load(RUBY_json)

# globals used for custom range builder and pre defined calibration constants via json
# info for cli custom builder
singleSupplyOffsetRatio = 32.0543
dualSupplyOffsetRatio = 2.6686
nativeDualSupplyGain = 4.5484
nativeSingleSupplyGain = 3.0350
memsLowAccChip = 2
memsHighAccChip = 10


# functions for printing strings in different colors
def prCyan(skk):
    print("\033[96m {}\033[00m".format(skk), end="", flush=True)


# function for building custom models where they may not currently exist in the system, returns as json
def get_custom_parameters():
    # mini command loop for custom builder
    flag = True
    while flag:
        CustomModel = ""
        print("Enter", end="", flush=True)
        prCyan("a")
        print(" for an accelerometer, or", end="", flush=True)
        prCyan("i")
        print(" for an inclinometer")
        InputType = input()

        match InputType:
            case "a":
                CustomModel = "JMHA" + "-"
            case "i":
                CustomModel = "JMHI" + "-"
            case _:
                print("parameter failed!")
                continue

        print("Enter", end="", flush=True)
        prCyan("number of axes")
        print(", up to a maximum of", end="", flush=True)
        match InputType:
            case "a":
                prCyan("3\n")
            case "i":
                prCyan("2\n")
        AxesCount = int(input())

        match InputType:
            case "a":
                if AxesCount <= 3 and AxesCount != 0:
                    CustomModel = CustomModel + str(AxesCount * 100) + "-"
                else:
                    print("parameter failed!")
                    continue
            case "i":
                if AxesCount <= 2 and AxesCount != 0:
                    CustomModel = CustomModel + str(AxesCount * 100) + "-"
                else:
                    print("parameter failed!")
                    continue
            case _:
                print("parameter failed!")
                continue

        print("Enter", end="", flush=True)
        prCyan("m12")
        print(" for a unit with a m12 connector, or", end="", flush=True)
        prCyan("db9")
        print(" for a unit with a db9 connector")
        connector = input()

        match connector:
            case "db9":
                CustomModel = CustomModel + "1-"
            case "m12":
                CustomModel = CustomModel + "4-"
            case _:
                print("parameter failed!")
                continue

        print("Enter", end="", flush=True)
        prCyan("v")
        print(" for a voltage output unit, or", end="", flush=True)
        prCyan("c")
        print(" for a current output unit")
        OutputType = input()

        print("Enter", end="", flush=True)
        prCyan("true")
        print(" for a single supply (0-5V / 4-20mA) unit, or", end="", flush=True)
        prCyan("false")
        print(" for a dual supply (+/- 5V) unit")
        tempDict = {"true": True, "false": False}
        targetSupply = tempDict.get(input())

        match OutputType:
            case "v":
                match targetSupply:
                    case True:
                        CustomModel = CustomModel + "S-"
                    case False:
                        CustomModel = CustomModel + "D-"
                    case _:
                        print("parameter failed!")
                        continue
            case "c":
                match targetSupply:
                    case True:
                        CustomModel = CustomModel + "L-"
                    case _:
                        print("parameter failed!")
                        continue
            case _:
                print("parameter failed!")
                continue

        print("Enter desired range in", end="", flush=True)
        match InputType:
            case "a":
                prCyan("g's")
            case "i":
                prCyan("degrees")
        print(" (max of ", end="", flush=True)
        match InputType:
            case "a":
                prCyan("10")
            case "i":
                prCyan("90")
        print(")")
        targetRange = float(input())

        match InputType:
            case "a":
                if targetRange <= 10:
                    CustomModel = CustomModel + f"{targetRange:.1f}"
                else:
                    print("parameter failed!")
                    continue
            case "i":
                if targetRange <= 90:
                    CustomModel = CustomModel + f"{targetRange:.1f}"
                else:
                    print("parameter failed!")
                    continue

        flag = False
        # because typos are a thing
        if targetRange is None or targetSupply is None or connector is None:
            print(
                "one or more parameters failed, hit enter to retry or use 'exit' to quit"
            )
            match input():
                case "exit":
                    exit()
                case _:
                    flag = True

    # now we can begin to build the custom model
    custom = {
        "model": CustomModel,
        "generic": True,
        "pca": "",
        "connector": "",
        "singleSupply": False,
        "offsetRatio": 1,
        "gain": 1,
    }

    custom["singleSupply"] = targetSupply
    match connector:
        case "m12":
            custom["connector"] = "F879930"
        case "db9":
            custom["connector"] = "F879929"
        case _:
            custom["connector"] = ""

    match targetSupply:
        case True:
            custom["offsetRatio"] = singleSupplyOffsetRatio
            match (targetRange <= memsLowAccChip):
                case True:
                    custom["gain"] = (
                        memsLowAccChip * nativeSingleSupplyGain
                    ) / targetRange
                    custom["pca"] = "F879926-997"
                case False:
                    custom["gain"] = (
                        memsHighAccChip * nativeSingleSupplyGain
                    ) / targetRange
                    custom["pca"] = "F879926-998"
        case False:
            custom["offsetRatio"] = dualSupplyOffsetRatio
            match (targetRange <= memsLowAccChip):
                case True:
                    custom["gain"] = (
                        memsLowAccChip * nativeDualSupplyGain
                    ) / targetRange
                    custom["pca"] = "F879926-997"
                case False:
                    custom["gain"] = (
                        memsHighAccChip * nativeDualSupplyGain
                    ) / targetRange
                    custom["pca"] = "F879926-998"

    # convert python dict to json, this ensures universial functionality of get_kanban_parts
    custom = json.dumps(custom)
    return json.loads(custom)


# takes in model (json) and prints out some parts used in the kanban depending on the desired part (RUBY only)
# does not call out hardware, epoxy, solder, or other small items
def get_kanban_parts(part):
    print("To build model: " + part["model"] + " you will need:")
    prCyan("PCA: " + part["pca"] + "\n")
    prCyan("Connector: " + part["connector"] + "\n")
    match part[
        "connector"
    ]:  # tells the user the housing cover compaitible with the connector
        case "F879929":
            prCyan("Housing: F848853-002" + "\n")
        case "F879930":
            prCyan("Housing: F848853-001" + "\n")
        case _:
            pass
    prCyan("Baseplate: F848852" + "\n")  # baseplate used for all analog RUBYs
    return


# walks through the process of building up PCAs (based on the REV 5 schematic for RUBY)
def pca_sbr_buildup(part):
    part = preDefinedParts.get(part)
    if part is None:
        return
    if part["generic"]:

        match part["singleSupply"]:
            case True:
                print("Populate the following SBRs")
                prCyan("R3 - 30k")
                prCyan("R7 - 0 Ohm")
                prCyan("R9, R16, R23 - 3.16k")
            case False:
                print("Populate the following SBRs")
                prCyan("R9, R16, R23 - 37.4k")

        print("\nhit enter when ready for next step")
        input()

        match part["model"][11]:
            case "L":
                print("Remove the following SBRs")
                prCyan("R31, R36, R41, R47, R57, R66")
                print("\nhit enter when ready for next step")
                input()
                print("Add the following SBRs")
                prCyan("R30, R35, R40, R49, R59, R68, R55, R64, R73 - 0 Ohm")
                print("\nhit enter when ready for next step")
                input()
            case _:
                # generic PCAs are all pre configured for voltage signal out
                pass

    print("SBR configuration complete!")
    return


# walks through the process of building up PCAs (based on the REV 5 schematic for RUBY)
# TODO: maybe use a gui to point out the specific positions of SBT resistors?
def pca_sbt_buildup(sbt):
    print("Populate the following SBTs")
    prCyan("R13 - " + str(sbt["offset_X"]) + "\n")
    prCyan("R8 - " + str(sbt["scale_X"]) + "\n")
    prCyan("R20 - " + str(sbt["offset_Y"]) + "\n")
    prCyan("R15 - " + str(sbt["scale_Y"]) + "\n")
    prCyan("R27 - " + str(sbt["offset_Z"]) + "\n")
    prCyan("R22 - " + str(sbt["scale_Z"]) + "\n")
    print("hit enter when ready for next step")
    input()
    print("place board back into test fixture and hit enter to begin verification test")
    input()
    return


# cli tool for building units with custom ranges
def custom_cli_tool():
    custom = get_custom_parameters()
    get_kanban_parts(custom)
    print("hit enter after you have collected your kit")
    input()
    pca_sbr_buildup(custom)
    # Ruby_calibration_routine(custom)
    return

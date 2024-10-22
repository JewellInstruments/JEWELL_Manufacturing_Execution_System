import time
import os
import datetime

import pyvisa


from instrumentation import data_aq_init
from instrumentation import data_aq_read


def set_source_voltage(
    instr: pyvisa.ResourceManager.open_resource, value: str, output_range: int
) -> None:
    """0=100mV, 1 = 10V, 2 = 100V

    +0135002
    +0000001"

    Args:
        instr (pyvisa.ResourceManager.open_resource): _description_
        value (str): _description_
        output_range (int): _description_
    """

    packet = f"{value}{output_range}"
    instr.write(packet)


def test_data_aq():
    rm = pyvisa.ResourceManager()

    source_name = "GPIB0::2::INSTR"
    data_aq_name = "ASRL15::INSTR"

    data_collection_filepath = "X:\\Engineering\\2-EPA MASTER FILE\\02 EL-(ELECTROLYTIC)\\13660 - Jewell ( SuperChamber2 )\\Qualification_Data\\Data_Collection"

    data_aq = rm.open_resource(data_aq_name)
    source = rm.open_resource(source_name)

    set_source_voltage(source, "+000000", 1)

    data_aq_init.config_data_aq_for_voltage(data_aq, "ANALOG", 1, differential=True)

    voltage = 15  # volts
    step = 0.250  # volts

    N = 2 * voltage / step

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")

    file = f"{timestamp}_data.csv"

    with open(os.path.join(data_collection_filepath, file), "w") as write_file:
        write_file.write("datetime, sourced (V), actual (V)\n")

    for i in range(0, int(N) + 1, 1):
        s = -voltage + i * step
        set_point = f"{s:07.3f}".replace(".", "")

        if s > 0:
            set_point = f"+{set_point}"

        print(set_point)
        set_source_voltage(source, set_point, 2)

        time.sleep(1)

        data = data_aq_read.read_data_from_data_aq(data_aq, "ANALOG", 1)

        value = data["PORT_1"][0]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(os.path.join(data_collection_filepath, file), "a") as write_file:
            string_to_write = f"{timestamp},{s},{value}\n"
            print(string_to_write)
            write_file.write(string_to_write)

    return


if __name__ == "__main__":
    test_data_aq()

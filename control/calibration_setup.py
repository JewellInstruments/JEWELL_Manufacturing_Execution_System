import os
import datetime


from system import settings

from system import stage_configuration
from network import get_specs
from network import api_calls
from network import filesystem


def calibration_setup() -> tuple[get_specs.mems_specs, dict, str, str]:
    """Get specs, create test index, and map serial numbers to ports they are connected to.

    Returns:
        tuple[mems_specs, dict, str, str]: mems specs object, unit_id dict, work_order from M2M, sales order from M2M.
    """

    json_data = filesystem.get_test_setup_json_data()

    part_no = json_data["part_no"]
    work_order = json_data["work_order"]
    sales_order = json_data["sales_order"]
    customer = json_data["customer"]
    name = json_data["name"]

    assets_list = []
    for asset in stage_configuration.assets:
        assets_list.append(asset["asset_number"])

    specs = get_specs.mems_specs(part_no)

    print("Getting new test index number")
    test_index = api_calls.get_test_index(
        part_no,
        work_order,
        sales_order,
        customer,
        name,
        assets_list,
        stage_configuration.__STAGE_NAME__,
    )

    print("Assigning test number to serial number.")
    unit_id_list = []
    serial_no_list = []
    rma_no_list = []
    for line in range(len(json_data["serial_no_list"])):
        serial_no = json_data["serial_no_list"][line]
        rma_no = json_data["serial_no_list"][line]
        rma_no_list.append(rma_no)
        serial_no_list.append(serial_no)

        unit_id_found = api_calls.get_unit_id(part_no, serial_no, rma_no)
        if unit_id_found is {}:
            print("Creating new unit id")
            unit_id = api_calls.create_unit_id_for_sensor(
                part_no, test_index, serial_no, rma_no
            )
        else:
            unit_id = "1"  # unit_id_found["unit_id"]

        unit_id_list.append(unit_id)

    index = datetime.datetime.now().strftime(settings.LOG_DATE_TIME)
    test_number = stage_configuration.TEST_NUMBER.format(index)

    os.environ["TEST_NUMBER"] = test_number

    year = datetime.datetime.now().strftime("%Y")

    print("creating new temporary test data directory.")
    filepath = os.path.join(
        settings.DATA_DIRECTORY_ROOT, f"MEMS_{year}", customer, sales_order, test_number
    )

    filesystem.init_directory(filepath)

    os.environ["SO_FILEPATH"] = filepath

    specs = get_specs.mems_specs(part_no)

    print("Building the unit id dict.")
    unit_id_dict = {}
    for item in range(len(serial_no_list)):
        unit_id_dict[f"PORT_{item+1}"] = {
            "part_no": part_no,
            "serial_no": serial_no_list[item],
            "rma_no": rma_no_list[item],
            "unit_id": unit_id_list[item],
        }

    return specs, unit_id_dict, work_order, sales_order

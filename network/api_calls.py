import socket
import os
import requests
from dataclasses import dataclass
import contextlib

from requests.compat import urljoin

from system import settings


# api_handler.login()


@dataclass
class Response:
    success: bool
    status_code: int
    data: any
    error: str | None


class APIHandler:
    def __init__(
        self,
        bearer_type: str = "JWT",
        base_url: str = settings.API_URL,
        login_url: str = "token/login/",
        refresh_url: str = "token/refresh/",
        login_email: str = os.environ["API_USER"],
        login_pass: str = os.environ["API_PASSWORD"],
    ) -> None:
        self.access_token = None
        self.refresh_token = None
        self.bearer_type = bearer_type
        self.base_url = base_url
        self.refresh_url = refresh_url
        self.login_url = login_url
        self.login_email = login_email
        self.login_pass = login_pass
        self.login()

    def login(self) -> bool:
        response = requests.post(
            f"{self.base_url}/{self.login_url}",
            json={"email": self.login_email, "password": self.login_pass},
            headers={"Content-Type": "Application/json"},
        )
        if response.status_code > 300:
            return False
        tokens = response.json()
        self.access_token = tokens["access"]
        self.refresh_token = tokens["refresh"]
        return True

    def update_access_token(self) -> bool:
        response = requests.post(
            f"{self.base_url}/{self.refresh_url}",
            json={"refresh": self.refresh_token},
            headers={"Content-Type": "Application/json"},
        )
        if response.status_code > 300:
            return False
        token = response.json()
        self.access_token = token["access"]
        return True

    def get(self, url: str) -> Response:
        response = requests.get(
            f"{self.base_url}/{url}",
            headers={"authorization": f"{self.bearer_type} {self.access_token}"},
        )
        if response.status_code == 401:
            with contextlib.suppress(Exception):
                temp = response.json()
                if "detail" in temp:
                    return Response(False, 401, f"Unauthorized: {temp['detail']}")
            if not self.update_access_token() and not self.login():
                return Response(
                    False,
                    401,
                    None,
                    "Unauthorized: Failed to refresh access token or login",
                )
            response = requests.get(
                f"{self.base_url}/{url}",
                headers={"authorization": f"{self.bearer_type} {self.access_token}"},
            )
        if response.status_code > 300:
            return Response(False, response.status_code, None, response.text)
        return Response(True, 200, response.json(), None)

    def post(self, url: str, data: dict) -> Response:
        response = requests.post(
            f"{self.base_url}/{url}",
            json=data,
            headers={
                "Content-Type": "application/json",
                "authorization": f"{self.bearer_type} {self.access_token}",
            },
        )
        if response.status_code == 401:
            with contextlib.suppress(Exception):
                temp = response.json()
                if "detail" in temp:
                    return Response(False, 401, None, f"Unauthorized: {temp['detail']}")
            if not self.update_access_token() and not self.login():
                return Response(
                    False,
                    401,
                    None,
                    "Unauthorized: Failed to refresh access token or login",
                )
            response = requests.post(
                f"{self.base_url}/{url}",
                json=data,
                headers={
                    "Content-Type": "application/json",
                    "authorization": f"{self.bearer_type} {self.access_token}",
                },
            )
        if response.status_code > 300:
            return Response(False, response.status_code, None, response.text)
        return Response(True, 200, response.json(), None)

    def update(self, url: str, data: dict) -> Response:
        response = requests.put(
            f"{self.base_url}/{url}",
            json=data,
            headers={
                "Content-Type": "Application/json",
                "authorization": f"{self.bearer_type} {self.access_token}",
            },
        )
        if response.status_code == 401:
            with contextlib.suppress(Exception):
                temp = response.json()
                if "detail" in temp:
                    return Response(False, 401, None, f"Unauthorized: {temp['detail']}")
            if not self.update_access_token() and not self.login():
                return Response(
                    False,
                    401,
                    None,
                    "Unauthorized: Failed to refresh access token or login",
                )
            response = requests.put(
                f"{self.base_url}/{url}",
                json=data,
                headers={
                    "Content-Type": "Application/json",
                    "authorization": f"{self.bearer_type} {self.access_token}",
                },
            )
        if response.status_code > 300:
            return Response(False, response.status_code, None, response.text)
        return Response(True, 200, response.json(), None)


def get_stage_configuration() -> dict:
    """get the stage configuration from the api

    Returns:
        str: unique stage configuration based on computer host name.
    """

    api_handler = APIHandler()

    stage_configuration_response = api_handler.get(
        f"stage_configuration/?computer_name={socket.gethostname()}"
    )

    if stage_configuration_response.status_code == 200:
        stage_configuration_data = stage_configuration_response.data[-1]
    else:
        stage_configuration_data = {}
    return stage_configuration_data


def get_stage_name() -> str:
    """get the stage name from the api

    Returns:
        str: unique stage name based on computer host name.
    """

    api_handler = APIHandler()

    stage_configuration_response = api_handler.get(
        f"stage_configuration/?computer_name={socket.gethostname()}"
    )
    # print(stage_configuration.data)

    if stage_configuration_response.status_code == 200:
        stage_configuration_data = stage_configuration_response.data[-1]
        stage_name = stage_configuration_data["stage_name"]
    else:
        stage_name = "UNKNOWN"
    return stage_name


def get_equipment_on_stage(stage_name: str) -> list[dict]:
    """get all equipment that is on the stage.

    Args:
        stage_name (str): unique stage name used for controlling where things are and which equipment is active.

    Returns:
        list[dict]: list of dicts for all asset info. includes cal info.
    """

    # assets_url = urljoin(settings.API_URL, "company_assets/")
    # assets = requests.get(assets_url, params={"location": stage_name})

    api_handler = APIHandler()

    assets = api_handler.get(f"company_assets/?location={stage_name}")

    # print(assets.status_code)

    return assets.data


def get_basic_data(part_no: str) -> dict:
    """get basic calibration/test data for a given part number from the api.

    Args:
        part_no (str): _description_

    Returns:
        dict: _description_
    """
    # specs_url = urljoin(settings.API_URL, "mems_linear_specs/")
    # specs = requests.get(specs_url, params={"part_no": part_no})

    api_handler = APIHandler()

    specs = api_handler.get(f"mems_linear_specs/?part_no={part_no}")
    # print(specs.data)
    data = specs.data[-1]
    return data


def get_tests_to_preform(part_no: str) -> dict:
    """get basic calibration/test data for a given part number from the api.

    Args:
        part_no (str): _description_

    Returns:
        dict: _description_
    """
    # specs_url = urljoin(settings.API_URL, "mems_linear_test/")
    # specs = requests.get(specs_url, params={"part_no": part_no})

    api_handler = APIHandler()

    specs = api_handler.get(f"mems_linear_test/?part_no={part_no}")

    data = specs.data[-1]

    return data


def get_assets_by_location(stage: str) -> list:
    """_summary_

    Args:
        stage (str): _description_

    Returns:
        list: _description_
    """
    # specs_url = urljoin(settings.API_URL, "company_assets/")

    # specs = requests.get(specs_url, params={"location": stage})

    # specs = specs.json()

    api_handler = APIHandler()

    specs_url = api_handler.get(f"company_assets/?location={stage}")
    # print(specs_url.data)

    return specs_url.data


def create_unit_id_for_sensor(
    part_no: str,
    test_index: str,
    serial_no: str,
    rma_no: str,
) -> str:
    """table needs to be made

    Args:
        part_no (str): _description_
        work_order (str): _description_
        serial_no (str): _description_
        sales_order (str): _description_
        name (str): who initiated the test
        assets (list): list of asset names used for calibration

    Returns:
        str: test index number
    """

    data = {
        "part_no": part_no,
        "test_index": test_index,
        "serial_no": serial_no,
        "rma_no": rma_no,
    }

    api_handler = APIHandler()

    response = api_handler.post("mems_linear_unit_id_log/", data=data)

    response = api_handler.get("mems_linear_unit_id_log/")

    print(response.response.data[-1])

    return response.data[-1]["unit_id"]  # response["unit_id"]


def get_test_index(
    part_no: str,
    work_order: str,
    sales_order: str,
    customer: str,
    name: str,
    assets: list,
    stage_name: str,
) -> int:
    """the table needs to be made...

    Args:
        part_no (str): _description_
        work_order (str): _description_
        sales_order (str): _description_
        customer (str): _description_
        name (int): pk for the User field where user matches email.
        assets (list): _description_

    Returns:
        int: _description_
    """

    api_handler = APIHandler()

    response = api_handler.get("mems_linear_test_executive/")
    initial_data = response.data[-1]

    data = {
        "test_index": initial_data["id"],
        "part_no": part_no,
        "work_order": work_order,
        "customer": customer,
        "sales_order": sales_order,
        "station": stage_name,
        "user": 2,
        "part_no_rev": "1",
        "test_result": "Fail",
        "assets": assets,
    }

    response = api_handler.post("mems_linear_test_executive/", data=data)

    # print(response.status_code)
    # api_handler = APIHandler()

    response = api_handler.get("mems_linear_test_executive/")
    data = response.data[-1]

    return data["id"]


def get_filepath_base(sensor_type: str) -> str:
    return ""


def get_work_order(work_order: str) -> tuple[str, str, str]:
    """_summary_

    Args:
        work_order (str): _description_

    Returns:
        tuple[str, str, str]: _description_
    """

    work_order_url = urljoin(settings.M2M_API_URL, "job_master/")

    work_order_data = requests.get(work_order_url, params={"fjobno": work_order})

    work_order_data = work_order_data.json()[-1]

    return (
        work_order_data["fjobno"],
        work_order_data["fsono"],
        work_order_data["fcompany"],
    )


def get_unit_id(part_no: str, serial_no: str, rma_no: str) -> int:
    """_summary_

    Args:
        part_no (str): _description_
        serial_no (str): _description_
        rma_no (str): _description_

    Returns:
        int: _description_
    """
    # unit_id_log_url = urljoin(settings.API_URL, "unit_id_log/")

    # unit_id_log_data = requests.get(
    #     unit_id_log_url,
    #     params={"part_no": part_no, "serial_no": serial_no, "rma_no": rma_no},
    # )

    api_handler = APIHandler()

    unit_id_log_data = api_handler.get(
        f"mems_linear_unit_id_log/?part_no={part_no}&serial_no={serial_no}&rma_no={rma_no}"
    )

    unit_id_log_data = unit_id_log_data.data

    print(unit_id_log_data)

    # unit_id_log_data = unit_id_log_data.json()

    return unit_id_log_data


def write_linearity_calibration_data(
    unit_id: int,
    axis_index: str,
    temp_index: int,
    cycle_index: int,
    reference: float,
    plate_temp: float,
    x_output: float,
    y_output: float,
    z_output: float,
    unit_temp: float,
) -> None:
    """_summary_

    Args:
        unit_id (int): _description_
        axis_index (str): _description_
        temp_index (int): _description_
        cycle_index (int): _description_
        reference (float): _description_
        plate_temp (float): _description_
        x_output (float): _description_
        y_output (float): _description_
        z_output (float): _description_
        unit_temp (float): _description_
    """

    api_handler = APIHandler()

    data = {
        "unit_id": unit_id,
        "axis_index": axis_index,
        "temp_index": temp_index,
        "cycle_index": cycle_index,
        "reference": reference,
        "plate_temp": plate_temp,
        "x_output": x_output,
        "y_output": y_output,
        "z_output": z_output,
        "unit_temp": unit_temp,
    }
    api_handler.post("mems_linear_thermal_data/", data=data)

    return


def write_static_calibration_data(
    unit_id: int,
    axis_index: str,
    output_up: float,
    output_down: float,
    pendulous_left: float,
    pendulous_right: float,
    bandwidth: float = 0.0,
    impedance: float = 0.0,
) -> None:
    """_summary_

    Args:
        unit_id (int): _description_
        axis_index (str): _description_
        output_up (float): _description_
        output_down (float): _description_
        pendulous_left (float): _description_
        pendulous_right (float): _description_
        bandwidth (float, optional): _description_. Defaults to 0.0.
        impedance (float, optional): _description_. Defaults to 0.0.
    """

    api_handler = APIHandler()

    data = {
        "unit_id": unit_id,
        "axis_index": axis_index,
        "output_up": output_up,
        "output_down": output_down,
        "pendulous_left": pendulous_left,
        "pendulous_right": pendulous_right,
        "bandwidth": bandwidth,
        "impedance": impedance,
    }

    api_handler.post("mems_linear_static_data/", data=data)
    return


def write_calibration_metrics(
    unit_id: int,
    axis_index: str,
    cycle_index: int,
    temp_index: int,
    scale_factor: float,
    moa: float,
    mpa: float,
    bias: float,
    sfts: float = 0.0,
    bts: float = 0.0,
) -> None:
    """write the calibration metrics to the api for easy reporting.d

    Args:
        unit_id (int): _description_
        axis_index (str): _description_
        cycle_index (int): _description_
        temp_index (int): _description_
        scale_factor (float): _description_
        moa (float): _description_
        mpa (float): _description_
        bias (float): _description_
        sfts (float, optional): _description_. Defaults to 0.0.
        bts (float, optional): _description_. Defaults to 0.0.
    """
    api_handler = APIHandler()

    data = {
        "unit_id": unit_id,
        "axis_index": axis_index,
        "cycle_index": cycle_index,
        "temp_index": temp_index,
        "scale_factor": scale_factor,
        "moa": moa,
        "mpa": mpa,
        "bias": bias,
        "sfts": sfts,
        "bts": bts,
    }

    api_handler.post("mems_linear_calibration_metrics/", data=data)
    return


def write_jdx_tumble_calibration_data(
    unit_id: int,
    reference: float,
    x_output: float,
    y_output: float,
    z_output: float,
) -> None:
    """_summary_

    Args:
        unit_id (int): _description_
        axis_index (str): _description_
        temp_index (int): _description_
        cycle_index (int): _description_
        reference (float): _description_
        plate_temp (float): _description_
        x_output (float): _description_
        y_output (float): _description_
        z_output (float): _description_
        unit_temp (float): _description_
    """

    static_table = "mems_linear_tumble_data/"
    static_url = urljoin(settings.API_URL, static_table)

    data = {
        "unit_id": unit_id,
        "axis_index": 0,
        "temp_index": 0,
        "cycle_index": 0,
        "reference": reference,
        "plate_temp": 22.5,
        "x_output": x_output,
        "y_output": y_output,
        "z_output": z_output,
        "unit_temp": 0,
    }
    requests.post(static_url, data=data)

    return

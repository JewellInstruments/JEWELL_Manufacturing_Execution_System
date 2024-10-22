from requests.compat import urljoin
import requests

specs_url = urljoin("http://qed8:8000/api", "mems_linear_specs")
specs = requests.get(specs_url, params={"part_no": "03550728-5371"})

print(specs)

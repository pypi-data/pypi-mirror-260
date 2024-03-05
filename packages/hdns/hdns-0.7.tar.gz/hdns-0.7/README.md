# hdns

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/your-package-name.svg)](https://badge.fury.io/py/your-package-name)

## Overview

This library is intended for people that do not have an static IP from their ISP but want to keep updated their A records at Hetzner DNS service

## Installation

```bash
pip install hdns requests json sys
```
Example usage to update all A records with the current IPv4 ip

```python
from hdns import arecords, ipv4

zone_id = "XXXXXXX"
auth_api_token = "XXXXXX"

ip = ipv4.get_ipv4()
records = arecords.get_all(zone_id, auth_api_token)

different_ip_zone_ids = []

for record in records:
    if record["value"] != ip:
        record["value"] = ip
        different_ip_zone_ids.append(record)
if different_ip_zone_ids:
    insert_records = arecords.insert_records(auth_api_token, different_ip_zone_ids)
    print(insert_records)
else:
    print("No need for update, IPv4 is still the same!")
```

ipv4: uses https://api.ipify.org API to get your IPv4 public IP
arecords.get_all(): accepts two values the zone_id and the auth_api_token to be able to function
ipv4.get_ipv4(): can be called without any value to return your public IP
arecords.insert_records(): accepts two values auth_api_token and an json array object with records that need to be modified

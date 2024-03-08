import requests
import json


def get_vm_price(vm_location: str, vm_size: str, current_vm_linux: bool):
    api_url = "https://prices.azure.com/api/retail/prices?api-version=2021-10-01-preview"
    query = f"armRegionName eq '{vm_location}' and armSkuName eq '{vm_size}' and priceType eq 'Consumption'"
    # print(query)
    response = requests.get(api_url, params={'$filter': query})
    json_data = json.loads(response.text)

    current_vm_price = -1
    # print(json_data['Items'])
    if current_vm_linux:
        for i in json_data['Items']:
            if ('Windows' not in i['productName'] and 'Priority' not in i['meterName']
                    and 'Spot' not in i['meterName']):
                current_vm_price = i['retailPrice']
                # print("i")
                # print(i)
    else:
        for i in json_data['Items']:
            # print("i")
            # print(i)
            if ('Windows' in i['productName'] and 'Priority' not in i['meterName']
                    and 'Spot' not in i['meterName']):
                current_vm_price = i['retailPrice']

    return current_vm_price


def get_disk_price(loc: str, product_name: str, sku_name: str):
    # if product_name.startswith('Premium '):
    meter_name = sku_name + ' Disk'
    # else:
    #     meter_name = sku_name + ' Disk'
    #     meter_name = sku_name.replace('LRS', 'Disks')
    # print(meter_name)
    url = "https://prices.azure.com/api/retail/prices?$filter=serviceName eq 'Storage' and priceType eq " \
          "'Consumption' and serviceFamily eq 'Storage' and productName eq '{}' and armRegionName eq '{}' and " \
          "skuName eq '{}' and meterName eq '{}'".format(product_name, loc, sku_name, meter_name)
    # print(url)
    headers = {}
    payload = {}
    res = requests.request("GET", url, headers=headers, data=payload)
    return json.loads(res.text)
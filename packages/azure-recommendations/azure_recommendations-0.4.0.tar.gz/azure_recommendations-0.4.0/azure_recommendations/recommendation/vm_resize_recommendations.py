import json
import logging
from datetime import datetime, timedelta
import pandas as pd
from azure_recommendations.recommendation.get_vm_price import get_vm_price

import requests
from azure.identity import ClientSecretCredential
from azure.mgmt.monitor import MonitorManagementClient
from azure.mgmt.compute import ComputeManagementClient
import math

from azure_recommendations.recommendation import utils

logging.basicConfig(level=logging.WARN)
logger = logging.getLogger()


# return the datapoints
def extract_datapoints_from_metrics(m_data: dict) -> list:
    d_points = []
    for item in m_data.value:
        # azure.mgmt.monitor.models.Metric
        # print("{} ({})".format(item.name.localized_value, item.unit))
        for timeserie in item.timeseries:
            for d in timeserie.data:
                # azure.mgmt.monitor.models.MetricData
                # print("{}: {} ".format(data.time_stamp,  data.average))
                i = {
                    "time_stamp": d.time_stamp,
                    "average": d.average
                }
                d_points.append(i)

    return d_points


# returns the average of CPU
def get_average(d_points):
    # Initialize variables for total and count
    total = 0
    count = 0

    # Iterate through data points and accumulate total and count for the last seven days
    for data in d_points:
        if data["average"]:
            total += data["average"]
            count += 1

    avg = 0

    # Calculate the average CPU utilization
    if count > 0:
        avg = total / count
        # print(f"Average over the last seven days: {avg:.2f}%")
    # else:
    # print("No data available for the last seven days.")

    return avg


class ResizeVm:
    def __init__(self, credentials: ClientSecretCredential, authorization_token: str):
        """
        :param credentials: ClientSecretCredential
        :param authorization_token:
        """
        super().__init__(credentials)
        self.credentials = credentials
        self.authorization_token = authorization_token

    # returns the metrics data
    def get_metrics(self, subs_id: str, from_time, to_time, metric_name: str, aggregation: str, vm_id: str):
        client = MonitorManagementClient(
            credential=self.credentials,
            subscription_id=subs_id
        )

        # Get CPU utilization
        metric_data = client.metrics.list(
            resource_uri=vm_id,
            timespan="{}/{}".format(from_time, to_time),
            metricnames=metric_name,
            # interval= datetime.timedelta(hours=1),
            interval=timedelta(days=1),
            aggregation=aggregation
        )

        return metric_data

    # returns the recommendations
    def get_resize_recommendation(self, vm_list: dict):
        """
        :param vm_list: list of Azure VMs
        :return:
        """
        logger.info(" ---Inside ResizeVM :: get_resize_recommendation()--- ")

        date_today = datetime.now().date()
        date_yesterday = date_today - timedelta(days=1)
        date_7_days_back = date_today - timedelta(days=6)
        date_tomorrow = date_today + timedelta(days=1)
        date_1_current_month = date_today.replace(day=1)

        resize_recommendations = {}

        for sid, vms in vm_list.items():
            compute_client = ComputeManagementClient(credential=self.credentials, subscription_id=sid)

            for vm in vms:
                cpu_metrics_data = self.get_metrics(
                    subs_id=sid,
                    from_time=date_7_days_back,
                    to_time=date_today,
                    metric_name='Percentage CPU',
                    aggregation='Average',
                    vm_id=vm.id
                )
                mem_metrics_data = self.get_metrics(
                    subs_id=sid,
                    from_time=date_7_days_back,
                    to_time=date_today,
                    metric_name='Available Memory Bytes',
                    aggregation='Average',
                    vm_id=vm.id
                )

                cpu_data_points = extract_datapoints_from_metrics(cpu_metrics_data)
                mem_data_points = extract_datapoints_from_metrics(mem_metrics_data)

                average_cpu = get_average(cpu_data_points)
                average_mem = get_average(mem_data_points) / 1000000

                current_vm_size = vm.hardware_profile.vm_size
                current_vm_location = vm.location
                current_vm_id = vm.id

                try:
                    if vm.os_profile.linux_configuration:
                        current_vm_linux = True
                    else:
                        current_vm_linux = False
                except Exception:
                    current_vm_linux = True

                vm_sizes = compute_client.virtual_machine_sizes.list(location=vm.location)

                for size in vm_sizes:
                    if size.name == current_vm_size:
                        current_size_cores = size.number_of_cores
                        current_size_memory = size.memory_in_mb

                avg_used_mem_percent = ((current_size_memory - average_mem) / current_size_memory) * 100

                if average_cpu < 50 and avg_used_mem_percent < 50:
                    current_vm_price_per_hour = get_vm_price(vm_location=current_vm_location, vm_size=current_vm_size,
                                                          current_vm_linux=current_vm_linux)

                    rg_name = ''
                    temp_list = vm.id.split('/')
                    i = 0
                    try:
                        while i < len(temp_list):
                            if temp_list[i] == 'resourceGroups':
                                rg_name = temp_list[i + 1]
                            i += 1
                    except Exception:
                        continue

                    available_sizes = compute_client.virtual_machines.list_available_sizes(
                        resource_group_name=rg_name,
                        vm_name=vm.name
                    )
                    available_vm_sizes = []

                    resize_recommendations.setdefault('VM Name', []).append(vm.name)
                    resize_recommendations.setdefault('VM ID', []).append(vm.id)
                    resize_recommendations.setdefault('Current Size', []).append(current_vm_size)
                    resize_recommendations.setdefault('Current VM price per month', []).append(
                        current_vm_price_per_hour * 730)
                    resize_recommendations.setdefault('Average CPU Utilization', []).append(average_cpu)
                    resize_recommendations.setdefault('Average Memory Usage (%)', []).append(avg_used_mem_percent)
                    resize_recommendations.setdefault('Location', []).append(vm.location)
                    resize_recommendations.setdefault('OS', []).append('Linux' if current_vm_linux else 'Windows')

                    max_ideal_cpu_cores = current_size_cores * 0.80
                    min_ideal_cpu_cores = current_size_cores * 0.40
                    max_ideal_mem = current_size_memory * 0.80
                    min_ideal_mem = current_size_memory * 0.40

                    resize_recommendations.setdefault('Recommended CPU Cores Range', []).append(
                        f'{math.ceil(min_ideal_cpu_cores)}-{math.floor(max_ideal_cpu_cores)}')
                    resize_recommendations.setdefault('Recommended Memory Range', []).append(
                        f'{min_ideal_mem}-{max_ideal_mem}'
                    )
                    new_sizes = []
                    potential_saving = 0.0

                    for size in available_sizes:
                        if (max_ideal_cpu_cores >= size.number_of_cores >= min_ideal_cpu_cores and
                                max_ideal_mem >= size.memory_in_mb >= min_ideal_mem):

                            # new_size_pricing
                            resized_vm_price_per_hour = get_vm_price(vm_location=current_vm_location, vm_size=size.name,
                                                                  current_vm_linux=current_vm_linux)

                            if current_vm_price_per_hour > resized_vm_price_per_hour:
                                potential_savings_per_hour = current_vm_price_per_hour - resized_vm_price_per_hour
                                new_sizes.append(size.name)
                                potential_saving = max(potential_saving, potential_savings_per_hour * 730)

                    if not new_sizes:
                        resize_recommendations.setdefault('Potential Savings Upto', []).append(None)
                        resize_recommendations.setdefault('New Sizes', []).append([])
                    else:
                        resize_recommendations.setdefault('Potential Savings Upto', []).append(potential_saving)
                        resize_recommendations.setdefault('New Sizes', []).append(new_sizes)

        df = pd.DataFrame(resize_recommendations)
        df = df[df['Potential Savings Upto'].notna()]
        return df

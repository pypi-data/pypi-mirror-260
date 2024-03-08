import logging
from azure_recommendations.recommendation.get_vm_price import get_vm_price

from azure.identity import ClientSecretCredential
from azure.mgmt.advisor import AdvisorManagementClient
from azure.mgmt.compute import ComputeManagementClient
import requests
import json

from azure_recommendations.recommendation import utils
from azure_recommendations.recommendation.utils import get_rg_name

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class advisor_recommendations:
    def __init__(self, credentials: ClientSecretCredential, authorization_token: str):
        """
        :param credentials: ClientSecretCredential
        """
        self.credentials = credentials
        self.authorization_token = authorization_token

    # Provides the recommendation from Azure advisor
    def azure_advisor_recommendations(self, subscription_list: list) -> list:
        """
        :param subscription_list: list of azure subscriptions
        :return: list of recommendations
        """
        logger.info(" ---Inside advisor_recommendations :: azure_advisor_recommendations()--- ")

        response = []
        recommendation_to_consider = [
            'Right-size or shutdown underutilized virtual machines',
        ]

        utils_obj = utils(self.credentials, self.authorization_token)

        vm_list = utils_obj.list_vms(subscriptions=subscription_list)

        for subscription in subscription_list:
            advisor_client = AdvisorManagementClient(credential=self.credentials, subscription_id=subscription)

            recommendation_list = advisor_client.recommendations.list()
            temp = {}
            # print(len(recommendation_list))
            for recommendation in recommendation_list:
                # print(f'{recommendation.short_description.solution}-{recommendation.resource_metadata.resource_id}')
                # print(recommendation.resource_metadata)
                # print(recommendation.short_description)
                # print(recommendation)

                if recommendation.short_description.solution == 'You have disks which have not been attached to a VM for more than 30 days. Please evaluate if you still need the disk.':
                    continue

                if recommendation.resource_metadata.resource_id not in temp:
                    temp[recommendation.resource_metadata.resource_id] = []
                if recommendation.short_description.solution not in temp[recommendation.resource_metadata.resource_id]:
                    # print(recommendation.short_description)
                    # print(recommendation.resource_metadata)
                    # print(recommendation)
                    current_price = 0
                    if recommendation.short_description.solution in recommendation_to_consider:
                        desc = (recommendation.short_description.solution + ": " +
                                recommendation.extended_properties['recommendationMessage'])

                        for vm in vm_list[subscription]:
                            if str(vm.id).lower() == str(recommendation.resource_metadata.resource_id).lower():
                                # print('*******************************3')

                                # price of vm from authentication less api
                                try:
                                    if vm.os_profile.linux_configuration:
                                        current_vm_linux = True
                                    else:
                                        current_vm_linux = False
                                except Exception:
                                    current_vm_linux = True
                                price = get_vm_price(vm_location=vm.location,
                                                     vm_size=vm.hardware_profile.vm_size, current_vm_linux=current_vm_linux)

                                current_price = price*730

                                # prices = utils_obj.get_price(subscription_id=subscription, resource=vm)
                                # if prices['unitOfMeasure'] == '1 Hour':
                                #     # print(prices)
                                #     current_price = 730 * prices['retail_price']
                    elif recommendation.extended_properties is not None:
                        if 'reservedResourceType' in recommendation.extended_properties:
                            try:
                                qty = recommendation.extended_properties['qty']
                            except Exception as e:
                                qty = 1
                            try:
                                term = recommendation.extended_properties['term']
                            except Exception as e:
                                term = None
                            try:
                                sku = recommendation.extended_properties['sku']
                            except Exception as e:
                                sku = ''

                            desc = f'{recommendation.short_description.solution}: {sku} - {str(qty)} - {str(term)}'
                        elif 'sku' in recommendation.extended_properties:
                            if 'Savings' in recommendation.extended_properties['sku']:
                                try:
                                    term = recommendation.extended_properties['term']
                                except Exception as e:
                                    term = None
                                desc = f'{recommendation.short_description.solution}: {str(term)}'
                            else:
                                desc = recommendation.short_description.solution
                        else:
                            desc = recommendation.short_description.solution

                    else:
                        desc = recommendation.short_description.solution


                    # savings = current_price - effective_price
                    # try:
                    #     savings_p = ((current_price - effective_price) / current_price) * 100
                    # except ZeroDivisionError:
                    #     savings_p = 0

                    try:
                        savings = float(recommendation.extended_properties['savingsAmount'])
                    except KeyError:
                        savings = 0
                    except Exception:
                        savings = 0

                    effective_price = (current_price - savings if current_price-savings > 0 else 0)
                    try:
                        savings_p = (savings/current_price)*100
                    except ZeroDivisionError:
                        savings_p = 0

                    temp1 = {
                        'recommendation': recommendation.short_description.solution,
                        'Category': recommendation.category,
                        'description': desc,
                        'resource group': get_rg_name(recommendation.resource_metadata.resource_id),
                        'resource name': str(recommendation.resource_metadata.resource_id).split('/')[-1],
                        'resource': recommendation.resource_metadata.resource_id.split('/')[-2],
                        'subscription_id': subscription,
                        'resource_id': recommendation.resource_metadata.resource_id,
                        'metadata': recommendation.extended_properties,
                        'current cost': current_price,
                        'effective cost': effective_price,
                        'savings': savings,
                        'savings %': savings_p,
                        'source': 'Azure'
                    }
                    temp.setdefault(recommendation.resource_metadata.resource_id, []).append(recommendation.short_description.solution)
                    response.append(temp1)

        return response


import functools
import time
from behave import *
from lib.car_object_repo import CarObjectRepo
import logging

@given('parse the input file and launch the website')
def parseAndLaunchPage(context):
    context.car_details = context.lib_common.read_input_file(context)
    context.lib_common.navigate_to_url("https://car-checking.com")


@then('waiting for the results...')
def sleepFor(context):
    time.sleep(int(2))


@then('validate for car_reg_num to the provided output')
def validateCarDetails(context):
    context.car_details = context.lib_common.read_input_file(context)
    car_results = {}
    test_pass = True
    for cars in context.car_details:
        context.lib_common.perform_action_on_element(CarObjectRepo.text_box, "click")
        context.lib_common.perform_action_on_element(CarObjectRepo.text_box, "type", cars)
        context.lib_common.perform_action_on_element(CarObjectRepo.check_now_button, "click")
        if context.lib_common.get_current_url() != "https://car-checking.com/report":
            car_results.update({cars: "Car Report not available on the website"})
            test_pass = False
        else:
            website_car_info = context.lib_common.read_website_car_info(
                context.lib_common.get_element(CarObjectRepo.bmw_maker).text, cars)
            logging.info("The reg_num - %s" %cars)
            logging.info("website_info - %s" %website_car_info)
            logging.info("From output_file - %s" %context.lib_common.read_output_file_and_match(context, cars))
            context.lib_common.navigate_to_url("https://car-checking.com")

            if (len(website_car_info) != len(context.lib_common.read_output_file_and_match(context, cars)) or
                website_car_info != context.lib_common.read_output_file_and_match(context, cars)):
                car_results.update({cars: "Car Report mismatch with the website"})
                test_pass = False
            else:
                car_results.update({cars: "Car Report match successful"})
    context.car_results = car_results
    context.test_pass = test_pass

@then('printing the output...')
def printOutput(context):
    logging.info("The status of the car reg_num -- %s" %context.car_results)
    assert context.test_pass

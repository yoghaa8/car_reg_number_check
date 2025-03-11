Feature: Car registration test

    Scenario: Validate the car details with car registration input
        Given parse the input file and launch the website
        #Input file is parsed and the car reg numbers are stored
        #The https://car-checking.com is launched to carry out the checks
        Then waiting for the results...
        And validate for car_reg_num to the provided output
        #For every car reg_number extract the website info
        #Validate the values with the values from the output file
        Then printing the output...
        #print the output list and test fail if any one reg_num details mismatch/missing

from selenium import webdriver                                                                                            #used for browser automation.
from selenium.webdriver.common.by import By                                                                               #used to specify the mechanism to locate elements within a web page.
from selenium.webdriver.support.ui import WebDriverWait                                                                   #used to wait for certain conditions to occur before proceeding with the execution of the code.
from selenium.common.exceptions import TimeoutException                                                                   #used to handle timeout exceptions that may occur during the execution of the code.
from selenium.webdriver.support import expected_conditions as EC                                                          #This module contains a set of predefined conditions that can be used with WebDriverWait.
import random                                                                                                             #used to generate random numbers.
import time                                                                                                               #used for adding delays in the code.

# Function to initialize the web driver
def initialize_driver():                                                                                                 #is responsible for initializing the WebDriver and opening a browser session.
        driver = webdriver.Chrome()                                                                                      #You can change this to any other supported browser also used to automate interactions with the Chrome browser.
        driver.get("http://sdetchallenge.fetch.com/")                                                                    #navigates the browser to the specified URL.
        time.sleep(5) 
        return driver                                                                                                    #returns the WebDriver instance to the caller.

# Function to get the weighing result
def get_weighing_result(driver):                                                                                         #performs specific tasks related to the web automation challenge.
    try:                                                                                                                 #try block, where we attempt to execute some code.
        return driver.find_element(By.ID, "weighing-result").text                                                        #This line tries to find the element with the ID "weighing-result" using the find_element method of the driver object. It uses the By.ID locator strategy to locate the element. If the element is found, its text content is returned.
    except Exception as e:                                                                                               #If an exception occurs during the execution of the try block, it's caught here. The caught exception object is assigned to the variable e.
        print("Error getting weighing result:", e)                                                                       #This line prints an error message along with the details of the caught exception.
        time.sleep(10) 
        return None

# Function to perform a weighing operation
def perform_weighing(driver, left_bowl, right_bowl):                                                                     #The two for loops are used to iterate over the elements of left_bowl and right_bowl lists, which contain the weights to be entered into the left and right bowls, respectively. 
    try:
        for i in range(len(left_bowl)):
            left_input = driver.find_element_by_id(f"left_{i}")                                                          #left_input or right_input is obtained by finding the input element with the dynamically generated ID using find_element_by_id.
            left_input.clear()                                                                                           #clear() method is called on the input element to clear any existing value.
            left_input.send_keys(left_bowl[i])                                                                           #send_keys() method is called to send the weight value from the corresponding list.

        for i in range(len(right_bowl)):
            right_input = driver.find_element_by_id(f"right_{i}")
            right_input.clear()
            right_input.send_keys(right_bowl[i])

        weigh_button = driver.find_element_by_id("weigh")                                                                #This line finds the "Weigh" button element using its ID.
        weigh_button.click()                                                                                             #This line clicks on the "Weigh" button.

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "weighing-result")))                      #This line waits for up to 10 seconds until an element with the ID "weighing-result" is present in the DOM. It uses WebDriverWait to wait for a specific condition to be met before proceeding further.
    except Exception as e:
        print("Error performing weighing:", e)

# Function to reset the bowls
def reset_bowls(driver):
    driver.find_element_by_id("reset").click()

# Function to click the fake bar button and get the alert message
def click_fake_gold_bar(driver, fake_gold_bar_index):
    fake_gold_bar_button = driver.find_element_by_xpath(f"//button[text()='{fake_gold_bar_index}']")
    fake_gold_bar_button.click()                                                                                              #This line clicks on the found button element.
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert = driver.switch_to.alert                                                                                            #This line switches the WebDriver focus to the alert dialog.
    alert_message = alert.text
    alert.accept()                                                                                                            #This line accepts the alert, dismissing it.
    time.sleep(10) 
    return alert_message

# Function to implement the algorithm to find the fake gold bar
def find_fake_gold_bar(driver):                                                                                               #It initializes variables such as fake_bar_index, weighing_count, and weighing_history.
    fake_gold_bar_index = None
    weighing_count = 0
    weighing_data = []                                                                   
                                                           
    while not fake_gold_bar_index:                                                                                            #It enters a while loop that continues until fake_bar_index is found (i.e., until a fake gold bar is identified).
        left_bowl = []                                                                                                        #Inside the loop, it generates random weights for the left and right bowls and performs a weighing operation using the perform_weighing function. It increments the weighing_count for each weighing operation.
        right_bowl = []

        # Generate random numbers for left and right bowls
        for _ in range(3):
            left_bowl.append(random.randint(0, 8))
            right_bowl.append(random.randint(0, 8))

        perform_weighing(driver, left_bowl, right_bowl)                                                                  #This line calls the perform_weighing function, passing the WebDriver instance (driver) along with the weights of the left and right bowls. This function performs a weighing operation on the web page using the provided weights.
        weighing_count += 1                                                                                              #increments the weighing_count variable by 1. This variable keeps track of the number of weighing operations performed.

        result = get_weighing_result(driver)                                                                             #This line calls the get_weighing_result function, passing the WebDriver instance (driver). This function retrieves the result of the weighing operation from the web page.
        if result is not None:                                                                                           #This line checks if the result obtained from the weighing operation is not None. If it's not None, it means the result was successfully obtained from the page.
            weighing_data.append((left_bowl, right_bowl, result))                                                        #This line appends a tuple containing the weights of the left and right bowls along with the result of the weighing operation to the weighing_history list. This list keeps track of the history of all weighing operations performed.

            if "left" in result:                                                                                         #This line checks if the string "left" is present in the result. If it is, it means that the fake gold bar is on the left side, and the minimum weight in the left bowl (min(left_bowl)) is considered as the index of the fake bar.
                fake_bar_index = min(left_bowl)
            elif "right" in result:                                                                                      #This line checks if the string "right" is present in the result. If it is, it means that the fake gold bar is on the right side, and the minimum weight in the right bowl (min(right_bowl)) is considered as the index of the fake bar.
                fake_bar_index = min(right_bowl)

            reset_bowls(driver)                                                                                          #This function resets the bowls on the web page, clearing any previous weights entered.
 
    alert_message = click_fake_gold_bar(driver, fake_gold_bar_index)                                                     #This line calls the click_fake_bar function, passing the WebDriver instance (driver) and the index of the fake gold bar (fake_bar_index). This function simulates clicking the button corresponding to the fake gold bar and retrieves the alert message that appears afterward.
    print("Alert message:", alert_message)                                                                               #This line prints the alert message obtained from the previous step. It shows what the message is indicating about the fake gold bar.
    print("Number of weighings:", weighing_count)                                                                        #This line prints the total number of weighing operations performed. It provides insight into how many times the algorithm had to weigh the gold bars to determine the fake one.
    print("Weighing data:")                                                                                              #This line prints a header indicating the start of the weighing history.
    for i, (left, right, result) in enumerate(weighing_data):                                                            #This line starts a loop that iterates over each entry in the weighing_history list. The enumerate function is used to get both the index (i) and the value ((left, right, result)) of each entry.
        print(f"Weighing {i+1}: Left: {left}, Right: {right}, Result: {result}")                                         #It displays the index of the weighing operation (i+1), along with the weights of the left and right bowls and the result of the weighing.

# Main function
def main():
    driver = initialize_driver()                                                                                         #This line initializes the WebDriver instance by calling the initialize_driver function. It opens a new browser window and navigates to the specified URL.
    find_fake_gold_bar(driver)                                                                                           #starts the process of finding the fake gold bar by performing weighing operations and analyzing the results.
    driver.quit()                                                                                                        #This line closes the browser window and terminates the WebDriver session once the process is completed 

if __name__ == "__main__":
    main()

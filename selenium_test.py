from selenium import webdriver

# Create a Chrome browser instance
driver = webdriver.Chrome()

url = input("Enter the URL: ")

# Open a webpage
driver.get(url)

# Print the title of the webpage
print("Webpage Title:", driver.title)
print("Current URL:", driver.current_url)

input("Press Enter to close the browser...")

# Close the browser
driver.quit()
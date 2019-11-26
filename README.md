# TL_Tactic_Check

Script to check viability of impression pixels for each tactic

Script will prompt for a csv containing the tactics and impression pixels you would like to check
# Expects:
at least 2 columns: "tactic_id" and "impression_pixel_json"
no more than one instance of a given tactic id
each value of the impression_pixel_json field should be enclosed in brackets

Will unescape impression pixel, remove whitespace characters, as well as the first and last bracket 

# Returns:
count of pixels that result in OK (2xx and 3xx) status codes
count of pixels that result in Failed (4xx and 5xx) status codes
count of pixels for which status codes could not be obtained (failed attempts)
a list of tactic ids and their corresponding pixels for failed status codes and failed attempts

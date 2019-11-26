import requests
import csv
import urllib   

count = 0

#set baseline variables
#dictionary mapping tactics to failed pixel calls
failed_pixels = {}
#count of ok response codes
count_ok = 0
#count of failed response codes
count_failed = 0
#count of failed attempts at pixel calls (no response code)
count_failed_attempt = 0
#create dictionary linking tactic id to impression pixel
imp_pixels = {}




#get tactics file for analysis 
tactic_file = raw_input("Enter tactic filename: ")



# function to clean impression pixel json field
def cleanup_pixel(raw_impression_pixel):
    #decode escaped characters, update NULLS, and remove quotations
    if raw_impression_pixel == 'NULL':
        raw_impression_pixel = ''
        return raw_impression_pixel
    clean_impression_pixel = raw_impression_pixel.translate(None, '\\"')

    #remove brackets from beginning and end of pixel
    pixel_length = len(clean_impression_pixel)
    last_index = pixel_length - 1

    if clean_impression_pixel[0] == '[' and clean_impression_pixel[last_index] == ']':
        clean_impression_pixel = clean_impression_pixel[1:last_index - 1]


    #break impression pixels for a given tactic into a list
    impression_pixel_list = clean_impression_pixel.split(',')
    
    return impression_pixel_list



# function to get status codes from http requests
def get_status_codes(pixel):
    try:
        r = requests.head(pixel)
        return str(r.status_code)[0]
    except: 
        return "failed attempt"



# function to print out a list of all pixels that failed from the failed pixel dictionary
def list_failed_pixels(failed_pixel_dict):
    for tactic in failed_pixel_dict:
        for pixel in failed_pixel_dict[tactic]:
            print "Tactic ID: " + tactic + "\nFailed Pixel: " + pixel





#read through CSV file to create a dictionary linking each tactic to its corresponding impression pixels
with open(tactic_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        # identify columns containing tactic id and impression pixel json and skip to first line of data
        if line_count == 0:
            for element in row:
                if element == 'tactic_id':
                    tactic_index = row.index(element)
                if element == 'impression_pixel_json':
                    pixel_index = row.index(element)    
            line_count += 1
            continue
        else:
            #assign each tactic and impression pixel to a variable
            tactic = row[tactic_index]
            raw_impression_pixel = row[pixel_index]
            
            #clean up impression pixel json
            impression_pixel = cleanup_pixel(raw_impression_pixel)
         
            #create a dictionary linking tactic ids to their corresponding impression pixels
            imp_pixels.setdefault(tactic, [])
            imp_pixels[tactic].append(impression_pixel)

            #increment line count to move to next line
            line_count += 1



            

#collect count of each type of status code for pixel tries and create a dictionary linking failed pixel calls with their corresponding tactic
for tactic in imp_pixels.keys():
    for pixel in imp_pixels[tactic]:
        #skip over null values
        if pixel == '':
            continue
        #get status codes for each pixel call
        else:
            #count number of OK status codes
            if get_status_codes(pixel) in ['2','3']:
                count_ok += 1

            #count number of Failed status codes and add to dictionary of failed calls with their corresponding tactic    
            elif get_status_codes(pixel) in ['4','5']:
                count_failed += 1
                
                failed_pixels.setdefault(tactic, [])
                failed_pixels[tactic].append(pixel)

            #count number of Failed pixel call attempts and add to dictionary of failed calls with their corresponding tactic    
            elif get_status_codes(pixel) == 'failed attempt':
                count_failed_attempt += 1

                failed_pixels.setdefault(tactic, [])
                failed_pixels[tactic].append(pixel)

        count += 1            





print "Number OK: ", count_ok
print "Number Failed: ", count_failed
print "Number Failed Attempts: ", count_failed_attempt
print list_failed_pixels(failed_pixels)









     
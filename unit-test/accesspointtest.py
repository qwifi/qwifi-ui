from twill.commands import *

import os
import twill
import subprocess

url = 'localhost:80/config/ap'

def ssid_test(ssid, session_mode):

    # Silence output from Twill commands
    f = open(os.devnull,"w")
    twill.set_output(f)

    # Generate File names for diff
    file_name = ssid + '.html'
    generated_html_path = 'output/ssid/' + file_name 
    expected_html_path = 'expected/ssidForm/' + file_name

    # Start with a fresh page every time
    go(url)

    print '\n**Testing SSID of ' + ssid + '**'

    code(200)
    # Fill the HTML forms with test values and submit
    fv("1","ssid",ssid)
    fv("1","session_mode",session_mode)

    submit('0')
    save_html(generated_html_path)

    # Diff with HTML page we know should 'come back'
    command = 'diff {0} {1}'.format(generated_html_path, expected_html_path)
    result = subprocess.call(command.split(), shell=False)

    if result is not 0:
        print 'Test failed'
    else:
        print 'Test Passed'



for i in range(1,5):
    ssid_test('Ssid_Device_Mode_' + `i`, 'device')

for i in range(1,5):
    ssid_test('Ssid_AP_Mode_' + `i`, 'ap')




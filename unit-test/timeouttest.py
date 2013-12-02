from twill.commands import *

import os
import twill
import subprocess

url = 'localhost:80'

def timeout_test(timeout, time_unit):

    # Silence output from Twill commands
    f = open(os.devnull,"w")
    twill.set_output(f)

    # Generate File names for diff
    # e.x. output/10seconds.html, expected/sessionsForm/10seconds.html
    file_name = `timeout` + time_unit + '.html'
    generated_html_path = 'output/timeout/' + file_name 
    expected_html_path = 'expected/sessionsForm/' + file_name

    # Start with a fresh page every time
    go(url)

    print '\n**Testing timeout of ' + `timeout` + ' ' + time_unit + '**'

    code(200)
    # Fill the HTML forms with test values and submit
    fv("1","timeout",`timeout`)
    fv("1","timeUnit",time_unit)
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
    timeout_test(i * 10,'seconds')
    timeout_test(i * 10,'minutes')
    timeout_test(i * 10,'hours')
    timeout_test(i * 10,'days')





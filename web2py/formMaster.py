def form():#called when the form.html is
    return dict()#just prints form.html
    
def form2():#calls form2.html
    timeout = request.vars.timeout
    timeUnit = request.vars.timeUnit
    timeout=int(timeout)
    if timeUnit == 'minutes':
        timeout=timeout*60
    elif timeUnit =='hours':
        timeout=timeout*3600
    elif timeUnit == 'days':
        timeout=timeout*86400 
    timeout=str(timeout)
    configFile = open('config.txt','w') #should open a file to write to
    configFile.write(timeout)  #should write the value from the form to the file
    configFile.write('\n')
    configFile.write(request.vars.ssidName)
    configFile.write('\n')
    return dict()#displays form2.html


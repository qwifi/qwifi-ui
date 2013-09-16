def form():#called when the form.html is
    return dict()#just prints form.html
    
def form2():#calls form2.html
    configFile = open('config.txt','w') #should open a file to write to
    configFile.write(request.vars.bob)  #should write the value from the form to the file
    return dict()#displays form2.html

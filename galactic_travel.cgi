#!/usr/bin/python

#	Project 1
#   Class:     CS 316
#   Date:      9/23/2018
#	Authors:   Trent Woods, Jared Rigdon
#   Purpose:   Get input from user via html get form that calculates the distance between 2 points

import cgi
import cgitb
import math
import sys

# opens the travel.html and applies it to the cgi program
header="Content-Type: text/html\n\n"

# common unit and dictionary for unit conversion
std_dist_unit = 'lightyear'
std_ang_unit='radian'
dist_units={
'lightyear':1.0,
'parsec':3.26,
'xlarn':20.786412,
'kilometer':1.0/(9.461*(10**12)),
'degree':0.0174533,
'radian':1.0,
'xarnian':0.01
}

#used to check for valid angles and distances
ang_list=['degree','radian','xarnian']
dist_list=['lightyear', 'parsec', 'xlarn', 'kilometer']

# retrieves the float and units and converts to a common units
def convert(val, unit, std_unit):
    for x in dist_units:
    	if x==unit:
    		return float(val*dist_units[unit]/dist_units[std_unit])   #convert to float
    #return an error
    print (header)
    print "<h1>Error<h1>"
    print "Invalid Units"
    return sys.exit()

# law of cosines states that c^2 = a^2 + b^2 - 2abcos(C)
def compute(dist_1, dist_2, angle):
    answer=0
    answer = dist_1**2 + dist_2**2 - 2*(dist_1)*(dist_2)*(math.cos(angle))
    answer = answer**0.5
    return answer 


def main():
    cgitb.enable()

    # get the field parameters
    form = cgi.FieldStorage()

    if "distx" not in form or "unitx" not in form or "disty" not in form or "unity" not in form or "anglea" not in form or "unita" not in form or "unitanswer" not in form:
        print (header)
        print "<h1>Error<h1>"
        print "Please fill in the empty blanks."
        return

    # assign the field parameters
    try: 
        distx = float(form.getvalue('distx'))
        unitx = (form.getvalue('unitx')).lower()
        disty = float(form.getvalue('disty'))
        unity = (form.getvalue('unity')).lower()
        anglea = float(form.getvalue('anglea'))
        unita = (form.getvalue('unita')).lower()
        unitanswer = (form.getvalue('unitanswer')).lower()
    except (TypeError,ValueError): 
        print(header)
        print "<h1>Error<h1>"
        print "Invalid Input!"
        return


    #check for correct units
    if unita not in ang_list or unitx not in dist_list or unity not in dist_list or unitanswer not in dist_list:
        print(header)
        print"<h1>Error<h1>"
        print"Invalid Distance/Angle Units"
        return

    # initialize float holders
    dist_1 = dist_2 = angle_con = 0.0

    # convert the two distances to common kilo
    # if the units match, dont need to worry about converstion
    if unitx != unity:
    	dist_1=convert(distx, unitx, std_dist_unit)
    	dist_2=convert(disty, unity, std_dist_unit)
    else:
    	dist_1=distx
    	dist_2=disty


    
    #convert angle to degree
    angle_con = convert(anglea, unita, std_ang_unit)
    #calculate the distance between the two points in lightyears
    distance_ly = compute(dist_1,dist_2,angle_con)

    #convert to desired units
    if unitx == unity:
        distance = convert(distance_ly, unitx, unitanswer)
    else:
        distance = convert(distance_ly, std_dist_unit, unitanswer)
    


   
    #display the html form with the filled in textboxes and the unitanswer textbox
    print (header)
    print '''<html>

            <head>
            <title>Intergalactic Travel Agency</title>
            </head>

            <body>
                <h1>Intergalactic Travel Agency</h1>
                <h2>By: Trent Woods and Jared Rigdon</h2>
                <h2>Compute distance between 2 places</h2>
                <h3>Input Format: </h3>
                The unit types this program can convert are included in the following
                <br>
                <h4>Distance: lightyear, parsec, kilometer, xlarn</h4>
                <h4>Angle: radian, degree, xarnian</h4>
                <form action="galactic_travel.cgi" method='get'>
                    Origin Distance to Earth:
                distx <input type = "text" name="distx" value="%s">
                unitx <input type = "text" name ="unitx" value="%s"><br><br>
                    Destination Distance to Earth:
                disty <input type = "text" name="disty" value="%s">
                unity <input type = "text" name ="unity" value="%s"><br><br>
                    Angle Seperation from Earth:
                anglea <input type = "text" name="anglea" value="%s">
                unita <input type = "text" name ="unita" value="%s"><br><br>
                    Distance computed:
                unitanswer %s <input type = "text" name="unitanswer" value="%s"> <br><br>
                    <input type="submit" value="Compute">
                </form>
            </body>

            </html>''' %(distx, unitx, disty, unity, anglea, unita, distance, unitanswer)

if __name__ == "__main__":
    main()

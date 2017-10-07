from random import *

actualGoodDataSet = set();
writeFile = open('../Downloads/SpoofedOutput.csv', 'w');

def createFakeDataForNonFire():
    file = open('../Downloads/output.csv','r');
    for line in file:
        lat, lon, _, _, date, _ = line.split(',');
        hh = lat + lon + date;
        actualGoodDataSet.add(hh);
    file.close()

    file = open('../Downloads/output.csv','r');
    for line in file:
        spoofFunc(line);
    file.close()

def spoofFunc(line):

    for i in xrange(0,5):
        lat, lon, air, ground, date, _ = line.split(',');
        lat = float(lat);

        if (i <=3):
            lat += randint(-10,10)/600.0;

        day, hr = date.split(' ');
        hr = int(hr)

        if (i >= 3):
            hr += randint(-6,6);
        if (hr < 0 ):
            hr = 0;
        if (hr > 23):
            hr = 23;

        date = day + " " + str(hr);

        hh = str(lat) + lon + date;

        if hh in actualGoodDataSet:
            continue;
        _, ground = ground.split(" ")
        writeFile.write(str(lat) + "," + lon + "," + air + "," + ground + "," + str(hr) + ",N\n");

createFakeDataForNonFire()
writeFile.close();

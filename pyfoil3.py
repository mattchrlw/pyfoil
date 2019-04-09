# PPPPPP          FFFFFFF        iii lll 333333  
# PP   PP yy   yy FF       oooo      lll    3333 
# PPPPPP  yy   yy FFFF    oo  oo iii lll   3333  
# PP       yyyyyy FF      oo  oo iii lll     333 
# PP           yy FF       oooo  iii lll 333333  .1
#         yyyyy                                                   
# Airfoiltools.com .dat downloader

import os
from os import path
import re
import subprocess as sub
import requests
import csv
from bs4 import BeautifulSoup

aft_url = 'http://airfoiltools.com/airfoil/seligdatfile?airfoil='
directory = os.getcwd() + '\dat\\'

if not os.path.exists(directory):
    os.makedirs(directory)

def get_foil_list():
    foil_list = []
    url = 'http://m-selig.ae.illinois.edu/ads/coord_seligFmt/'
    data = requests.get(url)
    soup = BeautifulSoup(data.text,'lxml')
    tabl = soup.find('table')
    rows = tabl.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        nam = cols[1].split('.')[0] if len(cols) == 5 else 'index'

        foil_list.append(nam) if nam != 'index' else None
    return foil_list[1::]

def get_foils():
    foil_list = get_foil_list()
    for items in foil_list:
        if os.path.isfile('\dat\\' + items):
            req = requests.get(aft_url + items + '-il').text
            file = open(directory + items + '.dat','w')
            file.write(req)
            print(items + ' foil saved')
            file.close()
        else:
            print(items + ' already exists')

def xfoil(re):
    foil_list = get_foil_list()
    comm = ""
    for items in foil_list:
        ps = sub.Popen(['xfoil.exe'],
            stdin=sub.PIPE,
            stdout=None,
            stderr=None,
            encoding='UTF-8')
        dat = items
        reynolds_number = re
        comm = "load dat\\" + dat + ".dat\n" + "oper\n" + "iter 70\n"
        comm += "vpar\n"
        comm += "n 13\n\n"
        comm += "alfa 0\n"
        comm += "visc " + reynolds_number + "\n"
        comm += "pacc\n"
        comm += reynolds_number + "\\" + dat + ".pol\n\n"
        comm += "aseq 0 20 .5\n"
        comm += "pacc\n"
        comm += "\n"
        try:
            outs, errs = ps.communicate(comm, timeout=10)
        except sub.TimeoutExpired:
            ps.kill()
            outs, errs = ps.communicate()
        ps.terminate()

def process_dat(reynolds_number):
    foil_list = get_foil_list()
    for item in foil_list:
        try:
            file = open('pol\\' + reynolds_number + '\\' + item + '.pol','r')
        except FileNotFoundError:
            continue
        alpha = []
        cl = []
        cd = []
        cdp = []
        cm = []
        top_xtr = []
        bot_xtr = []
        for index, line in enumerate(file):
            if "xtrf =" in line:
                xtrf_top = float(line[10:15])
                xtrf_bottom = float(line[29:34])
            elif "Mach =" in line:
                mach = float(line[10:15])
                re_str = line[29:38]
                re = float(re_str.replace(" ",""))
                ncrit = float(line[52:58])
            elif index >= 12 and line != "":
                alpha.append(float(str.strip(line[2:8])))
                cl.append(float(str.strip(line[9:17])))
                cd.append(float(str.strip(line[18:27])))
                cdp.append(float(str.strip(line[28:37])))
                cm.append(float(str.strip(line[38:46])))
                top_xtr.append(float(str.strip(line[47:55])))
                bot_xtr.append(float(str.strip(line[56:64])))
        # Thickness
        response = sub.run("xfoil load dat\\" + item + ".dat\n", stdout=sub.PIPE, shell=True)   
        output_string = response.stdout.decode()
        try:
            coordinate_pts = round(float(output_string.splitlines()[15][35:39]),7)
        except ValueError:
            continue
        thickness = round(float(output_string.splitlines()[17][19:29]),7)
        thickness_pt = round(float(output_string.splitlines()[17][38:46]),7)
        camber = round(float(output_string.splitlines()[18][19:29]),7)
        camber_pt = round(float(output_string.splitlines()[18][38:46]),7)
        leading_x = round(float(output_string.splitlines()[20][13:22]),7)
        leading_y = round(float(output_string.splitlines()[20][23:32]),7)
        trailing_x = round(float(output_string.splitlines()[21][13:22]),7)
        trailing_y = round(float(output_string.splitlines()[21][23:32]),7)
        chord = round(float(output_string.splitlines()[20][47:52]),7)
        with open('csv\\' + reynolds_number + '\\' + item + '.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile, dialect='excel')
            csvwriter.writerow(['Xtrf_top', xtrf_top])
            csvwriter.writerow(['Xtrf_bottom', xtrf_bottom])
            csvwriter.writerow(['Mach (0)', mach])
            csvwriter.writerow(['Re', re])
            csvwriter.writerow(['Ncrit', ncrit])
            csvwriter.writerow(['# of coord points', coordinate_pts])
            csvwriter.writerow(['Thickness', thickness])
            csvwriter.writerow(['Thickness point', thickness_pt])
            csvwriter.writerow(['Camber', camber, camber_pt])
            csvwriter.writerow(['Leading edge', leading_x, leading_y])
            csvwriter.writerow(['Trailing edge', trailing_x, trailing_y])
            csvwriter.writerow([])
            csvwriter.writerow(['Alpha','CL','CD','CDp','CM','Top_Xtr','Bot_Xtr'])
            for a, items in enumerate(alpha):
                csvwriter.writerow([alpha[a],
                                    cl[a],
                                    cd[a],
                                    cdp[a],
                                    cm[a],
                                    top_xtr[a],
                                    bot_xtr[a]])
        file.close()
        print(item, "complete")
    
# xfoil('1e5')          
# xfoil('2e5')
# xfoil('3e5')
# xfoil('4e5')
# xfoil('5e5')
# xfoil('6e5')
# xfoil('7e5')
# xfoil('8e5')
# xfoil('9e5')
# xfoil('1e6')
# process_dat('1e5')
# process_dat('2e5')
process_dat('3e5')
process_dat('4e5')
process_dat('5e5')
process_dat('6e5')
process_dat('7e5')
process_dat('8e5')
process_dat('9e5')
process_dat('1e6')

import pandas as pd
import subprocess
import shutil, os
from datetime import date

rawdata = pd.read_csv('companies.csv')

def filterUnappliedCompanies():
    return rawdata[rawdata['sentAt'].isnull()]

def compileClWithGivenParams(companyParam, positionParam, technology):
    laravelParam = 'false'
    # check if the technology array contains laravel as param
    if ('laravel' in technology):
        laravelParam = 'true'

    subprocess.call([
        "lualatex",
        "\def\\" + "company{" + f"{companyParam }" + " }",
        "\def\\" + "jobPosition{" + f"{positionParam }" + " }",
        "\def\\" + "laravelPosition{" + f"{ laravelParam }" + "}",
        "\\input clmain.tex"
    ])

def copyClToGivenLocation(file, newfilename):
    try:
        currentTime = date.today().strftime("%b-%d-%Y")
        dest = f"{os.getcwd()}{newfilename}-{currentTime}.pdf"
        return shutil.copy(file, dest)

    except Exception as error:
        print(error)

#def generateFileName(company, prefix = '/cls/'):
#    return f"{company}.pdf"

def generateCLs():
    try:
        for index, row in filterUnappliedCompanies().iterrows():
            print(row)
            compileClWithGivenParams(row.company, row.position, row.technology)
            newDestination = copyClToGivenLocation('clmain.pdf', '/cls/'+row.company)
            print(newDestination)

    except Exception as error:
        print(error)


generateCLs()

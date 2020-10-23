#!/usr/bin/env python
# -*- coding: utf-8 -*-
# You should replace the open_xlsb path for the path of your current user or the path where is located the file

import pandas as pd
from pyxlsb import open_workbook as open_xlsb
 
df = []
NOT_READ  = "T-resumen" #Se excluye la pestaña resumen que no contiene datos
 
with open_xlsb('/home/<<username>>/python/inventario revisión.xlsb') as wb:
    list_sheet = wb.sheets
    for sheet_name in list_sheet :
        if sheet_name != NOT_READ :
            with wb.get_sheet(sheet_name) as sheet:
                for row in sheet.rows():
                    df.append([item.v for item in row])
 
df = pd.DataFrame(df[2:], columns=df[0])    #Se eliminan las columnas superiores que no contienen datos
new_header = df.iloc[0]
df = df[1:]
df.columns = new_header

print df
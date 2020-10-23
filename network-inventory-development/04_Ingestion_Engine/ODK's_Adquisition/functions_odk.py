# -*- coding: utf-8 -*-

# Version: 1.0.0

# Global functions
global dirt
dirt=['iligible','no','no visi','no tiene activo fijo','sin numero activo fijo','n/n','no contiene activo fijo','no visible', 'sin etiqueta', 'ni visible', 'n/v','nv','ilegible','n/a', 's/a', 'na','no legible', 'no cuenta con activo fijo',
	'n/v deteriorado','sin activo fijo','no vicible','no hay','no tiene','no visble','nos visible','no visible',
	'no viaible', '.fhy', 'bxfj', 'cambiar la foto', 'hdjdjjdjfjfj', 'hdjrnnfjfjf', 'hffhthjih', 'hhyhigch',
	'hswkwjj', 'no aplica', 'no pude borrar elemnto', 'ns no visible', 'sin serie', 'sitio ibs no aplica', 'tutj',
	'uflp serie no visible', 'xxxxxxx', 'hsid# djdncg', 'sin informacion disponible', 'no tiene numero de serie',
	'hdkoe kg udkke' 'no se ve', 'ninguna', 'no tiene etiqueta y no se alcnaza a ver.', 'fue un error',
	'no legible', 'sin etiqueta', 'no disponible', 'no tiene', 'sin datos', 'num de serie no legible', 'etiqueta no legible', 'no cuenta con numero de serie',
	'no aplica por error se selecciona una tarjeta mas', 'enviado ya en reporte anterior', 'hlk', 'ninguno', 'la antena no tiene etiqueta por lo tanto tampoco numero de serie', 'no leguible',
	'sin targeta (por equivocacion se agrego este eslot 18 )', 'no cuenta con numeros de serie', 'enviados en reporte anterior .', 'sin etiqueta de numero de serie',
	'sin numero', 'sin informacion disponible', 'sin acceso a la antena', 'no tiene serie', 'sin acceso', 'no se pudo sacar ya que esta clausurado el sitio',
	'no se hizo por que no tenemos tarjeta se las llevo el ing de huawei gabriel lopez', 'sin informacion disponible', 'no aplica ta este segmento',
	'sin numero de serie visible', 'enviada en reporte  anterior', 'no hay antena', 'no se pudo sacar ya que esta clausurado y nos sacaron de sitio',
	'sin serie falta etiqueta', 'sin numero de serie no cuenta con la etiqueta', 'no tiene etiqueta', 'no existe', 'no serie visible', 'no hay bbu esta en resguardo por el ing gabriel lopez',
	'no legible', 'na', 'na hay  tarjeta', 'sin acceso al numero de serie', 'no visibles', 'uelp serie no visible', 'sin informacion disponible', 'sin tarjeta', 'fue un error de dedo no ay mas slot',
	'codigo no visible', 'num de serie no visible', 'sin informacion', 'no se aprecia el codigo', 'sin numero de serie', 'no trae la etiketa de numero de serie',
	'no aplica.', 'no se pudo sacar el numero  de serie ya q nos sacaron del sitio ya q esta clausurado', 'no tiene serie visible', 'no tiene serial ala vista',
	'no se tiene acceso a la antena', 'etiqueta no visible', 'no se puede tomar la foto porque tenemos la fan', "n/a  no se instalan antenas", 'no aplica sitio ibs',
	'sin numero', 'kcuvicuv', 'error no hay mas', 'no se puede apreciar el codigo', 'no aplica es ibs.', 'no  cuenta con etiquetas de n/s', 'esta ultima no vale','NaN','nan',
	'no hay tarjeta', 'esta no vale', 'falta', 'sin nÃºmero','s/n','0','n','k', 'sin número', 'sin número de serie', 'sin num de serie', 'sin etiqueta de activo fijo', 'sin activo', 'no contiene activó fijó','no tiene activó','N/V','visible']
# Validate Key Dad Function
def validate_key_dad(string):
	res = False
	if string == '':
		res =True
	return res

# Hash Function
def hash_key(column):
	import hashlib
	column_str =u''.join(column+"").encode('ascii', 'ignore').strip()
	result = hashlib.md5(column_str.encode()).hexdigest()
	return result

# Clean update_on field
def update_updated(word):
	if word == "\N":
		return ""
	else:
		return word

# Uuid random function
def generate_acn():
	import uuid
	return str(uuid.uuid1())

# Special functions for odk's

# Function to generate an array of the series and active, since these are repeated in a single record for the odk99
def process_activo(string):
	import re
	string2 = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	activo=str(string2.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u"))
	if activo.find("|"):
		ex = activo.split("|")
	else:
		ex=["",""]
	return ex

# Function to generate an array of the make and model, since these are repeated in a single record for the odk99
def process_marca_modelo(s,string):
	import re
	string2 = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	brand=str(string2.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u"))
	brand2 = brand.split('|')
	if len(brand2) == 0:
		exp = None
	# When the brand is the same for each serial number
	elif len(brand2) == 1:
		exp=[]
		for i in range(s):
			exp.append(brand2[0])
	# Everything matches
	elif len(brand2) == s:
		exp = brand2
	# When each series has two brands or model
	elif len(brand2) == 2*s:
		exp = []
		for i in range(s):
			exp.append(brand2[0]+"|"+brand2[1])
			del brand2[0:2]
	else:
		exp = [""] * s
	return exp

# Function that discriminates which brand or model to put, based on AT&T rules
def modify_brand(marca):
	try:
		marca = marca.encode("utf-8")
		marca=marca.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
		if marca.find('|')!=-1:
			marca = marca.strip()
			x=marca.split('|')
			if len(x)==2:
				if "oth" in x:
					x.remove('oth')
					newMarca = x[0]
					if newMarca in dirt:
						marcaCorregida = "oth"
						return marcaCorregida
					else:
						return newMarca
				else:
					if (x[0], x[1])in dirt:
						newMarca = "oth"
						return newMarca
					elif x[0] in dirt:
						x.remove(x[0])
						newMarca = x[0]
						return newMarca
					elif x[1] in dirt:
						x.remove(x[1])
						newMarca = x[0]
						return newMarca
			else:
				return x[0]
		else:
			return marca
	except Exception,e:
		return marca

# Function used in the post_specialTransformation function
def get_groups(listagrupos):
	newlist=[]
	for i in listagrupos:
		if i.find("Sub")!=-1:
			newlist.append(i)
		else:
			pass
	newlist2=[]
	for i in newlist:
		s=i.split(':')
		g=s[0]+':'+s[1]+':'+s[2]
		newlist2.append(g)
	newlist3=list(dict.fromkeys(newlist2))
	return newlist3

# Function used in the post_specialTransformation function
def extraer(string):
	l=string.split(':')
	if len(l)==4:
		word=l[0]+':'+l[1]+':'+l[2]
	else:
		word=string
	return word

# Function used in the post_specialTransformationdef function
def discriminateColumns(col1,col2):
	if col1!='':
		word=col1
	elif col2!='':
		word=col2
	else:
		word=col1
	return word

# Function used in the special_transformation function
def transform_ODK38(grupo):
	groups=grupo.split(':')
	if (len(groups)==5):
		col=groups[0]+':'+groups[1]+':'+groups[2]+':'+groups[3]
	elif(len(groups)==4):
		col=groups[0]+':'+groups[1]+':'+groups[2]
	else:
		col=grupo
	return col

# Search element functions

def search_odk12(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'mw':'AntenaMW'},{'vertical':'Vista'},{'horizontal':'Vista'},{'floor':'Vista'},{'config':'Configuraciones'},{'test':'Pruebas'},{'cambioantena':'Antena'},{'cambioodu':'ODU'},{'chidu':'IDU'},{'wires':'Cable'},{'certrfc':'Equipo de medicion'},{'fotografico':'Vista'},{'testing':'Pruebas'},{'polari':'Vista'},{'side':'Sitio'},{'aligment':'Vista'},{'tarjetas':'Tarjeta'},{'install':'Vista'},{'before':'Vista'},{'after':'Vista'},{'commisioning':'Vista'},{'soporte':'soporte'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if groups[2].lower().find('inventory')!=-1:
			for k in subgrupos:
				if k.lower().find('element')!=-1:
					indexx=subgrupos.index(k)
					word=values[indexx]
					break
				else:
					word='Not Found'
		else:
			for i in elementos1:
				if groups[2].lower().find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'

	elif (len(groups)==4):
		if groups[3].lower().find('inventory')!=-1:
			for k in subgrupos:
				if k.lower().find('element')!=-1:
					indexx=subgrupos.index(k)
					word=values[indexx]
					break
				else:
					word='Not Found'
		else:
			for i in elementos1:
				if groups[3].lower().find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'

	elif(len(groups)==5):
		if groups[4].lower().find('inventory')!=-1:
			for k in subgrupos:
				if k.lower().find('element')!=-1:
					indexx=subgrupos.index(k)
					word=values[indexx]
					break
				else:
					word='Not Found'
		else:
			for i in elementos1:
				if groups[4].lower().find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'
	return word

def search_odk28(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'Azimuts':'Vista Azimut'},{'Sectors':'Sector'},{'Paths':'Paths'},{'Shettler':'Shettler'},{'Cabinet':'Gabinete'},{'Bbus':'Bbus'}]
	elementos2=[{'Antenas':'Antena'},{'Rrus':'Rrus'},{'Cards':'Tarjeta'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		for i in elementos1:
			if grupo.find(i.keys()[0])!=-1:
				word=i.values()[0]
				break
			else:
				word='Not Found'
	elif (len(groups)==4):
		for i in elementos2:
			if grupo.find(i.keys()[0])!=-1:
				word=i.values()[0]
				break
			else:
				word='Not Found'
	else:
		word='root'
	return word

def search_odk29(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'before':'Vista'},{'after':'Vista'},{'sheet':'Reporte'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if groups[2].lower().find('items')!=-1:
			for i in subgrupos:
				if i.lower().find('itemtype')!=-1:
					indexx=subgrupos.index(i)
					word=values[indexx]
					break
				else:
					word='Not found'
		else:
			for i in elementos1:
				if groups[2].lower().find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'
	else:
		word='root'
	return word

def search_odk32(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'Azimuts':'Azimut'},{'Sectors':'Sector'},{'Paths':'Vista'},{'Shettler':'Shettler'},{'Cabinet':'Gabinete'},{'Brushidden':'Brushidden'},{'Bbus':'Bbus'},{'Inventory':'Equipo'},{'Antenna':'Antena'},{'Cards':'Cards'},{'Rrus':'Rrus'},{'Antenas':'Antena'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		ln = len(groups[2]) - 3
		#word = groups[2][5:ln]
		if (groups[2][5:ln] == 'Com'):
			word = 'Comisionamiento'
		else:
			word = groups[2][5:ln]
	elif (len(groups)==4):
		ln = len(groups[3]) - 3
		word = groups[3][5:ln]
	else:
		word='root'
	return word

def search_odk34(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'Secscr':'Pantalla Sector'},{'Comm':'Comisionamiento'},{'Shelter':'Shelter'},{'Azimuts':'Vista azimut'},{'Sectors':'Sector'},{'Antenas':'Antena'},{'Rrus':'Rru'},{'Paths':'Trayectoria'},{'Cabinet':'Gabinete'},{'Nodeb':'Nodo b'},{'Baterry':'Bateria'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if groups[2].find('Inv')!=-1:
			if (len(subgrupos))>0:
				for i in subgrupos:
					if(i.find('keyInvEquip')!=-1):
						indexx=subgrupos.index(i)
						word=values[indexx]
						break
					else:
						word='Not Found'
			else:
				word='Not Found'
		else:
			for i in elementos1:
				if groups[2].find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'
	elif (len(groups)==4):
		for i in elementos1:
			if groups[3].find(i.keys()[0])!=-1:
				word=i.values()[0]
				break
			else:
				word='Not Found'
	else:
		word='root'
	return word

def search_odk37(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'Pow':'Vista'},{'Ind':'Vista'},{'Inv':'Vista Inventario'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if groups[2].find('Ixn')!=-1:
			if (len(subgrupos))>0:
				for i in subgrupos:
					if(i.find('strIxnoEqu')!=-1):
						indexx=subgrupos.index(i)
						word=values[indexx]
						break
					else:
						word='Inventario'
			else:
				word='Not Found'
		else:
			for i in elementos1:
				if groups[2].find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'
	else:
		word='root'
	return word

def search_odk38(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'AntennaRRU':'RRu'},{'CabinetRack':'Gabinete'},{'BatteryBank':'Banco de baterias'},{'Shelter':'Shelter'},{'Pwr':'Planta de fuerza'},{'Transfers':'Transferencias'},{'Towers':'Torre'},{'Supports':'Soportes'},{'Materials':'Materiales'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root1'
	elif (len(groups)==3):
		if grupo.find('Vw')!=-1:
			word='Vista'
		else:
			if (len(subgrupos))>0:
				for i in subgrupos:
					if(i.find('keyType')!=-1):
						indexx=subgrupos.index(i)
						word=values[indexx]
						break
					else:
						word='Not Found'
			else:
				word='Not Found'
		if word=='Not Found':
			for i in elementos1:
				if groups[2].find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'

	elif (len(groups)==4):
		for i in elementos1:
			if groups[3].find(i.keys()[0])!=-1:
				word=i.values()[0]
				break
			else:
				word='Not Found'
	else:
		word='root'
	return word

def search_odk46(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'Pow':'Vista'},{'Ind':'Vista'},{'Inv':'Vista Inventario'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if groups[2].find('WdEqpt')!=-1:
			if (len(subgrupos))>0:
				for i in subgrupos:
					if(i.find('keyEqpt')!=-1):
						for j in subgrupos:
							if(j.find('strEqptOth')!=-1):
								indexx=subgrupos.index(j)
								word=values[indexx]
								break
							else:
								indexx=subgrupos.index(i)
								word=values[indexx]
						break
					else:
						word='Not Found'
			else:
				word='Not Found'
	else:
		word='root'
	return word

def search_odk55(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'paths':'Trayectoria'},{'shelter':'Shelter'},{'rack':'Rack'},{'cabinet':'Gabinete'},{'bbu':'Bbu'},{'cards':'Tarjeta'},{'task':'root'},{'comm':'Comisionamiento'},{'slot':'Bbu'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if groups[2].lower().find('equipmentremove')!=-1:
			for i in subgrupos:
				if i.lower().find('keyequipmentremove')!=-1:
					indexx=subgrupos.index(i)
					if values:
						word=values[indexx]
					else:
						word='root'
					break
				else:
					word='Not found'
		else:
			for i in elementos1:
				if groups[2].lower().find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'
	elif (len(groups)==4):
		if groups[3].lower().find('equipmentremove')!=-1:
			for i in subgrupos:
				if i.lower().find('keyequipmentremove')!=-1:
					indexx=subgrupos.index(i)
					if values:
						word=values[indexx]
					else:
						word='root'
					break
				else:
					word='Not found'
		else:
			for i in elementos1:
				if groups[3].lower().find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'
	else:
		word='root'
	return word

def search_odk56(cve_type,grupo,subgrupos,dictionary, keys, values):
	listaodk56=['DUW', 'TTCU', 'SPD', 'BAT', 'DUS', 'TPSU', 'TPDU', 'TBF', 'DUG']
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		ln = len(groups[2]) - 3
		#word = groups[2][5:ln]
		if (groups[2][5:8] == 'Mod'):
			word = 'Vista'
		elif (groups[2][5:8] == 'Gab'):
			word = 'Gabinete'
		elif (groups[2][5:8] == 'Cab'):
			word = 'Cable'
		elif (groups[2][5:8] == 'Ban'):
			word = 'Banco de Baterias'
		elif (groups[2][5:8] == 'Inv'):
			for i in subgrupos:
				if (i.find('keyElementoInv')!=-1):
					indexx=subgrupos.index(i)
					word=listaodk56[indexx]
					break
				else:
					word='Not Found'
		else:
			word = 'Not Found'
	elif (len(groups)==4):
		word = groups[3][5:8]
	else:
		word='root'
	return word

def search_odk58(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'Sectores':'Sector'},{'SectoresPhoto':'Fotos'},{'ElemInvPhoto':'Fotos Inventario'},{'HeightChange':'Cambio de altura'},{'AntennaChange':'Antena'},{'AzimuthTilt':'Azimut'},{'AdSector':'Sector'},{'Antenna':'Antenna'},{'Rrus':'Rru'},{'Rcus':'Rcu'},{'Boards':'Tarjeta'},{'Cards':'Tarjeta'},{'SectorData':'Sector'},{'Secscr':'Pantalla Sector'},{'Comm':'Comisionamiento'},{'Shelter':'Shelter'},{'Azimuts':'Vista azimut'},{'Sectors':'Sector'},{'Antenas':'Antena'},{'Rrus':'Rru'},{'Paths':'Trayectoria'},{'Cabinet':'Gabinete'},{'Nodeb':'Nodo b'},{'Baterry':'Bateria'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if groups[2].find('Inventario')!=-1:
			if (len(subgrupos))>0:
				for i in subgrupos:
					if(i.find('keyElemInv')!=-1):
						indexx=subgrupos.index(i)
						word=values[indexx]
						break
					else:
						word='Inventario'
			else:
				word='Not Found'
		else:
			for i in elementos1:
				if groups[2].find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'

	elif (len(groups)==4):
		if groups[3].find('ElemInv')!=-1:
			if (len(subgrupos))>0:
				for i in subgrupos:
					if(i.find('keyElemInv')!=-1):
						indexx=subgrupos.index(i)
						word=values[indexx]
						break
					else:
						word='Not Found'
			else:
				word='Not Found'
		else:
			for i in elementos1:
				if groups[3].find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'
	else:
		word='root'
	return word

def search_odk60(cve_type,grupo,subgrupos, dictionary, keys, values):
	groups=grupo.split(':')
	if len(groups)>3:
		if (groups[2].find("SondaChange")!=-1):
			word='Vista'
		else:
			for i in subgrupos:
				if len(subgrupos.split(':'))>2:
					key=i.split(':')[0]
					value=i.split(':')[1]
					if(key!='' and value!=''):
						if key=='strElementoInventarioOth':
							word=value
							break
						else:
							word='root'
					else:
						word='not found'
				else:
					word='not found'
	else:
		word='not found'
	return word

def search_odk61(cve_type,grupo,subgrupos,dictionary, keys, values):
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	else:
		if (grupo.find('VerificationInterconnection')!=-1):
			word='Router' + grupo[-1]
		else:
			word='Not Found'
	return word

def search_odk63(cve_type,grupo,subgrupos,dictionary, keys, values):
		word='Not Found'
		groups=grupo.split(':')
		if (len(groups)<=2):
			word='root'
		elif (len(groups)==3):
			if groups[2].lower().find('inventario')!=-1:
				for k in subgrupos:
					if k.lower().find('keyfabricante')!=-1:
						indexx=subgrupos.index(k)
						word=values[indexx]
						break
					else:
						word='Not Found'
		else:
			word='root'
		return word

def search_odk64(cve_type,grupo,subgroupos,dictionary, keys,values):
	array = dictionary
	if len(array)>0:
		if (grupo.find("View")!=-1):
			word='Vista'
		elif (grupo.find("Equi")!=-1):
			word = 'Equipo'+ grupo.split('Equi')[1]
		else:
			for i in array:
				key=i.split(':')[0]
				value=i.split(':')[1]
				if(key!='' and value!=''):
					if key=='Elemento(s) de Trabajo':
						word=value
						break
					else:
						word='root'
				else:
					word='not found'
	else:
		word='not found'
	return word

def search_odk65(cve_type,grupo,subgrupos,dictionary, keys, values):
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	else:
		if (grupo.find('Inventario')!=-1):
			if len(subgrupos)>0:
				for i in subgrupos:
					if (i.find('keyEquipment')!=-1):
						indexx=subgrupos.index(i)
						word=values[indexx]
						break
					else:
						word='Not found'
			else:
				word='Not found'
		elif (grupo.find('PruebasMedicion')!=-1):
			word='Medicion' + grupo[-1]
		elif (grupo.find('Fotografico')):
			word='Reporte Fotografico' + grupo[-1]
		else:
			if len(subgrupos)>0:
				for i in subgrupos:
					if (i.find('pic')!=-1):
						word='Vista'
						break
					else:
						word='Not Found'
			else:
				word='Not Found'
	return word

def search_odk66(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'reporte':'Vista'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		for i in elementos1:
			if groups[2].lower().find(i.keys()[0])!=-1:
				word=i.values()[0]
				break
			else:
				word='Not Found'

	elif (len(groups)==4):
		if groups[3].lower().find('inventario')!=-1:
			for i in subgrupos:
				if i.lower().find('keyequipment')!=-1:
					indexx=subgrupos.index(i)
					if values:
						word=values[indexx]
					else:
						word='root'
					break
				else:
					word='Not found'
	else:
		word='root'
	return word

def search_odk69(cve_type,grupo,subgrupos, dictionary, keys, values):
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		   word = 'Vista'
	elif (len(groups)==5):
		if (len(subgrupos))>0:
			for i in subgrupos:
				if(i.find('keyEquipmentTunel')!=-1):
					indexx=subgrupos.index(i)
					word=values[indexx]
					break
				else:
					word = 'Not Found'
		else:
			word = 'test'
	elif (len(groups)==4):
		for i in subgrupos:
			if(i.find('keyEquipment')!=-1):
				indexx=subgrupos.index(i)
				word=values[indexx]
				break
			elif(i.find('keyEquipmentDAS')!=-1):
				indexx=subgrupos.index(i)
				word=values[indexx]
				break
			elif(i.find('keyEquipmentTunel')!=-1):
				indexx=subgrupos.index(i)
				word=values[indexx]
				break
			else:
				word = 'Pantalla'
	else:
		word = 'Not Found'
	return word

def search_odk72(cve_type,grupo,subgrupos,dictionary, keys, values):
	lista=['fuerza', 'rack', 'card', 'oth', 'slprnc11']
	array = dictionary
	for i in lista:
		if i in array:
			word=i
			break
		else:
			word='root'
	return word

def search_odk75(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'instcab':'Vista'},{'instrack':'Rack'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if groups[2].lower().find('inventary')!=-1:
			for i in subgrupos:
				if i.lower().find('keyelement')!=-1:
					indexx=subgrupos.index(i)
					word=values[indexx]
					break
				else:
					word='Equipo'
		else:
			for i in elementos1:
				if groups[2].lower().find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'
	else:
		word='root'
	return word

def search_odk76(cve_type,grupo,subgrupos,dictionary, keys, values):
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		word='Pedido'
	elif(len(groups)==4):
		word='Pallet'
	else:
		word='Not Found'
	return word

def search_odk83(cve_type,grupo,subgrupos,dictionary, keys, values):
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	else:
		if (grupo.find('Inventory')!=-1):
			if len(subgrupos)>0:
				for i in subgrupos:
					if (i.find('strElement')!=-1):
						indexx=subgrupos.index(i)
						word=values[indexx]
						break
					else:
						word='Not found'
			else:
				word='Not found'
		else:
			if len(subgrupos)>0:
				for i in subgrupos:
					if (i.find('pic')!=-1):
						word='Vista'
						break
					else:
						word='Not Found'
			else:
				word='Not Found'
	return word

def search_odk84(cve_type,grupo,subgrupos,dictionary,keys,values):
	array=dictionary
	if len(array)>0:
		if (grupo.find("View")!=-1):
			word='Vista'
		elif (grupo.find("Equi")!=-1):
			word = grupo.split('Equi')[1]
		else:
			for i in array:
				key=i.split(':')[0]
				value=i.split(':')[1]
				if(key!='' and value!=''):
					if key=='Elemento':
						word=value
						break
					else:
						word='root'
				else:
					word='not found'
	else:
		word='not found'
	return word

def search_odk85(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'retirogenerador':'Vista'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if groups[2].lower().find('inventory')!=-1:
			for i in subgrupos:
				if i.lower().find('strelement')!=-1:
					indexx=subgrupos.index(i)
					word=values[indexx]
					break
				else:
					word='Equipo'
		else:
			for i in elementos1:
				if groups[2].lower().find(i.keys()[0])!=-1:
					word=i.values()[0]
					break
				else:
					word='Not Found'
	else:
		word='root'
	return word

def search_odk95(cve_type,grupo,subgrupos,dictionary, keys, values):
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		for i in subgrupos:
			if(i.find('keyElemInv')!=-1):
				indexx=subgrupos.index(i)
				word=values[indexx]
				break
			elif(i.find('strElemRetOth')!=-1):
				indexx=subgrupos.index(i)
				word=values[indexx]
				break
			else:
				word = 'Vista'
	else:
		word = 'Not Found'
	return word

def search_odk97(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'BdaInstall':'BDA'},{'Photo':'Foto'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		for i in elementos1:
			if groups[2].find(i.keys()[0])!=-1:
				word=i.values()[0] + groups[2][-2]
				break
			else:
				word='Not Found'
	elif (len(groups)==4):
		if groups[3].find('Inventory')!=-1:
			if len(subgrupos)>0:
				for i in subgrupos:
					if (i.find('keyElemInvI')!=-1):
						indexx=subgrupos.index(i)
						word=values[indexx]
						break
					else:
						word='Not found'
			else:
				word='Not found'
		else:
			for i in elementos1:
				if groups[3].find(i.keys()[0])!=-1:
					word=i.values()[0] + groups[3][-2]
					break
				else:
					word='Not Found'
	else:
		word='root'
	return word

def search_odk98(cve_type,grupo,subgrupos,dictionary, keys, values):
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if (groups[2][5:12] == 'Screens'):
			word = 'Pantalla'
		else:
			for i in subgrupos:
				if(i.find('strElemInvOth')!=-1):
					indexx=subgrupos.index(i)
					word=values[indexx]
					break
				elif(i.find('keyElemInv')!=-1):
					indexx=subgrupos.index(i)
					word=values[indexx]
					break
				else:
					word = 'Vista'
	else:
		word = 'Not Found'
	return word

def search_odk99(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'cabinet':'Gabinete'},{'struct':'Estructura'},{'shelter':'shelter'},{'cbbattery':'Banco de baterias'},{'cbattery':'Bateria'},{'srack':'Rack'},{'sbattery':'Bateria'},{'sbbank':'Banco de baterias'}]
	elementos2=[{'twelement':'keytelement'},{'irack':'ertype'},{'lrack':'ertype'},{'powerdc':'dcetype'},{'hvac':'hvactype'},{'other':'othtype'},{'ecabinet':'ecabtype'},{'gen':'gentype'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		for i in elementos1:
			if groups[2].lower().find(i.keys()[0])!=-1:
				word=i.values()[0]
				break
			else:
				word='Not Found'
		if word=='Not Found':
			for j in elementos2:
				if groups[2].lower().find(j.keys()[0])!=-1:
					for k in subgrupos:
						if k.lower().find(j.values()[0])!=-1:
							indexx=subgrupos.index(k)
							word=values[indexx]
							bandera=True
							break
						else:
							bandera=False
							word='Not found'
					if bandera:
						break

	elif(len(groups)==4):
		for i in elementos1:
			if groups[3].lower().find(i.keys()[0])!=-1:
				word=i.values()[0]
				break
			else:
				word='Not Found'
		if word=='Not Found':
			for j in elementos2:
				if groups[3].lower().find(j.keys()[0])!=-1:
					for k in subgrupos:
						if k.lower().find(j.values()[0])!=-1:
							indexx=subgrupos.index(k)
							word=values[indexx]
							bandera=True
							break
						else:
							bandera=False
							word='Not found'
					if bandera:
						break
	elif(len(groups)==5):
		for i in elementos1:
			if groups[4].lower().find(i.keys()[0])!=-1:
				word=i.values()[0]
				break
			else:
				word='Not Found'
		if word=='Not Found':
			for j in elementos2:
				if groups[4].lower().find(j.keys()[0])!=-1:
					for k in subgrupos:
						if k.lower().find(j.values()[0])!=-1:
							indexx=subgrupos.index(k)
							word=values[indexx]
							bandera=True
							break
						else:
							bandera=False
							word='Not found'
					if bandera:
						break
	return word

def search_odk108(cve_type,grupo,subgrupos,dictionary, keys, values):
	array = dictionary
	if len(array)>0:
		if (grupo.find("View")!=-1):
			word='Vista'
		elif (grupo.find("Equi")!=-1):
			word = grupo.split('Equi')[1]
		else:
			for i in array:
				key=i.split(':')[0]
				value=i.split(':')[1]
				if(key!='' and value!=''):
					if key=='Elemento':
						word=value
						break
					else:
						word='root'
				else:
					word='not found'
	else:
		word='not found'
	return word

def search_odk111(cve_type,grupo,subgrupos,dictionary, keys, values):
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if (groups[2][5:10] == 'Floor'):
			word = 'Zona de instalacion'
		else:
			for i in subgrupos:
				if(i.find('keyEqType')!=-1):
					indexx=subgrupos.index(i)
					word=values[indexx]
					break
				elif(i.find('strModelOth')!=-1):
					indexx=subgrupos.index(i)
					word=values[indexx]
					break
				else:
					word = 'Vista'
	elif (len(groups)==4):
		for i in subgrupos:
			if(i.find('keyCabinetType')!=-1):
				indexx=subgrupos.index(i)
				word =  'Gabinete ' + values[indexx]
				break
			else:
				word =  'Gabinete'
	else:
		word = 'Not Found'
	return word

def search_odk114(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'Azimuts':'Vista Azimut'},{'Sectors':'Sector'},{'Paths':'Vista trayectoria'},{'Shettler':'Shettler'},{'Cabinet':'Gabinete'},{'Bbus':'Bbus'},{'Brushidden':'Brushidden'},{'Bbus':'Bbus'},{'Inventory':'Equipo'},{'Antenna':'Antena'},{'Cards':'Cards'},{'Rrus':'Rrus'},{'Antenas':'Antena'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		for i in elementos1:
			if groups[2].find(i.keys()[0])!=-1:
				word=i.values()[0] + groups[2][-1]
				break
			else:
				word='Not Found'
	elif (len(groups)==4):
		for i in elementos1:
			if groups[3].find(i.keys()[0])!=-1:
				word=i.values()[0] + groups[3][-1]
				break
			else:
				word='Not Found'
	else:
		word='root'
	return word

def search_odk115(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'cellinstall':'root'},{'cellinstallp':'Vista'},{'photoreport':'Vista'},{'smallswap':'Vista'}, {'celluninstall':'root'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		if groups[2].lower().find('inventario')!=-1:
			for i in subgrupos:
				if i.lower().find('eleminv')!=-1:
					indexx=subgrupos.index(i)
					word=values[indexx]
		elif groups[2].lower().find('inventory')!=-1:
			for i in subgrupos:
				if i.lower().find('eleminv')!=-1:
					indexx=subgrupos.index(i)
					word=values[indexx]
		else:
			for i in elementos1:
				if groups[2].lower().find(i.keys()[0])!=-1:
					word=i.values()[0]

	elif (len(groups)==4):
		for i in elementos1:
			if groups[3].lower().find(i.keys()[0])!=-1:
				word=i.values()[0]
	return word

def search_odk136(cve_type,grupo,subgrupos,dictionary, keys, values):
	elementos1=[{'install':'Caja'},{'instodf':'ODF'},{'mediciones':'Vista'}]
	word='Not Found'
	groups=grupo.split(':')
	if (len(groups)<=2):
		word='root'
	elif (len(groups)==3):
		for i in elementos1:
			if groups[2].lower().find(i.keys()[0])!=-1:
				word=i.values()[0]
				break
			else:
				word='Not Found'
	else:
		word='root'
	return word

# Functions for clean schema

def clean_str_odk12(string):
	import re
	listaModelos=['keymodelodua','keymodelodub', 'keymodelodunamea','keymodelodunameb','modelo_de_idu','modelo_de_lantena_de_mw','modelo_de_odu','modeloacopladoraoth','modeloacopladorboth','modeloantennaboth','modeloantennanamea','modeloantennanameaoth','modeloantennanameb','modeloantennanameboth','modelooduaoth','modelooduboth','modeloodunamea','modeloodunameaoth','modeloodunameboth','modeloradioaoth','modeloradioboth','modeloradionamea','modeloradionameaoth','modeloradionameb','modeloradionameboth','modeloradioa','modeloradiob','modeloacopladora','modeloacopladorb','modeloantennaa','modeloantennab','modeloodua','modeloodub','modeloodunameb','modelooth']
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","")
	str_clean_3 = str_clean_2.replace(" ","_").replace("-","_")
	str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("activo_fijo_scanner","activo").replace("activo_scanner","activo").replace('*','')
	str_clean_5 = str_clean_4.replace("_a","").replace("_b","").replace("_del_equipo_de_medicion","")
	str_clean_6 = str_clean_5.replace("strmodel","modelo").replace("strmodelidua", "modelo").replace("strmodelidub","modelo").replace("strmodeltowerb","modelo")
	str_clean_7 = str_clean_6.replace("modeloidua","modelo").replace("modeloidub","modelo").replace("modelotowerb","modelo")
	str_clean_8 = str_clean_7.replace("decazimuthreala","decazimuthreal").replace("decazimuthrealb","decazimuthreal")
	str_clean_9 = str_clean_8.replace("decantennahtfloora","decantennahtfloor").replace("decantennahtfloorb","decantennahtfloor")
	str_clean_10 = str_clean_9.replace("decantennahttwra","decantennahttwr").replace("decantennahttwrb","decantennahttwr")
	str_clean_11 = str_clean_10.replace("decdiameterantennaa","decdiameterantenna").replace("decdiameterantennab","decdiameterantenna")
	str_clean_12 = str_clean_11.replace("_inventariar","").replace("decazimuthreal","azimuth_real")
	str_clean_13 = str_clean_12.replace("imgalarmsaa","imgalarms").replace("imgalarmsab","imgalarms").replace("imgalarmsba","imgalarms").replace("imgalarmsbb","imgalarms")
	str_clean_14 = str_clean_13.replace("imglinkconfigaa","imglinkconfig").replace("imglinkconfigab","imglinkconfig").replace("imglinkconfigba","imglinkconfig").replace("imglinkconfigbb","imglinkconfig")
	str_clean_15 = str_clean_14.replace("keyelement","elemento").replace("strelement","elemento").replace("strelementidua","elemento").replace("strelementidub","elemento").replace("strelementtowerb","elemento")
	str_clean_16 = str_clean_15.replace("elementoidua","elemento").replace("elementoidub","elemento").replace("elementotowerb","elemento").replace("/","")
	str_clean_17 = str_clean_16.replace("codigo_de_sitio_corregido","codigo_de_sitio").replace("keymanufactureracopladora","keymanufactureracoplador").replace("keymanufactureracopladorb","keymanufactureracoplador")
	str_clean_18 = str_clean_17.replace("keyserialmodeacopladora","keyserialmode").replace("keyserialmodeacopladorb","keyserialmode")
	for k in listaModelos:
		str_clean_18 = str_clean_18.replace(k,"modelo")
	str_clean_19 = str_clean_18.replace("codigo_de_sitio_lado","codigo_de_sitio").replace("codigo_de_sitio_lado_oth","codigo_de_sitio").replace("codigo_de_sitio_oth","codigo_de_sitio")
	return str_clean_19

def clean_str_odk28(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace(".","")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 =str_clean_2.replace("numero_de_","").replace("_antena_rf","").replace("_tarjeta","")
	str_clean_4 = str_clean_3.replace("?","").replace(".","").replace("'","").replace("no_","")
	series=['numero_de_serie','serial','serie_antena_rf','serie_bbu_m','serie_bbu']
	for i in series:
		str_clean_4 = str_clean_4.replace(i,"serie")
	return str_clean_4

def clean_str_odk29(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace(".","").replace("/","_")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	return str_clean_2

def clean_str_odk32(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace("?","").replace("'","")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_escanner","_esc").replace("_manual","_man").replace("_escaner","")
	str_clean_4 = str_clean_3.replace("'","").replace("_bbu_m","").replace("_esc","").replace("_man","").replace("_fijo","").replace("_manual","").replace("_fijo_manual","")
	str_clean_5 = str_clean_4.replace("_antenna_rf","").replace("_de_gabinete","").replace("_tarjeta","").replace("marca_y_modelo_antena_rf","marca")
	return str_clean_5

def clean_str_odk34(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace(".","").replace("'","")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("numero_activo","activo").replace("numero_serie","serie").replace("vista_montaje_modulos_de_Nodo_B","vista_modulos_nodoB")
	str_clean_4 = str_clean_3.replace("numero_de_","").replace("_manual","").replace("_escanner","").replace("marca_y_modelo_antena_rf","marca")
	str_clean_5 = str_clean_4.replace("_antenna_rf","")
	return str_clean_5

def clean_str_odk37(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_")
	str_clean_3 = str_clean_2.replace("numero_","").replace("_manual","").replace("_fijo","").replace("modelo_equipo","modelo").replace("_otro","").replace("modelo_destino","modelo").replace("modelo_origen","modelo")
	return str_clean_3

def clean_str_odk38(string):
	import re
	if string == None:
		string_key = ""
	else:
		string_key = string
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("marca_oth","marca").replace("numero_de_activo","activo").replace("numero_de_activoescaner","activo").replace("numero_de_activomanua","activo")
	str_clean_4 = str_clean_3.replace("numero_de_serie_escaner","serie").replace("numero_de_serie_manual","serie").replace("activoescaner","activo").replace("activomanual","activo")
	return str_clean_4

def clean_str_odk46(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_manual","").replace("_escaner","")
	return str_clean_3

def clean_str_odk55(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace(".","")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_escaner","").replace("_manual","")
	str_clean_4 = str_clean_3.replace("_de_bbu","").replace("_de_gabinete","").replace("_de_tarjeta","")
	return str_clean_4

def clean_str_odk56(string):
	import re
	if string == None:
		string_key = ""
	else:
		string_key = string
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string_key.encode("utf-8"))
	str_clean_1 = str_clean.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","").replace("activo_fijo","activo")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_manual","").replace("_escaner","")
	return str_clean_3

def clean_str_odk58(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace(".","").replace("/","_").replace("nº_","")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("numero_de_sector","sectores").replace("numero_de_","").replace("activo_fijo","activo").replace("_escaner","").replace("_manual","")
	str_clean_4 = str_clean_3.replace("marca_de_fo_hibrido","marca").replace("marca_de_fo","marca").replace("_de_antena_retirada","")
	return str_clean_4

def clean_str_odk60(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_manual","").replace("_escaner","")
	str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("numero_activo","activo")
	return str_clean_4

def clean_str_odk61(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace(".","").replace("/","_")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	return str_clean_2

def clean_str_odk63(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","").replace("/","_")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_manual","").replace("_escaner","")
	str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("numero_activo","activo")
	return str_clean_4

def clean_str_odk64(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_fijo","").replace("_escaner","").replace("_manual","")
	return str_clean_3

def clean_str_odk65(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","").replace("nº_","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_manual","").replace("_escaner","")
	str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("numero_activo","activo")
	return str_clean_4

def clean_str_odk66(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace(".","").replace("/","_")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_escaner","").replace("_manual","")
	str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("numero_activo","activo")
	return str_clean_4

def clean_str_odk69(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_fijo","").replace("_escaner","").replace("_manual","").replace("_numero","")
	return str_clean_3

def clean_str_odk72(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_manual","").replace("_escaner","").replace("_scanner","").replace("numero_","").replace("_fijo","").replace("modelo_del_equipo","modelo").replace("marca_del_equipo","marca")
	str_clean_4 = str_clean_3.replace("marca_del_equipo_otra","marca").replace("modelo_del_equipo_otro","modelo").replace("_otra","").replace("_otro","")
	return str_clean_4

def clean_str_odk75(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_fijo","").replace("_escaner","").replace("_manual","").replace("_numero","").replace("_scanner","")
	return str_clean_3

def clean_str_odk76(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_escaner","").replace("_fijo","").replace("_manual","").replace("_scanner","")
	str_clean_4 = str_clean_3.replace(",na","").replace(".","")
	return str_clean_4

def clean_str_odk83(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_fijo","").replace("_escaner","").replace("_manual","").replace("_numero","").replace("_o_placa_de_identificacion","")
	return str_clean_3

def clean_str_odk84(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_fijo","").replace("_escaner","").replace("_manual","").replace("_numero","").replace("_scanner","").replace("_o_placa_de_identificacion","")
	return str_clean_3

def clean_str_odk85(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_fijo","").replace("_escaner","").replace("_manual","").replace("_numero","").replace("__o_placa_de_identificacion","")
	return str_clean_3

def clean_str_odk95(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_fijo","").replace("_escaner","").replace("_manual","").replace("_numero","")
	str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("numero_activo","activo")
	return str_clean_4

def clean_str_odk97(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace(".","")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_escaner","").replace("_fijo","")
	str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("_manual","").replace("_escaner","")
	return str_clean_4

def clean_str_odk98(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_manual","").replace("_escaner","")
	str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("numero_activo","activo")
	return str_clean_4

def clean_str_odk99(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	#str_clean_2 = str_clean_1.replace("numero de ","").replace(" manual","").replace(" escaner","")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_")
	str_clean_3 = str_clean_2.replace("numero_de_activo","activo").replace("numero_de_serie","serie").replace(" escaner","")
	str_clean_4 = str_clean_3.replace("activo_fijo_manual","activo").replace("activo_manual","activo").replace("serie_manual","serie").replace("marca_manual","marca").replace("activo_fijo","activo")
	str_clean_5 = str_clean_4.replace("tipo_de_elemento","tipo_elemento").replace("tipo_de_equipo","tipo_equipo").replace("?","").replace("¿","")
	str_clean_6 = str_clean_5.replace("status","estatus")
	return str_clean_6

def clean_str_odk108(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_manual","").replace("_escaner","")
	str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("numero_activo","activo").replace("__otro_","")
	return str_clean_4

def clean_str_odk111(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace("á","a").replace("é","e").replace("í","i").replace("ó","o").replace("ú","u")
	str_clean_2 = str_clean_1.replace(" ","_").replace("-","_").replace(".","").replace("/","_")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_manual","").replace("_escaner","")
	str_clean_4 = str_clean_3.replace("activo_fijo","activo").replace("numero_activo","activo").replace("_scanner","")
	str_clean_5 = str_clean_4.replace("_del_equipo","").replace("_otro","").replace("_otra","")
	return str_clean_5

def clean_str_odk114(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace(".","").replace("'","")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_escaner","").replace("_fijo","").replace("_manual","").replace("_scanner","")
	str_clean_4 = str_clean_3.replace("marca_y_modelo_antena_rf","marca").replace("_antenna_rf","").replace("_/_","_")
	str_clean_5 = str_clean_4.replace("_de_gabinete_rack","").replace("modelo_tarjeta","modelo").replace("_escanner","")
	return str_clean_5

def clean_str_odk115(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace(".","")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("_manual","").replace("activo_fijo","activo")
	str_clean_4 = str_clean_3.replace("_otro","").replace("_manual","").replace("activi_fijo","activo").replace("_escaner","")
	return str_clean_4

def clean_str_odk136(string):
	import re
	str_clean = rs = re.sub("[,;:{}()\\n\\t=]","",string.encode("utf-8"))
	str_clean_1 = str_clean.replace(" ","_").replace("-","_").replace("/","")
	str_clean_2 = str_clean_1.replace("ó","o").replace("á","a").replace("é","e").replace("í","i").replace("ú","u")
	str_clean_3 = str_clean_2.replace("numero_de_","").replace("activo_fijo","activo").replace("activo_odf","activo")
	str_clean_4 = str_clean_3.replace("_escaner","").replace("_manual","").replace("_scanner","").replace("_de_odf","").replace("_de_caja","")
	return str_clean_4

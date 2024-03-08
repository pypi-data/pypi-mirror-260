#!/usr/bin/env python3

#import re, os, json, sys
#from traceback import format_exc as traceback_format_exc
#from datetime import datetime, timedelta

import re, sys, os
from .ecuapass_info_cartaporte_NTA import CartaporteNTA
from .ecuapass_extractor import Extractor
from .ecuapass_data import EcuData
from .ecuapass_utils import Utils

#----------------------------------------------------------
USAGE = "\
Extract information from document fields analized in AZURE\n\
USAGE: ecuapass_info_cartaportes.py <Json fields document>\n"
#----------------------------------------------------------
# Main
#----------------------------------------------------------
def main ():
	args = sys.argv
	fieldsJsonFile = args [1]
	runningDir = os.getcwd ()
	CartaporteInfo = CartaporteByza (fieldsJsonFile, runningDir)
	mainFields = CartaporteInfo.getMainFields ()
	Utils.saveFields (mainFields, fieldsJsonFile, "Results")

#----------------------------------------------------------
# Class that gets main info from Ecuapass document 
#----------------------------------------------------------
class CartaporteByza (CartaporteNTA):
	def __init__ (self, fieldsJsonFile, runningDir):
		super().__init__ (fieldsJsonFile, runningDir)
		self.empresa   = EcuData.getEmpresaInfo ("BYZA")

	def getSubjectInfo (self, key):
		return self.getSubjectInfoByza (key)

	#-----------------------------------------------------------
	# Clean watermark: depending for each "company" class
	#-----------------------------------------------------------
	def cleanWaterMark (self, text):
		print ("-- cleanWaterMark in text: ")
		print (text)

		text = re.sub ("Byza\n|Byza", "", text)

		value1 = "soluciones que facilitan tuvida"
		value2 = value1+"\n"
		text   = re.sub (rf"{value2}|{value1}", "", text)
		return text.strip()

	#-------------------------------------------------------------------
	#-- For BYZA: CO:exportacion or EC:importacion. The contrary for NTA
	#-------------------------------------------------------------------
	def getTipoProcedimiento (self):
		tipoProcedimiento = None
		procedimientos    = {"CO":"IMPORTACION", "EC":"EXPORTACION"}
		try:
			numero            = super().getNumeroDocumento ()
			codigoPais        = self.getCodigoPais (numero)
			tipoProcedimiento = procedimientos [codigoPais]
		except:
			print (f"Alerta: No se pudo determinar tipo de procedimiento (Importación/Exportación)")
			tipoProcedimiento = "IMPORTACION||LOW"

		return tipoProcedimiento

#--------------------------------------------------------------------
# Call main 
#--------------------------------------------------------------------
if __name__ == '__main__':
	main ()


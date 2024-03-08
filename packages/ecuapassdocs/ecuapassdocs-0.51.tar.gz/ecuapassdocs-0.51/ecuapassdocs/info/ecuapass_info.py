
import os, json, re

from .ecuapass_data import EcuData
from .ecuapass_extractor import Extractor
from .ecuapass_utils import Utils

# Base class for all info document clases: CartaporteInfo (CPI), EcuMNF (MCI), EcuDCL (DTAI)
class EcuInfo:
	def __init__ (self, fieldsJsonFile, runningDir):
		self.fieldsJsonFile      = fieldsJsonFile
		self.runningDir          = runningDir
		self.resourcesPath       = os.path.join (runningDir, "resources", "data-cartaportes") 
		self.fields              = json.load (open (fieldsJsonFile))
		self.fields ["jsonFile"] = fieldsJsonFile
		self.ecudoc              = {}

	#-- For all types of documents (fixed fro NTA and BYZA, check the others)
	def getNumeroDocumento (self):
		text   = Utils.getValue (self.fields, "00b_Numero")
		numero = Extractor.getNroDocumento (text)

		codigo = self.getCodigoPais (numero)
		self.fields ["00_Pais"] = {"value":codigo, "content":codigo}
		return numero

	#-- Returns the first two letters from document number
	def getCodigoPais (self, numero):
		try:
			if numero.startswith ("CO"): 
				return "CO"
			elif numero.startswith ("EC"): 
				return "EC"
		except:
			print (f"ALERTA: No se pudo determinar código del pais desde el número: '{numero}'")
		return ""

	#-- Return updated PDF document fields
	def getDocFields (self):
		return self.fields

	#-- Get data and value from document main fields"""
	def getNombreEmpresa (self):
		return self.empresa ["nombre"]

	def getDireccionEmpresa (self):
		return self.empresa ["direccion"]

	#-----------------------------------------------------------
	#-- Return IMPORTACION or EXPORTACION
	#-----------------------------------------------------------
	def getTipoProcedimiento (self):
		return "IMPORTACION||LOW"

	#-----------------------------------------------------------
	# Get info from mercancia: INCONTERM, Ciudad, Precio, Tipo Moneda
	#-----------------------------------------------------------
	def getIncotermInfo (self, text):
		info = {"incoterm":None, "precio":None, "moneda":None, "pais":None, "ciudad":None}

		try:
			text = text.replace ("\n", " ")

			# Precio
			text, precio    = Extractor.getRemoveNumber (text)
			info ["precio"] = Utils.checkLow (Utils.convertToAmericanFormat (precio))
			text = text.replace (precio, "") if precio else text

			# Incoterm
			termsString = Extractor.getDataString ("tipos_incoterm.txt", 
			                                        self.resourcesPath, From="keys")
			reTerms = rf"\b({termsString})\b" # RE for incoterm
			incoterm = Utils.getValueRE (reTerms, text)
			info ["incoterm"] = Utils.checkLow (incoterm)
			text = text.replace (incoterm, "") if incoterm else text

			# Moneda
			info ["moneda"] = "USD"
			text = text.replace ("USD", "")
			text = text.replace ("$", "")

			# Get ciudad from text and Search 'pais' in previos boxes
			ciudadPais   = Extractor.extractCiudadPais (text, self.resourcesPath) 
			ciudad, pais = ciudadPais ["ciudad"], ciudadPais ["pais"]

			info ["ciudad"], info ["pais"] = self.searchPaisPreviousBoxes (ciudad, pais)
			if not info ["pais"]:
				info ["pais"]   = Utils.checkLow (info["pais"])
				info ["ciudad"] = Utils.addLow (info ["ciudad"])
			elif info ["pais"] and not info ["ciudad"]:
				info ["ciudad"] = Utils.addLow (info ["ciudad"])

		except:
			Utils.printException ("Obteniendo informacion de 'mercancía'")

		return info

	#-----------------------------------------------------------
	# Clean watermark: depending for each "company" class
	#-----------------------------------------------------------
	def cleanWaterMark (self, text):
		return text

#!/usr/bin/env python3

import os
from datetime import datetime

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# Send feedback (text and PDF file) to azure blob
class EcuFeedback:
	#----------------------------------------------------------------
	#-- Get the blob client to write to Azure blob
	#----------------------------------------------------------------
	def getBlobClient (text_blob_name):
		# Azure Storage account connection string
		connection_string = "DefaultEndpointsProtocol=https;AccountName=lgformsstorage;AccountKey=BHsWkVaWQYStRq8FOpoIl0jI39W+WFvrSJmxesr0euIEJe+qkSi0LoTM0HZfyOn2XbYfnHir7CD8+ASt6ZJnwg==;EndpointSuffix=core.windows.net"

		# Azure Blob Storage container name
		container_name = "blobfeedback"

		# Initialize the BlobServiceClient
		blob_service_client = BlobServiceClient.from_connection_string (connection_string)

		# Create a container (if it doesn't exist)
		container_client = blob_service_client.get_container_client(container_name)
		blob_client = container_client.get_blob_client (text_blob_name)

		return (blob_client)

	#----------------------------------------------------------------
	# Send an empty file with log info as its filename
	#----------------------------------------------------------------
	def sendLog (logMessage):
		try:
			text_blob_name = f"{logMessage}"
			blob_client    = EcuFeedback.getBlobClient (text_blob_name)
			blob_client.upload_blob ("", overwrite=True)
		except:
			print (f"No se pudo enviar el log'")

	def sendFeedback (zipFilepath, docFilepath):
		# Azure Storage account connection string
		connection_string = "DefaultEndpointsProtocol=https;AccountName=lgformsstorage;AccountKey=BHsWkVaWQYStRq8FOpoIl0jI39W+WFvrSJmxesr0euIEJe+qkSi0LoTM0HZfyOn2XbYfnHir7CD8+ASt6ZJnwg==;EndpointSuffix=core.windows.net"

		# Azure Blob Storage container name
		container_name = "blobfeedback"

		# Get text from zip file
		feedbackText = EcuFeedback.getTextFromZipFile (zipFilepath)

		# Upload the feedback data to Azure Blob Storage
		EcuFeedback.upload_feedback_to_azure_storage (connection_string, container_name, feedbackText, docFilepath)

		return (f"REALIMENTACION: Documento {docFilepath}")

	#-- Upload text to azure
	def upload_feedback_to_azure_storage(connection_string, container_name, text_data, docFilepath):
		# Initialize the BlobServiceClient
		blob_service_client = BlobServiceClient.from_connection_string(connection_string)

		# Create a container (if it doesn't exist)
		container_client = blob_service_client.get_container_client(container_name)
		#container_client.create_container()

		fileSufix = EcuFeedback.getCurrentDateTimeString ()
		# Upload the text data as a blob
		text_blob_name = f"feedback-{fileSufix}.txt"
		text_blob_client = container_client.get_blob_client (text_blob_name)
		text_blob_client.upload_blob (text_data, overwrite=True)

		# Upload the PDF file as a blob
		if docFilepath != None and os.path.exists(docFilepath):
			pdf_blob_name = f"feedback-{fileSufix}.pdf"
			pdf_blob_client = container_client.get_blob_client(pdf_blob_name)
			with open(docFilepath, "rb") as pdf_file:
				pdf_blob_client.upload_blob(pdf_file, overwrite=True)

		print("Feedback data uploaded to Azure Blob Storage.")

	def getTextFromZipFile (zip_file_path):
		import zipfile
		import io

		try:
			# Open the ZIP file for reading
			with zipfile.ZipFile (zip_file_path, 'r') as zip_file:
				# Extract the first (and only) file from the ZIP archive
				file_info = zip_file.infolist()[0]
				extracted_text = zip_file.read(file_info.filename).decode('utf-8')

			#print("Extracted Text:")
			#print(extracted_text)
			return extracted_text

		except Exception as e:
			print("Error:", str(e))


	def getCurrentDateTimeString():
		current_datetime = datetime.now()
		formatted_datetime = current_datetime.strftime("%Y-%m-%d_%H:%M:%S")
		return formatted_datetime


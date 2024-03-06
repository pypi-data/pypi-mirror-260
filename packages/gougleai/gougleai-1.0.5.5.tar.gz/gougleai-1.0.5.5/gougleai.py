import requests
import json

apiKey = ""
orgId = ""

class models:
	list = """GLT-1: gougleai.models.glt.glt1 (gougleai.models.glt.versions[0])
GLT-1.0.5 Beta: gougleai.models.glt.glt105 (gougleai.models.glt.versions[1])
GIC-1: gougleai.models.gic.gic1 (gougleai.models.gic.versions[0])
GIC-1.0.5 Beta: gougleai.models.gic.gic105 (gougleai.models.gic.versions[1])"""
	
	class glt:
		glt1 = "gougleai.models.glt.glt1"
		glt105 = "gougleai.model.glt.glt105"
		versions = [glt1, glt105]
	class gic:
		gic1 = "gougleai.models.gic.gic1"
		gic105 = "gougleai.model.glt.gic105"
		versions = [gic1, gic105]

def complete(model, prompt:str, maxTokenNumber:int = 100):
	if apiKey == "":
		raise Exception("API Key cannot be empty string.")
	else:
		complete.choices = []
		if str(model) in models.list:
			if str(model) in models.glt.__dict__.values():
				if prompt != "":
					url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
					headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {apiKey}'}
					
					params = {'prompt': prompt, 'max_tokens': maxTokenNumber}
					req = requests.post(url, data=params, headers=headers)
					data = req.text
					
					result = data
					
					complete.choices = [result]
					return complete
				else:
					raise Exception("Cannot complete empty string.")
			else:
				raise Exception("Model '" + str(model) + "' is not a Text Completion model.\nSee https://github.com/gougle-official/gougleai-python/blob/main/README.md#models for the models list with model types.")
		elif model != "":
			raise Exception("Model '" + str(model) + "' not found in gougleai API.")
		else:
			raise Exception("Model cannot be empty.")

class chat:
	def complete(model, chatHistory:object, maxTokenNumber:int = 100):
		if chatHistory["role"] != "ai" and chatHistory["role"] != "system" and chatHistory["role"] != "user":
			raise Exception("Role must be 'ai', 'system' or 'user', cannot be '" + chatHistory["role"] + "'.")
		if apiKey == "":
			raise Exception("API Key cannot be empty string.")
		else:
			complete.choices = []
			if str(model) in models.list:
				if str(model) in models.glt.__dict__.values():
					if chatHistory != {} and chatHistory["message"] != "":
						url = 'https://api.openai.com/v1/engines/davinci-codex/completions'
						headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {apiKey}'}

						params = {'prompt': chatHistory, 'max_tokens': maxTokenNumber}
						params = json.dumps(params).encode('utf-8')

						req = requests.post(url, data=params, headers=headers)
						data = req.text
						
						result = data

						complete.choices = [result]
						return complete
					else:
						raise Exception("Cannot complete empty conversation.")
				else:
					raise Exception("Model '" + str(model) + "' is not a Text Completion model.\nSee https://github.com/gougle-official/gougleai-python/blob/main/README.md#models for the models list with model types.")

			elif model != "":
				raise Exception("Model '" + str(model) + "' not found in gougleai API.")
			else:
				raise Exception("Model cannot be empty.")
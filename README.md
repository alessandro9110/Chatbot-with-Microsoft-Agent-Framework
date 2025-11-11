# Labs
  
## Azure DevOps Pipeline per Chatbot Agent su Azure AI Foundry

Questa repository include una pipeline CI/CD per il deploy di un chatbot come agente su Azure AI Foundry, integrando Cosmos DB e Azure AI Search.

### File principali YAML

- **azure-pipelines.yml**: Definisce la pipeline Azure DevOps con le seguenti fasi:
	- Test: installa le dipendenze e lancia i test (es. pytest).
	- Deploy: effettua il provisioning delle risorse Azure (Cosmos DB, AI Search) e il deploy dell'agente su AI Foundry.
	- Personalizza i comandi di deploy in base al tuo agente/modello.

- **pipeline-parameters.yml**: Contiene i parametri personalizzabili per la pipeline, tra cui:
	- `azureSubscription`: Nome della sottoscrizione Azure.
	- `resourceGroup`: Nome del resource group.
	- `location`: Regione Azure.
	- `cosmosDbName`: Nome del database Cosmos DB.
	- `aiSearchName`: Nome del servizio Azure AI Search.
	- `aiFoundryName`: Nome dell'istanza AI Foundry.

### Come usare la pipeline

1. Configura i parametri in `pipeline-parameters.yml` secondo la tua infrastruttura Azure.
2. Personalizza i comandi di deploy in `azure-pipelines.yml` per adattarli al tuo agente e modello.
3. Esegui la pipeline su Azure DevOps per testare e deployare il chatbot agent.

### Esempio di configurazione parametri

```yaml
parameters:
	- name: azureSubscription
		type: string
		default: 'AZURE_SUBSCRIPTION_ID'
	- name: resourceGroup
		type: string
		default: 'chatbot-rg'
	- name: location
		type: string
		default: 'westeurope'
	- name: cosmosDbName
		type: string
		default: 'chatbot-cosmosdb'
	- name: aiSearchName
		type: string
		default: 'chatbot-search'
	- name: aiFoundryName
		type: string
		default: 'chatbot-foundry'
```

### Personalizzazione deploy agente

Nel file `azure-pipelines.yml`, aggiungi lo script o task specifico per il deploy del tuo agente su Azure AI Foundry, ad esempio:

```yaml
		- script: |
				az ai foundry agent deploy --name ${{ parameters.aiFoundryName }} --resource-group ${{ parameters.resourceGroup }} --model-path ./agent
			displayName: 'Deploy Chatbot Agent su AI Foundry'
```

Sostituisci il comando con quello adatto al tuo agente/modello.

### Note
- Assicurati di avere i permessi necessari sulla sottoscrizione Azure.
- Puoi estendere la pipeline aggiungendo step di test end-to-end, validazione, o deploy di altri componenti.

## Chatbot Agent

Il codice dell'agente è organizzato nella cartella `agent/` e utilizza Azure Agent Framework per orchestrare il chatbot con Azure AI Foundry, Azure AI Search e Cosmos DB.

### Struttura del progetto

- `main.py`: File principale con la classe `ChatbotAgent` che gestisce le interazioni.
- `config.py`: Configurazione con variabili d'ambiente.
- `cosmos_client.py`: Client per interagire con Cosmos DB (seguendo best practices di data modeling).
- `ai_search_client.py`: Client per Azure AI Search con ricerca vettoriale.
- `requirements.txt`: Dipendenze Python.

### Configurazione

Imposta le seguenti variabili d'ambiente:

```bash
export AZURE_AI_PROJECT_ENDPOINT="https://your-project.azure.com"
export AZURE_AI_MODEL_DEPLOYMENT_NAME="gpt-4o"
export COSMOS_ENDPOINT="https://your-cosmos.documents.azure.com:443/"
export COSMOS_KEY="your-cosmos-key"
export COSMOS_DATABASE="chatbot-db"
export COSMOS_CONTAINER="conversations"
export AI_SEARCH_ENDPOINT="https://your-search.search.windows.net"
export AI_SEARCH_KEY="your-search-key"
export AI_SEARCH_INDEX="knowledge-base"
```

### Utilizzo

```python
from agent import ChatbotAgent

async def main():
    chatbot = ChatbotAgent()
    response = await chatbot.chat("user123", "Hello, search for AI news")
    print(response)

asyncio.run(main())
```

### Features

- **Orchestrazione**: Utilizza Azure Agent Framework per coordinare i servizi.
- **Ricerca vettoriale**: Integra Azure AI Search per RAG (Retrieval-Augmented Generation).
- **Persistenza conversazioni**: Salva e recupera lo storico chat su Cosmos DB con partizionamento per utente.
- **Scalabilità**: Architettura cloud-native pronta per il deploy su Azure.
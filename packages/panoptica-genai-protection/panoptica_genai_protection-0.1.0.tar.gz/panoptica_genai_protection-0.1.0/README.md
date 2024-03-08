# Project Marvin
Marvin is intended to provide protection for LLM-driven components of software systems.

We do so by inspecting prompts (and in the future LLM responses to these prompts) with NLP techniques to determine if 
they are suspected to malicious activity. 

## Components
* [Marvin SDK](./sdk) - Python SDK to programmatically integrate system with LLM protection
* [Prompt Inspection Server](./prompt_inspection_server) - HTTP server to serve the requests made by Marvin SDK
* [Demo Chat App](./chat_app) - Simple streamlit-based chat app to demo Marvin capabilities

## Code Generation
We use auto-generated request/response models from OpenAPI spec,
using [datamodel-code-generator](https://koxudaxi.github.io/datamodel-code-generator/). 

The server spec is under [prompt/openapi/openapi.yaml](openapi/prompt_inspection.yaml).
We use its generated artifacts in both the client and the server.

_Note: Currently we only generate model files and not the client/server code utilizing them._

### Installing `datamodel-code-generator`
```shell
pip install datamodel-code-generator
```

### Generating the `models.py` 
The following snippet would generate the `models.py` file with all the schema objects declared in `openapi.yaml`, 
and copy the generated file to its location in the SDK folder.

```shell
datamodel-codegen --input openapi/prompt_inspection.yaml \
  --input-file-type openapi \
  --output prompt_inspection_server/prompt_inspection/models/models.py \
  --disable-timestamp

cp prompt_inspection_server/prompt_inspection/models/models.py sdk/panoptica_genai_protection/models.py


datamodel-codegen --input openapi/producer.yaml \
  --input-file-type openapi \
  --output prompt_inspection_server/prompt_inspection/models/attack-analytics.py \
  --disable-timestamp

```

### copying commmon code to server and batch_processing
```shell
cp -r common/ prompt_inspection_server/prompt_inspection/common
cp -r common/ batch_processing/common
```  
or run the script
```shell
./copy_common.sh
```


## CODEOWNERS
Please modify this file to include your team and CODEOWNER rules

## Jenkins pipeline
Please refer to the [SRE-Pipeline-Library](https://wwwin-github.cisco.com/pages/eti/sre-pipeline-library/) documentation for further information on how to modify your Jenkinsfile to your needs

### `docker-compose.yaml`
This file will create a system that includes postgres and the backend.
to start follow this steps
```
cd attack-analytics
docker-compose -f docker-compose.yaml up db --build -d
docker-compose -f docker-compose.yaml up migration --build -d
docker-compose -f docker-compose.yaml up forensic --build -d
```
# chatbot

## Steps to install Ollama locally via Docker
1. Install Docker Desktop
2. Put the ollama image
3. Run the container containing the Ollama image

## Inteacting with the model
### Directly through docker
1. Execute the following commands to interact with the model:
   Note: There are various models provided by Ollama, but for this example, I am using moondream and Llama3
   1. ollama run moondream
   2. Wait for the model to fininsh downloading
   3. When the server runs, you can interact with ollama's moondream by typing in your questions and wait for a response

### Via curl
1. We can also interact with the models using the curl command.
2. Simply run the following commands:
   1. curl http://localhost:11434/api/generate -d '{
  "model": "llama3",
  "prompt": "Why is the sky blue?"

}'
Update the model as well as prompt parameters to your model and prompt questions.

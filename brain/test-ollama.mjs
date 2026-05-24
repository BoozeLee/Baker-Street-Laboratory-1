import { Ollama } from 'ollama';
const client = new Ollama({ host: 'http://localhost:11434' });
console.log('Starting chat...');
const stream = client.chat({
  model: 'mistral:instruct',
  messages: [{ role: 'user', content: 'hi' }],
  stream: true,
});
for await (const chunk of stream) {
  console.log(JSON.stringify(chunk));
}

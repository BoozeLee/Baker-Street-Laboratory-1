import { Ollama } from 'ollama';
const client = new Ollama({ host: 'http://localhost:11434' });
console.log('Starting chat...');
const stream = await client.chat({
  model: 'mistral:instruct',
  messages: [{ role: 'user', content: 'hi' }],
  stream: true,
});
console.log('Got stream object:', typeof stream[Symbol.asyncIterator]);
for await (const chunk of stream) {
  console.log('Chunk:', JSON.stringify(chunk).substring(0,200));
}

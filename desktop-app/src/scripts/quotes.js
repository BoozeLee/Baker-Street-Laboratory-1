/* Baker Street Laboratory — Sherlock Holmes Daily Deduction Quotes */

const HOLMES_QUOTES = [
  { text: "When you have eliminated the impossible, whatever remains, however improbable, must be the truth.", source: "The Sign of Four" },
  { text: "The game is afoot.", source: "The Adventure of the Abbey Grange" },
  { text: "You see, but you do not observe. The distinction is clear.", source: "A Scandal in Bohemia" },
  { text: "The world is full of obvious things which nobody by any chance ever observes.", source: "The Hound of the Baskervilles" },
  { text: "There is nothing more deceptive than an obvious fact.", source: "The Boscombe Valley Mystery" },
  { text: "A man's brain originally is like a little empty attic, and you have to stock it with such furniture as you choose.", source: "A Study in Scarlet" },
  { text: "Education never ends, Watson. It is a series of lessons, with the greatest for the last.", source: "His Last Bow" },
  { text: "Crime is common. Logic is rare. Therefore it is upon the logic rather than upon the crime that you should dwell.", source: "The Adventure of the Copper Beeches" },
  { text: "I never guess. It is a shocking habit — destructive to the logical faculty.", source: "The Sign of Four" },
  { text: "It has long been an axiom of mine that the little things are infinitely the most important.", source: "A Case of Identity" },
  { text: "You know my methods. Apply them.", source: "The Hound of the Baskervilles" },
  { text: "My name is Sherlock Holmes. It is my business to know what other people don't know.", source: "The Adventure of the Blue Carbuncle" },
  { text: "To a great mind, nothing is little.", source: "A Study in Scarlet" },
  { text: "Detection is, or ought to be, an exact science and should be treated in the same cold and unemotional manner.", source: "The Sign of Four" },
  { text: "Work is the best antidote to sorrow, my dear Watson.", source: "The Adventure of the Empty House" },
  { text: "There is nothing like first-hand evidence.", source: "A Study in Scarlet" },
  { text: "Mediocrity knows nothing higher than itself, but talent instantly recognizes genius.", source: "The Valley of Fear" },
  { text: "It is a capital mistake to theorize before you have all the evidence.", source: "A Study in Scarlet" },
  { text: "The world is big enough for us. No ghosts need apply.", source: "The Adventure of the Sussex Vampire" },
  { text: "My mind rebels at stagnation. Give me problems, give me work!", source: "The Sign of Four" },
  { text: "The temptation to form premature theories upon insufficient data is the bane of our profession.", source: "The Valley of Fear" },
  { text: "I am a brain, Watson. The rest of me is a mere appendix.", source: "The Adventure of the Mazarin Stone" },
  { text: "Singularity is almost invariably a clue.", source: "A Study in Scarlet" },
  { text: "When a doctor goes wrong, he is the first of criminals.", source: "The Adventure of the Speckled Band" },
  { text: "Once you eliminate the impossible, whatever remains, no matter how improbable, must be the truth.", source: "The Beryl Coronet" },
  { text: "You know my methods, Watson. There was not one of them which I did not apply to the inquiry.", source: "The Adventure of the Crooked Man" },
  { text: "When once your point of view is changed, the very thing which was so damning becomes a clue to the truth.", source: "The Problem of Thor Bridge" },
  { text: "The difficulty is to detach the framework of fact from the embellishments of theorists.", source: "The Adventure of Wisteria Lodge" },
  { text: "It is my belief, Watson, founded upon my experience, that the lowest and vilest alleys in London do not present a more dreadful record of sin than does the smiling and beautiful countryside.", source: "The Adventure of the Copper Beeches" },
  { text: "I cannot live without brain-work. What else is there to live for?", source: "The Sign of Four" }
];

function getDailyQuote() {
  const now = new Date();
  const start = new Date(now.getFullYear(), 0, 0);
  const dayOfYear = Math.floor((now - start) / (1000 * 60 * 60 * 24));
  return HOLMES_QUOTES[dayOfYear % HOLMES_QUOTES.length];
}

function displayDailyQuote() {
  const quoteEl = document.getElementById('daily-quote-text');
  const authorEl = document.getElementById('daily-quote-author');
  if (!quoteEl || !authorEl) return;

  const quote = getDailyQuote();
  quoteEl.textContent = '';
  authorEl.textContent = '';
  authorEl.style.opacity = '0';

  let i = 0;
  const chars = quote.text.split('');
  const typeInterval = setInterval(() => {
    if (i < chars.length) {
      quoteEl.textContent += chars[i++];
    } else {
      clearInterval(typeInterval);
      setTimeout(() => {
        authorEl.textContent = `— ${quote.source}`;
        requestAnimationFrame(() => {
          authorEl.style.opacity = '1';
        });
      }, 200);
    }
  }, 28);
}

document.addEventListener('DOMContentLoaded', displayDailyQuote);

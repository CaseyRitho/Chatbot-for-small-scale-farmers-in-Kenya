const chatHistory = document.querySelector(".chat-history");
const userMessageInput = document.getElementById("user-message");
const sendButton = document.getElementById("button");

const OpenAI = require("openai");

const api = "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";

const openai = new OpenAI({
  apiKey: api,
  dangerouslyAllowBrowser: true,
});

var counties = [
  "Baringo",
  "Bomet",
  "Bungoma",
  "Busia",
  "Elgeyo Marakwet",
  "Embu",
  "Garissa",
  "Homa Bay",
  "Isiolo",
  "Kajiado",
  "Kakamega",
  "Kericho",
  "Kiambu",
  "Kilifi",
  "Kirinyaga",
  "Kisii",
  "Kisumu",
  "Kitui",
  "Kwale",
  "Laikipia",
  "Lamu",
  "Machakos",
  "Makueni",
  "Mandera",
  "Marsabit",
  "Meru",
  "Migori",
  "Mombasa",
  "Murang'a",
  "Nairobi",
  "Nakuru",
  "Nandi",
  "Narok",
  "Nyamira",
  "Nyandarua",
  "Nyeri",
  "Samburu",
  "Siaya",
  "Taita Taveta",
  "Tana River",
  "Tharaka Nithi",
  "Trans Nzoia",
  "Turkana",
  "Uasin Gishu",
  "Vihiga",
  "Wajir",
  "West Pokot",
];

async function runCompletion(user_input) {
  const completion = await openai.chat.completions.create({
    model: "gpt-3.5-turbo",
    messages: [{ role: "assistant", content: user_input }],
  });
  console.log(completion.choices[0].message.content);
  return completion.choices[0].message.content;
}

sendButton.addEventListener("click", async () => {
  const userMessage = userMessageInput.value;
  if (userMessage.trim().length === 0) {
    return; // Prevent empty messages
  }

  // Display user message
  const userMessageElement = document.createElement("div");
  userMessageElement.classList.add("message", "user-message");
  userMessageElement.textContent = userMessage;
  chatHistory.appendChild(userMessageElement);

  userMessageInput.value = "";

  var lowerCaseSentence = userMessage.toLowerCase();
  var lowerCaseCounties = counties.map((county) => county.toLowerCase());

  // Loop through each word in the counties array
  for (var i = 0; i < lowerCaseCounties.length; i++) {
    // Check if the word exists in the lowercase sentence
    if (lowerCaseSentence.includes(lowerCaseCounties[i])) {
      const botMessage =
        "Please enter the specific area in the county you come from";
      const botMessageElement = document.createElement("div");
      botMessageElement.classList.add("message", "bot-message");
      botMessageElement.textContent = botMessage;
      chatHistory.appendChild(botMessageElement);

      return;
    }
  }

  const results = await runCompletion(userMessage);

  const botMessage = results;
  const botMessageElement = document.createElement("div");
  botMessageElement.classList.add("message", "bot-message");
  botMessageElement.textContent = botMessage;
  chatHistory.appendChild(botMessageElement);

  chatHistory.scrollTo(0, chatHistory.scrollHeight);
});

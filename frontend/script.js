const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const output = document.getElementById("output");

let chatHistory = [];
const USER_ID = "user_1"; // can be dynamic

// Load chat history on page load
window.addEventListener("DOMContentLoaded", async () => {
  try {
    const res = await fetch(`http://127.0.0.1:8000/get_history?user_id=${USER_ID}`);
    if (res.ok) {
      chatHistory = await res.json();
      renderChat();
    }
  } catch (err) {
    console.error("Could not fetch history", err);
  }
});

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message) return;

  chatHistory.push({ type: "user", text: message });
  renderChat();
  messageInput.value = "";

  const typingId = addTypingIndicator();

  try {
    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: USER_ID, message })
    });
    const data = await res.json();

    removeTypingIndicator(typingId);

    const intentClass = `intent-${data.intent || "default"}`;
    chatHistory.push({ type: "ai", text: data.reply, intentClass });
    renderChat();

    // Save history
    await fetch("http://127.0.0.1:8000/save_history", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: USER_ID, history: chatHistory })
    });

  } catch (err) {
    removeTypingIndicator(typingId);
    chatHistory.push({ type: "ai", text: "Server error", intentClass: "intent-urgent" });
    renderChat();
    console.error(err);
  }
});

function renderChat() {
  output.innerHTML = chatHistory.map(msg => {
    const cls = msg.type === "user" ? "user message" : `ai message ${msg.intentClass || ""}`;
    return `<div class="${cls}"><p>${msg.text}</p></div>`;
  }).join("");
  output.scrollTop = output.scrollHeight;
}

function addTypingIndicator() {
  const id = `typing-${Date.now()}`;
  const div = document.createElement("div");
  div.id = id;
  div.className = "ai message intent-default";
  div.innerHTML = `<p id="typing">AI is typing<span class="dots">...</span></p>`;
  output.appendChild(div);
  output.scrollTop = output.scrollHeight;
  return id;
}
function removeTypingIndicator(id) {
  const div = document.getElementById(id);
  if (div) div.remove();
}

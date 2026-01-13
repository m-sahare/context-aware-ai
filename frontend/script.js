const form = document.getElementById("chat-form");
const messageInput = document.getElementById("message");
const output = document.getElementById("output");

form.addEventListener("submit", async (e) => {
  // 🚨 THIS IS CRITICAL — stops page refresh
  e.preventDefault();

  const message = messageInput.value.trim();
  if (!message) return;

  // Show thinking text
  output.innerHTML = "<p><b>AI:</b> Thinking...</p>";

  try {
    const response = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        user_id: "user_1",
        message: message
      })
    });

    const data = await response.json();

    // ✅ Replace output ONCE
    output.innerHTML = `
      <p><b>Intent:</b> ${data.intent}</p>
      <p><b>AI:</b> ${data.reply}</p>
    `;

    // Clear input AFTER response
    messageInput.value = "";

  } catch (error) {
    output.innerHTML = "<p style='color:red'>Server error</p>";
    console.error(error);
  }
});

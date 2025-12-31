async function loadMessages() {
    const response = await fetch("../export/messages.json");
    const messages = await response.json();
    renderMessages(messages);
}

function renderMessages(messages) {
    const container = document.getElementById("messages");

    for (const msg of messages) {
        const bubble = document.createElement("div");
        bubble.classList.add("message");
        bubble.classList.add(msg.author.role === "self" ? "self" : "other");

        bubble.textContent = msg.text || "";

        if (msg.attachments && msg.attachments.length > 0) {
            const attBox = document.createElement("div");
            attBox.className = "attachments";

            for (const att of msg.attachments) {
                if (!att.local_path) continue;

                if (att.type === "photo") {
                    const img = document.createElement("img");
                    img.src = "../" + att.local_path.replace("\\", "/");
                    attBox.appendChild(img);
                }

                if (att.type === "voice_message") {
                    const audio = document.createElement("audio");
                    audio.controls = true;
                    audio.src = "../" + att.local_path.replace("\\", "/");
                    attBox.appendChild(audio);
                }
            }

            bubble.appendChild(attBox);
        }

        container.appendChild(bubble);
    }
}

loadMessages();

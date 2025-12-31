function formatDateTime(isoString) {
    const date = new Date(isoString);
    return date.toLocaleString(undefined, {
        year: "numeric",
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
    });
}

async function loadMessages() {
    const response = await fetch("../export/messages.json");
    const messages = await response.json();
    renderMessages(messages);
}

function renderMessages(messages) {
    const container = document.getElementById("messages");

    for (const msg of messages) {
        const wrapper = document.createElement("div");
        wrapper.classList.add("message-wrapper");
        wrapper.classList.add(msg.author.role === "self" ? "self" : "other");

        // Meta (author + time)
        const meta = document.createElement("div");
        meta.className = "message-meta";
        meta.textContent = `${msg.author.name} · ${formatDateTime(msg.datetime)}`;

        // Message bubble
        const bubble = document.createElement("div");
        bubble.classList.add("message");
        bubble.classList.add(msg.author.role === "self" ? "self" : "other");
        bubble.textContent = msg.text || "";

        // Attachments
        if (msg.attachments && msg.attachments.length > 0) {
            const attBox = document.createElement("div");
            attBox.className = "attachments";

            for (const att of msg.attachments) {
                if (!att.local_path) continue;

                const path = "../" + att.local_path.replace("\\", "/");

                if (att.type === "photo") {
                    const img = document.createElement("img");
                    img.src = path;
                    attBox.appendChild(img);
                }

                if (att.type === "voice_message") {
                    const audio = document.createElement("audio");
                    audio.controls = true;
                    audio.src = path;
                    attBox.appendChild(audio);
                }
            }

            bubble.appendChild(attBox);
        }

        wrapper.appendChild(meta);
        wrapper.appendChild(bubble);
        container.appendChild(wrapper);
    }
}

loadMessages();

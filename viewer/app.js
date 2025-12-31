/* =====================
   Date helpers
   ===================== */

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

function formatDay(isoString) {
    const date = new Date(isoString);
    return date.toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric"
    });
}

/* =====================
   Theme
   ===================== */

function setupTheme() {
    const toggle = document.getElementById("theme-toggle");
    const saved = localStorage.getItem("theme");

    if (saved === "dark") {
        document.body.classList.add("dark");
        toggle.textContent = "☀";
    }

    toggle.addEventListener("click", () => {
        document.body.classList.toggle("dark");
        const isDark = document.body.classList.contains("dark");
        toggle.textContent = isDark ? "☀" : "🌙";
        localStorage.setItem("theme", isDark ? "dark" : "light");
    });
}

/* =====================
   Autoscroll
   ===================== */

function setupAutoscroll() {
    const toggle = document.getElementById("scroll-toggle");
    const saved = localStorage.getItem("autoscroll");

    let enabled = saved !== "false"; // default = true
    toggle.textContent = enabled ? "⬇️" : "⬆️";

    toggle.addEventListener("click", () => {
        enabled = !enabled;
        localStorage.setItem("autoscroll", enabled ? "true" : "false");
        toggle.textContent = enabled ? "⬇️" : "⬆️";
    });

    return () => {
        if (enabled) {
            window.scrollTo(0, document.body.scrollHeight);
        }
    };
}

/* =====================
   Messages rendering
   ===================== */

async function loadMessages() {
    const response = await fetch("../export/messages.json");
    const messages = await response.json();

    renderMessages(messages);
    setupSearch();
    setupTheme();

    const applyAutoscroll = setupAutoscroll();
    applyAutoscroll();
}

function renderMessages(messages) {
    const container = document.getElementById("messages");
    container.innerHTML = "";

    let lastDay = null;

    for (const msg of messages) {
        const currentDay = msg.datetime.split("T")[0];

        if (currentDay !== lastDay) {
            const separator = document.createElement("div");
            separator.className = "day-separator";
            separator.textContent = formatDay(msg.datetime);
            container.appendChild(separator);
            lastDay = currentDay;
        }

        const wrapper = document.createElement("div");
        wrapper.classList.add("message-wrapper", msg.author.role);
        wrapper.dataset.text = (msg.text || "").toLowerCase();

        const meta = document.createElement("div");
        meta.className = "message-meta";
        meta.textContent = `${msg.author.name} · ${formatDateTime(msg.datetime)}`;

        const bubble = document.createElement("div");
        bubble.classList.add("message", msg.author.role);
        bubble.textContent = msg.text || "";

        if (msg.attachments) {
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

            if (attBox.children.length > 0) {
                bubble.appendChild(attBox);
            }
        }

        wrapper.appendChild(meta);
        wrapper.appendChild(bubble);
        container.appendChild(wrapper);
    }
}

/* =====================
   Search
   ===================== */

function setupSearch() {
    const input = document.getElementById("search");

    input.addEventListener("input", () => {
        const query = input.value.trim().toLowerCase();
        const wrappers = document.querySelectorAll(".message-wrapper");

        wrappers.forEach(wrapper => {
            const text = wrapper.dataset.text;
            const bubble = wrapper.querySelector(".message");

            if (!query) {
                wrapper.style.display = "";
                bubble.innerHTML = bubble.textContent;
                return;
            }

            if (text.includes(query)) {
                wrapper.style.display = "";
                const regex = new RegExp(`(${query})`, "gi");
                bubble.innerHTML = bubble.textContent.replace(regex, "<mark>$1</mark>");
            } else {
                wrapper.style.display = "none";
            }
        });
    });
}

loadMessages();

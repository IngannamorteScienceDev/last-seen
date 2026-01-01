/* =====================
   Global state
   ===================== */

let allMessages = [];
let pageSize = 100;
let currentPage = 0;
let totalPages = 0;

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
   Pagination
   ===================== */

function setupPaginationControls() {
    document.getElementById("prev-page").onclick = () => {
        if (currentPage > 0) {
            currentPage--;
            renderCurrentPage();
        }
    };

    document.getElementById("next-page").onclick = () => {
        if (currentPage < totalPages - 1) {
            currentPage++;
            renderCurrentPage();
        }
    };
}

function renderCurrentPage() {
    const start = currentPage * pageSize;
    const end = start + pageSize;
    const slice = allMessages.slice(start, end);

    renderMessages(slice);
    updatePaginationLabel();

    window.scrollTo(0, document.body.scrollHeight);
}

function updatePaginationLabel() {
    document.getElementById("page-label").textContent =
        `Page ${currentPage + 1} / ${totalPages}`;
}

/* =====================
   Messages rendering
   ===================== */

function renderMessages(messages) {
    const container = document.getElementById("messages");
    container.innerHTML = "";

    let lastDay = null;

    for (const msg of messages) {
        const day = msg.datetime.split("T")[0];

        if (day !== lastDay) {
            const sep = document.createElement("div");
            sep.className = "day-separator";
            sep.textContent = formatDay(msg.datetime);
            container.appendChild(sep);
            lastDay = day;
        }

        const wrapper = document.createElement("div");
        wrapper.classList.add("message-wrapper", msg.author.role);

        const meta = document.createElement("div");
        meta.className = "message-meta";
        meta.textContent = `${msg.author.name} · ${formatDateTime(msg.datetime)}`;

        const bubble = document.createElement("div");
        bubble.classList.add("message", msg.author.role);
        bubble.textContent = msg.text || "";

        if (msg.attachments) {
            const box = document.createElement("div");
            box.className = "attachments";

            for (const att of msg.attachments) {
                if (!att.local_path) continue;
                const path = "../" + att.local_path.replace("\\", "/");

                if (att.type === "photo") {
                    const img = document.createElement("img");
                    img.src = path;
                    box.appendChild(img);
                }

                if (att.type === "voice_message") {
                    const audio = document.createElement("audio");
                    audio.controls = true;
                    audio.src = path;
                    box.appendChild(audio);
                }
            }

            if (box.children.length > 0) {
                bubble.appendChild(box);
            }
        }

        wrapper.appendChild(meta);
        wrapper.appendChild(bubble);
        container.appendChild(wrapper);
    }
}

/* =====================
   Init
   ===================== */

async function loadMessages() {
    const res = await fetch("../export/messages.json");
    allMessages = await res.json();

    totalPages = Math.ceil(allMessages.length / pageSize);

    // start from last page (latest messages)
    currentPage = totalPages - 1;

    setupTheme();
    setupPaginationControls();
    renderCurrentPage();
}

loadMessages();

/* =====================
   State
   ===================== */

let allMessages = [];
let pageSize = 100;
let currentPage = 0;
let totalPages = 0;

/* =====================
   Date helpers
   ===================== */

function formatDateTime(iso) {
    const d = new Date(iso);
    return d.toLocaleString(undefined, {
        year: "numeric",
        month: "short",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit"
    });
}

function formatDay(iso) {
    const d = new Date(iso);
    return d.toLocaleDateString(undefined, {
        year: "numeric",
        month: "long",
        day: "numeric"
    });
}

/* =====================
   Theme
   ===================== */

function setupTheme() {
    const btn = document.getElementById("theme-toggle");
    const saved = localStorage.getItem("theme");

    if (saved === "dark") {
        document.body.classList.add("dark");
        btn.textContent = "☀";
    }

    btn.onclick = () => {
        document.body.classList.toggle("dark");
        const isDark = document.body.classList.contains("dark");
        btn.textContent = isDark ? "☀" : "🌙";
        localStorage.setItem("theme", isDark ? "dark" : "light");
    };
}

/* =====================
   Pagination
   ===================== */

function setupPagination() {
    document.getElementById("prev-page").onclick = () => {
        if (currentPage > 0) {
            currentPage--;
            renderPage();
        }
    };

    document.getElementById("next-page").onclick = () => {
        if (currentPage < totalPages - 1) {
            currentPage++;
            renderPage();
        }
    };
}

function updatePageLabel() {
    document.getElementById("page-label").textContent =
        `Page ${currentPage + 1} / ${totalPages}`;
}

function renderPage() {
    const start = currentPage * pageSize;
    const end = start + pageSize;
    renderMessages(allMessages.slice(start, end));
    updatePageLabel();
    window.scrollTo(0, document.body.scrollHeight);
}

/* =====================
   Rendering
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

        const wrap = document.createElement("div");
        wrap.classList.add("message-wrapper", msg.author.role);

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

            if (box.children.length > 0) bubble.appendChild(box);
        }

        wrap.appendChild(meta);
        wrap.appendChild(bubble);
        container.appendChild(wrap);
    }
}

/* =====================
   Init
   ===================== */

async function loadMessages() {
    const res = await fetch("../export/messages.json");
    allMessages = await res.json();

    totalPages = Math.ceil(allMessages.length / pageSize);
    currentPage = totalPages - 1; // start from latest

    setupTheme();
    setupPagination();
    renderPage();
}

loadMessages();

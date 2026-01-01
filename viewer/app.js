/* =====================
   STATE
   ===================== */

let meta = null;
let currentPage = null;

/* =====================
   HELPERS
   ===================== */

function formatTime(iso) {
    const d = new Date(iso);
    return d.toLocaleTimeString(undefined, {
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
   THEME
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
        const dark = document.body.classList.contains("dark");
        btn.textContent = dark ? "☀" : "🌙";
        localStorage.setItem("theme", dark ? "dark" : "light");
    };
}

/* =====================
   DATA LOADING
   ===================== */

async function loadMeta() {
    const res = await fetch("../export/meta.json");
    meta = await res.json();
}

async function loadPage(pageIndex) {
    const res = await fetch(
        `../export/pages/page_${String(pageIndex).padStart(3, "0")}.json`
    );
    return await res.json();
}

/* =====================
   RENDERING
   ===================== */

function renderMessages(messages) {
    const container = document.querySelector(".messages");
    if (!container) {
        console.error("Messages container not found");
        return;
    }

    container.innerHTML = "";

    let lastDay = null;

    for (let i = 0; i < messages.length; i++) {
        const msg = messages[i];
        const prev = messages[i - 1];
        const next = messages[i + 1];

        const day = msg.datetime.split("T")[0];
        if (day !== lastDay) {
            const sep = document.createElement("div");
            sep.className = "time";
            sep.textContent = formatDay(msg.datetime);
            container.appendChild(sep);
            lastDay = day;
        }

        const samePrev = prev && prev.author.role === msg.author.role;
        const sameNext = next && next.author.role === msg.author.role;

        let group = "start";
        if (samePrev && sameNext) group = "middle";
        else if (samePrev) group = "end";

        const bubble = document.createElement("div");
        bubble.className = `message ${msg.author.role} ${group}`;

        // meta only for first in group
        if (!samePrev) {
            const metaDiv = document.createElement("div");
            metaDiv.className = "message-meta";
            metaDiv.textContent = `${msg.author.name} · ${formatTime(msg.datetime)}`;
            bubble.appendChild(metaDiv);
        }

        if (msg.text) {
            const text = document.createElement("div");
            text.textContent = msg.text;
            bubble.appendChild(text);
        }

        // attachments (safe)
        if (msg.attachments && msg.attachments.length > 0) {
            const box = document.createElement("div");
            box.className = "attachments";

            for (const att of msg.attachments) {
                if (!att.local_path) continue;
                const path = "../" + att.local_path.replaceAll("\\", "/");

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

        container.appendChild(bubble);
    }
}

function updatePagination() {
    document.getElementById("page-label").textContent =
        `Page ${meta.total_pages - currentPage} / ${meta.total_pages}`;

    document.getElementById("prev-page").disabled =
        currentPage === meta.total_pages - 1;

    document.getElementById("next-page").disabled =
        currentPage === 0;
}

/* =====================
   CONTROLS
   ===================== */

function setupPagination() {
    document.getElementById("prev-page").onclick = async () => {
        if (currentPage < meta.total_pages - 1) {
            await showPage(currentPage + 1);
        }
    };

    document.getElementById("next-page").onclick = async () => {
        if (currentPage > 0) {
            await showPage(currentPage - 1);
        }
    };
}

async function showPage(pageIndex) {
    const page = await loadPage(pageIndex);
    currentPage = pageIndex;
    renderMessages(page.messages);
    updatePagination();

    const search = document.getElementById("search");
    if (search) search.value = "";
}

/* =====================
   SEARCH (CURRENT PAGE)
   ===================== */

function setupSearch() {
    const input = document.getElementById("search");

    input.addEventListener("input", () => {
        const q = input.value.trim().toLowerCase();
        const bubbles = document.querySelectorAll(".message");

        bubbles.forEach(bubble => {
            const text = bubble.textContent.toLowerCase();
            bubble.style.display = !q || text.includes(q) ? "" : "none";
        });
    });
}

/* =====================
   INIT
   ===================== */

async function init() {
    await loadMeta();

    setupTheme();
    setupPagination();
    setupSearch();

    // start from LAST page (latest messages)
    const lastPage = meta.total_pages - 1;
    await showPage(lastPage);
}

init();

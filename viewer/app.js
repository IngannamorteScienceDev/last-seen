let meta = null;
let currentPage = null;

/* ---------- helpers ---------- */

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

/* ---------- theme ---------- */

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

/* ---------- data ---------- */

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

/* ---------- render ---------- */

function renderMessages(messages) {
    const container = document.querySelector(".messages");
    container.innerHTML = "";

    let lastDay = null;

    for (let i = 0; i < messages.length; i++) {
        const msg = messages[i];
        const prev = messages[i - 1];
        const next = messages[i + 1];

        // ---- day separator ----
        const day = msg.datetime.split("T")[0];
        if (day !== lastDay) {
            const sep = document.createElement("div");
            sep.className = "time";
            sep.textContent = formatDay(msg.datetime);
            container.appendChild(sep);
            lastDay = day;
        }

        // ---- UNIFIED grouping logic ----
        const samePrev =
            prev &&
            prev.author.role === msg.author.role &&
            prev.author.name === msg.author.name;

        const sameNext =
            next &&
            next.author.role === msg.author.role &&
            next.author.name === msg.author.name;

        let group = "start";
        if (samePrev && sameNext) group = "middle";
        else if (samePrev) group = "end";

        const bubble = document.createElement("div");
        bubble.className = `message ${msg.author.role} ${group}`;

        // meta ONLY at start of group (for BOTH self & other)
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

        container.appendChild(bubble);
    }
}

/* ---------- pagination ---------- */

function updatePagination() {
    document.getElementById("page-label").textContent =
        `Page ${meta.total_pages - currentPage} / ${meta.total_pages}`;

    document.getElementById("prev-page").disabled =
        currentPage === meta.total_pages - 1;

    document.getElementById("next-page").disabled =
        currentPage === 0;
}

async function showPage(pageIndex) {
    const page = await loadPage(pageIndex);
    currentPage = pageIndex;
    renderMessages(page.messages);
    updatePagination();
}

function setupPagination() {
    document.getElementById("prev-page").onclick = () => {
        if (currentPage < meta.total_pages - 1) {
            showPage(currentPage + 1);
        }
    };

    document.getElementById("next-page").onclick = () => {
        if (currentPage > 0) {
            showPage(currentPage - 1);
        }
    };
}

/* ---------- search ---------- */

function setupSearch() {
    const input = document.getElementById("search");
    input.addEventListener("input", () => {
        const q = input.value.toLowerCase();
        document.querySelectorAll(".message").forEach(m => {
            m.style.display = !q || m.textContent.toLowerCase().includes(q)
                ? ""
                : "none";
        });
    });
}

/* ---------- init ---------- */

async function init() {
    await loadMeta();
    setupTheme();
    setupPagination();
    setupSearch();

    const lastPage = meta.total_pages - 1;
    showPage(lastPage);
}

init();

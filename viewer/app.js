let meta = null;
let dateIndex = null;
let currentPage = null;

/* ---------- helpers ---------- */

function formatTime(iso) {
    const d = new Date(iso);
    return d.toLocaleTimeString(undefined, {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit"
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
    meta = await fetch("../export/meta.json").then(r => r.json());
}

async function loadDateIndex() {
    dateIndex = await fetch("../export/date_index.json").then(r => r.json());
}

async function loadPage(page) {
    return await fetch(
        `../export/pages/page_${String(page).padStart(3, "0")}.json`
    ).then(r => r.json());
}

/* ---------- render ---------- */

function renderMessages(messages) {
    const container = document.querySelector(".messages");
    container.innerHTML = "";

    let lastDay = null;

    messages.forEach((msg, i) => {
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

        const samePrev = prev && prev.author.name === msg.author.name;
        const sameNext = next && next.author.name === msg.author.name;

        let group = "start";
        if (samePrev && sameNext) group = "middle";
        else if (samePrev) group = "end";

        const bubble = document.createElement("div");
        bubble.className = `message ${msg.author.role} ${group}`;

        if (!samePrev) {
            const meta = document.createElement("div");
            meta.className = "message-meta";
            meta.textContent = `${msg.author.name}`;
            bubble.appendChild(meta);
        }

        if (msg.text) {
            const text = document.createElement("div");
            text.textContent = msg.text;
            bubble.appendChild(text);
        }

        // hover menu
        const hover = document.createElement("div");
        hover.className = "hover-menu";

        const time = document.createElement("span");
        time.className = "hover-time";
        time.textContent = formatTime(msg.datetime);

        const copy = document.createElement("button");
        copy.className = "copy-btn";
        copy.textContent = "📋";
        copy.onclick = () => navigator.clipboard.writeText(msg.text || "");

        hover.appendChild(time);
        hover.appendChild(copy);
        bubble.appendChild(hover);

        container.appendChild(bubble);
    });
}

/* ---------- pagination ---------- */

async function showPage(page) {
    const data = await loadPage(page);
    currentPage = page;
    renderMessages(data.messages);

    document.getElementById("page-label").textContent =
        `Page ${meta.total_pages - page} / ${meta.total_pages}`;
}

function setupPagination() {
    document.getElementById("prev-page").onclick = () => {
        if (currentPage < meta.total_pages - 1) showPage(currentPage + 1);
    };

    document.getElementById("next-page").onclick = () => {
        if (currentPage > 0) showPage(currentPage - 1);
    };
}

/* ---------- sticky date ---------- */

function setupStickyDate() {
    const messagesEl = document.querySelector(".messages");
    const sticky = document.getElementById("sticky-date");

    messagesEl.addEventListener("scroll", () => {
        const times = [...messagesEl.querySelectorAll(".time")];
        let current = null;

        for (const t of times) {
            const r = t.getBoundingClientRect();
            const pr = messagesEl.getBoundingClientRect();
            if (r.top - pr.top <= 8) current = t;
            else break;
        }

        if (current) {
            sticky.textContent = current.textContent;
            sticky.classList.add("visible");
        }
    });
}

/* ---------- jump to date ---------- */

function setupDatePicker() {
    const picker = document.getElementById("date-picker");

    picker.addEventListener("change", async () => {
        const date = picker.value;
        if (!dateIndex[date]) {
            alert("No messages on this date");
            return;
        }

        const { page, offset } = dateIndex[date];
        await showPage(page);

        const bubbles = document.querySelectorAll(".message");
        if (bubbles[offset]) {
            bubbles[offset].scrollIntoView({ behavior: "smooth" });
        }
    });
}

/* ---------- init ---------- */

async function init() {
    await loadMeta();
    await loadDateIndex();

    setupTheme();
    setupPagination();
    setupStickyDate();
    setupDatePicker();

    await showPage(meta.total_pages - 1);
}

init();

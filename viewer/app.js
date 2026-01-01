/* =====================
   State
   ===================== */

let allMessages = [];
const pageSize = 100;

// pageIndex = 0 means "latest page"
let pageIndex = 0;
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
   Pagination core (from last to first)
   ===================== */

function getPageSlice() {
    // We assume allMessages is chronological: oldest -> newest
    // pageIndex=0 -> last chunk (newest)
    const total = allMessages.length;

    const end = total - (pageIndex * pageSize);
    const start = Math.max(0, end - pageSize);

    return allMessages.slice(start, end);
}

function updatePageLabel() {
    // Display pages as 1..N where 1 is the latest
    const current = pageIndex + 1;
    document.getElementById("page-label").textContent = `Page ${current} / ${totalPages}`;
}

function updateButtons() {
    const prevBtn = document.getElementById("prev-page"); // newer
    const nextBtn = document.getElementById("next-page"); // older

    prevBtn.disabled = (pageIndex === 0);
    nextBtn.disabled = (pageIndex === totalPages - 1);
}

function renderPage() {
    const slice = getPageSlice();
    renderMessages(slice);
    updatePageLabel();
    updateButtons();

    // Reset search input when switching pages (safer UX)
    const search = document.getElementById("search");
    if (search) search.value = "";
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
        wrap.dataset.text = (msg.text || "").toLowerCase();

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

            if (box.children.length > 0) bubble.appendChild(box);
        }

        wrap.appendChild(meta);
        wrap.appendChild(bubble);
        container.appendChild(wrap);
    }
}

/* =====================
   Search (current page only)
   ===================== */

function setupSearch() {
    const input = document.getElementById("search");

    input.addEventListener("input", () => {
        const query = input.value.trim().toLowerCase();
        const wrappers = document.querySelectorAll(".message-wrapper");

        wrappers.forEach(wrapper => {
            const text = wrapper.dataset.text || "";
            const bubble = wrapper.querySelector(".message");

            if (!query) {
                wrapper.style.display = "";
                bubble.innerHTML = bubble.textContent;
                return;
            }

            if (text.includes(query)) {
                wrapper.style.display = "";
                const regex = new RegExp(`(${escapeRegExp(query)})`, "gi");
                bubble.innerHTML = bubble.textContent.replace(regex, "<mark>$1</mark>");
            } else {
                wrapper.style.display = "none";
            }
        });
    });
}

function escapeRegExp(s) {
    return s.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

/* =====================
   Controls
   ===================== */

function setupPaginationControls() {
    document.getElementById("prev-page").onclick = () => {
        // newer
        if (pageIndex > 0) {
            pageIndex--;
            renderPage();
        }
    };

    document.getElementById("next-page").onclick = () => {
        // older
        if (pageIndex < totalPages - 1) {
            pageIndex++;
            renderPage();
        }
    };
}

/* =====================
   Init
   ===================== */

async function loadMessages() {
    const res = await fetch("../export/messages.json");
    allMessages = await res.json();

    totalPages = Math.max(1, Math.ceil(allMessages.length / pageSize));
    pageIndex = 0; // start at latest

    setupTheme();
    setupPaginationControls();
    setupSearch();
    renderPage();
}

loadMessages();

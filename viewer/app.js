/* =====================
   State
   ===================== */

let meta = null;
let currentPage = null;

/* =====================
   Helpers
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
   Data loading
   ===================== */

async function loadMeta() {
    const res = await fetch("../export/meta.json");
    meta = await res.json();
}

async function loadPage(pageIndex) {
    const res = await fetch(`../export/pages/page_${String(pageIndex).padStart(3, "0")}.json`);
    return await res.json();
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

        const metaDiv = document.createElement("div");
        metaDiv.className = "message-meta";
        metaDiv.textContent = `${msg.author.name} · ${formatDateTime(msg.datetime)}`;

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

        wrap.appendChild(metaDiv);
        wrap.appendChild(bubble);
        container.appendChild(wrap);
    }
}

function updatePagination() {
    document.getElementById("page-label").textContent =
        `Page ${meta.total_pages - currentPage} / ${meta.total_pages}`;

    document.getElementById("prev-page").disabled = (currentPage === meta.total_pages - 1);
    document.getElementById("next-page").disabled = (currentPage === 0);
}

/* =====================
   Controls
   ===================== */

function setupControls() {
    document.getElementById("prev-page").onclick = async () => {
        if (currentPage < meta.total_pages - 1) {
            currentPage++;
            await showPage(currentPage);
        }
    };

    document.getElementById("next-page").onclick = async () => {
        if (currentPage > 0) {
            currentPage--;
            await showPage(currentPage);
        }
    };
}

async function showPage(pageIndex) {
    const page = await loadPage(pageIndex);
    currentPage = pageIndex;
    renderMessages(page.messages);
    updatePagination();

    // reset search
    const search = document.getElementById("search");
    if (search) search.value = "";
}

/* =====================
   Search (current page only)
   ===================== */

function setupSearch() {
    const input = document.getElementById("search");

    input.addEventListener("input", () => {
        const q = input.value.trim().toLowerCase();
        const wrappers = document.querySelectorAll(".message-wrapper");

        wrappers.forEach(wrap => {
            const text = wrap.dataset.text || "";
            const bubble = wrap.querySelector(".message");

            if (!q) {
                wrap.style.display = "";
                bubble.innerHTML = bubble.textContent;
            } else if (text.includes(q)) {
                wrap.style.display = "";
                const re = new RegExp(`(${q})`, "gi");
                bubble.innerHTML = bubble.textContent.replace(re, "<mark>$1</mark>");
            } else {
                wrap.style.display = "none";
            }
        });
    });
}

/* =====================
   Init
   ===================== */

async function init() {
    await loadMeta();

    setupTheme();
    setupControls();
    setupSearch();

    // start from LAST page (latest messages)
    const lastPage = meta.total_pages - 1;
    await showPage(lastPage);
}

init();

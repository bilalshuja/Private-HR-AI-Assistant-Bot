$(document).ready(function () {
    const TYPING_SPEED = 20;

    // --- 1. Theme Logic ---
    function updateThemeUI(theme) {
        $('html').attr('data-theme', theme);
        const btnText = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
        const btnIcon = theme === 'dark' ? '<i class="fa-regular fa-sun"></i>' : '<i class="fa-regular fa-moon"></i>';
        $('#toggle-dark-mode').html(`${btnIcon} <span>${btnText}</span>`);
    }

    const savedTheme = localStorage.getItem('theme') || 'light';
    updateThemeUI(savedTheme);

    $('#toggle-dark-mode').click(function () {
        const current = $('html').attr('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', next);
        updateThemeUI(next);
    });

    // --- 2. Chat Logic ---
    function scrollToBottom() {
        const container = document.getElementById("chat-container");
        container.scrollTop = container.scrollHeight;
    }

    function appendMessage(role, text, isTyping = false) {
        const className = role === 'user' ? 'user-message' : 'bot-message';
        const avatar = role === 'user' ? '<i class="fa-solid fa-user"></i>' : '<i class="fa-solid fa-robot"></i>';
        const msgId = `msg-${Date.now()}`;

        const html = `
            <div class="message ${className}">
                <div class="avatar">${avatar}</div>
                <div class="content" id="${msgId}"></div>
            </div>`;
        
        $('#chat-container').append(html);
        scrollToBottom();

        if (isTyping) {
            let i = 0;
            function type() {
                if (i < text.length) {
                    $(`#${msgId}`).append(text.charAt(i));
                    i++;
                    setTimeout(type, TYPING_SPEED);
                    scrollToBottom(); // Scroll as it types
                }
            }
            type();
        } else {
            $(`#${msgId}`).text(text);
        }
    }

    // --- 3. Send Message ---
    $('#search-form').submit(function (e) {
        e.preventDefault();
        const query = $('#query').val().trim();
        if (!query) return;

        // User Message
        appendMessage('user', query);
        $('#query').val('');

        // Loading Indicator
        const loadingId = `loading-${Date.now()}`;
        $('#chat-container').append(`
            <div id="${loadingId}" class="message bot-message">
                <div class="avatar"><i class="fa-solid fa-robot"></i></div>
                <div class="content">Thinking... <i class="fa-solid fa-spinner fa-spin"></i></div>
            </div>
        `);
        scrollToBottom();

        // API Call
        $.ajax({
            type: "POST",
            url: "/",
            data: { query: query },
            success: function (data) {
                $(`#${loadingId}`).remove();
                if (data.response) {
                    appendMessage('bot', data.response, true);
                } else {
                    appendMessage('bot', "Sorry, I couldn't process that.");
                }
                loadHistory(); // Refresh Sidebar
            },
            error: function () {
                $(`#${loadingId}`).remove();
                appendMessage('bot', "Error: Server not responding.");
            }
        });
    });

    // --- 4. History Logic ---
    window.loadHistory = function () {
        $.get("/history", function (data) {
            const list = $('#history-list');
            list.empty();
            
            if (!data.history) return;

            ['Today', 'Yesterday', 'Older'].forEach(section => {
                const items = data.history[section];
                if (items && items.length > 0) {
                    list.append(`<li style="font-weight:bold; padding-top:10px; cursor:default;">${section}</li>`);
                    items.forEach(item => {
                        if (item.type === 'User') {
                            const safeMsg = item.message.replace(/'/g, "\\'");
                            list.append(`
                                <li onclick="loadChat('${safeMsg}')">
                                    <span><i class="fa-regular fa-message"></i> ${item.message}</span>
                                    <button class="delete-btn" onclick="event.stopPropagation(); deleteChat('${safeMsg}')">
                                        <i class="fa-solid fa-xmark"></i>
                                    </button>
                                </li>
                            `);
                        }
                    });
                }
            });
        });
    }

    window.loadChat = function(msg) {
        $('#query').val(msg);
        $('#search-form').submit();
    }

    window.deleteChat = function(msg) {
        $.ajax({
            type: "POST",
            url: "/delete-history-item",
            contentType: "application/json",
            data: JSON.stringify({ message: msg }),
            success: function() { loadHistory(); }
        });
    }

    $('#clear-history-btn').click(function() {
        if(confirm("Clear all history?")) {
            $.post("/clear-history", function() { 
                loadHistory(); 
                $('#chat-container').html(''); // Clear UI
            });
        }
    });

    // Initial Load
    loadHistory();
});
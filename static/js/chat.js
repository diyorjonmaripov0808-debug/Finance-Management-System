/**
 * Chat System JavaScript
 * Handles real-time message updates, auto-scrolling, and dynamic metadata refreshing.
 */

class ChatManager {
    constructor(config) {
        this.containerId = config.containerId || 'chat_messages';
        this.refreshInterval = config.refreshInterval || 5000;
        this.metadataIds = config.metadataIds || [];
        this.container = document.getElementById(this.containerId);
        this.isRefreshing = false;

        if (this.container) {
            this.init();
        }
    }

    init() {
        this.scrollToBottom();
        this.startAutoRefresh();
        console.log('ChatManager initialized');
    }

    scrollToBottom() {
        if (this.container) {
            this.container.scrollTop = this.container.scrollHeight;
        }
    }

    shouldScroll() {
        if (!this.container) return false;
        // Check if user is near bottom (within 50px)
        return this.container.scrollTop + this.container.clientHeight >= this.container.scrollHeight - 50;
    }

    async refresh() {
        if (this.isRefreshing) return;
        this.isRefreshing = true;

        try {
            const response = await fetch('?refresh=true');
            if (!response.ok) throw new Error('Refresh failed');

            const html = await response.text();
            const parser = new DOMParser();
            const doc = parser.parseFromString(html, 'text/html');

            // 1. Update Chat Messages
            const newMessages = doc.getElementById(this.containerId);
            if (newMessages && newMessages.innerHTML !== this.container.innerHTML) {
                const autoScroll = this.shouldScroll();
                this.container.innerHTML = newMessages.innerHTML;
                if (autoScroll) this.scrollToBottom();
            }

            // 2. Update Metadata
            this.metadataIds.forEach(id => {
                const newEl = doc.getElementById(id);
                const oldEl = document.getElementById(id);
                if (newEl && oldEl && newEl.innerHTML !== oldEl.innerHTML) {
                    oldEl.innerHTML = newEl.innerHTML;

                    // Add a brief "highlight" effect if it's a badge or status change
                    if (oldEl.classList.contains('badge')) {
                        oldEl.style.transition = 'none';
                        oldEl.style.opacity = '0.5';
                        setTimeout(() => {
                            oldEl.style.transition = 'opacity 0.3s ease';
                            oldEl.style.opacity = '1';
                        }, 50);
                    }
                }
            });

        } catch (error) {
            console.error('Chat Refresh Error:', error);
        } finally {
            this.isRefreshing = false;
        }
    }

    startAutoRefresh() {
        this.refreshTimer = setInterval(() => this.refresh(), this.refreshInterval);
    }

    stopAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }
    }
}

// Global initialization for admin chat
document.addEventListener('DOMContentLoaded', () => {
    if (document.getElementById('chat_messages')) {
        window.chatManager = new ChatManager({
            containerId: 'chat_messages',
            refreshInterval: 5000,
            metadataIds: [
                'user_status',
                'user_wallets_count',
                'user_last_activity',
                'unread-count',      // For sidebar
                'global_unread_count' // If present as ID
            ]
        });
    }
});

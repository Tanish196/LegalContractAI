import React, { useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import { MessageCircle, X, Sparkles } from "lucide-react";

const ChatBubble: React.FC = () => {
    const navigate = useNavigate();
    const location = useLocation();
    const [isHovered, setIsHovered] = useState(false);
    const [dismissed, setDismissed] = useState(false);

    // Hide on chat-assistant page or if dismissed
    if (location.pathname === "/chat-assistant" || dismissed) return null;

    return (
        <div className="fixed bottom-6 right-6 z-50 flex items-end gap-3">
            {/* Tooltip / Hover Label */}
            <div
                className={`
          transition-all duration-300 ease-out origin-right
          ${isHovered ? "opacity-100 scale-100 translate-x-0" : "opacity-0 scale-95 translate-x-2 pointer-events-none"}
        `}
            >
                <div className="bg-card border border-border/60 rounded-xl px-4 py-3 shadow-lg
          dark:bg-card dark:border-[hsl(var(--highlight))/0.3] dark:shadow-[0_0_20px_rgba(33,150,243,0.15)]
          max-w-[200px]"
                >
                    <p className="text-sm font-medium text-foreground whitespace-nowrap flex items-center gap-1.5">
                        <Sparkles className="h-3.5 w-3.5 text-[hsl(var(--highlight))]" />
                        AI Legal Assistant
                    </p>
                    <p className="text-xs text-muted-foreground mt-0.5">
                        Ask anything or draft contracts
                    </p>
                </div>
            </div>

            {/* Main Bubble Button */}
            <button
                onClick={() => navigate("/chat-assistant")}
                onMouseEnter={() => setIsHovered(true)}
                onMouseLeave={() => setIsHovered(false)}
                className="
          group relative w-14 h-14 rounded-full
          bg-primary text-primary-foreground
          dark:bg-[hsl(var(--highlight))] dark:text-black
          shadow-lg hover:shadow-xl
          dark:shadow-[0_4px_20px_rgba(33,150,243,0.4)]
          dark:hover:shadow-[0_4px_30px_rgba(33,150,243,0.6)]
          transition-all duration-300 ease-out
          hover:scale-110 active:scale-95
          flex items-center justify-center
          cursor-pointer
        "
                aria-label="Open AI Chat Assistant"
            >
                {/* Ping animation ring */}
                <span className="absolute inset-0 rounded-full bg-primary/30 dark:bg-[hsl(var(--highlight))/0.3] animate-ping opacity-30" />

                {/* Icon */}
                <MessageCircle className="h-6 w-6 relative z-10 transition-transform duration-300 group-hover:rotate-12" />

                {/* Close/dismiss mini button */}
                <span
                    onClick={(e) => {
                        e.stopPropagation();
                        setDismissed(true);
                    }}
                    className="
            absolute -top-1 -right-1 w-5 h-5 rounded-full
            bg-destructive text-destructive-foreground
            flex items-center justify-center
            opacity-0 group-hover:opacity-100
            transition-opacity duration-200
            hover:scale-110
            cursor-pointer
            z-20
          "
                    aria-label="Dismiss chat bubble"
                >
                    <X className="h-3 w-3" />
                </span>
            </button>
        </div>
    );
};

export default ChatBubble;

# AC-MOT — video panel visibility and verified full screen (v69)

Slide 15 ("Ablation result") keeps its **Watch AC-MOT vs Baseline videos** button, which opens the
separate video library on the "Baseline vs final · uav0000249" clip. This version fixes two things
in that library and changes nothing else.

**1. The video window is always visible.** In v68 the player could be pushed below the panel on
short or narrow windows, so the video ended up off screen with no way to scroll to it. The player
now keeps a minimum height and the panel scrolls instead of spilling.

**2. Full screen works, and degrades gracefully.** The full-screen control is larger, and a second
large button sits directly on the selected video. It now covers the standard, WebKit and MS
Fullscreen APIs plus Safari/iOS `webkitEnterFullscreen`. If the browser refuses full screen — for
example inside an embedded frame with a restrictive permissions policy — the video falls back to a
full-window view with a short explanation, and the button becomes "Exit full screen". Esc leaves
the full-window view first and only then closes the library.

Lazy loading is kept: a video file is requested only when its tab is selected. The five video files
and the picture library are unchanged and remain separate. Fonts, colors, layout, navigation and
all scientific content are unchanged.

This version is copied from v68. Older versions were not changed.

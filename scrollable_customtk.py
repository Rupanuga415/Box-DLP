"""Scrollable CustomTkinter example.

Run:
    python Python/Projects/scrollable_customtk.py

This creates a `ScrollableFrame` (vertical) using a `tk.Canvas` and a
`customtkinter`-styled inner frame so widgets remain visible when the
window is too small.
"""

import customtkinter as ctk
import tkinter as tk

class ScrollableFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        # Get the fg_color we were initialized with (if any)
        try:
            my_fg = self.cget("fg_color")
        except Exception:
            my_fg = None
        # Determine an effective background color that matches CTk styling
        parent_bg = None
        try:
            parent_bg = self.master.cget("fg_color")
            if not parent_bg or parent_bg == "transparent":
                # Try internal CTk attribute for root window
                try:
                    parent_bg = self.master._fg_color
                except Exception:
                    parent_bg = None
        except Exception:
            parent_bg = None

        canvas_bg = self._canvas_bg()
        
        # Try to extract a single color from parent_bg
        if not canvas_bg and parent_bg:
            canvas_bg = self._normalize_color(parent_bg)

        # Fallback to dark CTk theme color
        if not canvas_bg:
            canvas_bg = "#242424"

        self.canvas = tk.Canvas(self, highlightthickness=0, bd=0, bg=canvas_bg)
        try:
            self.v_scroll = ctk.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        except Exception:
            self.v_scroll = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.canvas.configure(yscrollcommand=self.v_scroll.set)

        # Make the inner frame use a solid, non-rounded background matching the app
        inner_bg = None
        try:
            # Use my_fg if I was explicitly initialized with a color
            if my_fg and my_fg != "transparent":
                inner_bg = self._normalize_color(my_fg)
            elif parent_bg and parent_bg != "transparent":
                inner_bg = self._normalize_color(parent_bg)
            else:
                fg = self.cget("fg_color")
                if fg and fg != "transparent":
                    inner_bg = self._normalize_color(fg)
        except Exception:
            inner_bg = None

        # If still no inner_bg, use the fallback dark color
        if not inner_bg:
            inner_bg = "#242424"

        # Use the determined background color (not transparent) so no white shows through
        self.inner = ctk.CTkFrame(self.canvas, fg_color=inner_bg)
        self.window = self.canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.canvas.pack(side="left", fill="both", expand=True)

        # Initially don't pack the scrollbar; show it only when needed
        self._scrollbar_visible = False

        self.inner.bind("<Configure>", self._on_inner_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        # Mouse wheel scrolling (Windows / Mac / Linux)
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _canvas_bg(self):
        try:
            bg = self.cget("fg_color")
            if not bg or bg == "transparent":
                return None
            if isinstance(bg, (tuple, list)):
                for part in bg:
                    if isinstance(part, str) and part and part != "transparent":
                        return part
                return None
            # Normalize into a string and take the first token (handles "gray86 gray17", "('gray86','gray17')", etc.)
            bg_s = str(bg)
            for ch in '(),':
                bg_s = bg_s.replace(ch, ' ')
            bg_s = bg_s.strip()
            if not bg_s:
                return None
            return bg_s.split()[0]
        except Exception:
            return None

    def _normalize_color(self, val):
        if not val:
            return None
        try:
            if isinstance(val, (tuple, list)):
                for part in val:
                    if isinstance(part, str) and part and part != "transparent":
                        return part
                return None
            s = str(val)
            for ch in '[],()':
                s = s.replace(ch, ' ')
            s = s.replace('\'', ' ')
            s = s.replace('"', ' ')
            s = s.replace(',', ' ')
            s = s.strip()
            if not s:
                return None
            for token in s.split():
                if token and token != 'transparent':
                    return token
            return None
        except Exception:
            return None

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.window, width=event.width)
        self._update_scrollbar()
        # ensure inner frame fills the canvas vertically when content is smaller
        self._adjust_inner_height()

    def _adjust_inner_height(self):
        try:
            self.inner.update_idletasks()
            req_h = self.inner.winfo_reqheight()
            view_h = self.canvas.winfo_height()
            new_h = max(req_h, view_h)
            # set the window item's height so the inner frame covers canvas when content small
            self.canvas.itemconfig(self.window, height=new_h)
        except Exception:
            pass

    def _on_mousewheel(self, event):
        if hasattr(event, 'delta'):
            delta = -1 * int(event.delta / 120)
        elif event.num == 4:
            delta = -1
        elif event.num == 5:
            delta = 1
        else:
            delta = 0
        self.canvas.yview_scroll(delta, "units")

    def _on_inner_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self._update_scrollbar()

    def _update_scrollbar(self):
        bbox = self.canvas.bbox("all")
        if not bbox:
            need = False
        else:
            content_height = bbox[3] - bbox[1]
            view_height = self.canvas.winfo_height()
            need = content_height > view_height

        if need and not self._scrollbar_visible:
            self.v_scroll.pack(side="right", fill="y")
            self._scrollbar_visible = True
        elif not need and self._scrollbar_visible:
            try:
                self.v_scroll.pack_forget()
            except Exception:
                pass
            self._scrollbar_visible = False


def demo():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.geometry("420x300")
    root.title("CustomTkinter Scrollable Demo")

    container = ScrollableFrame(root)
    container.pack(fill="both", expand=True, padx=10, pady=10)

    for i in range(10):
        row = ctk.CTkFrame(container.inner, height=50)
        row.pack(fill="x", pady=5)
        lbl = ctk.CTkLabel(row, text=f"Item {i+1}")
        lbl.pack(side="left", padx=10, pady=10)
        btn = ctk.CTkButton(row, text="Click")
        btn.pack(side="right", padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    demo()

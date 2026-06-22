
import json
import os
import sys
import threading
from pathlib import Path
from datetime import datetime
import urllib.parse
import urllib.request
import urllib.error
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

API_GET = "https://memo-bulletinboard-v2.oikki-api.win/getNotes"
API_DELETE = "https://memo-bulletinboard-v2.oikki-api.win/deleteNote"

FLAGGED_WORDS_FILENAME = "flagged_words.json"

DEFAULT_FLAGGED_CONFIG = {'description': 'Words and URL parts listed here are highlighted by the moderator tool. This only affects local highlighting. It does not block posts or delete anything automatically.', 'flagged_words': ['fuck', 'fucking', 'fucked', 'fucker', 'shit', 'shitty', 'bitch', 'bitches', 'bastard', 'asshole', 'arsehole', 'dick', 'cock', 'cunt', 'piss', 'slut', 'whore', 'twat', 'wanker', 'motherfucker', 'sex', 'sexy', 'porn', 'porno', 'pornography', 'nude', 'naked', 'boobs', 'tits', 'tit', 'penis', 'vagina', 'cum', 'cumming', 'ejaculate', 'ejaculation', 'masturbate', 'masturbation', 'blowjob', 'handjob', 'deepthroat', 'anal', 'rape', 'rapist', 'futanari', 'futa', 'gooner', 'gooners', 'gooning', 'horny', 'kys', 'kill yourself', 'retard', 'retarded', 'stfu', 'idiot', 'moron', 'nigger', 'nigga', 'niggah', 'niggar', 'nigguh', 'nigguhh', 'niggas', 'niggaz', 'nigglet', 'niglet', 'coon', 'spook', 'chink', 'gook', 'spic', 'wetback', 'raghead', 'sandnigger', 'kike', 'gyppo', 'gypo', 'faggot', 'fag', 'tranny', 'dyke', 'cuck', 'incel', 'femboy', 'femboys'], 'flagged_url_parts': ['http', 'https', 'www', '.com', '.net', '.org', '.gg', '.io', '.co', '.uk', 'discord.gg', 'discord.com', 'youtu.be', 'youtube.com', 'tiktok.com', 'twitter.com', 'x.com', 'instagram.com', 'facebook.com', 't.me', 'telegram', 'patreon.com', 'onlyfans', 'linktr.ee', 'bit.ly', 'tinyurl', 'paypal.me']}


def get_app_directory():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


def ensure_flagged_words_file(path):
    if path.exists():
        return
    path.write_text(json.dumps(DEFAULT_FLAGGED_CONFIG, indent=4, ensure_ascii=False), encoding="utf-8")


def load_flagged_config(path):
    ensure_flagged_words_file(path)
    with path.open("r", encoding="utf-8-sig") as f:
        data = json.load(f)

    flagged_words = data.get("flagged_words", [])
    flagged_url_parts = data.get("flagged_url_parts", [])

    if not isinstance(flagged_words, list):
        flagged_words = []
    if not isinstance(flagged_url_parts, list):
        flagged_url_parts = []

    flagged_words = [str(item).strip() for item in flagged_words if str(item).strip()]
    flagged_url_parts = [str(item).strip() for item in flagged_url_parts if str(item).strip()]

    return flagged_words, flagged_url_parts


def normalize_for_flagging(text):
    if not text:
        return ""

    text = str(text).lower()

    replacements = {
        "0": "o",
        "1": "i",
        "3": "e",
        "4": "a",
        "5": "s",
        "7": "t",
        "8": "b",
        "@": "a",
        "$": "s",
        "!": "i",
        "|": "i",
        "+": "t",
        "ⓐ": "a",
        "🅐": "a",
        "а": "a",
        "ｅ": "e",
        "е": "e",
        "ｉ": "i",
        "і": "i",
        "ｏ": "o",
        "о": "o",
        "ｓ": "s",
        "ѕ": "s",
        "ｔ": "t",
        "ｇ": "g",
        "ɡ": "g",
        "ｎ": "n",
        "ñ": "n",
    }

    for source, target in replacements.items():
        text = text.replace(source, target)

    cleaned = []
    for char in text:
        if char.isalnum() or char.isspace():
            cleaned.append(char)
        else:
            cleaned.append(" ")

    return " ".join("".join(cleaned).split())


def remove_spaces(text):
    return text.replace(" ", "")


def collapse_repeated_characters(text):
    if not text:
        return ""

    output = []
    last = None

    for char in text:
        if char != last:
            output.append(char)
            last = char

    return "".join(output)


def flagged_match(content, terms):
    normalized = normalize_for_flagging(content)
    compact = remove_spaces(normalized)
    squeezed = collapse_repeated_characters(compact)

    for term in terms:
        normalized_term = normalize_for_flagging(term)
        compact_term = remove_spaces(normalized_term)
        squeezed_term = collapse_repeated_characters(compact_term)

        if normalized_term and normalized_term in normalized:
            return True
        if compact_term and compact_term in compact:
            return True
        if squeezed_term and squeezed_term in squeezed:
            return True

    return False




def http_get_json(url, params):
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"
    req = urllib.request.Request(
        full_url,
        headers={
            "User-Agent": "PinboardModerator/1.0",
            "Accept": "application/json, text/plain, */*",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        raw = response.read().decode("utf-8", errors="replace")
        try:
            return json.loads(raw)
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Server did not return valid JSON.\nURL: {full_url}\nResponse:\n{raw}") from e


def http_get_text(url, params):
    query = urllib.parse.urlencode(params)
    full_url = f"{url}?{query}"
    req = urllib.request.Request(
        full_url,
        headers={
            "User-Agent": "PinboardModerator/1.0",
            "Accept": "*/*",
        },
        method="GET",
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


class PinboardModeratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("VRChat Pinboard Moderator")
        self.root.geometry("1280x760")
        self.root.minsize(1000, 620)

        self.notes = []
        self.filtered_notes = []
        self.user_counts = {}
        self.selected_userhash = None
        self.flagged_words_path = get_app_directory() / FLAGGED_WORDS_FILENAME
        self.flagged_words, self.flagged_url_parts = load_flagged_config(self.flagged_words_path)

        self.pinboard_id_var = tk.StringVar()
        self.hash_key_var = tk.StringVar()
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Enter your pinboard ID and hash key, then click Fetch Notes.")
        self.only_selected_user_var = tk.BooleanVar(value=False)

        self._build_ui()
        self._prompt_credentials_on_start()

    def _build_ui(self):
        top = ttk.Frame(self.root, padding=10)
        top.pack(fill="x")

        ttk.Label(top, text="Pinboard ID").grid(row=0, column=0, sticky="w", padx=(0, 6))
        ttk.Entry(top, textvariable=self.pinboard_id_var, width=24).grid(row=0, column=1, sticky="we", padx=(0, 12))

        ttk.Label(top, text="Hash Key").grid(row=0, column=2, sticky="w", padx=(0, 6))
        ttk.Entry(top, textvariable=self.hash_key_var, width=40, show="*").grid(row=0, column=3, sticky="we", padx=(0, 12))

        ttk.Button(top, text="Fetch Notes", command=self.fetch_notes).grid(row=0, column=4, padx=(0, 6))
        ttk.Button(top, text="Prompt for IDs", command=self.prompt_credentials).grid(row=0, column=5, padx=(0, 6))
        ttk.Button(top, text="Refresh", command=self.fetch_notes).grid(row=0, column=6, padx=(0, 6))
        ttk.Button(top, text="Reload Flagged Words", command=self.reload_flagged_words).grid(row=0, column=7)

        ttk.Label(top, text="Search").grid(row=1, column=0, sticky="w", padx=(0, 6), pady=(10, 0))
        search_entry = ttk.Entry(top, textvariable=self.search_var, width=40)
        search_entry.grid(row=1, column=1, columnspan=2, sticky="we", padx=(0, 12), pady=(10, 0))
        search_entry.bind("<KeyRelease>", lambda e: self.apply_filters())

        ttk.Checkbutton(
            top,
            text="Show only selected user",
            variable=self.only_selected_user_var,
            command=self.apply_filters,
        ).grid(row=1, column=3, sticky="w", pady=(10, 0))

        ttk.Button(top, text="Delete Selected Notes", command=self.delete_selected_notes).grid(row=1, column=4, padx=(0, 6), pady=(10, 0))
        ttk.Button(top, text="Delete All From Selected User", command=self.delete_selected_user_notes).grid(row=1, column=5, columnspan=2, sticky="we", pady=(10, 0))

        for i in range(8):
            top.columnconfigure(i, weight=1 if i in (1, 3) else 0)
        top.columnconfigure(3, weight=2)

        body = ttk.Panedwindow(self.root, orient=tk.HORIZONTAL)
        body.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        left = ttk.Frame(body, padding=8)
        right = ttk.Frame(body, padding=8)
        body.add(left, weight=1)
        body.add(right, weight=4)

        ttk.Label(left, text="User Hash Groups").pack(anchor="w")
        self.user_listbox = tk.Listbox(left, exportselection=False)
        self.user_listbox.pack(fill="both", expand=True, pady=(6, 0))
        self.user_listbox.bind("<<ListboxSelect>>", lambda e: self.on_user_selected())

        user_btns = ttk.Frame(left)
        user_btns.pack(fill="x", pady=(8, 0))
        ttk.Button(user_btns, text="Clear User Filter", command=self.clear_user_selection).pack(side="left")

        ttk.Label(right, text="Notes").pack(anchor="w")

        columns = ("index", "userHash", "timestamp", "content")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", selectmode="extended")
        self.tree.heading("index", text="Index")
        self.tree.heading("userHash", text="User Hash")
        self.tree.heading("timestamp", text="Timestamp")
        self.tree.heading("content", text="Content")

        self.tree.column("index", width=70, anchor="center")
        self.tree.column("userHash", width=260, anchor="w")
        self.tree.column("timestamp", width=170, anchor="w")
        self.tree.column("content", width=700, anchor="w")

        yscroll = ttk.Scrollbar(right, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(right, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)

        self.tree.pack(fill="both", expand=True, side="left")
        yscroll.pack(fill="y", side="right")
        xscroll.pack(fill="x", side="bottom")

        self.tree.tag_configure("flagged", background="#c94f5d", foreground="white")
        self.tree.bind("<<TreeviewSelect>>", lambda e: self._update_status_selection())

        bottom = ttk.Frame(self.root, padding=(10, 0, 10, 10))
        bottom.pack(fill="x")
        ttk.Label(bottom, textvariable=self.status_var).pack(anchor="w")

    def _prompt_credentials_on_start(self):
        self.root.after(200, self.prompt_credentials)

    def prompt_credentials(self):
        pinboard_id = simpledialog.askstring("Pinboard ID", "Enter the Pinboard ID:", parent=self.root)
        if pinboard_id:
            self.pinboard_id_var.set(pinboard_id.strip())

        hash_key = simpledialog.askstring("Hash Key", "Enter the Hash Key:", parent=self.root, show="*")
        if hash_key:
            self.hash_key_var.set(hash_key.strip())

    def reload_flagged_words(self):
        try:
            self.flagged_words, self.flagged_url_parts = load_flagged_config(self.flagged_words_path)
            for note in self.notes:
                note["flagged"] = self._looks_bad(note["content"])
            self.apply_filters()
            messagebox.showinfo(
                "Flagged Words Reloaded",
                f"Loaded {len(self.flagged_words)} flagged words and {len(self.flagged_url_parts)} flagged URL parts.\n\nFile:\n{self.flagged_words_path}"
            )
        except Exception as e:
            messagebox.showerror("Failed To Reload Flagged Words", str(e))

    def _set_busy(self, is_busy, message=None):
        self.root.config(cursor="watch" if is_busy else "")
        if message:
            self.status_var.set(message)
        self.root.update_idletasks()

    def fetch_notes(self):
        pinboard_id = self.pinboard_id_var.get().strip()
        if not pinboard_id:
            messagebox.showerror("Missing Pinboard ID", "Enter a Pinboard ID first.")
            return

        def worker():
            try:
                self.root.after(0, lambda: self._set_busy(True, "Fetching notes..."))
                data = http_get_json(API_GET, {"pinboardId": pinboard_id})
                notes = []
                for _, note in data.items():
                    content = str(note.get("content", ""))
                    user_hash = str(note.get("userHash", ""))
                    index = int(note.get("index", -1))
                    raw_timestamp = note.get("timestamp", "")
                    timestamp = self._format_timestamp(raw_timestamp)
                    notes.append(
                        {
                            "index": index,
                            "userHash": user_hash,
                            "timestamp": timestamp,
                            "content": content,
                            "flagged": self._looks_bad(content),
                        }
                    )
                notes.sort(key=lambda n: (n["userHash"], n["index"]))
                self.root.after(0, lambda: self._load_notes(notes))
            except urllib.error.HTTPError as e:
                body = e.read().decode("utf-8", errors="replace")
                self.root.after(0, lambda: messagebox.showerror("Fetch Failed", f"HTTP {e.code}\n{body}"))
                self.root.after(0, lambda: self._set_busy(False, "Fetch failed."))
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Fetch Failed", str(e)))
                self.root.after(0, lambda: self._set_busy(False, "Fetch failed."))

        threading.Thread(target=worker, daemon=True).start()

    def _load_notes(self, notes):
        self.notes = notes
        self.selected_userhash = None
        self.only_selected_user_var.set(False)
        self._rebuild_user_counts()
        self._refresh_user_list()
        self.apply_filters()
        self._set_busy(False, f"Loaded {len(self.notes)} notes from {len(self.user_counts)} user hash groups.")

    def _rebuild_user_counts(self):
        counts = {}
        for note in self.notes:
            counts[note["userHash"]] = counts.get(note["userHash"], 0) + 1
        self.user_counts = dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0])))

    def _refresh_user_list(self):
        self.user_listbox.delete(0, tk.END)
        self.user_listbox.insert(tk.END, "All users")
        for user_hash, count in self.user_counts.items():
            self.user_listbox.insert(tk.END, f"{user_hash}  ({count})")
        self.user_listbox.selection_clear(0, tk.END)
        self.user_listbox.selection_set(0)

    def on_user_selected(self):
        selection = self.user_listbox.curselection()
        if not selection:
            return
        idx = selection[0]
        if idx == 0:
            self.selected_userhash = None
        else:
            text = self.user_listbox.get(idx)
            self.selected_userhash = text.split("  (", 1)[0]
        self.apply_filters()

    def clear_user_selection(self):
        self.selected_userhash = None
        self.only_selected_user_var.set(False)
        self.user_listbox.selection_clear(0, tk.END)
        self.user_listbox.selection_set(0)
        self.apply_filters()

    def apply_filters(self):
        search = self.search_var.get().strip().lower()
        filtered = []
        for note in self.notes:
            if self.only_selected_user_var.get() and self.selected_userhash and note["userHash"] != self.selected_userhash:
                continue
            if search:
                hay = f'{note["userHash"]} {note["content"]} {note["index"]} {note["timestamp"]}'.lower()
                if search not in hay:
                    continue
            filtered.append(note)

        self.filtered_notes = filtered
        self._refresh_tree()

    def _refresh_tree(self):
        self.tree.delete(*self.tree.get_children())
        for note in self.filtered_notes:
            tags = ("flagged",) if note["flagged"] else ()
            self.tree.insert(
                "",
                "end",
                iid=str(note["index"]),
                values=(note["index"], note["userHash"], note["timestamp"], note["content"]),
                tags=tags,
            )
        self._update_status_selection()

    def _update_status_selection(self):
        selected = self.tree.selection()
        flagged = sum(1 for n in self.filtered_notes if n["flagged"])
        base = f"Showing {len(self.filtered_notes)} notes"
        if self.selected_userhash:
            base += f" for {self.selected_userhash}"
        base += f". Flagged-looking notes in current view: {flagged}."
        if selected:
            base += f" Selected: {len(selected)}."
        self.status_var.set(base)

    def delete_selected_notes(self):
        pinboard_id = self.pinboard_id_var.get().strip()
        hash_key = self.hash_key_var.get().strip()
        if not pinboard_id or not hash_key:
            messagebox.showerror("Missing Credentials", "Enter both Pinboard ID and Hash Key first.")
            return

        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("Nothing Selected", "Select one or more notes first.")
            return

        indexes = sorted(int(i) for i in selected)
        if not messagebox.askyesno(
            "Confirm Delete",
            f"Delete {len(indexes)} selected note(s)?\n\nIndexes: {', '.join(map(str, indexes))}"
        ):
            return

        self._delete_indexes(pinboard_id, hash_key, indexes)

    def delete_selected_user_notes(self):
        pinboard_id = self.pinboard_id_var.get().strip()
        hash_key = self.hash_key_var.get().strip()
        if not pinboard_id or not hash_key:
            messagebox.showerror("Missing Credentials", "Enter both Pinboard ID and Hash Key first.")
            return

        if not self.selected_userhash:
            messagebox.showinfo("No User Selected", "Pick a user hash from the list on the left first.")
            return

        indexes = [n["index"] for n in self.notes if n["userHash"] == self.selected_userhash]
        if not indexes:
            messagebox.showinfo("No Notes", "That user has no notes loaded.")
            return

        if not messagebox.askyesno(
            "Confirm Bulk Delete",
            f"Delete all {len(indexes)} notes from this user?\n\n{self.selected_userhash}"
        ):
            return

        self._delete_indexes(pinboard_id, hash_key, indexes)

    def _delete_indexes(self, pinboard_id, hash_key, indexes):
        def worker():
            deleted = 0
            failed = []
            self.root.after(0, lambda: self._set_busy(True, f"Deleting {len(indexes)} notes..."))
            for idx in indexes:
                try:
                    http_get_text(API_DELETE, {"pinboardId": pinboard_id, "hashKey": hash_key, "index": idx})
                    deleted += 1
                except urllib.error.HTTPError as e:
                    body = e.read().decode("utf-8", errors="replace")
                    failed.append((idx, f"HTTP {e.code}: {body}"))
                except Exception as e:
                    failed.append((idx, str(e)))

            def finish():
                self._set_busy(False)
                msg = f"Deleted {deleted} note(s)."
                if failed:
                    msg += "\n\nFailed:\n" + "\n".join(f"{idx}: {reason}" for idx, reason in failed[:20])
                messagebox.showinfo("Delete Finished", msg)
                self.fetch_notes()

            self.root.after(0, finish)

        threading.Thread(target=worker, daemon=True).start()

    @staticmethod
    def _format_timestamp(value):
        try:
            ts = int(str(value))
            if ts > 9999999999:
                dt = datetime.fromtimestamp(ts / 1000)
            else:
                dt = datetime.fromtimestamp(ts)
            return dt.strftime("%d/%m/%Y, %H:%M:%S")
        except Exception:
            return str(value)

    def _looks_bad(self, text):
        return (
            flagged_match(text, self.flagged_words)
            or flagged_match(text, self.flagged_url_parts)
        )


if __name__ == "__main__":
    root = tk.Tk()
    try:
        style = ttk.Style()
        if "vista" in style.theme_names():
            style.theme_use("vista")
    except Exception:
        pass
    app = PinboardModeratorApp(root)
    root.mainloop()

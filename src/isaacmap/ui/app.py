"""Tkinter Research Map for confirmed clean canonical floor pipelines."""

from __future__ import annotations

import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk

from PIL import ImageGrab, ImageTk

from isaacmap.preview import (
    SUPPORTED_FLOOR,
    SUPPORTED_FLOORS,
    PreviewGeneration,
    PreviewGenerationFailed,
    PreviewError,
    UnsupportedPreviewFloor,
    generate_preview,
)
from isaacmap.seed import InvalidSeedError, decode_seed

from .icons import IconCacheResult, ensure_official_icon_cache
from .models import PreviewMapModel, legend_labels, preview_to_dict, room_tooltip
from .renderer import MapLayout, hit_test_room, render_map


GAME_VERSION = "Repentance+ v1.9.7.17.J460"
PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_ICON_CACHE = PROJECT_ROOT / "output" / "ui_cache"

FLOOR_NAMES = (
    "Basement I",
    "Basement II",
    "Caves I",
    "Caves II",
    "Depths I",
    "Depths II",
    "Womb I",
    "Womb II",
    "Sheol",
    "Cathedral",
    "The Chest",
    "Dark Room",
)
FLOOR_OPTIONS = tuple(
    (
        f"{floor:<18}[{'SUPPORTED' if floor in SUPPORTED_FLOORS else 'UNSUPPORTED'}]",
        floor,
    )
    for floor in FLOOR_NAMES
)
FLOOR_BY_DISPLAY = dict(FLOOR_OPTIONS)
DISPLAY_BY_FLOOR = {floor: display for display, floor in FLOOR_OPTIONS}

BG = "#171513"
PANEL = "#211e1b"
PANEL_ALT = "#292520"
TEXT = "#e5d9c9"
MUTED = "#9f9589"
ACCENT = "#b89a62"
GOOD = "#80b982"
WARN = "#d0a15e"
MAP_BG = "#151311"


class ResearchPreviewApp:
    """Input → clean preview adapter → renderer, with no generator logic."""

    def __init__(
        self,
        root: tk.Tk | None = None,
        *,
        icon_cache_dir: Path | str = DEFAULT_ICON_CACHE,
    ) -> None:
        self.root = root or tk.Tk()
        self.root.title("Isaac Offline Map Generator — Research Preview")
        self.root.geometry("1100x750")
        self.root.minsize(900, 650)
        self.root.configure(bg=BG)

        self.current_preview: PreviewGeneration | None = None
        self.current_model: PreviewMapModel | None = None
        self.current_layout: MapLayout | None = None
        self._map_photo: ImageTk.PhotoImage | None = None
        self._seed_editing = False
        self._resize_job: str | None = None
        self._tooltip_room_id: int | None = None
        self.icon_cache: IconCacheResult = ensure_official_icon_cache(icon_cache_dir)

        self._configure_style()
        self._build_variables()
        self._build_window()
        self._build_tooltip()
        self._show_empty_map()
        self._on_floor_selected()

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TCombobox", fieldbackground=PANEL_ALT, background=PANEL_ALT, foreground=TEXT)
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", PANEL_ALT)],
            selectbackground=[("readonly", PANEL_ALT)],
            selectforeground=[("readonly", TEXT)],
        )
        style.configure(
            "Preview.TButton",
            background="#685638",
            foreground="#fff6e7",
            bordercolor="#89724c",
            padding=(10, 7),
        )
        style.map("Preview.TButton", background=[("active", "#806a45"), ("disabled", "#3c3730")])
        style.configure("Dark.TCheckbutton", background=PANEL, foreground=TEXT)
        style.map("Dark.TCheckbutton", background=[("active", PANEL)], foreground=[("active", TEXT)])

    def _build_variables(self) -> None:
        self.seed_var = tk.StringVar(value="B911 99AC")
        self.seed_var.trace_add("write", self._format_seed_input)
        self.difficulty_var = tk.StringVar(value="HARD")
        self.floor_display_var = tk.StringVar(value=FLOOR_OPTIONS[0][0])
        self.status_var = tk.StringVar(value="Ready")
        self.scope_warning_var = tk.StringVar(value="")
        self.details_visible = tk.BooleanVar(value=False)

    def _build_window(self) -> None:
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        header = tk.Frame(self.root, bg=PANEL, padx=18, pady=11)
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        tk.Label(
            header,
            text="Isaac Offline Map Generator — Research Preview",
            bg=PANEL,
            fg=TEXT,
            font=("Segoe UI Semibold", 16),
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            header,
            text=f"Game: {GAME_VERSION}  •  Full Layout Research Map",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, sticky="w", pady=(3, 0))

        badges = tk.Frame(header, bg=PANEL)
        badges.grid(row=0, column=1, rowspan=2, sticky="e")
        self._badge(badges, "Algorithm\nCONFIRMED_BINARY", GOOD).pack(side="left", padx=4)
        self._badge(badges, "External validation\nNOT_EXTERNALLY_VALIDATED_GAMEPLAY", WARN).pack(side="left", padx=4)

        main = tk.Frame(self.root, bg=BG, padx=12, pady=12)
        main.grid(row=1, column=0, sticky="nsew")
        main.grid_rowconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)

        left = tk.Frame(main, bg=PANEL, width=310, padx=15, pady=14)
        left.grid(row=0, column=0, sticky="nsw", padx=(0, 12))
        left.grid_propagate(False)
        self._build_controls(left)

        map_panel = tk.Frame(main, bg=PANEL, padx=10, pady=10)
        map_panel.grid(row=0, column=1, sticky="nsew")
        map_panel.grid_rowconfigure(1, weight=1)
        map_panel.grid_columnconfigure(0, weight=1)
        tk.Label(
            map_panel,
            text="MAP CANVAS  •  occupied 13×13 GridIndex bounds auto-fit",
            bg=PANEL,
            fg=MUTED,
            font=("Consolas", 9),
        ).grid(row=0, column=0, sticky="w", pady=(0, 7))
        self.map_canvas = tk.Canvas(
            map_panel,
            bg=MAP_BG,
            highlightthickness=1,
            highlightbackground="#3b3630",
            cursor="crosshair",
        )
        self.map_canvas.grid(row=1, column=0, sticky="nsew")
        self.map_canvas.bind("<Configure>", self._on_canvas_resize)
        self.map_canvas.bind("<Motion>", self._on_map_motion)
        self.map_canvas.bind("<Leave>", lambda _event: self._hide_tooltip())

        warning = tk.Label(
            map_panel,
            textvariable=self.scope_warning_var,
            bg=PANEL,
            fg=WARN,
            justify="left",
            anchor="w",
            font=("Segoe UI", 9),
        )
        warning.grid(row=2, column=0, sticky="ew", pady=(8, 0))

        footer = tk.Frame(self.root, bg=PANEL_ALT, padx=18, pady=9)
        footer.grid(row=2, column=0, sticky="ew")
        footer.grid_columnconfigure(0, weight=1)
        self.legend_label = tk.Label(
            footer,
            text=self._legend_text(),
            bg=PANEL_ALT,
            fg=TEXT,
            font=("Segoe UI", 9),
            anchor="w",
            justify="left",
            wraplength=1040,
        )
        self.legend_label.grid(row=0, column=0, sticky="ew")
        tk.Label(
            footer,
            text=(
                "Topology ✓   Boss ✓   Super Secret ✓   Shop ✓   Treasure ✓   Secret ✓     "
                "Ultra Secret ✓   Normal variants ✓"
            ),
            bg=PANEL_ALT,
            fg=MUTED,
            font=("Segoe UI", 9),
        ).grid(row=1, column=0, sticky="w", pady=(4, 0))

    def _badge(self, parent: tk.Widget, text: str, color: str) -> tk.Label:
        return tk.Label(
            parent,
            text=text,
            bg="#26231f",
            fg=color,
            justify="left",
            padx=9,
            pady=5,
            relief="solid",
            borderwidth=1,
            font=("Consolas", 8),
        )

    def _build_controls(self, parent: tk.Frame) -> None:
        parent.grid_columnconfigure(0, weight=1)
        row = 0
        tk.Label(parent, text="Seed", bg=PANEL, fg=TEXT, anchor="w", font=("Segoe UI Semibold", 10)).grid(row=row, column=0, sticky="ew")
        row += 1
        self.seed_entry = tk.Entry(
            parent,
            textvariable=self.seed_var,
            bg=PANEL_ALT,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Consolas", 14, "bold"),
        )
        self.seed_entry.grid(row=row, column=0, sticky="ew", pady=(4, 10), ipady=6)
        row += 1

        tk.Label(parent, text="Difficulty", bg=PANEL, fg=TEXT, anchor="w", font=("Segoe UI Semibold", 10)).grid(row=row, column=0, sticky="ew")
        row += 1
        difficulty = ttk.Combobox(
            parent,
            textvariable=self.difficulty_var,
            values=("NORMAL", "HARD"),
            state="readonly",
        )
        difficulty.grid(row=row, column=0, sticky="ew", pady=(4, 10))
        row += 1

        tk.Label(parent, text="Floor", bg=PANEL, fg=TEXT, anchor="w", font=("Segoe UI Semibold", 10)).grid(row=row, column=0, sticky="ew")
        row += 1
        floor_combo = ttk.Combobox(
            parent,
            textvariable=self.floor_display_var,
            values=tuple(display for display, _ in FLOOR_OPTIONS),
            state="readonly",
        )
        floor_combo.grid(row=row, column=0, sticky="ew", pady=(4, 10))
        floor_combo.bind("<<ComboboxSelected>>", lambda _event: self._on_floor_selected())
        row += 1

        buttons = tk.Frame(parent, bg=PANEL)
        buttons.grid(row=row, column=0, sticky="ew")
        buttons.grid_columnconfigure((0, 1), weight=1)
        ttk.Button(buttons, text="Generate", style="Preview.TButton", command=self.generate).grid(row=0, column=0, columnspan=2, sticky="ew")
        self.export_json_button = ttk.Button(buttons, text="Export JSON", command=self.export_json, state="disabled")
        self.export_json_button.grid(row=1, column=0, sticky="ew", padx=(0, 3), pady=(6, 0))
        self.export_png_button = ttk.Button(buttons, text="Export Map Image", command=self.export_png, state="disabled")
        self.export_png_button.grid(row=1, column=1, sticky="ew", padx=(3, 0), pady=(6, 0))
        row += 1

        self.status_label = tk.Label(
            parent,
            textvariable=self.status_var,
            bg=PANEL,
            fg=GOOD,
            justify="left",
            anchor="w",
            wraplength=280,
            font=("Segoe UI", 9),
        )
        self.status_label.grid(row=row, column=0, sticky="ew", pady=(9, 9))
        row += 1

        tk.Label(parent, text="Generation Summary", bg=PANEL, fg=ACCENT, anchor="w", font=("Segoe UI Semibold", 10)).grid(row=row, column=0, sticky="ew")
        row += 1
        self.summary_text = self._readonly_text(parent, height=11)
        self.summary_text.grid(row=row, column=0, sticky="ew", pady=(4, 7))
        row += 1

        ttk.Checkbutton(
            parent,
            text="Generation Details",
            variable=self.details_visible,
            command=self._toggle_details,
            style="Dark.TCheckbutton",
        ).grid(row=row, column=0, sticky="w")
        row += 1
        self.details_text = self._readonly_text(parent, height=9)
        self.details_text.grid(row=row, column=0, sticky="nsew", pady=(4, 0))
        self.details_text.grid_remove()

    def _readonly_text(self, parent: tk.Widget, *, height: int) -> tk.Text:
        return tk.Text(
            parent,
            height=height,
            bg="#191715",
            fg=TEXT,
            relief="flat",
            font=("Consolas", 8),
            padx=7,
            pady=6,
            wrap="word",
            state="disabled",
        )

    def _build_tooltip(self) -> None:
        self.tooltip = tk.Toplevel(self.root)
        self.tooltip.withdraw()
        self.tooltip.overrideredirect(True)
        self.tooltip.configure(bg="#806a45")
        self.tooltip_label = tk.Label(
            self.tooltip,
            bg="#24201c",
            fg=TEXT,
            justify="left",
            padx=8,
            pady=6,
            font=("Consolas", 9),
        )
        self.tooltip_label.pack(padx=1, pady=1)

    def _format_seed_input(self, *_args: object) -> None:
        if self._seed_editing:
            return
        value = self.seed_var.get()
        compact = "".join(value.split()).upper()[:8]
        formatted = compact[:4]
        if len(compact) > 4:
            formatted += " " + compact[4:]
        if formatted != value:
            self._seed_editing = True
            self.seed_var.set(formatted)
            self._seed_editing = False
            self.root.after_idle(lambda: self.seed_entry.icursor(tk.END))

    def _selected_floor(self) -> str:
        return FLOOR_BY_DISPLAY.get(self.floor_display_var.get(), self.floor_display_var.get())

    def _on_floor_selected(self) -> None:
        floor = self._selected_floor()
        spec = SUPPORTED_FLOORS.get(floor)
        if spec is None:
            self._set_status("UNSUPPORTED — generator not recovered yet", WARN)
            self.scope_warning_var.set(
                f"{floor} remains UNSUPPORTED — FAIL CLOSED. No floor parameters are approximated.\n"
                "External gameplay validation remains independent and not yet available."
            )
            return
        replay_note = ""
        if len(spec.replayed_floors) > 1:
            replay_note = (
                "Offline replay: "
                + " → ".join(
                    f"{item} {'generated' if item == floor else '✓'}"
                    for item in spec.replayed_floors
                )
                + ".\n"
            )
        self._set_status(f"SUPPORTED — confirmed accepted {floor} layout", GOOD)
        self.scope_warning_var.set(
            f"{floor} accepted layout: Ultra Secret + ordinary ROOM_DEFAULT configs.\n"
            f"{replay_note}"
            "External gameplay validation remains independent and not yet available."
        )

    def _set_status(self, message: str, color: str = GOOD) -> None:
        self.status_var.set(message)
        self.status_label.configure(fg=color)

    def generate(self) -> bool:
        seed = self.seed_var.get()
        try:
            decode_seed(seed)  # Always use the current strict checksum validator.
        except (InvalidSeedError, TypeError):
            self._set_status("Invalid Isaac seed", "#d77a6f")
            return False

        floor = self._selected_floor()
        if floor not in SUPPORTED_FLOORS:
            self._set_status("UNSUPPORTED — generator not recovered yet", WARN)
            return False

        self._set_status("Generating with clean offline pipeline…", ACCENT)
        self.root.update_idletasks()
        try:
            preview = generate_preview(seed, self.difficulty_var.get(), floor)
        except UnsupportedPreviewFloor:
            self._set_status("UNSUPPORTED — generator not recovered yet", WARN)
            return False
        except (PreviewGenerationFailed, PreviewError, OSError, ValueError) as error:
            self._set_status(f"Generation failed closed: {error}", "#d77a6f")
            return False

        self.current_preview = preview
        self.current_model = PreviewMapModel.from_preview(preview)
        self.legend_label.configure(text=self._legend_text())
        self.export_json_button.configure(state="normal")
        self.export_png_button.configure(state="normal")
        self._update_generation_text()
        self._render_current_map()
        suffix = ""
        if preview.attempt_count > 1:
            retries = preview.attempt_count - 1
            suffix = f" • {preview.attempt_count} attempts ({retries} retr{'y' if retries == 1 else 'ies'})"
        self._set_status(f"Generated {preview.generation_status}{suffix}", GOOD)
        return True

    def _update_generation_text(self) -> None:
        assert self.current_preview is not None
        preview = self.current_preview
        rooms = preview.rooms
        summary = (
            f"Seed:\n{preview.seed}\n\n"
            f"Difficulty:\n{preview.difficulty}\n\n"
            f"Floor:\n{preview.floor}\n\n"
            f"Attempts: {preview.attempt_count}\n"
            f"Final attempt: {preview.final_attempt_index}\n"
            f"Rooms: {len(rooms)}\n\n"
            f"Algorithm evidence:\n{preview.algorithm_evidence}\n\n"
            f"External validation:\n{preview.gameplay_fixture}"
        )
        self._replace_text(self.summary_text, summary)

        payload = preview_to_dict(preview)
        boss_config = payload["boss_room_config"]
        boss_config_text = (
            "none"
            if boss_config is None
            else f"stage={boss_config['stage']} mode={boss_config['mode']} resource={boss_config['resource_index']}"
        )
        trace = "\n".join(
            f"Attempt {item['attempt']}: {item['outcome']}"
            for item in payload["attempt_trace"]
        )
        replay = "\n".join(
            f"{floor}: {'generated' if floor == preview.floor else 'replayed ✓'}"
            for floor in preview.replayed_floors
        )
        details = (
            f"Start seed uint32: {preview.start_seed} (0x{preview.start_seed:08X})\n"
            f"Stage seed: {payload['stage_seed']} (0x{payload['stage_seed']:08X})\n"
            f"Attempt count: {payload['attempts']}\n"
            f"Secret GridIndex: {payload['secret_grid_index'] if payload['secret_grid_index'] is not None else 'none'}\n"
            f"Ultra Secret GridIndex: {payload['ultra_secret_grid_index'] if payload['ultra_secret_grid_index'] is not None else 'none'}\n"
            f"Level RNG final state: 0x{payload['final_level_rng_state']:08X}\n"
            f"LevelGenerator RNG final state: 0x{payload['final_level_generator_rng_state']:08X}\n"
            f"Boss ID: {payload['boss_id']}\n"
            f"Boss RoomConfig: {boss_config_text}\n"
            f"BossPool index: {payload['boss_pool_index']}\n"
            f"BossPool persistent state: 0x{payload['boss_pool_persistent_state']:08X}\n"
            f"Super Secret GridIndex: {', '.join(map(str, payload['super_secret_grid_indices']))}\n"
            f"Shop GridIndex: {payload['shop_grid_index']}\n"
            f"Treasure GridIndex: {payload['treasure_grid_index']}\n\n"
            f"Offline generation replay\n{replay}\n\n"
            f"Attempt trace\n{trace}"
        )
        self._replace_text(self.details_text, details)

    @staticmethod
    def _replace_text(widget: tk.Text, value: str) -> None:
        widget.configure(state="normal")
        widget.delete("1.0", tk.END)
        widget.insert("1.0", value)
        widget.configure(state="disabled")

    def _toggle_details(self) -> None:
        if self.details_visible.get():
            self.summary_text.configure(height=4)
            self.details_text.grid()
        else:
            self.summary_text.configure(height=11)
            self.details_text.grid_remove()

    def _show_empty_map(self) -> None:
        self.map_canvas.delete("all")
        self.map_canvas.create_text(
            380,
            230,
            text="Enter a valid Isaac seed and click Generate\n\nResearch Preview — not an Exact Full Map",
            fill=MUTED,
            justify="center",
            font=("Segoe UI", 13),
        )

    def _on_canvas_resize(self, _event: tk.Event[tk.Misc]) -> None:
        if self._resize_job is not None:
            self.root.after_cancel(self._resize_job)
        self._resize_job = self.root.after(100, self._render_current_map)

    def _render_current_map(self) -> None:
        self._resize_job = None
        if self.current_model is None:
            self._show_empty_map()
            return
        width = max(320, self.map_canvas.winfo_width())
        height = max(240, self.map_canvas.winfo_height())
        image, self.current_layout = render_map(
            self.current_model,
            width,
            height,
            icons=self.icon_cache.images,
        )
        self._map_photo = ImageTk.PhotoImage(image)
        self.map_canvas.delete("all")
        self.map_canvas.create_image(0, 0, image=self._map_photo, anchor="nw")

    def _on_map_motion(self, event: tk.Event[tk.Misc]) -> None:
        if self.current_model is None or self.current_layout is None:
            self._hide_tooltip()
            return
        room = hit_test_room(self.current_model, self.current_layout, event.x, event.y)
        if room is None:
            self._hide_tooltip()
            return
        if room.generation_index != self._tooltip_room_id:
            self._tooltip_room_id = room.generation_index
            self.tooltip_label.configure(text=room_tooltip(room))
        self.tooltip.deiconify()
        self.tooltip.update_idletasks()
        margin = 8
        offset = 14
        root_left = self.root.winfo_rootx()
        root_top = self.root.winfo_rooty()
        root_right = root_left + self.root.winfo_width()
        root_bottom = root_top + self.root.winfo_height()
        tip_width = self.tooltip.winfo_reqwidth()
        tip_height = self.tooltip.winfo_reqheight()
        x = event.x_root + offset
        y = event.y_root + offset
        if x + tip_width > root_right - margin:
            x = event.x_root - tip_width - offset
        if y + tip_height > root_bottom - margin:
            y = event.y_root - tip_height - offset
        x = max(root_left + margin, min(x, root_right - tip_width - margin))
        y = max(root_top + margin, min(y, root_bottom - tip_height - margin))
        self.tooltip.geometry(f"+{x}+{y}")

    def _hide_tooltip(self) -> None:
        self._tooltip_room_id = None
        self.tooltip.withdraw()

    def _legend_text(self) -> str:
        labels = legend_labels(self.current_model)
        return "Legend:   " + "     ".join(labels)

    def _output_stem(self) -> str:
        assert self.current_preview is not None
        compact_seed = self.current_preview.seed.replace(" ", "")
        floor = SUPPORTED_FLOORS[self.current_preview.floor]
        return f"{compact_seed}_{self.current_preview.difficulty}_{floor.output_slug}"

    def export_json(self) -> Path | None:
        if self.current_preview is None:
            return None
        output = PROJECT_ROOT / "output" / "maps" / f"{self._output_stem()}.json"
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(
            json.dumps(preview_to_dict(self.current_preview), indent=2),
            encoding="utf-8",
        )
        self._set_status(f"Exported JSON: {output}", GOOD)
        return output

    def export_png(self) -> Path | None:
        if self.current_model is None:
            return None
        output = PROJECT_ROOT / "output" / "maps" / f"{self._output_stem()}.png"
        output.parent.mkdir(parents=True, exist_ok=True)
        image, _layout = render_map(
            self.current_model,
            1400,
            900,
            icons=self.icon_cache.images,
        )
        image.convert("RGBA").save(output)
        self._set_status(f"Exported map image: {output}", GOOD)
        return output

    def run(self) -> None:
        self.root.mainloop()


def capture_smoke_screenshots(
    normal_seed: str = "B911 99AC",
    hard_seed: str | None = None,
    floor: str = SUPPORTED_FLOOR,
    output_dir: Path | str = PROJECT_ROOT / "output" / "screenshots",
) -> tuple[Path, Path]:
    """Run the real Tk UI for NORMAL/HARD and capture its window."""

    root = tk.Tk()
    app = ResearchPreviewApp(root)
    root.geometry("1100x750+0+0")
    root.attributes("-topmost", True)
    root.update_idletasks()
    root.update()
    target = Path(output_dir)
    target.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    spec = SUPPORTED_FLOORS.get(floor)
    if spec is None:
        root.destroy()
        raise UnsupportedPreviewFloor(f"{floor!r}: UNSUPPORTED — generator not recovered yet")
    seeds = {"NORMAL": normal_seed, "HARD": hard_seed or normal_seed}
    for difficulty, filename in (
        ("NORMAL", f"preview_{spec.output_slug}_normal.png"),
        ("HARD", f"preview_{spec.output_slug}_hard.png"),
    ):
        app.seed_var.set(seeds[difficulty])
        app.difficulty_var.set(difficulty)
        app.floor_display_var.set(DISPLAY_BY_FLOOR[floor])
        app._on_floor_selected()
        if not app.generate():
            root.destroy()
            raise RuntimeError(f"UI smoke generation failed for {difficulty}: {app.status_var.get()}")
        app.details_visible.set(True)
        app._toggle_details()
        root.update_idletasks()
        root.update()
        output = target / filename
        ImageGrab.grab(window=root.winfo_id()).save(output)
        outputs.append(output)
    root.destroy()
    return outputs[0], outputs[1]


def main() -> int:
    ResearchPreviewApp().run()
    return 0

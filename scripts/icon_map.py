"""
Maps this repo's icon names to the Bearded Icons source files they come from.

`icons/BeardedIcons` is not hand-drawn: every SVG in it is a byte-for-byte copy
of a file in `vendor/bearded-icons/src/shared/icons/`, renamed from upstream's
VS Code naming to the freedesktop icon names KDE actually looks up. This table
IS that rename -- the one piece of information the port adds -- and
`gen_icons.py` replays it to rebuild the icon theme from the submodule.

Keys are the installed icon name (without `.svg`); values are the upstream
basename (also without `.svg`). Several keys deliberately share one value:
freedesktop has multiple mimetype names for the same kind of file (e.g.
`text-x-python` and `text-x-python3`) and every archive format reuses upstream's
single `zip` icon.

To add a new file type, add a row here and re-run `scripts/gen_icons.py` -- you
do not need to touch the SVGs. Upstream ships ~390 icons against the ~91 mapped
below, so there is plenty left to wire up; see AGENTS.md.
"""

# Where the source SVGs live inside the vendor/bearded-icons submodule.
UPSTREAM_ICON_DIR = "src/shared/icons"

# freedesktop mimetype icon name -> upstream basename
MIMETYPES = {
    "application-gzip":             "zip",
    "application-javascript":       "js",
    "application-json":             "json",
    "application-octet-stream":     "file",
    "application-pdf":              "pdf",
    "application-sql":              "sql",
    "application-toml":             "toml",
    "application-typescript":       "typescript",
    "application-vnd.sqlite3":      "sqlite",
    "application-x-7z-compressed":  "zip",
    "application-x-compressed-tar": "zip",
    "application-x-executable":     "binary",
    "application-x-font-ttf":       "fontttf",
    "application-x-javascript":     "js",
    "application-x-php":            "php",
    "application-x-rar":            "zip",
    "application-x-ruby":           "ruby",
    "application-x-shellscript":    "shell",
    "application-x-sqlite3":        "sqlite",
    "application-x-tar":            "zip",
    "application-x-yaml":           "yaml",
    "application-xhtml+xml":        "html",
    "application-xml":              "xml",
    "application-yaml":             "yaml",
    "application-zip":              "zip",
    "audio-flac":                   "audio",
    "audio-mpeg":                   "audiomp3",
    "audio-x-generic":              "audio",
    "audio-x-wav":                  "audiowav",
    "font-otf":                     "fontotf",
    "font-ttf":                     "fontttf",
    "image-bmp":                    "image",
    "image-gif":                    "imagegif",
    "image-jpeg":                   "imagejpg",
    "image-png":                    "imagepng",
    "image-svg+xml":                "svg",
    "image-webp":                   "imagewebp",
    "image-x-generic":              "image",
    "image-x-icon":                 "imageico",
    "inode-directory":              "folder",
    "text-csharp":                  "csharp",
    "text-css":                     "css",
    "text-csv":                     "csv",
    "text-dockerfile":              "docker",
    "text-html":                    "html",
    "text-javascript":              "js",
    "text-markdown":                "markdown",
    "text-plain":                   "file",
    "text-rust":                    "rust",
    "text-x-c++hdr":                "hpp",
    "text-x-c++src":                "cpp",
    "text-x-chdr":                  "cheader",
    "text-x-cmake":                 "cmake",
    "text-x-csharp":                "csharp",
    "text-x-csrc":                  "c",
    "text-x-dockerfile":            "docker",
    "text-x-generic":               "file",
    "text-x-go":                    "go",
    "text-x-ini":                   "conf",
    "text-x-java-source":           "java",
    "text-x-java":                  "java",
    "text-x-javascript":            "js",
    "text-x-kotlin":                "kotlin",
    "text-x-log":                   "log",
    "text-x-lua":                   "lua",
    "text-x-makefile":              "makefile",
    "text-x-markdown":              "markdown",
    "text-x-patch":                 "diff",
    "text-x-php":                   "php",
    "text-x-properties":            "properties",
    "text-x-python":                "python",
    "text-x-python3":               "python",
    "text-x-r":                     "r",
    "text-x-ruby":                  "ruby",
    "text-x-rust":                  "rust",
    "text-x-sass":                  "sass",
    "text-x-scss":                  "scss",
    "text-x-shellscript":           "shell",
    "text-x-sql":                   "sql",
    "text-x-tex":                   "latex",
    "text-x-typescript":            "typescript",
    "text-x-yaml":                  "yaml",
    "text-xml":                     "xml",
    "unknown":                      "file",
    "video-mp4":                    "mp4",
    "video-webm":                   "video",
    "video-x-generic":              "video",
    "video-x-matroska":             "video",
}

# freedesktop places icon name -> upstream basename
PLACES = {
    "folder-open": "folder_open",
    "folder-root": "root_folder",
    "folder":      "folder",
}

# Installed subdirectory -> mapping, mirroring index.theme's Directories= list.
CONTEXTS = {
    "mimetypes": MIMETYPES,
    "places": PLACES,
}

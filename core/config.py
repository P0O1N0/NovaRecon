USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/120.0",
]

COMMON_ACTION_NAMES = [
    "getComments", "getPosts", "getUsers", "getArticles", "getData",
    "fetchComments", "fetchPosts", "loadMore", "get_content", "list",
    "get_comments", "get_posts", "get_products", "search", "query"
]

COMMON_DIRS = [
    "admin", "login", "wp-admin", "administrator", "panel", "dashboard",
    "api", "ajax", "graphql", "rest", "uploads", "images", "assets",
    "js", "css", "fonts", "includes", "backup", "db", "sql", "config",
    "logs", "tmp", "temp", "private", "secret"
]

SENSITIVE_FILES = [
    ".git/HEAD", ".env", ".env.backup", ".env.local", ".DS_Store",
    "robots.txt", "sitemap.xml", "crossdomain.xml", "phpinfo.php",
    "server-status", "server-info", "console", "actuator", "health"
]

CLASS_PATTERNS = {
    "user": ["user", "member", "account", "profile", "login", "register", "signup", "customer"],
    "content": ["comment", "post", "article", "news", "story", "blog", "content", "feed", "review"],
    "admin": ["admin", "administrator", "panel", "dashboard", "manage", "control", "cms", "edit", "delete"],
    "api": ["api", "ajax", "rest", "graphql", "endpoint", "v1", "v2", "json"],
}
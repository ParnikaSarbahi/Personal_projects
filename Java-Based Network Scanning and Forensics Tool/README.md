# JScanSec 🔒

**JScanSec** is a beginner-friendly cybersecurity toolkit built in Java. It is designed to help users perform basic digital forensic and security checks without the need for external dependencies or a database.

---

## 📦 Features

- ✅ **Log Analyzer**: Parses system log files to detect suspicious entries.
- 📸 **Metadata Extractor**: Extracts EXIF metadata from image files.
- 🌐 **Port Scanner**: Scans a given IP address for open TCP ports.
- 🔍 **Web Vulnerability Scanner**: Checks websites for:
  - Exposed sensitive files (e.g., `.env`, `wp-config.php`)
  - Leaky HTTP headers (`X-Powered-By`, `Server`)
  - Risky HTTP methods (`PUT`, `DELETE`, etc.)

---

## 🛠️ Requirements

- Java 17 or later
- No external libraries or frameworks needed

---

## 🚀 How to Run

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/JScanSec.git
   cd JScanSec

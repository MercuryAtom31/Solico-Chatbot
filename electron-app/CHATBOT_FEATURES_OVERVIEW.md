# 🤖 Smart Sales Chatbot – Feature Overview & Design Rationale

## ✅ **Key Features**

### 🧠 1. Dual Intelligence: Local & Online Modes
- **Offline Mode (Default)**  
  - Uses a locally running AI model (LLaMA 2 via Ollama) to generate answers even when there's no internet connection.  
  - Responses are streamed live, word-by-word, for a fluid chat experience.

- **Online Mode (Toggle-enabled)**  
  - When enabled, the chatbot fetches the latest information from the internet using **Google Search or Google News** (via SerpAPI).  
  - It augments the local AI’s knowledge with **real-time data**, providing citations with sources.

---

### 🌐 2. Online/Offline Mode Toggle
- The user can switch between online and offline modes **directly from the interface** via a simple checkbox.  
- Gives full control over how the chatbot operates:  
  - Enable **online mode** when up-to-date info is needed.  
  - Stay in **offline mode** for secure or disconnected environments.

---

### 🔎 3. Smart Web Search Integration (SerpAPI)
- Automatically determines if a user’s query needs **live info** (e.g., recent news, prices, trends).  
- Performs a **Google Search** or **Google News Search** and returns:  
  - Title, source, snippet, and date (if available).  
  - Inline citations like [1], [2] in the response.

---

### ⚙️ 4. Query Analyzer
- Detects:  
  - Whether a query needs **current/recent information**.  
  - Whether the query is **related to the printing industry** (customized for client context).  
- Helps decide when to search online vs. use offline answers.

---

### 💾 5. Caching Search Results
- Saves previous search queries for **up to 7 days** to reduce API usage and improve speed.  
- Prevents repeated searches for the same question.

---

### 📉 6. API Usage Tracking & Rate Limiting
- Limits the number of online searches per month (default: **100 searches**).  
- Automatically resets the counter every new month.  
- If the limit is exceeded, it gracefully falls back to offline mode.

---

### 🖥️ 7. Electron-Based Desktop UI
- Built with **Electron**, the chatbot has a native app feel.  
- Key UI features:  
  - **Chat sidebar** for navigating, renaming, and deleting past conversations.  
  - **Responsive design** for different screen sizes.  
  - **Stylish message bubbles** with assistant/user distinction.  
  - **Status badge** for connection mode (Online or Offline).

---

### 💻 8. Cross-Platform Compatibility
- Fully functional on **Windows (ThinkPad)** and **macOS (MacBook)**.  
- Automatically starts Ollama in the background and works independently of cloud services.  
- Electron UI + Flask backend bundled with PyInstaller for each OS.

---

### 🔒 9. Privacy-First, Local Execution
- All AI processing happens **on the user’s machine**.  
- No cloud dependencies unless online mode is explicitly enabled.  
- Ideal for **privacy-conscious users** in sales and business environments.

---

## 💡 Rationale Behind Feature Choices

| Design Choice                     | Reason                                                                 |
|----------------------------------|------------------------------------------------------------------------|
| **Dual Mode (Online + Offline)** | Ensures the chatbot works without internet, while still offering real-time search when needed. |
| **User-Controlled Toggle**       | Gives users flexibility to choose the mode that fits their needs — no guessing, no errors. |
| **Local AI Model (Ollama)**      | Faster responses, full privacy, and no reliance on external APIs.     |
| **SerpAPI Search Integration**   | Provides up-to-date info, ideal for fast-moving industries like sales, print, and logistics. |
| **Query Analyzer**               | Reduces unnecessary API calls and ensures smart usage of online search when it adds value. |
| **Caching & Rate Limiting**      | Saves costs and prevents excessive API use. Great for budget-conscious deployments. |
| **Electron UI**                  | Native feel, easy deployment, and a consistent experience across Mac and Windows. |
| **Cross-platform Support**       | Designed for sales teams using both MacBooks and ThinkPad laptops.    |
| **Security & Portability**       | Runs locally with sensitive settings stored in `.env`, keeping control in the hands of your client. |

---

## 📦 Deployment Highlights
- The chatbot comes packaged with:  
  - **All dependencies pre-bundled** (including Ollama, LLM model).  
  - A **one-click startup** for both platforms.  
  - **No installation required** for end users.

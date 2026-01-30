## 📖 Introduction
This is an experimental project inspired by my own desire for a more abstract way to search for appropriate sounds and patches on my keyboard at short notice. 
Think of it as a **powerful search engine for your synth sounds**

The idea is to be able to use NLP (Natural Language Processing) to enter a prompt and return a list of appropriate sounds that fit that description and send the result via MIDI program change back to my device.

> **Example:** Enter the prompt *"Soft airy pluck"* $\rightarrow$ Return a list of MIDI banks/programs that best fit that description.

## ⚡ Why though?
...because it's a fun project.

In all seriousness though, I have been in many situations where I have had **zero time to prepare** and needed to find more creative patches outside of just my regular "bread and butter" sounds.

Although this is a small application, I believe the concept is quite profound, using more abstract language to obtain a musical result which may have applications outside of just sound retrieval, perhaps extending into the realm of sound generation.

---

## ✨ Key Features
* **🤖 AI Auto-Indexer:** Automatically sends MIDI Program Changes to your synth, records a short audio clip of every patch, and builds a sonic database.
* **🔍 Semantic Search:** Search by "vibe" or "timbre" (e.g., *"Dark dystopian pad"*) rather than just patch names. Use **LAION-CLAP** audio embedding technology.
* **🎹 Instant Recall:** Double-click a search result to send the Bank/Program Change message immediately to your hardware.
* **🧠 Local & Private:** All audio analysis happens locally on your machine. No cloud uploads.

---


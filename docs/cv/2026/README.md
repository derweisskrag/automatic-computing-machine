---
header-includes:
  - \usepackage{graphicx}
  - \usepackage{enumitem}
  - \usepackage{caption}
  - \usepackage{tabularx}
  - \usepackage{booktabs}
  - \usepackage{needspace}
  - \usepackage{fontawesome5}
  - \usepackage[hidelinks]{hyperref}
  - \hypersetup{colorlinks=true, linkcolor=blue, urlcolor=blue}
---
### CV 2026

# Sergei Ivanov

## Summary

Performance-driven systems engineer specializing in Rust and low-level backend architecture. Deeply experienced in writing memory-conscious software, handling explicit allocations, and diagnosing runtime memory constraints (e.g., addressing **wasm32** heap limits). Proficient in reading and translating low-level C paradigms (such as Linux kernel **llist.c** patterns) into safe, high-performance implementations. Proven track record of architecting native language bindings via **Maturin/PyO3**, managing containerized environments (**Docker**), and automating cross-platform releases to PyPI using **GitHub Actions**. Passionate about open-source architecture, decoupled systems, and maintaining a lightweight, high-productivity development workflow.


## Education

University of Tartu (Narva College) — Tallinn/Narva, Estonia Bachelor of Science (BSc) in Information Technology Systems Development | 09.2023 – 06.2026

* Professional Higher Education Programme (Regular Studies, Full-time). Diploma No. EA 005831.


## Certifications
- **Foundational C# with Microsoft**  
  *Issued by FreeCodeCamp, November 14, 2024*  
  [Verification Link](https://www.freecodecamp.org/certification/fccbe4b8c5a-8a27-493c-a983-a09fb9b9632d/foundational-c-sharp-with-microsoft)



## Experience

What do I offer you and why should you hire me? I bring a unique combination of skills and experience that align perfectly with your needs:

* Production-Ready Concurrency: Engineered a multi-service Discord bot suite using Rust (Serenity/Tokio), implementing safe, asynchronous multi-threaded event loops capable of handling high-throughput satellite development workflows without data races.

* Robust Backend Architecture: Designed and deployed custom Axum backend integrations for the Jira API, offering real-time, bi-directional task tracking and automated issue state management that removes manual overhead.

* Type-Safe Data Ingestion: Built a high-reliability ETL pipeline using Reqwest and PostgreSQL to ingest mission data from Google Sheets and Apps Script webhooks, ensuring strict type-safety and memory optimization during data translation.

* Optimized Containerization: Containerized the ecosystem using Docker multi-stage builds, offering the team highly optimized image sizes and isolated, reproducible deployments for mission-critical operations.

Here is the summary of my experience in a structured format:

```{.render-experience data="experience"}
```

## Skills

### Languages & Core Runtimes

* Systems & Backend: Rust (Axum, Tokio, SQLx, Serenity), C (Reading/Analysis), Zig, Python (PyO3/Maturin)

* Scripting & Automation: Lua, JavaScript / TypeScript, Deno

### Systems Architecture & DevOps

* Containerization & CI/CD: Docker, Podman, GitHub Actions, Multi-stage builds, Automated packaging (PyPI/Crates.io)

* Data & Networking: PostgreSQL, SQLite, REST APIs, gRPC, WASM32 compilation & memory optimization, TLS 1.3

* Linux & Analysis: Linux systems environment, Network analysis (Wireshark), Posix-compliant environments

### Testing & Tooling

* Quality Assurance: Unit testing, Integration testing, API black-box testing

* Environment: NeoVim, Git, Jira, GitHub Projects

## Projects

### 1. dsa_kuuking — High-Performance Python-Rust Hybrid Framework & Thesis

#### Situation

Python-native data structures frequently suffer from significant overhead due to dynamic memory allocations, a problem amplified when trying to analyze massive computational complexity at scale.

#### Task 

Architect a hybrid data structures library that delegates heavy algorithmic execution to a native backend, optimizing memory footprints and execution speed.

#### Action

* Developed a 1000+ LOC hybrid framework using Rust (PyO3/Maturin) to compile high-performance data structures directly into native Python extensions.

* Analyzed and translated raw low-level C memory paradigms (including the Linux kernel list.c and Red-Black tree architectures) into safe, fast Rust implementations.

* Diagnosed and resolved critical runtime constraints during a wasm32-unknown-unknown target compilation, identifying exactly where the browser heap hit a MemoryError and shifting to native memory bindings via Maturin.

* Automated the complete compilation and release lifecycle via GitHub Actions, handling cross-platform binary wheels for automatic deployment to PyPI.

#### Result

Successfully deployed the library to PyPI, proving that moving heavy object models into an optimized Rust runtime guarantees near-native execution speed and highly predictable memory utilization.


### 2. High-Performance API & Microservices Exploration (2025)
- **Situation**: Identified the need to build a high-performance, secure system to handle microservices communication.
- **Task**: To develop a proof-of-concept API using Rust and Deno, exploring different communication protocols and secure data transfer.
- **Action**: 
  - Designed and built a REST API using **Deno** and a high-performance backend using **Axum (Rust)**, exchanging data via Server Actions.
  - Explored and implemented **gRPC with TLS 1.3** to secure communication between a Rust client and a Rust API.
  - Successfully debugged and resolved incompatibility issues between Deno and the gRPC/TLS setup by isolating the problem and proving functionality with a Rust client.
  - Managed sensitive files (`.key`, `.pem`) with `.gitignore` to maintain security.
- **Result**: Gained practical experience with advanced protocols (**gRPC, TLS**) and high-performance languages (**Rust**), proving the ability to solve complex system-level problems and maintain secure configurations.


## Contributions and Projects

- **Game Performance Analysis**: Used **OpenHardwareMonitor** and **Intel VTune** to analyze a game's performance, identifying and reporting on caching and memory usage issues to the developers.
- **Open Source Contribution**: Identified and reported incompatibility issues with **NumPy, Pandas, and SciPy**, collaborating on GitHub to monitor the resolution.
- **Volunteer Work**: Google Sheets and Apps Script development for a local non-profit, automating data collection and reporting processes.


## Languages

- **Russian**: Native
- **English**: B2 (speaking, writing) 
- **Estonian**: C1 (speaking, writing)

> *Certified through formal examination*

import asyncio
from playwright.async_api import async_playwright

html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sergei Ivanov - CV 2026</title>
    <style>
        @page {
            size: A4;
            margin: 18mm 16mm;
            @bottom-right {
                content: counter(page) " / " counter(pages);
                font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
                font-size: 8pt;
                color: #718096;
            }
        }
        
        *, *::before, *::after {
            box-sizing: border-box;
        }

        body {
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.5;
            color: #2d3748;
            margin: 0;
            padding: 0;
            background-color: #ffffff;
        }

        /* Header Accent Banner Style */
        .header-container {
            margin-bottom: 20px;
            border-bottom: 2px solid #2b6cb0;
            padding-bottom: 12px;
        }

        h1 {
            font-size: 24pt;
            color: #1a365d;
            margin: 0 0 4px 0;
            font-weight: 700;
            letter-spacing: -0.5px;
        }

        .subtitle {
            font-size: 11pt;
            color: #4a5568;
            font-weight: 500;
            margin: 0 0 6px 0;
        }

        .contact-info {
            font-size: 9pt;
            color: #718096;
        }

        h2 {
            font-size: 13pt;
            color: #2b6cb0;
            margin: 20px 0 10px 0;
            padding-bottom: 4px;
            border-bottom: 1px solid #e2e8f0;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            page-break-after: avoid;
        }

        h3, h4 {
            font-size: 11pt;
            color: #2d3748;
            margin: 12px 0 6px 0;
            page-break-after: avoid;
        }

        p {
            margin: 0 0 8px 0;
            text-align: justify;
        }

        ul {
            margin: 0 0 10px 0;
            padding-left: 20px;
        }

        li {
            margin-bottom: 4px;
        }

        strong {
            color: #1a365d;
        }

        .highlight-box {
            background-color: #f7fafc;
            border-left: 4px solid #2b6cb0;
            padding: 10px 14px;
            margin-bottom: 15px;
        }

        .highlight-box p {
            margin-bottom: 6px;
            font-style: italic;
        }
        
        .highlight-box p:last-child {
            margin-bottom: 0;
        }

        .project-block, .experience-block {
            margin-bottom: 16px;
            page-break-inside: avoid;
        }

        .project-title, .exp-title {
            font-weight: bold;
            font-size: 11pt;
            color: #1a365d;
            margin-bottom: 4px;
        }

        .meta-line {
            font-size: 9pt;
            color: #4a5568;
            font-style: italic;
            margin-bottom: 6px;
        }

        .skills-grid {
            display: block;
        }

        .skills-section {
            margin-bottom: 10px;
        }

        .skills-section strong {
            display: inline-block;
            width: 180px;
            color: #2b6cb0;
        }

        .lang-list {
            list-style-type: none;
            padding-left: 0;
        }

        .lang-list li {
            margin-bottom: 4px;
        }

        a {
            color: #2b6cb0;
            text-decoration: none;
        }
    </style>
</head>
<body>

    <div class="header-container">
        <h1>Sergei Ivanov</h1>
        <div class="subtitle">Systems Software Engineer | Rust Specialist</div>
        <div class="contact-info">
            Estonia &bull; <a href="https://github.com/derweisskrag/automatic-computic-machine">GitHub Profile</a>
            &bull; <a href="https://www.linkedin.com/in/sergei-ivanov-50a652280">LinkedIn Profile</a>
        </div>
    </div>

    <h2>Summary</h2>
    <p>
        Performance-driven systems engineer specializing in <strong>Rust</strong> and low-level backend architecture. Deeply experienced in writing memory-conscious software, handling explicit allocations, and diagnosing runtime memory constraints (e.g., addressing <strong>wasm32</strong> heap limits). Proficient in reading and translating low-level C paradigms (such as Linux kernel <strong>llist.c</strong> patterns) into safe, high-performance implementations. Proven track record of architecting native language bindings via <strong>Maturin/PyO3</strong>, managing containerized environments (<strong>Docker</strong>), and automating cross-platform releases to PyPI using <strong>GitHub Actions</strong>. Passionate about open-source architecture, decoupled systems, and maintaining a lightweight, high-productivity development workflow.
    </p>

    <h2>Education</h2>
    <div class="project-block">
        <div class="project-title">University of Tartu (Narva College) <span style="font-weight: normal; color: #4a5568;">— Tallinn/Narva, Estonia</span></div>
        <div class="meta-line">Bachelor of Science (BSc) in Information Technology Systems Development | 09.2023 – 06.2026</div>
        <ul>
            <li>Professional Higher Education Programme (Regular Studies, Full-time). Diploma No. EA 005831.</li>
        </ul>
    </div>

    <h2>Certifications</h2>
    <ul>
        <li><strong>Foundational C# with Microsoft</strong> — Issued by FreeCodeCamp (November 14, 2024) | <a href="https://www.freecodecamp.org/certification/fccbe4b8c5a-8a27-493c-a983-a09fb9b9632d/foundational-c-sharp-with-microsoft">Verification Link</a></li>
    </ul>

    <h2>Experience</h2>
    <div class="highlight-box">
        <p><strong>What do I offer you and why should you hire me?</strong> I bring a unique combination of skills and experience that align perfectly with your needs:</p>
        <ul>
            <li><strong>Production-Ready Concurrency:</strong> Engineered a multi-service Discord bot suite using Rust (Serenity/Tokio), implementing safe, asynchronous multi-threaded event loops capable of handling high-throughput satellite development workflows without data races.</li>
            <li><strong>Robust Backend Architecture:</strong> Designed and deployed custom Axum backend integrations for the Jira API, offering real-time, bi-directional task tracking and automated issue state management that removes manual overhead.</li>
            <li><strong>Type-Safe Data Ingestion:</strong> Built a high-reliability ETL pipeline using Reqwest and PostgreSQL to ingest mission data from Google Sheets and Apps Script webhooks, ensuring strict type-safety and memory optimization during data translation.</li>
            <li><strong>Optimized Containerization:</strong> Containerized the ecosystem using Docker multi-stage builds, offering the team highly optimized image sizes and isolated, reproducible deployments for mission-critical operations.</li>
        </ul>
    </div>

    <div class="experience-block">
        <div class="exp-title">Tudengite Satelliit <span style="font-weight: normal; color: #4a5568;">— Software Developer</span></div>
        <div class="meta-line">10.2025 – Present &bull; Tech Stack: Rust, Tokio, Axum, PostgreSQL, Docker, Jira API, Google Apps Script</div>
    </div>

    <h2>Skills</h2>
    <div class="skills-grid">
        <div class="skills-section">
            <strong>Systems & Backend:</strong> Rust (Axum, Tokio, SQLx, Serenity), C (Reading/Analysis), Zig, Python (PyO3/Maturin)
        </div>
        <div class="skills-section">
            <strong>Scripting & Automation:</strong> Lua, JavaScript / TypeScript, Deno
        </div>
        <div class="skills-section">
            <strong>Containerization & CI/CD:</strong> Docker, Podman, GitHub Actions, Multi-stage builds, Automated packaging (PyPI/Crates.io)
        </div>
        <div class="skills-section">
            <strong>Data & Networking:</strong> PostgreSQL, SQLite, REST APIs, gRPC, WASM32 compilation & memory optimization, TLS 1.3
        </div>
        <div class="skills-section">
            <strong>Linux & Analysis:</strong> Linux systems environment, Network analysis (Wireshark), Posix-compliant environments
        </div>
        <div class="skills-section">
            <strong>Testing & Tooling:</strong> Unit & Integration testing, API black-box testing, NeoVim, Git, Jira, GitHub Projects
        </div>
    </div>

    <h2>Projects</h2>
    
    <div class="project-block">
        <div class="project-title">1. dsa_kuuking — High-Performance Python-Rust Hybrid Framework & Thesis</div>
        <p style="margin-top: 4px; margin-bottom: 2px;"><strong>Situation:</strong> Python-native data structures frequently suffer from significant overhead due to dynamic memory allocations, a problem amplified when trying to analyze massive computational complexity at scale.</p>
        <p style="margin-bottom: 2px;"><strong>Task:</strong> Architect a hybrid data structures library that delegates heavy algorithmic execution to a native backend, optimizing memory footprints and execution speed.</p>
        <p style="margin-bottom: 2px;"><strong>Action:</strong></p>
        <ul>
            <li>Developed a 1000+ LOC hybrid framework using Rust (PyO3/Maturin) to compile high-performance data structures directly into native Python extensions.</li>
            <li>Analyzed and translated raw low-level C memory paradigms (including the Linux kernel list.c and Red-Black tree architectures) into safe, fast Rust implementations.</li>
            <li>Diagnosed and resolved critical runtime constraints during a wasm32-unknown-unknown target compilation, identifying exactly where the browser heap hit a MemoryError and shifting to native memory bindings via Maturin.</li>
            <li>Automated the complete compilation and release lifecycle via GitHub Actions, handling cross-platform binary wheels for automatic deployment to PyPI.</li>
        </ul>
        <p><strong>Result:</strong> Successfully deployed the library to PyPI, proving that moving heavy object models into an optimized Rust runtime guarantees near-native execution speed and highly predictable memory utilization.</p>
    </div>

    <div class="project-block">
        <div class="project-title">2. Secure Microservices & High-Performance API Exploration</div>
        <p style="margin-top: 4px; margin-bottom: 2px;"><strong>Situation:</strong> Identified the need to build a high-performance, secure system to handle microservices communication.</p>
        <p style="margin-bottom: 2px;"><strong>Task:</strong> To develop a proof-of-concept API using Rust and Deno, exploring different communication protocols and secure data transfer.</p>
        <p style="margin-bottom: 2px;"><strong>Action:</strong></p>
        <ul>
            <li>Designed and built a REST API using Deno and a high-performance backend using Axum (Rust), exchanging data via Server Actions.</li>
            <li>Explored and implemented gRPC with TLS 1.3 to secure communication between a Rust client and a Rust API.</li>
            <li>Successfully debugged and resolved incompatibility issues between Deno and the gRPC/TLS setup by isolating the problem and proving functionality with a Rust client.</li>
            <li>Managed sensitive files (.key, .pem) with .gitignore to maintain configuration security.</li>
        </ul>
        <p><strong>Result:</strong> Gained practical experience with advanced protocols (gRPC, TLS) and high-performance languages (Rust), proving the ability to solve complex system-level problems and maintain secure configurations.</p>
    </div>

    <h2>Contributions & Independent Work</h2>
    <ul>
        <li><strong>Game Performance Analysis:</strong> Used OpenHardwareMonitor and Intel VTune to analyze a game's performance, identifying and reporting on caching and memory usage issues to the developers.</li>
        <li><strong>Open Source Contribution:</strong> Identified and reported incompatibility issues with NumPy, Pandas, and SciPy, collaborating on GitHub to monitor the resolution.</li>
        <li><strong>Volunteer Work:</strong> Google Sheets and Apps Script development for a local non-profit, automating data collection and reporting processes.</li>
    </ul>

    <h2>Languages</h2>
    <ul class="lang-list">
        <li><strong>Russian:</strong> Native</li>
        <li><strong>Estonian:</strong> C1 (Professional Academic & Clinical Proficiency — Certified)</li>
        <li><strong>English:</strong> B2 (Full Professional Working Proficiency)</li>
    </ul>

</body>
</html>
"""
async def generate_pdf():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.set_content(html_content)
        # Emulate print media styles (@page margins)
        await page.pdf(path="Sergei_Ivanov_Rust_CV.pdf", format="A4", prefer_css_page_size=True)
        await browser.close()
        print("File compiled successfully via Playwright Engine!")

asyncio.run(generate_pdf())
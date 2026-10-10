from pathlib import Path
import fitz


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "Ibrahim_Khalil_Akil_Professional_Portfolio.pdf"
PAGE_W, PAGE_H = fitz.paper_size("a4")


def rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[i:i + 2], 16) / 255 for i in (0, 2, 4))


NAVY = rgb("0F172A")
NAVY_2 = rgb("172033")
INDIGO = rgb("4F46E5")
PURPLE = rgb("7C3AED")
PINK = rgb("DB2777")
GREEN = rgb("059669")
BLUE = rgb("2563EB")
WHITE = rgb("FFFFFF")
PAPER = rgb("F8FAFC")
CARD = rgb("FFFFFF")
INK = rgb("172033")
SLATE = rgb("475569")
MUTED = rgb("64748B")
BORDER = rgb("CBD5E1")
SOFT_INDIGO = rgb("EEF2FF")
SOFT_BLUE = rgb("EFF6FF")
SOFT_PINK = rgb("FDF2F8")
SOFT_GREEN = rgb("ECFDF5")


def text_width(text, size, font="helv"):
    return fitz.get_text_length(text, fontname=font, fontsize=size)


def wrap_text(text, width, size, font="helv"):
    lines = []
    for paragraph in text.split("\n"):
        words = paragraph.split()
        if not words:
            lines.append("")
            continue
        current = words[0]
        for word in words[1:]:
            candidate = current + " " + word
            if text_width(candidate, size, font) <= width:
                current = candidate
            else:
                lines.append(current)
                current = word
        lines.append(current)
    return lines


def draw_text(page, x, y, width, text, size=10, font="helv", color=INK,
              line_height=None, max_lines=None):
    line_height = line_height or size * 1.35
    lines = wrap_text(text, width, size, font)
    if max_lines and len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while last and text_width(last + "...", size, font) > width:
            last = last[:-1]
        lines[-1] = last.rstrip() + "..."
    cursor = y
    for line in lines:
        page.insert_text((x, cursor), line, fontsize=size, fontname=font, color=color)
        cursor += line_height
    return cursor


def card_rect(page, rect, accent=INDIGO, fill=CARD):
    page.draw_rect(rect, color=BORDER, fill=fill, width=0.7)
    page.draw_rect(fitz.Rect(rect.x0, rect.y0, rect.x0 + 5, rect.y1), color=accent, fill=accent)


def pill(page, x, y, text, fill=SOFT_INDIGO, color=INDIGO, size=7.8):
    width = text_width(text, size, "hebo") + 14
    rect = fitz.Rect(x, y, x + width, y + 18)
    page.draw_rect(rect, color=fill, fill=fill)
    page.insert_text((x + 7, y + 12.5), text, fontsize=size, fontname="hebo", color=color)
    return width


def draw_tags(page, x, y, max_width, tags, fill=SOFT_INDIGO, color=INDIGO):
    cursor_x = x
    cursor_y = y
    for tag in tags:
        width = text_width(tag, 7.5, "hebo") + 14
        if cursor_x + width > x + max_width:
            cursor_x = x
            cursor_y += 23
        pill(page, cursor_x, cursor_y, tag, fill=fill, color=color, size=7.5)
        cursor_x += width + 6
    return cursor_y + 18


def add_page_base(doc, section, page_number):
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, color=PAPER, fill=PAPER)
    page.draw_rect(fitz.Rect(0, 0, PAGE_W, 7), color=INDIGO, fill=INDIGO)
    page.insert_text((42, 29), "IBRAHIM KHALIL AKIL", fontsize=7.5,
                     fontname="hebo", color=INDIGO)
    page.insert_text((PAGE_W - 42 - text_width(section.upper(), 7.5, "hebo"), 29),
                     section.upper(), fontsize=7.5, fontname="hebo", color=MUTED)
    page.draw_line((42, PAGE_H - 35), (PAGE_W - 42, PAGE_H - 35), color=BORDER, width=0.6)
    page.insert_text((42, PAGE_H - 19), "Professional Portfolio | 2026",
                     fontsize=7.2, fontname="helv", color=MUTED)
    number = f"{page_number:02d}"
    page.insert_text((PAGE_W - 42 - text_width(number, 7.2, "hebo"), PAGE_H - 19),
                     number, fontsize=7.2, fontname="hebo", color=INDIGO)
    return page


def section_title(page, title, subtitle=None):
    page.insert_text((42, 65), title, fontsize=23, fontname="hebo", color=NAVY)
    page.draw_rect(fitz.Rect(42, 75, 104, 79), color=INDIGO, fill=INDIGO)
    if subtitle:
        draw_text(page, 42, 99, PAGE_W - 84, subtitle, size=9.5, color=SLATE,
                  line_height=13.5, max_lines=2)


def draw_cover(doc):
    page = doc.new_page(width=PAGE_W, height=PAGE_H)
    page.draw_rect(page.rect, color=NAVY, fill=NAVY)
    page.draw_rect(fitz.Rect(0, 0, 14, PAGE_H), color=INDIGO, fill=INDIGO)
    page.draw_rect(fitz.Rect(PAGE_W - 140, 0, PAGE_W, 210), color=PURPLE, fill=PURPLE,
                   fill_opacity=0.18, stroke_opacity=0)
    page.draw_rect(fitz.Rect(PAGE_W - 235, PAGE_H - 175, PAGE_W, PAGE_H),
                   color=PINK, fill=PINK, fill_opacity=0.12, stroke_opacity=0)

    page.insert_text((54, 66), "PROFESSIONAL PORTFOLIO", fontsize=9,
                     fontname="hebo", color=rgb("A5B4FC"))
    page.draw_rect(fitz.Rect(54, 79, 132, 83), color=INDIGO, fill=INDIGO)

    draw_text(page, 54, 154, 475, "IBRAHIM\nKHALIL AKIL", size=38,
              font="hebo", color=WHITE, line_height=43)
    draw_text(page, 57, 260, 480,
              "Full Stack Developer | Ethical Hacker | Red Team Practitioner",
              size=13.5, font="hebo", color=rgb("C7D2FE"), line_height=18)

    page.draw_rect(fitz.Rect(54, 305, 58, 387), color=PINK, fill=PINK)
    draw_text(page, 72, 326, 455,
              "I build IoT and connected systems, deliver production software, and assess web, API, cloud-connected, and infrastructure attack surfaces. My work combines secure engineering, full-stack architecture, offensive security, and remediation-focused reporting.",
              size=11.2, color=rgb("E2E8F0"), line_height=16.5, max_lines=5)

    stats = [
        ("7", "Documented security assessments"),
        ("10+", "Major software projects"),
        ("5+", "Years in technology"),
    ]
    start_x = 54
    gap = 12
    width = (PAGE_W - 108 - 2 * gap) / 3
    for index, (number, label) in enumerate(stats):
        x = start_x + index * (width + gap)
        rect = fitz.Rect(x, 428, x + width, 520)
        page.draw_rect(rect, color=rgb("334155"), fill=NAVY_2, width=0.8)
        page.insert_text((x + 15, 466), number, fontsize=24, fontname="hebo", color=WHITE)
        draw_text(page, x + 15, 491, width - 30, label, size=8.7,
                  color=rgb("CBD5E1"), line_height=11.5, max_lines=2)

    page.insert_text((54, 572), "CORE FOCUS", fontsize=8.5, fontname="hebo", color=rgb("A5B4FC"))
    draw_tags(page, 54, 589, PAGE_W - 108, [
        "IoT & Connected Systems", "Web & API Security", "Red Team Assessments",
        "Full-Stack Architecture", "Authentication & Authorization", "AI Integration"
    ], fill=rgb("26304A"), color=rgb("C7D2FE"))

    page.draw_line((54, 701), (PAGE_W - 54, 701), color=rgb("334155"), width=0.8)
    draw_text(page, 54, 727, 500,
              "Montreal, Quebec, Canada  |  brhimakil@gmail.com  |  github.com/brahimakil",
              size=8.6, color=rgb("CBD5E1"), line_height=12)
    page.insert_text((54, 787), "SELECTED WORK, ASSESSMENTS, AND TECHNICAL CAPABILITIES",
                     fontsize=7.4, fontname="hebo", color=rgb("64748B"))
    page.insert_text((PAGE_W - 70, 787), "01", fontsize=7.4, fontname="hebo", color=rgb("A5B4FC"))


def role_card(page, y, height, title, period, company, summary, bullets, accent=INDIGO):
    rect = fitz.Rect(42, y, PAGE_W - 42, y + height)
    card_rect(page, rect, accent=accent)
    page.insert_text((58, y + 25), title, fontsize=13, fontname="hebo", color=NAVY)
    period_width = text_width(period, 8.2, "hebo") + 16
    pill(page, PAGE_W - 58 - period_width, y + 11, period,
         fill=SOFT_INDIGO, color=INDIGO, size=8.2)
    page.insert_text((58, y + 45), company, fontsize=8.5, fontname="hebo", color=accent)
    cursor = draw_text(page, 58, y + 65, PAGE_W - 116, summary, size=9.1,
                       color=SLATE, line_height=12.5, max_lines=2)
    cursor += 5
    for bullet in bullets:
        page.insert_text((61, cursor), "-", fontsize=9, fontname="hebo", color=accent)
        cursor = draw_text(page, 73, cursor, PAGE_W - 137, bullet, size=8.5,
                           color=INK, line_height=11.5, max_lines=2)
        cursor += 2


def draw_experience(doc):
    page = add_page_base(doc, "Experience", 2)
    section_title(page, "Professional Experience",
                  "Secure engineering, offensive security, and end-to-end product delivery.")

    role_card(page, 125, 165,
              "Ethical Hacker & Red Team Practitioner", "2026 - Present",
              "Independent Security Assessments | Confidential Engagements",
              "Security testing across web applications, APIs, cloud-connected systems, and exposed infrastructure.",
              [
                  "Tested authentication flows, multi-tenant authorization, REST and GraphQL APIs, JWT sessions, and file-handling workflows.",
                  "Documented high-impact findings and produced evidence registers, severity ratings, negative tests, and remediation guidance.",
              ], accent=PINK)

    role_card(page, 305, 145,
              "Full Stack Developer - ChiBox", "2026",
              "Brainkets | Product Development",
              "Worked with Brainkets as a developer of ChiBox, contributing directly to the product's implementation and delivery.",
              [
                  "Developed ChiBox as part of the Brainkets team and helped turn product requirements into a working digital platform.",
                  "Contributed across architecture, feature implementation, integration, production delivery, and team collaboration.",
              ], accent=PURPLE)

    role_card(page, 465, 150,
              "Freelance Full Stack Developer", "Early 2025 - Present",
              "Self-Employed | Remote",
              "Architecting and delivering complete solutions from discovery and budgeting through deployment and optimization.",
              [
                  "Led requirements analysis, technical specification, architecture, implementation, and client communication.",
                  "Built and deployed secure applications with scalable APIs, real-time features, payments, media, and modern CI/CD.",
              ], accent=INDIGO)

    role_card(page, 630, 130,
              "Junior Mobile & Web Developer", "2023 - Early 2025",
              "Analytica Company | Full-Time",
              "Delivered 5+ production websites while building a strong foundation in modern web and mobile engineering.",
              [
                  "Developed production-ready web experiences with clean architecture and responsive interfaces.",
              ], accent=GREEN)


SECURITY_ENGAGEMENTS = [
    {
        "name": "BrainSpace ERP",
        "type": "Web & API",
        "description": "Multi-tenant ERP/SaaS assessment covering tenant isolation, authentication boundaries, file handling, and exposed services.",
        "outcome": "Confirmed full-system compromise",
        "critical": True,
        "findings": ["Auth Bypass", "IDOR / BOLA", "Path Traversal", "Upload", "Pre-Auth RCE", "Data Exposure", "Misconfiguration"],
    },
    {
        "name": "VioletPro / FoodServiceLB",
        "type": "Multi-System",
        "description": "Assessment of connected business applications, administrative surfaces, and sensitive data-handling workflows.",
        "outcome": "Confirmed full-system compromise",
        "critical": True,
        "findings": ["SQLi", "Upload RCE", "Broken Authorization", "Stored XSS", "Weak Crypto", "Backup Exposure"],
    },
    {
        "name": "Omega Software",
        "type": "API Security",
        "description": "Multi-tenant ERP/API assessment focused on tenant boundaries, injection resistance, error handling, and abuse controls.",
        "outcome": "Confirmed high-impact cross-tenant access",
        "critical": False,
        "findings": ["Time-Based SQLi", "Cross-Tenant Access", "Path Disclosure", "Rate Limiting", "CAPTCHA Weakness"],
    },
    {
        "name": "ChiBox / Brainkets",
        "type": "Web & Mobile",
        "description": "Marketplace and mobile-app assessment covering registration, upload, session, exposed-service, and source controls.",
        "outcome": "Confirmed full-system compromise",
        "critical": True,
        "findings": ["Upload RCE", "Privileged Registration", "Secret Exposure", "Service Exposure", "Session Weakness"],
    },
    {
        "name": "Lebanese International University",
        "type": "Education",
        "description": "University portal and API testing across public surfaces, sessions, input handling, and application error behavior.",
        "outcome": "Confirmed injection and sensitive-data exposure",
        "critical": False,
        "findings": ["SQLi", "Reflected XSS", "Error Disclosure", "Data Exposure", "CSRF", "Cookie Security"],
    },
    {
        "name": "Phenix Solutions Plus",
        "type": "Authorization",
        "description": "ERP and e-commerce API assessment of account-resource isolation, registration workflows, and exposed internals.",
        "outcome": "Confirmed cross-account resource access",
        "critical": False,
        "findings": ["IDOR / BOLA", "Path Disclosure", "Config Exposure", "Source Exposure", "Workflow Weakness"],
    },
    {
        "name": "Islamic University of Lebanon",
        "type": "Reconnaissance",
        "description": "Public attack-surface mapping with clear separation between confirmed exposure and verified negative test results.",
        "outcome": "Confirmed public data exposure and attack-surface findings",
        "critical": False,
        "findings": ["Directory Exposure", "Data Exposure", "Error Leakage", "Negative Testing"],
    },
]


def security_card(page, y, item):
    rect = fitz.Rect(42, y, PAGE_W - 42, y + 205)
    accent = PINK if item["critical"] else INDIGO
    card_rect(page, rect, accent=accent)
    page.insert_text((58, y + 26), item["name"], fontsize=14, fontname="hebo", color=NAVY)
    badge_width = text_width(item["type"], 7.7, "hebo") + 14
    pill(page, PAGE_W - 58 - badge_width, y + 12, item["type"],
         fill=SOFT_INDIGO, color=INDIGO, size=7.7)
    draw_text(page, 58, y + 50, PAGE_W - 116, item["description"],
              size=8.8, color=SLATE, line_height=12, max_lines=3)

    outcome_fill = SOFT_PINK if item["critical"] else SOFT_BLUE
    outcome_color = PINK if item["critical"] else BLUE
    outcome_rect = fitz.Rect(58, y + 92, PAGE_W - 58, y + 124)
    page.draw_rect(outcome_rect, color=outcome_fill, fill=outcome_fill)
    page.insert_text((69, y + 105), "OUTCOME", fontsize=6.8, fontname="hebo", color=outcome_color)
    draw_text(page, 69, y + 118, PAGE_W - 138, item["outcome"], size=8.7,
              font="hebo", color=INK, line_height=11, max_lines=1)

    page.insert_text((58, y + 148), "HIGH-LEVEL FINDING CLASSES", fontsize=6.8,
                     fontname="hebo", color=MUTED)
    draw_tags(page, 58, y + 157, PAGE_W - 116, item["findings"],
              fill=SOFT_INDIGO, color=INDIGO)


def draw_security_pages(doc):
    page = add_page_base(doc, "Security Assessments", 3)
    section_title(page, "Security Assessments 01",
                  "Named targets with high-level finding classes only. No endpoints, payloads, credentials, personal data, or reproduction steps.")
    for y, item in zip((125, 347, 569), SECURITY_ENGAGEMENTS[:3]):
        security_card(page, y, item)

    page = add_page_base(doc, "Security Assessments", 4)
    section_title(page, "Security Assessments 02",
                  "Evidence-led assessment outcomes across marketplace, education, and ERP environments.")
    for y, item in zip((125, 347, 569), SECURITY_ENGAGEMENTS[3:6]):
        security_card(page, y, item)

    page = add_page_base(doc, "Security Methodology", 5)
    section_title(page, "Security Assessments 03",
                  "Attack-surface mapping, confirmed findings, verified negative tests, and remediation-focused reporting.")
    security_card(page, 125, SECURITY_ENGAGEMENTS[6])

    left = fitz.Rect(42, 354, 287, 558)
    right = fitz.Rect(305, 354, PAGE_W - 42, 558)
    card_rect(page, left, accent=INDIGO)
    card_rect(page, right, accent=PURPLE)
    page.insert_text((58, 382), "Assessment Methodology", fontsize=13, fontname="hebo", color=NAVY)
    methodology = [
        "Scope and attack-surface mapping",
        "DNS and certificate-transparency research",
        "Subdomain, URL, API, and service enumeration",
        "Authentication and authorization testing",
        "Source and artifact review",
        "Manual validation and negative testing",
    ]
    cursor = 409
    for item in methodology:
        page.insert_text((60, cursor), "-", fontsize=9, fontname="hebo", color=INDIGO)
        cursor = draw_text(page, 72, cursor, 195, item, size=8.4, color=INK,
                           line_height=11.2, max_lines=2) + 3

    page.insert_text((321, 382), "Reporting Standard", fontsize=13, fontname="hebo", color=NAVY)
    reporting = [
        "Executive and technical summaries",
        "Evidence registers and severity ratings",
        "Attack-chain and impact analysis",
        "Verified negative-test documentation",
        "Prioritized remediation guidance",
        "Clear separation of fact and hypothesis",
    ]
    cursor = 409
    for item in reporting:
        page.insert_text((323, cursor), "-", fontsize=9, fontname="hebo", color=PURPLE)
        cursor = draw_text(page, 335, cursor, 195, item, size=8.4, color=INK,
                           line_height=11.2, max_lines=2) + 3

    tools = fitz.Rect(42, 580, PAGE_W - 42, 752)
    card_rect(page, tools, accent=GREEN, fill=SOFT_GREEN)
    page.insert_text((58, 610), "Selected Security Tooling", fontsize=13,
                     fontname="hebo", color=NAVY)
    draw_text(page, 58, 633, PAGE_W - 116,
              "Nmap, Nuclei, SQLmap, HTTPx, Subfinder, Gobuster, Masscan, MassDNS, gau, curl, dig, OpenSSL, netcat, apktool, Shodan, CertSpotter, crt.sh, and Wayback.",
              size=9, color=SLATE, line_height=13, max_lines=4)
    page.insert_text((58, 702), "TECHNOLOGY COVERAGE", fontsize=6.8, fontname="hebo", color=GREEN)
    draw_tags(page, 58, 713, PAGE_W - 116,
              ["PHP / Laravel", "Node.js", "React", "Vue", "Next.js", "Angular",
               "MySQL", "PostgreSQL", "AWS / S3", "Cloudflare / R2"],
              fill=WHITE, color=GREEN)


PROJECTS = [
    {
        "name": "IoT Solutions & Connected Systems",
        "status": "Main Focus",
        "primary": True,
        "description": "Primary portfolio focus connecting device data, secure APIs, real-time processing, automation-ready services, and monitoring interfaces.",
        "features": ["Device integration", "Real-time telemetry", "Cloud workflows", "Monitoring dashboards"],
        "stack": ["IoT", "Real-time Data", "Cloud APIs", "Node.js", "React"],
    },
    {
        "name": "Respike - Trading Learning Platform",
        "status": "In Production",
        "description": "A multi-panel learning platform with payments, wallet management, real-time updates, and optimized video delivery for 150+ active users.",
        "features": ["USDT / TRC20 payments", "Bunny.net video", "Wallet systems", "Mobile app"],
        "stack": ["Next.js", "React", "NestJS", "MongoDB", "Firebase", "Blockchain"],
    },
    {
        "name": "Internship Management System",
        "status": "Delivered",
        "description": "A three-panel environment for administrators, mentors, and students with real-time chat, AI support, task tracking, and analytics.",
        "features": ["Role-based access", "Real-time chat", "AI assistant", "Progress tracking"],
        "stack": ["React", "TypeScript", "Express.js", "MongoDB", "Socket.io"],
    },
    {
        "name": "School Management System",
        "status": "Delivered",
        "description": "An education platform for administrators, teachers, and students with classes, assignments, messaging, and AI-powered insights.",
        "features": ["Multi-role portals", "Course management", "Assignments", "Messaging"],
        "stack": ["Next.js", "TypeScript", "NestJS", "MongoDB"],
    },
    {
        "name": "Routee - Taxi Management Platform",
        "status": "Live",
        "description": "A real-time taxi management and booking system deployed to iOS and Android with 20+ active drivers in Venezuela.",
        "features": ["GPS tracking", "Driver management", "Payments", "Route optimization"],
        "stack": ["React Native", "TypeScript", "Firebase", "Google Maps API"],
    },
    {
        "name": "Football Coaching Platform",
        "status": "Delivered",
        "description": "A responsive multi-role coaching platform with training video, coach management, performance tracking, and messaging.",
        "features": ["Admin and user panels", "Training media", "Performance tracking", "Messaging"],
        "stack": ["React", "Node.js", "MongoDB"],
    },
]


def project_card(page, y, item):
    rect = fitz.Rect(42, y, PAGE_W - 42, y + 205)
    accent = PINK if item.get("primary") else INDIGO
    card_rect(page, rect, accent=accent)
    draw_text(page, 58, y + 27, 355, item["name"], size=13.2,
              font="hebo", color=NAVY, line_height=16, max_lines=2)
    badge_width = text_width(item["status"], 7.6, "hebo") + 14
    badge_fill = SOFT_PINK if item.get("primary") else SOFT_GREEN
    badge_color = PINK if item.get("primary") else GREEN
    pill(page, PAGE_W - 58 - badge_width, y + 12, item["status"],
         fill=badge_fill, color=badge_color, size=7.6)
    draw_text(page, 58, y + 65, PAGE_W - 116, item["description"], size=8.8,
              color=SLATE, line_height=12.2, max_lines=3)
    page.insert_text((58, y + 112), "CAPABILITIES", fontsize=6.8, fontname="hebo", color=MUTED)
    draw_tags(page, 58, y + 122, PAGE_W - 116, item["features"],
              fill=SOFT_BLUE, color=BLUE)
    page.insert_text((58, y + 162), "TECHNOLOGY", fontsize=6.8, fontname="hebo", color=MUTED)
    draw_tags(page, 58, y + 172, PAGE_W - 116, item["stack"],
              fill=SOFT_INDIGO, color=INDIGO)


def draw_project_pages(doc):
    page = add_page_base(doc, "Software Portfolio", 6)
    section_title(page, "Software Portfolio 01",
                  "IoT and connected systems lead a portfolio spanning education, finance, real-time communication, payments, and media.")
    for y, item in zip((125, 347, 569), PROJECTS[:3]):
        project_card(page, y, item)

    page = add_page_base(doc, "Software Portfolio", 7)
    section_title(page, "Software Portfolio 02",
                  "Mobile operations, coaching experiences, and additional production-ready client work.")
    for y, item in zip((125, 347, 569), PROJECTS[3:]):
        project_card(page, y, item)


SKILL_GROUPS = [
    ("Offensive Security", "Web penetration testing, API security, red team assessments, REST, GraphQL, JWT, OAuth, SAML, and multi-tenant authorization."),
    ("Recon & Tooling", "Nmap, Nuclei, SQLmap, HTTPx, Subfinder, Gobuster, Masscan, Shodan, certificate transparency, and passive DNS."),
    ("Security Reporting", "Executive summaries, evidence registers, severity classification, attack-chain analysis, remediation, and negative tests."),
    ("Frontend", "React, Next.js, TypeScript, React Native, CSS/SCSS, responsive design, Redux, and Zustand."),
    ("Backend", "NestJS, Express.js, Node.js, REST APIs, real-time systems, authentication, authorization, and Socket.io."),
    ("Data & Realtime", "MongoDB, Firebase, Firestore, PostgreSQL, real-time synchronization, and data modeling."),
    ("Cloud & Delivery", "Vercel, Render, Railway, Docker, Git/GitHub, CI/CD, Bunny.net, and Google Maps API."),
    ("Architecture & Business", "End-to-end solutions, project architecture, security-first design, requirements analysis, budgeting, and client relations."),
]


def skill_card(page, x, y, width, title, text, accent):
    rect = fitz.Rect(x, y, x + width, y + 105)
    card_rect(page, rect, accent=accent)
    page.insert_text((x + 16, y + 25), title, fontsize=10.5, fontname="hebo", color=NAVY)
    draw_text(page, x + 16, y + 48, width - 32, text, size=7.9,
              color=SLATE, line_height=10.8, max_lines=5)


def add_link_text(page, x, y, text, uri, width=None):
    page.insert_text((x, y), text, fontsize=8.4, fontname="hebo", color=INDIGO)
    width = width or text_width(text, 8.4, "hebo")
    page.insert_link({"kind": fitz.LINK_URI, "from": fitz.Rect(x, y - 10, x + width, y + 3), "uri": uri})


def draw_skills_contact(doc):
    page = add_page_base(doc, "Skills & Contact", 8)
    section_title(page, "Skills & Contact",
                  "A blended engineering and security toolkit for building, testing, and improving modern digital products.")

    width = (PAGE_W - 102) / 2
    accents = [PINK, INDIGO, PURPLE, BLUE, INDIGO, GREEN, BLUE, PURPLE]
    for index, ((title, text), accent) in enumerate(zip(SKILL_GROUPS, accents)):
        col = index % 2
        row = index // 2
        x = 42 + col * (width + 18)
        y = 125 + row * 119
        skill_card(page, x, y, width, title, text, accent)

    contact = fitz.Rect(42, 615, PAGE_W - 42, 771)
    page.draw_rect(contact, color=NAVY, fill=NAVY)
    page.draw_rect(fitz.Rect(42, 615, 48, 771), color=INDIGO, fill=INDIGO)
    page.insert_text((62, 644), "LET'S BUILD OR SECURE SOMETHING VALUABLE", fontsize=8,
                     fontname="hebo", color=rgb("A5B4FC"))
    page.insert_text((62, 670), "Available for full-stack engineering, application security, and authorized red team opportunities.",
                     fontsize=9.2, fontname="helv", color=WHITE)
    page.insert_text((62, 697), "Computer Science Degree - Islamic University in Lebanon",
                     fontsize=8.4, fontname="hebo", color=rgb("CBD5E1"))
    page.insert_text((62, 717), "Montreal, Quebec, Canada", fontsize=8.4,
                     fontname="hebo", color=rgb("CBD5E1"))
    add_link_text(page, 62, 741, "brhimakil@gmail.com", "mailto:brhimakil@gmail.com")
    add_link_text(page, 220, 741, "+1 514 451 5554", "https://wa.me/15144515554")
    add_link_text(page, 354, 741, "github.com/brahimakil", "https://github.com/brahimakil")
    add_link_text(page, 62, 763, "linkedin.com/in/ibrahim-akil-329b8b308",
                  "https://www.linkedin.com/in/ibrahim-akil-329b8b308/")


def build_pdf():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT.exists():
        OUTPUT.unlink()

    doc = fitz.open()
    draw_cover(doc)
    draw_experience(doc)
    draw_security_pages(doc)
    draw_project_pages(doc)
    draw_skills_contact(doc)
    doc.set_metadata({
        "title": "Ibrahim Khalil Akil - Professional Portfolio",
        "author": "Ibrahim Khalil Akil",
        "subject": "Full Stack Development, Ethical Hacking, and Red Team Portfolio",
        "keywords": "full stack developer, ethical hacker, red team, web security, API security, portfolio",
        "creator": "Ibrahim Khalil Akil Portfolio",
    })
    doc.save(OUTPUT, garbage=4, deflate=True, clean=True)
    doc.close()

    check = fitz.open(OUTPUT)
    assert check.page_count == 8, f"Expected 8 pages, got {check.page_count}"
    extracted = "\n".join(page.get_text() for page in check)
    required = [
        "BrainSpace ERP", "VioletPro / FoodServiceLB", "Omega Software",
        "ChiBox / Brainkets", "Lebanese International University",
        "Phenix Solutions Plus", "Islamic University of Lebanon",
        "Full Stack Developer - ChiBox", "Brainkets | Product Development",
        "IoT Solutions & Connected Systems", "Respike - Trading Learning Platform", "Skills & Contact"
    ]
    forbidden = [
        "topup", "MTV Lebanon", "HAMIT", "Ayoub Computers",
        "Namou Properties", "Learny Labs", "Hikvision"
    ]
    for value in required:
        assert value in extracted, f"Missing required PDF text: {value}"
    for value in forbidden:
        assert value.lower() not in extracted.lower(), f"Forbidden PDF text found: {value}"
    check.close()
    print(OUTPUT)


if __name__ == "__main__":
    build_pdf()

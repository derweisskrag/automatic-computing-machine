local M = {}

-- Experience Table
-- For: 2026
M.experience = {
  {
    company = "Tudengite Satelliit",
    role = "Software Developer",
    period = {start = "2025-10", finish = "Present"},
    -- Added more tech to match your new bullets
    tech = {"Rust", "Tokio", "Axum", "PostgreSQL", "Docker", "Jira API"},
    bullets = {
      "Engineered a multi-service Discord bot suite using Rust (Serenity/Tokio) to automate satellite development workflows.",
      "Developed custom integrations for the Jira API via Axum, enabling real-time task tracking directly from Discord.",
      "Built a ETL (Extract, Transform, Load) pipeline using Reqwest and PostgreSQL to bridge Google Sheets mission data with internal databases.",
      "Containerized the entire ecosystem using Docker, ensuring reproducible deployments for mission-critical operations."
    }
  }
}

-- Education table
-- 
M.education = {
  seconday = {
    start = "09.2007",
    ending = "06.2016",
    location = "Narva-Jõesuu",
    school = "School nr. 5",
    status = "Completed"
  },

  upper_secondary = {
    start = "09.2016",
    ending = "06.2019",
    location = "Narva",
    school = "Upper-Secondary School nr. 1",
    status = "Completed"
  },

  tertiary = {
    start = "09.2019",
    ending = "05.2021",
    location = "Tallinn",
    school = "TalTech",
    status = "Uncompleted"
  },

  bachelor = {
    start = "09.2023",
    ending = "06.2026",
    location = "Narva",
    school = "Narva College",
    status = "Completed"
  }
}

return M
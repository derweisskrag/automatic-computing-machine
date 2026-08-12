package.path = package.path .. ";./?.lua" 
local utils = require('utils')
local data = dofile("data.lua")
local diagrams = dofile("diagrams.lua")

function Header(el)
  -- If it's a Level 2 header (Experience, Education, Projects), 
  -- ensure it starts on a new page if we are near the bottom.
  if el.level == 2 then
    return { pandoc.RawBlock("latex", "\\needspace{5\\baselineskip}"), el }
  end
end

function CodeBlock(el)
    local data_key = el.attributes['data']

    if el.classes:includes("render-diagram") then
        local selected = diagrams[data_key]
        if selected then
            return pandoc.RawBlock('latex', utils.render_figure(selected))
        end

    elseif el.classes:includes("render-education") then
        local selected = data[data_key]
        if selected then
            return pandoc.RawBlock('latex', utils.render_cv_education(selected))
        end

    elseif el.classes:includes("render-experience") then
        local selected = data[data_key]
        if selected then
            return pandoc.RawBlock('latex', utils.render_cv_experience(selected))
        end
    end
end
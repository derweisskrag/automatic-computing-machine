package.path = package.path .. ";./?.lua"
local utils = require('utils')
local data = dofile("data.lua")
local diagrams = dofile("diagrams.lua")

function Header(el)
  -- Level 1: Always clear page (New Chapters get their own start)
  if el.level == 1 then
    return { pandoc.RawBlock("latex", "\\clearpage"), el }
  end

  -- Level 2, 3, etc: Let LaTeX handle the flow naturally.
  -- This prevents 1.1, 1.2, or 2.3.1 from jumping to new pages unnecessarily.
  return el
end

function CodeBlock(el)
  if el.classes:includes("render-table") then
    -- [Existing table logic here]
    local data_key = el.attributes['data']
    local selected_data = data[data_key]
    if selected_data then
      local result_latex = utils.render_table(selected_data)
      return pandoc.RawBlock('latex', result_latex)
    end

  elseif el.classes:includes("render-diagram") then
    local data_key = el.attributes['data']
    local selected_diagram = diagrams[data_key]
    
    if selected_diagram then
      -- 1. Use pandoc.read with 'markdown' format so it sees the [@]
      -- 2. Use pandoc.write to convert it to LaTeX specifically
      local doc = pandoc.read(selected_diagram.caption, 'markdown')
      local processed_caption = pandoc.write(doc, 'latex')
      
      -- Remove the trailing newline pandoc.write adds
      processed_caption = processed_caption:gsub("%s+$", "")
      
      selected_diagram.caption = processed_caption
      local result_latex = utils.render_figure(selected_diagram)
      return pandoc.RawBlock('latex', result_latex)
    end
  end
end
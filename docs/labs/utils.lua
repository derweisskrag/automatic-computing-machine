local M = {}

function M.render_table(data_object)
    local caption = data_object.caption or "Data Table"
    local rows = data_object.rows
    local columns = data_object.headers -- Use explicit headers if provided

    -- Fallback: Extract and sort if no headers defined
    if not columns then
        columns = {}
        for key, _ in pairs(rows[1]) do
            table.insert(columns, key)
        end
        table.sort(columns)
    end

    local latex = "\\begin{table}[H]\n\\centering\n\\caption{" .. caption .. "}\n"
    latex = latex .. "\\begin{tabular}{|" .. string.rep("l|", #columns) .. "}\n\\hline\n"

    -- Header row
    for i, col in ipairs(columns) do
        -- If using explicit headers, we might want to capitalize them
        latex = latex .. "\\textbf{" .. col:gsub("_", " "):sub(1,1):upper() .. col:sub(2) .. "}"
        if i < #columns then latex = latex .. " & " end
    end
    latex = latex .. " \\\\ \\hline\n"

    -- Data rows
    for _, row in ipairs(rows) do
        for i, col in ipairs(columns) do
            -- Handle potential nil values and ensure string conversion
            local val = tostring(row[col] or row[col:lower()] or "")
            latex = latex .. val
            if i < #columns then latex = latex .. " & " end
        end
        latex = latex .. " \\\\ \\hline\n"
    end

    latex = latex .. "\\end{tabular}\n\\end{table}"
    return latex
end

-- function M.render_table(data_object)
--     local caption = data_object.caption or "Data Table"
--     local rows = data_object.rows
--     local first = rows[1]

--     -- Extract column names dynamically
--     local columns = {}
--     for key, _ in pairs(first) do
--         table.insert(columns, key)
--     end

--     -- Sort columns for consistent order (optional)
--     table.sort(columns)

--     -- Build LaTeX
--     local latex = "\\begin{table}[h]\n\\caption{" .. caption .. "}\n"

--     -- Build column spec: one 'c' per column
--     latex = latex .. "\\begin{tabular}{|" .. string.rep("c|", #columns) .. "}\n\\hline\n"

--     -- Header row
--     for i, col in ipairs(columns) do
--         latex = latex .. "\\textbf{" .. col:gsub("_", "\\_") .. "}"
--         if i < #columns then
--             latex = latex .. " & "
--         end
--     end
--     latex = latex .. " \\\\ \\hline\n"

--     -- Data rows
--     for _, row in ipairs(rows) do
--         for i, col in ipairs(columns) do
--             latex = latex .. tostring(row[col] or "")
--             if i < #columns then
--                 latex = latex .. " & "
--             end
--         end
--         latex = latex .. " \\\\ \\hline\n"
--     end

--     latex = latex .. "\\end{tabular}\n\\end{table}"
--     return latex
-- end




-- function M.render_table(data_object)
--     local caption = data_object.caption or "Data Structure Metrics"
--     local rows_data = data_object.rows
    
--     -- 1. Start Table and Put CAPTION ON TOP (per p. 14 of guide)
--     local latex = "\\begin{table}[h]\n\\caption{" .. caption .. "}\n"
--     latex = latex .. "\\begin{tabular}{|l|c|c|c|}\n\\hline\n"
    
--     local first = rows_data[1]
--     if first.time then
--         latex = latex .. "\\textbf{Name} & \\textbf{Time} & \\textbf{Space} \\\\ \\hline\n"
--         for _, item in ipairs(rows_data) do
--             latex = latex .. string.format("%s & %s & %s \\\\ \\hline\n", 
--                 item.name, item.time, item.space)
--         end
--     else
--         latex = latex .. "\\textbf{Name} & \\textbf{Access} & \\textbf{Search} & \\textbf{Notes} \\\\ \\hline\n"
--         for _, item in ipairs(rows_data) do
--             latex = latex .. string.format("%s & %s & %s & %s \\\\ \\hline\n", 
--                 item.name, item.access, item.search, item.notes)
--         end
--     end
    
--     latex = latex .. "\\end{tabular}\n\\end{table}"
--     return latex
-- end

function M.render_figure(diagram_obj)
    local path = diagram_obj.path
    local caption_text = diagram_obj.caption 
    
    -- Figure remains centered, but caption will be left-aligned via YAML setting
    local latex = "\\begin{figure}[ht]\n\\centering\n"
    latex = latex .. "\\includegraphics[width=0.8\\textwidth]{" .. path .. "}\n"
    latex = latex .. "\\caption{" .. caption_text .. "}\n"
    latex = latex .. "\\end{figure}"
    
    return latex
end

return M
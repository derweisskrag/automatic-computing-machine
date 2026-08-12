local M = {}

-- Render Education as a Clean Table
function M.render_cv_education(edu_data)
    local latex = "\\noindent\\begin{tabularx}{\\textwidth}{@{}l l r r@{}}\n"
    latex = latex .. "\\textbf{Institution} & \\textbf{Degree} & \\textbf{Period} & \\textbf{Status} \\\\ \\midrule\n"
    
    local order = {"bachelor", "tertiary", "upper_secondary", "seconday"}
    for _, key in ipairs(order) do
        local edu = edu_data[key]
        if edu then
            -- Note: We use \\\\ to end the row
            latex = latex .. string.format("%s & %s & %s -- %s & %s \\\\\n", 
                edu.school, key:gsub("_", " "):upper(), edu.start, edu.ending, edu.status)
        end
    end
    latex = latex .. "\\end{tabularx}\n\\vspace{10pt}\n"
    return latex
end

-- Render Experience as a Table with Embedded List
function M.render_cv_experience(exp_list)
    local latex = ""
    for _, exp in ipairs(exp_list) do
        latex = latex .. "\\noindent\\begin{tabularx}{\\textwidth}{@{}X >{\\raggedleft\\arraybackslash}p{4cm}@{}}\n"
        latex = latex .. "\\textbf{" .. exp.company .. "} & \\small " .. exp.period.start .. " -- " .. exp.period.finish .. " \\\\\n"
        latex = latex .. "\\textit{" .. exp.role .. "} & \\footnotesize{\\texttt{" .. table.concat(exp.tech, ", ") .. "}} \\\\\n"
        latex = latex .. "\\end{tabularx}\n"
        latex = latex .. "\\begin{itemize}[leftmargin=0.2in, nosep, topsep=2pt]\n"
        for _, bullet in ipairs(exp.bullets) do
            latex = latex .. "  \\item " .. bullet .. "\n"
        end
        latex = latex .. "\\end{itemize}\n\\vspace{8pt}\n"
    end
    return latex
end

function M.render_figure(diagram_obj)
    local path = diagram_obj.path 
    local caption_text = diagram_obj.caption 
    local latex = "\\begin{figure}[ht]\n\\centering\n"
    latex = latex .. "\\includegraphics[width=0.75\\textwidth]{" .. path .. "}\n"
    latex = latex .. "\\caption*{" .. caption_text .. "}\n" 
    latex = latex .. "\\end{figure}"
    return latex
end

return M
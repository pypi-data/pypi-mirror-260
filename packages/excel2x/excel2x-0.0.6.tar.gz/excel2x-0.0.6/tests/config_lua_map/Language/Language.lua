
local Language_type = {
    -- [String] 主键
    key = nil,
    -- [String] zhs
    zhs = nil,
    -- [String] en
    en = nil,
}

local Language = {
    ["LANGUAGE_EN"] = {
        ["key"] = "LANGUAGE_EN",
        ["zhs"] = "English",
        ["en"] = "English",
    },
    ["LANGUAGE_ZHS"] = {
        ["key"] = "LANGUAGE_ZHS",
        ["zhs"] = "中文简体",
        ["en"] = "中文简体",
    },
    ["OK"] = {
        ["key"] = "OK",
        ["zhs"] = "好的",
        ["en"] = "OK",
    },
    ["RATE"] = {
        ["key"] = "RATE",
        ["zhs"] = "评价",
        ["en"] = "Rate\"hello\"",
    },
    ["SAVE"] = {
        ["key"] = "SAVE",
        ["zhs"] = "保存",
        ["en"] = "Save",
    },
}
return Language

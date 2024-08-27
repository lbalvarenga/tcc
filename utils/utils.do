program define block_prompt
  args proceed
  if `proceed' {
    local cmd 0
    n display as result "Please send [ENTER] on command window to continue."
    display _request(cmd)  
  }
end

program define _print
  args text
  local h ""
  local c 0
  
  if strlen("`text'") == 0 {
    return
  }
  
  while `c' < strlen("`text'") + 4 {
    local h = "`h'" + "*"
    local c = `c' + 1
  }
  

  n display as result char(10) + "`h'" + char(10) + "* `text' *" + char(10) + "`h'"
end


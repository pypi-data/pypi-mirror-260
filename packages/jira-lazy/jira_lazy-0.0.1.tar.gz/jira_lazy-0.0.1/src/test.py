from jira_lazy import Session, issue_search, PageParseException
from json import dumps

s = Session("https://link11.atlassian.net", ("m.harrison@link11.com", "ATATT3xFfGF0GunPXxAwh6a0QyqzhV2eUYSiudxFkXkxwXQqT35WKUoSW7eIxrfK01LnWhbGh3AKRnG73liEBY9HkHVh22p-iF16R8RGzaFFFQCQ3z7VLoLgqMB5j8wVbAqHzeoRBw_pnHyR__xJk0tUXw2ZDAOL_qLvJUQCw2t4LLJYv-o_xVw=211DB83A"))

for issue in issue_search(s, "project=AL4"):
    print(issue["key"], issue["fields"]["summary"])

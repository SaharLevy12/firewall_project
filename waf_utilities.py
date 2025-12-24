import re

class WAF_Utilities:
    def check_sql_injection(payload):

        password = payload["password"]

        suspicious_chars = [
        "'", '"', ";", "--", "#", "/*", "*/", 
        "(", ")", "*", "|", "&", "^", "%", "$",
        "@", "\\", "`", "~", "<", ">"
    ]
        
        suspicious_keywords = [
        "select", "union", "insert", "update", "delete",
        "drop", "alter", "create", "exec", "execute",
        "xp_", "sp_", "waitfor", "delay", "sleep",
        "benchmark", "pg_sleep", "load_file", "char(",
        "concat", "substring", "ascii", "version",
        "information_schema", "sysobjects", "syscolumns",
        "v$version", "utl_inaddr", "bfilename", "xp_regread",
        "xp_cmdshell", "declare", "cast", "convert",
        "hex(", "unhex", "0x", "ord(", "chr(",
        "database()", "user()", "current_user",
        "schema()", "version()", "@@version"
    ]
    
        boolean_patterns = [
        r"\bor\s+[\w'\"\.]+\s*=\s*[\w'\"\.]+\b",
        r"\band\s+[\w'\"\.]+\s*=\s*[\w'\"\.]+\b",
        r"\bor\s+\d+\s*=\s*\d+\b",
        r"\band\s+\d+\s*=\s*\d+\b",
        r"\bor\s+['\"][\w]*['\"]\s*=\s*['\"][\w]*['\"]\b",
        r"\band\s+['\"][\w]*['\"]\s*=\s*['\"][\w]*['\"]\b",
        r"\bor\s+true\b",
        r"\band\s+false\b",
        r"\bor\s+\d+\s*like\s*\d+\b",
        r"\bor\s+['\"].*['\"]\s*like\s*['\"].*['\"]\b",
    ]
    
        break_query_patterns = [
        r"'.*--",
        r'\".*--',
        r"'.*#",
        r'\".*#',
        r"'.*/\*",
        r'\".*/\*',
        r"'.*;",
        r'\".*;',
        r"\).*--",
        r"\).*#",
    ]
    
        advanced_patterns = [
        # התקפות מבוססות זמן (Time-based)
        r"sleep\s*\([^)]*\)",
        r"pg_sleep\s*\([^)]*\)",
        r"benchmark\s*\([^)]*\)",
        r"waitfor\s+delay",
        r"dbms_pipe\.receive_message",
        
        # התקפות מבוססות שגיאות (Error-based)
        r"extractvalue\s*\([^)]*\)",
        r"updatexml\s*\([^)]*\)",
        r"exp\s*\([^)]*\)",
        r"cast\s*\([^)]*\)",
        r"convert\s*\([^)]*\)",
        
        # Union attacks
        r"union\s+(all\s+)?select",
        r"union\s+(all\s+)?select.*from",
        
        # Stacked queries
        r";\s*(select|insert|update|delete|drop|create|alter|exec|execute)",
        r"\)\s*;\s*",
        
        # Boolean-based blind
        r"and\s+[\w'\"\.]+\s*=\s*[\w'\"\.]+\s+--",
        r"or\s+[\w'\"\.]+\s*=\s*[\w'\"\.]+\s+--",
        
        # Hex encoding
        r"0x[0-9a-fA-F]+",
        r"char\s*\([^)]*\)",
        
        # System information gathering
        r"@@\w+",
        r"version\s*\(\)",
        r"database\s*\(\)",
        r"user\s*\(\)",
        r"current_user",
        
        # File system access
        r"load_file\s*\([^)]*\)",
        r"into\s+outfile",
        r"into\s+dumpfile",
    ]
    
    
        # בדיקה בסיסית - מחרוזת ריקה או null
        if not password or len(password.strip()) == 0:
            return False, "Clear"

        lowered = password.lower()

        # בדיקה 1: תווים מסוכנים
        char_count = 0
        for c in suspicious_chars:
            count = lowered.count(c)
            char_count += count
            if count > 3:  # יותר מדי תווים מסוכנים
                return True, "Dangerous"

        # בדיקה 2: מילות מפתח מסוכנות
        for keyword in suspicious_keywords:
            if re.search(r'\b' + re.escape(keyword) + r'\b', lowered):
                return True, f"Dangerous - Contains SQL keyword: {keyword}"

        # בדיקה 3: דפוסים בוליאניים
        for pattern in boolean_patterns:
            if re.search(pattern, lowered, re.IGNORECASE):
                return True, "Dangerous - Boolean pattern detected"

        # בדיקה 4: שבירת שאילתות
        for pattern in break_query_patterns:
            if re.search(pattern, lowered, re.IGNORECASE):
                return True, "Dangerous - Query termination pattern"

        # בדיקה 5: דפוסים מתקדמים
        for pattern in advanced_patterns:
            if re.search(pattern, lowered, re.IGNORECASE):
                return True, "Dangerous - Advanced SQL injection pattern"

        # בדיקה 6: hex מורכב
        if WAF_Utilities.contains_complex_hex(password):
            return True, "Dangerous - Complex hex/char encoding detected"

        # בדיקה 7: הערות SQL בסוף
        if WAF_Utilities.has_sql_comment_at_end(password):
            return True, "Dangerous - SQL comment at end"

        # בדיקה 8: stacked queries
        if WAF_Utilities.has_stacked_queries(password):
            return True, "Dangerous - Stacked query pattern"

        # בדיקה 9: אורך חריג - מחרוזות ארוכות מדי חשודות
        if len(password) > 1000:
            return True, "Suspicious - Input too long"

        # בדיקה 10: יותר מדי רווחים (ניסיון לעקוף)
        if password.count(' ') > 20 or password.count('\t') > 10:
            return True, "Suspicious - Too many whitespace characters"

        # בדיקה 11: שילוב של מספרים ואופרטורים מתמטיים
        math_pattern = r"\d+\s*[\+\-\*\/]\s*\d+"
        if re.search(math_pattern, password) and char_count > 2:
            return True, "Suspicious - Mathematical operation with special chars"

        return False, "Clear"


    def contains_complex_hex(s):
        # מזהה רצפי char() עם מספרים מרובים
        char_pattern = r"char\s*\(\s*\d+\s*(,\s*\d+\s*)*\)"
        if re.search(char_pattern, s, re.IGNORECASE):
            return True
        
        # מזהה רצפים hex ארוכים
        hex_pattern = r"0x[0-9a-fA-F]{20,}"
        if re.search(hex_pattern, s):
            return True
            
        return False
    
    # בדיקת SQL comments בסוף המחרוזת
    def has_sql_comment_at_end(s):
        patterns = [r".*--.*$", r".*#.*$", r".*/\*.*\*/.*$"]
        for pattern in patterns:
            if re.search(pattern, s, re.IGNORECASE):
                return True
        return False
    
    # בדיקת stacked queries
    def has_stacked_queries(s):
        stacked_patterns = [
            r";\s*$",  # פסיק בסוף
            r"\)\s*;",  # סוגריים ואז פסיק
            r"'\)\s*;",  # ' ) ; דפוס נפוץ
            r"\"\)\s*;",  # " ) ;
        ]
        for pattern in stacked_patterns:
            if re.search(pattern, s, re.IGNORECASE):
                return True
        return False
import re

# Compile regex patterns
pattern_with_assign = re.compile(r"""
(?P<full_decl>
\b(?:static|extern)?\s*
[A-Za-z_][A-Za-z0-9_]*\s*
(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*
(\[\s*\w*\s*\]\s*)+
=\s*\{
[\s\S]*?
\};
)
""", re.VERBOSE | re.MULTILINE)

pattern_without_assign = re.compile(r"""
(?P<full_decl>
\b(?:static|extern)?\s*
[A-Za-z_][A-Za-z0-9_]*\s*
(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*
(\[\s*\w*\s*\]\s*)+
;
)
""", re.VERBOSE | re.MULTILINE)

def extract_arrays(code_str):
    result = {}
    # Extract arrays with initialization
    for match in pattern_with_assign.finditer(code_str):
        arr_name = match.group("name")
        arr_decl = match.group("full_decl")
        result[arr_name] = arr_decl
    # Extract arrays without initialization
    for match in pattern_without_assign.finditer(code_str):
        arr_name = match.group("name")
        arr_decl = match.group("full_decl")
        result[arr_name] = arr_decl
    return result

# Example usage:
code = """
static arr_demo[][4] = {
{1, 2, 3},
{MAX, 47},
};

extern int my_array;
"""

arr_dict = extract_arrays(code)
print(arr_dict)

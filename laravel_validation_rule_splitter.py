import pyperclip
def split_laravel_validation_rule(rules:str):
    return list(map(lambda rule: f"{rule.strip()}", rules.split('|')))

while (s := input('Enter the rule string: ')):
    s = s.strip(" \t'")
    pyperclip.copy(split_laravel_validation_rule(s))
    print('Copied result to clipboard, Haribol ..')
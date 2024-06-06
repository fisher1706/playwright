import re

# Example response text (rsp.text)
rsp_text = '''
<html>
<head><title>Test Page</title></head>
<body>
<form method="post">
  <input type="hidden" name="csrfmiddlewaretoken" value="your_csrf_token_here">
  <!-- Other form fields -->
</form>
</body>
</html>
'''

# Perform the regex search
match = re.search(r'<input type="hidden" name="csrfmiddlewaretoken" value="(.+?)">', rsp_text)
print(match)
print(match.group(1))

# Check if a match was found and extract the token
if match:
    csrf_token = match.group(1)
    print("CSRF Token:", csrf_token)
else:
    print("CSRF Token not found.")

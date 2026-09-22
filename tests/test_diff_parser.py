from app.parsers.diff import parse_patch


def test_parse_patch():
    patch = """@@ -10,3 +10,4 @@
 def login():
-    password = "1234"
+    password = get_password()
+    validate_password(password)
"""

    result = parse_patch(patch)

    assert len(result) == 1

    hunk = result[0]

    assert hunk["old_start"] == 10
    assert hunk["old_count"] == 3

    assert hunk["new_start"] == 10
    assert hunk["new_count"] == 4

    assert hunk["changes"] == [
        {
            "type": "context",
            "content": "def login():",
        },
        {
            "type": "removed",
            "content": '    password = "1234"',
        },
        {
            "type": "added",
            "content": "    password = get_password()",
        },
        {
            "type": "added",
            "content": "    validate_password(password)",
        },
    ]
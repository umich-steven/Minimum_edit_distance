from pathlib import Path

TEST_FILE = Path(__file__).parent / "test_strings.txt"


def load_cases(path=TEST_FILE):
    """Yields (source, target, expected_sub1, expected_sub2) for each test case."""
    cases = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip() or line.startswith("#"):
                continue
            if "|" not in line:          # loose-strings section at the bottom
                continue
            src, tgt, d1, d2 = line.split("|")
            cases.append((src, tgt, int(d1), int(d2)))
    return cases


def min_edit_distance(source, target):
    m, n = len(source), len(target)
    s = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        for j in range(n + 1):
            if i == 0 and j == 0:
                s[i][j] = 0
            elif i == 0:
                s[i][j] = s[i][j - 1] + 1
            elif j == 0:
                s[i][j] = s[i - 1][j] + 1
            elif source[i - 1] == target[j - 1]:
                s[i][j] = s[i - 1][j - 1]
            else:
                s[i][j] = min(s[i - 1][j] + 1, s[i][j - 1] + 1, s[i - 1][j - 1] + (0 if source[i - 1] == target[j - 1] else 2))
    return s[m][n]


if __name__ == "__main__":
    passed = failed = 0
    for src, tgt, _, expected in load_cases():
        got = min_edit_distance(src, tgt)
        if got == expected:
            passed += 1
        else:
            failed += 1
            print(f"FAIL  {src!r} -> {tgt!r}: expected {expected}, got {got}")
    print(f"{passed} passed, {failed} failed")

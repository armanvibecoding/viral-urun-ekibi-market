# -*- coding: utf-8 -*-
"""tools/build.py --check geçiyor mu (kopyalar kaynakla aynı, SKILL.md kuralları, manifest sürümleri)."""
import os
import subprocess
import sys
import unittest

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BuildCheck(unittest.TestCase):
    def test_check(self):
        r = subprocess.run([sys.executable, os.path.join(KOK, "tools", "build.py"), "--check"],
                           cwd=KOK, capture_output=True, text=True, encoding="utf-8")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("SONUÇ: GEÇTİ", r.stdout)


if __name__ == "__main__":
    unittest.main()

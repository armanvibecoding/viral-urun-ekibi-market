"""Her SKILL.md frontmatter'ı geçerli YAML olmalı (ChatGPT/agent skills doğrulaması YAML ile yapar)."""
import glob, os, re
import yaml

KOK = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_skill_frontmatter_gecerli_yaml():
    dosyalar = sorted(glob.glob(os.path.join(KOK, "skills", "*", "SKILL.md")))
    assert dosyalar
    for f in dosyalar:
        metin = open(f, encoding="utf-8").read()
        m = re.match(r"^---\r?\n(.*?)\r?\n---\r?\n", metin, re.S)
        assert m, f
        fm = yaml.safe_load(m.group(1))
        assert fm.get("name") == os.path.basename(os.path.dirname(f)), f
        assert isinstance(fm.get("description"), str) and fm["description"], f

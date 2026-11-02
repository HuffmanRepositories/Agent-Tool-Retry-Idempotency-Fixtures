import json, subprocess, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class FixtureTests(unittest.TestCase):
 def test_validator(self):
  p=subprocess.run([sys.executable,str(ROOT/"scripts/validate_fixtures.py")],cwd=ROOT,text=True,capture_output=True)
  self.assertEqual(p.returncode,0,p.stdout+p.stderr)
  self.assertIn("12 draft fixtures",p.stdout)
 def test_json_objects(self):
  for p in (ROOT/"fixtures").glob("*.json"):
   with self.subTest(file=p.name): self.assertIsInstance(json.loads(p.read_text()),dict)
if __name__=="__main__": unittest.main()

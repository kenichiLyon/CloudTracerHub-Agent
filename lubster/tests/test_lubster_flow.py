import json
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parents[2]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from lubster.config import load_config, load_incident
from lubster.diagnosis import diagnose


def test_lubster_diagnosis_has_five_layers():
    cfg = load_config(str(BASE / "examples" / "lubster.config.json"))
    inc = load_incident(file_path=str(BASE / "examples" / "incidents" / "unified_auth_timeout.json"))
    out = diagnose(inc, cfg)
    assert out["meta"]["engine"] == "lubster"
    assert len(out["layers"]) == 5
    assert out["layers"][0]["layer"] == "现象"
    assert out["layers"][-1]["layer"] == "变更"
    assert isinstance(out["recommendations"], list) and len(out["recommendations"]) >= 2
    json.dumps(out, ensure_ascii=False)

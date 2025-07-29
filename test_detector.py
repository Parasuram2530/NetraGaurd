from core.detector import CrowdDetector

detector = CrowdDetector(person_threshold=10)
detector.run(0)
from typing import Optional, Dict
import csv
from io import StringIO


class ViolationService:
    def __init__(self, repo):
        self.repo = repo

    def list_violations(self):
        return self.repo.get_all()

    def create_violation(self, name, absen, kelas, violation_type, reason):
        return self.repo.create(name=name, absen=absen, kelas=kelas,
                                violation_type=violation_type, reason=reason)

    def update_violation(self, vid, **kwargs) -> Optional[Dict]:
        return self.repo.update(vid, **kwargs)

    def delete_violation(self, vid) -> bool:
        return self.repo.delete(vid)

    def export_to_csv(self) -> str:
        """Export all violations to CSV format"""
        violations = self.repo.get_all()
        
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=['id', 'name', 'absen', 'kelas', 'violation_type', 'reason'])
        writer.writeheader()
        
        for violation in violations:
            writer.writerow({
                'id': violation['id'],
                'name': violation['name'],
                'absen': violation['absen'],
                'kelas': violation['kelas'],
                'violation_type': violation['violation_type'],
                'reason': violation['reason']
            })
        
        return output.getvalue()

    def import_from_csv(self, csv_content: str) -> tuple[int, int]:
        """Import violations from CSV content
        Returns (success_count, error_count)
        """
        success_count = 0
        error_count = 0
        
        try:
            reader = csv.DictReader(StringIO(csv_content))
            for row in reader:
                try:
                    self.create_violation(
                        name=row.get('name', '').strip(),
                        absen=row.get('absen', '').strip(),
                        kelas=row.get('kelas', '').strip(),
                        violation_type=row.get('violation_type', '').strip(),
                        reason=row.get('reason', '').strip()
                    )
                    success_count += 1
                except Exception as e:
                    error_count += 1
        except Exception as e:
            error_count += 1
        
        return success_count, error_count

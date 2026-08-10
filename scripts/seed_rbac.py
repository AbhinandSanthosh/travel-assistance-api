"""Seed the permissions and role_permissions tables from CSV.

Safe to re-run: existing permissions (by permission_code) and existing
role_permission links (by role_id + permission_id) are left untouched.

Usage:
    python -m scripts.seed_rbac

Requires seed_data/roles.csv to already be loaded into the `roles`
table -- this script looks roles up by role_name, it does not create
them.
"""

import csv
import pathlib
import sys

from src.db.session import SessionLocal
from src.models.administration.permission import Permission
from src.models.administration.role import Role
from src.models.administration.role_permission import RolePermission

SEED_DIR = pathlib.Path(__file__).resolve().parent.parent / "seed_data"


def seed_permissions(db) -> dict[str, Permission]:
    path = SEED_DIR / "permissions.csv"
    existing = {p.permission_code: p for p in db.query(Permission).all()}

    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.reader(f):
            if not row or not row[0].strip():
                continue
            code, name, description = row[0].strip(), row[1].strip(), row[2].strip()

            if code in existing:
                continue

            perm = Permission(
                permission_code=code,
                permission_name=name,
                description=description,
            )
            db.add(perm)
            existing[code] = perm

    db.commit()
    return {code: perm for code, perm in existing.items()}


def seed_role_permissions(db, permissions: dict[str, Permission]) -> None:
    path = SEED_DIR / "role_permissions.csv"
    roles = {r.role_name: r for r in db.query(Role).all()}

    existing_links = {
        (rp.role_id, rp.permission_id) for rp in db.query(RolePermission).all()
    }

    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            role_name = row["role_name"].strip()
            permission_code = row["permission_code"].strip()

            role = roles.get(role_name)
            if role is None:
                print(
                    f"  ! skipping grant for unknown role '{role_name}' "
                    "-- is seed_data/roles.csv loaded?",
                    file=sys.stderr,
                )
                continue

            perm = permissions.get(permission_code)
            if perm is None:
                print(
                    f"  ! skipping grant for unknown permission "
                    f"'{permission_code}'",
                    file=sys.stderr,
                )
                continue

            key = (role.id, perm.id)
            if key in existing_links:
                continue

            db.add(RolePermission(role_id=role.id, permission_id=perm.id))
            existing_links.add(key)

    db.commit()


def main() -> None:
    db = SessionLocal()
    try:
        print("Seeding permissions...")
        permissions = seed_permissions(db)
        print(f"  {len(permissions)} permission(s) present.")

        print("Seeding role_permissions...")
        seed_role_permissions(db, permissions)
        print("  Done.")
    finally:
        db.close()


if __name__ == "__main__":
    main()

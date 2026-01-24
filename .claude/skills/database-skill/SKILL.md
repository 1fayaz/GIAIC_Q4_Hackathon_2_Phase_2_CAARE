---
name: database-skill
description: Design and manage database schemas, create tables, and handle safe, maintainable migrations.
---

# Database Skill – Schema Design & Migrations

## Instructions

1. **Schema Design**
   - Identify entities and relationships clearly
   - Normalize data appropriately (avoid over/under-normalization)
   - Define primary keys, foreign keys, and constraints
   - Choose correct data types and defaults
   - Plan for future extensibility

2. **Table Creation**
   - Create tables with explicit constraints
   - Use indexes for frequently queried fields
   - Enforce data integrity at the database level
   - Avoid nullable fields unless required
   - Follow consistent naming conventions

3. **Migrations**
   - Use versioned, reversible migrations
   - Keep migrations small and focused
   - Avoid destructive changes without backups
   - Ensure migrations are idempotent when possible
   - Test migrations on staging before production

4. **Relationships & Constraints**
   - Define foreign keys with proper cascading rules
   - Use unique constraints where applicable
   - Leverage check constraints for data validation
   - Maintain referential integrity at all times

## Best Practices
- Treat the database schema as source code
- Prefer explicit constraints over application-only validation
- Document schema decisions and trade-offs
- Use transactions for multi-step schema changes
- Optimize indexes based on real query patterns
- Keep migrations backward-compatible when possible

## Example Structure
```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT NOT NULL UNIQUE,
  password_hash TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

-- Migration example
ALTER TABLE users
ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT true;

# Mapping Notes

This folder `Master_DB` is the authoritative source for the cross-domain knowledge graph. Use it to manage high-level entities and relationships; keep raw artifacts under `Drone/` and `Laser/`.

- master_nodes.csv: entities across Drone, Laser, and Shared domains.
- master_edges.csv: relationships between entities.

Recommended path hints in `spec_json`:

- Use relative hints like `../Drone/CAD/...` or `../Laser/Tests/...` so the graph stays portable.
- Reference PDFs, CAD, and datasets without embedding content; store content in `Drone/` or `Laser/`.

Provenance:

- `primary_source` should reference an email, document, or dataset identifier, e.g., `Nikolay_Email_2025-11-25`.

Change control:

- Update `status` to `validated` after review.
- Prefer additive changes; avoid destructive edits without archiving the prior row.

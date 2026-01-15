# Neo4j Cypher Queries for Drone-Laser Knowledge Graph

## Overview Queries

### View all nodes (limited)
```cypher
MATCH (n) 
RETURN n 
LIMIT 50
```

### Count all nodes by type
```cypher
MATCH (n)
RETURN labels(n)[0] as NodeType, count(*) as Count
ORDER BY Count DESC
```

### Count all relationships by type
```cypher
MATCH ()-[r]->()
RETURN r.relation_type as RelationType, count(*) as Count
ORDER BY Count DESC
```

---

## Drone Motor Queries

### Complete Drone Motor ecosystem
```cypher
MATCH (s {node_id:'SYS_DRONE_MOTOR_20KW'})-[r]-(n) 
RETURN s, r, n
```

### Drone Motor supply chain
```cypher
MATCH path = (s {node_id:'SYS_DRONE_MOTOR_20KW'})-[*1..3]-(org:PartnerOrg)
RETURN path
```

### Who designs, manufactures, and supplies the Drone Motor?
```cypher
MATCH (motor {node_id:'SYS_DRONE_MOTOR_20KW'})
OPTIONAL MATCH (motor)-[designed:REL {relation_type:'DESIGNED_BY'}]->(designer)
OPTIONAL MATCH (motor)-[manufactured:REL {relation_type:'MANUFACTURED_AT'}]->(manufacturer)
OPTIONAL MATCH (motor)-[supplied:REL {relation_type:'SUPPLIED_BY'}]->(supplier)
RETURN motor.name as System,
       designer.name as Designer,
       manufacturer.name as Manufacturer,
       supplier.name as Supplier
```

### Drone Motor funding and phases
```cypher
MATCH (motor {node_id:'SYS_DRONE_MOTOR_20KW'})-[r:REL {relation_type:'EXECUTED_IN_PHASE'}]->(phase)
MATCH (phase)<-[:REL]-(funding:FundingSource)
RETURN motor, r, phase, funding
```

---

## Laser Queries

### Complete Laser ecosystem
```cypher
MATCH (s {node_id:'SYS_LASER_XRAY_MONO'})-[r]-(n) 
RETURN s, r, n
```

### Laser partners and support organizations
```cypher
MATCH (laser {node_id:'SYS_LASER_XRAY_MONO'})-[r]-(org:PartnerOrg)
RETURN laser, r, org
```

### Laser physics principles
```cypher
MATCH (laser {node_id:'SYS_LASER_XRAY_MONO'})-[r:REL {relation_type:'OPERATES_ON_PRINCIPLE'}]->(physics:PhysicsPrinciple)
RETURN laser.name as System, physics.name as PhysicsPrinciple
```

---

## Cross-Domain Queries

### All partner organizations and their roles
```cypher
MATCH (org:PartnerOrg)
OPTIONAL MATCH (org)<-[r]-(system)
RETURN org.name as Organization, 
       org.subtype as Type,
       collect(DISTINCT r.relation_type) as Roles,
       collect(DISTINCT system.name) as RelatedSystems
ORDER BY org.name
```

### All systems with export control classifications
```cypher
MATCH (system)-[r:REL {relation_type:'SUBJECT_TO_EXPORT_CONTROL'}]->(export:ExportControl)
RETURN system.name as System,
       system.domain as Domain,
       export.name as ExportControl,
       export.description as Description
```

### ITAR vs Dual-Use systems
```cypher
MATCH (system)-[:REL {relation_type:'SUBJECT_TO_EXPORT_CONTROL'}]->(export:ExportControl)
RETURN export.name as Classification,
       collect(system.name) as Systems
ORDER BY export.name
```

### All Q-SMEC use cases and their linked systems
```cypher
MATCH (usecase:UseCase)-[r:REL {relation_type:'USES_CASE'}]-(system:System)
RETURN usecase.name as UseCase,
       system.name as System,
       system.domain as Domain
```

### Funding breakdown by domain
```cypher
MATCH (funding:FundingSource)
OPTIONAL MATCH (funding)-[:REL]->(phase:RnD_Phase)
OPTIONAL MATCH (phase)<-[:REL {relation_type:'EXECUTED_IN_PHASE'}]-(system:System)
RETURN funding.name as Funding,
       collect(DISTINCT system.domain) as Domains,
       collect(DISTINCT system.name) as Systems
```

---

## Exploration & Discovery

### Find all paths between two nodes
```cypher
MATCH path = shortestPath(
  (a {node_id:'ORG_ACOM_BG'})-[*..5]-(b {node_id:'ORG_UA_OPTICS'})
)
RETURN path
```

### Most connected nodes (hub analysis)
```cypher
MATCH (n)
RETURN n.name as Name, 
       n.node_type as Type,
       size((n)--()) as Connections
ORDER BY Connections DESC
LIMIT 10
```

### Find nodes with specific properties
```cypher
MATCH (n)
WHERE n.status = 'draft'
RETURN n.node_type as Type, n.name as Name, n.status as Status
```

### Full-text search across names and descriptions
```cypher
MATCH (n)
WHERE toLower(n.name) CONTAINS 'motor' 
   OR toLower(n.description) CONTAINS 'motor'
RETURN n.name as Name, n.node_type as Type, n.description as Description
```

---

## Data Quality & Metadata

### View all node properties
```cypher
MATCH (n {node_id:'SYS_DRONE_MOTOR_20KW'})
RETURN properties(n)
```

### Check for orphaned nodes (no relationships)
```cypher
MATCH (n)
WHERE NOT (n)--()
RETURN n.node_type as Type, n.name as Name
```

### View spec_json details for systems
```cypher
MATCH (n:System)
RETURN n.name as System, n.spec_json as Specifications
```

### Source provenance tracking
```cypher
MATCH (n)
WHERE n.primary_source IS NOT NULL
RETURN n.primary_source as Source, 
       collect(n.name) as DerivedEntities,
       count(*) as Count
ORDER BY Count DESC
```

---

## Advanced Analysis

### Multi-hop partner network
```cypher
MATCH path = (org1:PartnerOrg)-[*2..4]-(org2:PartnerOrg)
WHERE org1 <> org2
RETURN path
LIMIT 25
```

### Technology dependency tree
```cypher
MATCH path = (system:System)-[:REL {relation_type:'OPERATES_ON_PRINCIPLE'}*1..2]->(physics:PhysicsPrinciple)
RETURN path
```

### Cross-domain collaboration patterns
```cypher
MATCH (drone:System {domain:'Drone'})-[:REL]-(sharedNode)-[:REL]-(laser:System {domain:'Laser'})
RETURN drone.name as DroneSystem,
       sharedNode.name as SharedEntity,
       sharedNode.node_type as EntityType,
       laser.name as LaserSystem
```

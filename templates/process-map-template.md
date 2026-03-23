# Process Map Template

**Process Name:** [Name]
**Owner:** [Owner]
**Date:** [YYYY-MM-DD]

## Metadata
- Trigger:
- Frequency:
- SLA:
- Participants:

## Current State
Describe the AS-IS process at a high level.

```mermaid
flowchart LR
  Start([Start]) --> Step1[Step 1]
  Step1 --> Decision{Decision}
  Decision -->|Yes| Step2[Step 2]
  Decision -->|No| Rework[Rework]
  Step2 --> End([End])
  Rework --> Step1
```

## Future State
Describe the TO-BE process and improvements.

```mermaid
flowchart LR
  Start([Start]) --> Step1[Improved step]
  Step1 --> Step2[Validated step]
  Step2 --> End([End])
```

## Swimlane Example
```mermaid
flowchart LR
  subgraph Business
    B1[Initiate request]
  end
  subgraph System
    S1[Process request]
  end
  B1 --> S1
```

## Bottlenecks
| Step | Issue | Impact | Recommendation |
| --- | --- | --- | --- |
| [Step] | [Issue] | [Impact] | [Recommendation] |

## Related Templates
- [FRD Template](./frd-template.md)
- [Gap Analysis Template](./gap-analysis-template.md)
- [Stakeholder Register Template](./stakeholder-register-template.md)

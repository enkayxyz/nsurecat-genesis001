# API Routes Module

FastAPI routers connecting frontend to backend business logic.

## Architecture Diagram

```mermaid
flowchart LR
  subgraph Routes[API Routes]
    Shop[Shop Router] --> Agent[Mock Shopper]
    Save[Save Router] --> Arc[Arc Service]
  end
  Frontend --> Shop
  Frontend --> Save
  Agent --> |savings| Frontend
  Arc --> |payment| Frontend
```

## Contents Index

- **Files:**
  - [save.py](../../../docs/api_routes/save.md) - Router for saving/paying fees.
  - [shop.py](../../../docs/api_routes/shop.md) - Router for shopping insurance quotes.

- **Subfolders:** None

## Entry Points

- Mounted in `backend/main.py` under `/v1/` prefix.

## Contracts

- Shop: POST /shop with coverage fields → savings response.
- Save: POST /save with wallet address → payment status.

## Tests/Verification

- Integration tests in `tests/api_routes/`.

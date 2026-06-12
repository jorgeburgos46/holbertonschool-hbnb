# HBnB High-Level Package Diagram

## Package Diagram

```mermaid
flowchart TB
    subgraph PresentationLayer[Presentation Layer]
        API[API Endpoints]
        Services[Application Services]
    end

    subgraph BusinessLogicLayer[Business Logic Layer]
        Facade[HBnB Facade\n(unified interface)]
        Models[Core Models\nUser, Place, Review, Amenity]
    end

    subgraph PersistenceLayer[Persistence Layer]
        Repositories[Repositories / DAOs]
        DB[(Database)]
    end

    API --> Services
    Services --> Facade
    Facade --> Models
    Models --> Repositories
    Repositories --> DB

    Models -. "business rules / entity behavior" .-> Facade
    Repositories -. "data access results" .-> Facade
```

## Explanatory Notes

### 1. Presentation Layer
- Handles user interaction through API endpoints and service classes.
- Receives requests, validates inputs at the boundary, and delegates operations to the business layer.
- In this architecture, the presentation layer communicates with the rest of the application through the facade.

### 2. Business Logic Layer
- Contains the core domain models such as User, Place, Review, and Amenity.
- Implements the application rules, relationships, and validation logic.
- The facade provides a simplified interface so the presentation layer does not need to know every internal detail of the models.

### 3. Persistence Layer
- Manages storage and retrieval of application data.
- Repositories or DAOs interact directly with the database.
- The business logic layer relies on this layer to persist and fetch entities.

## Role of the Facade Pattern

The facade pattern acts as a single interface between the presentation layer and the rest of the application. It simplifies communication by:
- hiding the internal complexity of the model and persistence layers;
- reducing coupling between API/services and domain logic;
- providing one clear entry point for operations such as creating, reading, updating, and deleting entities.

This keeps the architecture organized, easier to maintain, and aligned with the layered design of the HBnB application.

---

## Task 1: Detailed Class Diagram — Business Logic Layer

### Overview
All entities inherit from a BaseModel that provides common attributes.
The diagram shows the four main entities and their relationships.

```mermaid
classDiagram
    class BaseModel {
        +UUID id
        +datetime created_at
        +datetime updated_at
        +save()
        +to_dict()
    }

    class User {
        +String first_name
        +String last_name
        +String email
        +String password
        +Boolean is_admin
        +register()
        +update_profile()
        +delete()
    }

    class Place {
        +String title
        +String description
        +Float price
        +Float latitude
        +Float longitude
        +User owner
        +List amenities
        +create()
        +update()
        +delete()
        +list()
    }

    class Review {
        +Place place
        +User user
        +Integer rating
        +String comment
        +create()
        +update()
        +delete()
        +list_by_place()
    }

    class Amenity {
        +String name
        +String description
        +create()
        +update()
        +delete()
        +list()
    }

    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    User "1" --> "0..*" Place : owns
    User "1" --> "0..*" Review : writes
    Place "1" --> "0..*" Review : has
    Place "0..*" --> "0..*" Amenity : includes
```

### Entity Descriptions

**BaseModel** — Base class for all entities. Provides `id`, `created_at`, and `updated_at`.

**User** — Represents registered users. Can be admin or regular user.

**Place** — A property listed by a user. Has amenities and receives reviews.

**Review** — Written by a user about a specific place. Includes rating and comment.

**Amenity** — A feature that can be associated with multiple places.

---
---

## Task 2: Sequence Diagrams for API Calls

---

### 1. User Registration

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant BusinessLogic
    participant Database

    Client->>API: POST /users (first_name, last_name, email, password)
    API->>BusinessLogic: validate_user_data()
    BusinessLogic->>BusinessLogic: check email format & required fields
    BusinessLogic->>Database: check_email_exists(email)
    Database-->>BusinessLogic: email not found
    BusinessLogic->>Database: save_user(user_data)
    Database-->>BusinessLogic: user saved (id, created_at)
    BusinessLogic-->>API: return new User object
    API-->>Client: 201 Created (user_id, email)
```

**Description:** The client sends user data to the API. The Business Logic validates
the input and checks for duplicate emails. If valid, the user is saved to the database
and a success response is returned.

---

### 2. Place Creation

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant BusinessLogic
    participant Database

    Client->>API: POST /places (title, description, price, latitude, longitude)
    API->>BusinessLogic: validate_token(token)
    BusinessLogic->>Database: get_user_by_token(token)
    Database-->>BusinessLogic: return authenticated User
    BusinessLogic->>BusinessLogic: validate_place_data()
    BusinessLogic->>Database: save_place(place_data, owner_id)
    Database-->>BusinessLogic: place saved (id, created_at)
    BusinessLogic-->>API: return new Place object
    API-->>Client: 201 Created (place_id, title)
```

**Description:** An authenticated user sends place details. The API verifies the
user token, the Business Logic validates the data, and the place is saved with the
owner reference. A success response with the new place ID is returned.

---

### 3. Review Submission

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant BusinessLogic
    participant Database

    Client->>API: POST /places/{place_id}/reviews (rating, comment)
    API->>BusinessLogic: validate_token(token)
    BusinessLogic->>Database: get_user_by_token(token)
    Database-->>BusinessLogic: return authenticated User
    BusinessLogic->>Database: get_place(place_id)
    Database-->>BusinessLogic: return Place object
    BusinessLogic->>BusinessLogic: validate_review_data()
    BusinessLogic->>Database: save_review(review_data, user_id, place_id)
    Database-->>BusinessLogic: review saved (id, created_at)
    BusinessLogic-->>API: return new Review object
    API-->>Client: 201 Created (review_id, rating)
```

**Description:** An authenticated user submits a review for a specific place.
The Business Logic verifies both the user and the place exist, validates the
review data, and saves it linked to both the user and place.

---

### 4. Fetching a List of Places

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant BusinessLogic
    participant Database

    Client->>API: GET /places?price=100&latitude=18.4&longitude=-66.1
    API->>BusinessLogic: parse_filters(params)
    BusinessLogic->>BusinessLogic: validate_filter_params()
    BusinessLogic->>Database: get_places(filters)
    Database-->>BusinessLogic: return list of Place objects
    BusinessLogic->>BusinessLogic: format_response(places)
    BusinessLogic-->>API: return formatted places list
    API-->>Client: 200 OK (list of places)
```

**Description:** A client requests a list of places with optional filters such as
price and location. The Business Logic validates and parses the filters, queries
the database, formats the results, and returns the list to the client.

---
---

## Task 3: Documentation Compilation

### Introduction

This document serves as the comprehensive technical blueprint for **HBnB Evolution**,
a simplified AirBnB-like application. It covers the full architecture and design of
the system, including the layered architecture, business logic entities, and API
interaction flows.

The purpose of this document is to guide the implementation phases of the project
by providing a clear and detailed reference for developers. All diagrams follow
UML notation and were created using Mermaid.js.

---

### Project Overview

HBnB Evolution allows users to:
- **Register and manage** their user profiles
- **List properties** (places) with details like price and location
- **Leave reviews** for places they have visited
- **Manage amenities** that can be associated with places

---

### Architecture Summary

The application is built on a **three-layer architecture**:

| Layer | Responsibility |
|---|---|
| Presentation | Exposes REST API endpoints to the client |
| Business Logic | Validates data and applies business rules |
| Persistence | Stores and retrieves data from the database |

The **Facade Pattern** acts as the bridge between the Presentation Layer and
the Business Logic Layer, providing a clean and unified interface.

---

### Design Decisions

**Why Layered Architecture?**
Separating concerns into three distinct layers makes the application easier to
maintain, test, and scale. Each layer can be modified independently without
affecting the others.

**Why the Facade Pattern?**
The Facade Pattern simplifies communication between layers by hiding internal
complexity. The Presentation Layer never directly accesses the database — it
always goes through the Business Logic Layer.

**Why a BaseModel?**
All entities (User, Place, Review, Amenity) share common attributes: `id`,
`created_at`, and `updated_at`. Centralizing these in a BaseModel avoids
code duplication and enforces consistency.

**Why UUID for IDs?**
UUIDs guarantee uniqueness across distributed systems and avoid predictable
sequential IDs, which improves security.

---

### Entity Relationship Summary

| Entity | Relationship |
|---|---|
| User → Place | A user can own many places |
| User → Review | A user can write many reviews |
| Place → Review | A place can have many reviews |
| Place ↔ Amenity | A place can have many amenities; an amenity can belong to many places |

---

### API Flow Summary

| API Call | Method | Endpoint |
|---|---|---|
| User Registration | POST | /users |
| Place Creation | POST | /places |
| Review Submission | POST | /places/{place_id}/reviews |
| Fetch List of Places | GET | /places |

---

### Conclusion

This technical document provides a complete blueprint for HBnB Evolution.
The diagrams and explanatory notes defined here will guide all implementation
phases, ensuring consistency between the design and the final product.
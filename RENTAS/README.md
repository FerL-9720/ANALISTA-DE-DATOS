# Sistema de Gestión de Rentas - Esquema de Base de Datos

## 📌 Visión General
Esquema relacional para un sistema de gestión de rentas inmobiliarias con módulo fotovoltaico integrado. Incluye:
- Gestión de clientes y representantes
- Control de propiedades y locales
- Procesos de facturación y pagos
- Subsistema especializado para rentas fotovoltaicas

---

## 🗃️ Tablas Principales

| Tabla               | Clave Primaria       | Descripción                             |
|---------------------|----------------------|-----------------------------------------|
| `clientes`          | `id_cliente` (INT)   | Registro de clientes morales/físicos    |
| `propiedades`       | `id_propiedad` (INT) | Catálogo de propiedades inmobiliarias   |
| `locales`           | `id_local` (INT)     | Unidades de renta dentro de propiedades |
| `rentas`            | `id_rentas` (INT)    | Contratos activos de arrendamiento      |

---

## 🔗 Relaciones Clave

### 1. Estructura Cliente-Representante
```mermaid
graph TD
    A[clientes] -- id_cliente --> B[representantes_clientes]
    B -- id_cliente_moral --> A
    B -- id_pmoral --> C[pmoral]
    C -- id_representante --> D[representantes]


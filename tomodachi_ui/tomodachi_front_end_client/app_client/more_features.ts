"use client"; // This is optional, mainly for React components, can be removed

// -- 1. satisfies usage --
const colorConfig = {
  primary: "#3498db",
  secondary: "#2ecc71",
  danger: "#e74c3c",
} satisfies Record<string, string>;

type ColorKey = keyof typeof colorConfig;
const myKey: ColorKey = "danger";

// -- 2. as const --
const directions = ["north", "south", "east", "west"] as const;
type Direction = typeof directions[number];

// -- 3. Discriminated unions + exhaustive checks --
type ApiStatus =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: string }
  | { status: "error"; error: Error };

function handleStatus(state: ApiStatus): string {
  switch (state.status) {
    case "idle":
      return "Waiting…";
    case "loading":
      return "Loading…";
    case "success":
      return `Result: ${state.data}`;
    case "error":
      return `Error: ${state.error.message}`;
  }
}

// -- 4. Advanced mapped + conditional types --
type ApiConfig = {
  users: { method: "GET"; path: "/api/users" };
  posts: { method: "POST"; path: "/api/posts" };
};

type ApiRoutes = {
  [K in keyof ApiConfig]: `${ApiConfig[K]["method"]} ${ApiConfig[K]["path"]}`;
};

// -- 5. Narrowing with satisfies and as const --
const userRole = "admin" as const;
type Role = "admin" | "user" | "guest";
const user: { role: Role } = { role: userRole };

// -- 6. Exhaustive config with satisfies --
const routePermissions = {
  "/dashboard": ["admin", "user"],
  "/admin": ["admin"],
  "/guest": ["guest"],
} satisfies Record<string, Role[]>;

// -- 7. Type predicate for runtime check --
function isSuccess(status: ApiStatus): status is { status: "success"; data: string } {
  return status.status === "success";
}

// -- 8. Utility: Get keys of an object --
function getKeys<T extends object>(obj: T): Array<keyof T> {
  return Object.keys(obj) as Array<keyof T>;
}

const keys = getKeys(colorConfig);

// --- Main console logic ---

console.log("Color keys:", keys.join(", "));

const status: ApiStatus = { status: "success", data: "Hello!" };
console.log("Status handler result:", handleStatus(status));

console.log("Directions:", directions.join(", "));

console.log("Permissions for /admin:", routePermissions["/admin"].join(", "));

// Runtime check for isSuccess
if (isSuccess(status)) {
  console.log("Status is success with data:", status.data);
} else {
  console.log("Status is not success");
}

// Display ApiRoutes type as example - only at type-level (no runtime)
type ExampleRoute = ApiRoutes["users"]; // "GET /api/users"
console.log("Example API Route (type-level):", "GET /api/users (inferred)");

console.log("User role:", user.role);

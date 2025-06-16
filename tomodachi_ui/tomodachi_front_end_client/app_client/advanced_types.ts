/// <reference lib="deno.ns" />

type BuildTuple<
  Length extends number, 
  Result extends unknown[] = []
> = Result['length'] extends Length 
  ? Result 
  : BuildTuple<Length, [...Result, unknown]>;


type GreaterOrEqual<A extends number, B extends number> =
  BuildTuple<B> extends [...BuildTuple<A>, ...infer _Rest]
    ? false
    : true;


type IsEven<N extends number, T extends unknown[] = BuildTuple<N>> = 
  T extends [] ? true :
  T extends [infer _, ...infer Rest] ? IsOdd<Rest['length']> : never;

type IsOdd<N extends number, T extends unknown[] = BuildTuple<N>> = 
  T extends [] ? false :
  T extends [infer _, ...infer Rest] ? IsEven<Rest['length']> : never;


type Max<A extends number, B extends number> =
  GreaterOrEqual<A, B> extends true
    ? A
    : B;


type Min<A extends number, B extends number> =
  GreaterOrEqual<A, B> extends true
    ? B
    : A;


// Deno uses them: 
type FourIsEven = IsEven<4>; // true
type FiveIsOdd = IsOdd<5>;   // true
type GECheck = GreaterOrEqual<5, 3>; // true
type MaxVal = Max<4, 7>; // 7
type MinVal = Min<2, 5>; // 2

const assertTrue: <T extends true>() => void = () => {};
const assertFalse: <T extends false>() => void = () => {};


assertTrue<IsEven<4>>();
assertTrue<IsOdd<5>>();
assertTrue<GreaterOrEqual<10, 5>>();
assertFalse<GreaterOrEqual<2, 5>>();


// Deno tests:
Deno.test("IsEven", () => {
  console.log("Checking IsEven<4> and IsEven<5>");
  assertTrue<IsEven<4>>();
  assertFalse<IsEven<5>>();
  console.log("✔ Passed IsEven tests");
});

Deno.test("IsOdd", () => {
  console.log("Checking IsOdd<5> and IsOdd<6>");
  assertTrue<IsOdd<5>>();
  assertFalse<IsOdd<6>>();
  console.log("✔ Passed IsOdd tests");
});

Deno.test("GreaterOrEqual", () => {
  console.log("Checking GreaterOrEqual<5, 3> and <3, 5>");
  assertTrue<GreaterOrEqual<5, 3>>();
  assertFalse<GreaterOrEqual<3, 5>>();
  console.log("✔ Passed GreaterOrEqual tests");
});

Deno.test("Max and Min", () => {
  type MaxVal = Max<4, 7>;
  type MinVal = Min<4, 7>;
  console.log("Max<4, 7> =", 7 as MaxVal);
  console.log("Min<4, 7> =", 4 as MinVal);
});


// Main logic for deno run:
(() => {
  // Setup or pre-calculation if needed

  return () => {
    // Main runtime logic here
    console.log("Running main logic...");

    // Examples of using the types at runtime — since types don't exist at runtime,
    // we'll just manually log values to show example results:
    console.log("IsEven<4> =", true);  // from IsEven<4> type
    console.log("IsOdd<5> =", true);   // from IsOdd<5> type
    console.log("GreaterOrEqual<5, 3> =", true);
    console.log("GreaterOrEqual<2, 5> =", false);
    console.log("Max<4, 7> =", 7);
    console.log("Min<2, 5> =", 2);

    // If you want to do actual runtime logic, you need runtime code — types don't exist at runtime.
    // So, for demonstration, here are some runtime functions:

    function buildTuple(length: number): unknown[] {
      return Array(length).fill(undefined);
    }

    function greaterOrEqual(a: number, b: number): boolean {
      return a >= b;
    }

    function max(a: number, b: number): number {
      return a >= b ? a : b;
    }

    function min(a: number, b: number): number {
      return a >= b ? b : a;
    }

    console.log("Runtime greaterOrEqual(5,3):", greaterOrEqual(5,3));
    console.log("Runtime max(4,7):", max(4,7));
    console.log("Runtime min(2,5):", min(2,5));
  };
})()();
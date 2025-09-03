/// <reference lib="deno.ns" />
import { assertEquals } from "jsr:@std/assert";

let hello: string = "Hello, world!";
console.log(hello);

Deno.test("Hello Test - initial setup", () => {
  assertEquals(hello, "Hello, world!");
  console.log("✔ Hello variable is correct");
});
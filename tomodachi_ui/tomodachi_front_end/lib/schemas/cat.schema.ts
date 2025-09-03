import { z } from "zod";

export const CatSchema = z.object({
  name: z.string().nullable(),
  breed: z.string().nullable(),
  age: z.number().int().nonnegative().nullable(),
  is_adopted: z.boolean().nullable().optional(),
  arrival_date: z.string().nullable(), // or z.string().optional() if it can be missing
});


// You can also export types for type safety:
export type Cat = z.infer<typeof CatSchema>;
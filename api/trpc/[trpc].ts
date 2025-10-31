import { createNextApiHandler } from "@trpc/server/adapters/next";
import { appRouter } from "../../server/routers.js";
import { createContext } from "../../server/_core/context.js";

export default createNextApiHandler({
  router: appRouter,
  createContext,
});


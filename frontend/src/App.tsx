import { useState } from "react";
import Home from "./pages/Home";
import Preview from "./pages/Preview";
import Code from "./pages/Code";
import Nav from "./components/Nav";

export type Route = "home" | "preview" | "code";

export default function App() {
  const [route, setRoute] = useState<Route>("home");
  return (
    <div className="min-h-screen flex flex-col">
      <Nav route={route} setRoute={setRoute} />
      <main className="flex-1 container mx-auto max-w-6xl px-4 py-6">
        {route === "home"    && <Home onDone={() => setRoute("preview")} />}
        {route === "preview" && <Preview onCode={() => setRoute("code")} />}
        {route === "code"    && <Code />}
      </main>
    </div>
  );
}
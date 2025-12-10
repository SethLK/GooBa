import esbuild from "esbuild";

esbuild.build({
  entryPoints: ["src/index.ts"], // Entry file (change if necessary)
  bundle: true,                  // Bundle everything into one file
  outfile: "dist/gooba.js",      // Output location and filename
  format: "esm",                 // Output as ECMAScript Module (for <script type="module">)
  sourcemap: true,               // Include sourcemap (helpful for debugging)
  minify: false,                 // Do not minify in development (you can set to `true` for production)
  target: "esnext",              // Use modern JS features, works well for browsers that support ES modules
  globalName: "Gooba",           // This will make the output accessible globally as `Gooba` (useful for browsers)
})
.then(() => {
  console.log("Build complete!");
})
.catch((error) => {
  console.error("Build failed:", error);
});

import esbuild from "esbuild";

esbuild.build({
  entryPoints: ["src/index.ts"],
  bundle: true,
  outfile: "dist/gooba.js",
  format: "esm",
  sourcemap: true,
  minify: false,
});
